import time
import threading
import tkinter as tk
import tkinter.ttk as ttk
import random
from os import startfile
from numpy.random import gamma, normal
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image
import scipy.stats
import numpy as np

flag = True
flag_x = True
flag_y = True

stop = False

stat = 0
stat_x = 0
stat_y = 0


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.gamma_shape = 2.0
        self.gamma_scale = 2.0  # E=2*2=4, D=2*2^2
        self.exponential_scale = 1.0  # E=1, D=1^2

        self.time_xy = 0
        self.time_x = 0
        self.time_y = 0

        self.window_size_x = self.winfo_screenwidth()
        self.window_size_y = self.winfo_screenheight()

        # окно
        self.attributes('-fullscreen', True)

        #
        tab_control_style = ttk.Style()
        tab_control_style.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {"configure": {"padding": [100, 10],
                                            "font": ('URW Gothic L', '30', 'bold')}, }})
        tab_control_style.theme_use("MyStyle")

        self.tab_control = ttk.Notebook(self)
        self.tab1 = tk.Frame(self.tab_control)
        self.tab2 = tk.Frame(self.tab_control)
        #self.tab3 = tk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Главная')
        self.tab_control.add(self.tab2, text='Модель')
        #self.tab_control.add(self.tab3, text='Авторы')
        self.tab_control.pack(expand=1, fill='both')

        # TAB1 ---------------------------------------------------------------------------------------------------------
        str1 = 'Московский государственный университет имени М.В. Ломоносова'
        str2 = '"Случайный поиск в задачах разной размерности"'
        self.tab1_lbl1 = tk.Label(self.tab1, text=str1, font=("Arial Bold", 30))
        self.tab1_lbl2 = tk.Label(self.tab1, text=str2, font=("Arial Bold", 30))
        self.tab1_btn2 = tk.Button(self.tab1, text="Выход", font=("Arial", 30), bg="#2F4F4F",
                                   fg="#FFFFFF", width=20,
                                   command=lambda: self.destroy())
        self.tab1_btn1 = tk.Button(self.tab1, text="Теория", font=("Arial", 30), bg="#2F4F4F",
                                   fg="#FFFFFF", width=20,
                                   command=lambda: startfile('theory.pdf'))
        self.tab1_lbl3 = tk.Label(self.tab1, text="2022", font=("Arial Bold", 30))

        self.tab1_frame1 = tk.Frame(self.tab1)

        k = 300

        self.img3 = Image.open("images/logo_vmk_so_shriftom.png")
        self.img3 = self.img3.resize((k, k))
        self.tatras3 = ImageTk.PhotoImage(self.img3)
        canvas3 = tk.Canvas(self.tab1_frame1, width=self.img3.size[0] + 20, height=self.img3.size[1] + 20)
        #
        canvas3.create_image(10, 10, anchor=tk.NW, image=self.tatras3)

        self.img4 = Image.open("images/sign-fizfak-official.jpg")
        self.img4 = self.img4.resize((k, k))
        self.tatras4 = ImageTk.PhotoImage(self.img4)
        canvas1 = tk.Canvas(self.tab1_frame1, width=self.img4.size[0] + 20, height=self.img4.size[1] + 20)
        #
        canvas1.create_image(10, 10, anchor=tk.NW, image=self.tatras4)

        self.img5 = Image.open("images/logotip-mgu.png")
        self.img5 = self.img5.resize((k, k))
        self.tatras5 = ImageTk.PhotoImage(self.img5)
        canvas2 = tk.Canvas(self.tab1_frame1, width=self.img5.size[0] + 20, height=self.img5.size[1] + 20)
        #
        canvas2.create_image(10, 10, anchor=tk.NW, image=self.tatras5)

        self.tab1_lbl1.pack(side=tk.TOP, pady=10)
        self.tab1_lbl2.pack(side=tk.TOP, pady=0)
        self.tab1_frame1.pack(side=tk.TOP, expand=1, fill=tk.BOTH)
        canvas1.pack(side=tk.LEFT, expand=1)
        canvas2.pack(side=tk.LEFT, expand=1)
        canvas3.pack(side=tk.LEFT, expand=1)
        self.tab1_lbl3.pack(side=tk.BOTTOM, pady=10)
        self.tab1_btn2.pack(side=tk.BOTTOM)
        self.tab1_btn1.pack(side=tk.BOTTOM, pady=2)
        # --------------------------------------------------------------------------------------------------------------

        # TAB2 ---------------------------------------------------------------------------------------------------------
        # рабочая область
        self.tab2_frame2 = tk.Frame(self.tab2, bg='#DDDDDD')
        self.tab2_frame2.pack(side=tk.RIGHT, fill=tk.Y)
        self.tab2_frame1 = tk.Frame(self.tab2, bg='#CCCCCC')
        self.tab2_frame1.pack(expand=True, fill=tk.BOTH)

        # self.canvas_size_x = self.window_size_x - self.tab2_frame2[0] - 5
        # self.canvas_size_y = self.window_size_y - self.tab2_frame2[1] - 5

        # рабочая область
        self.canvas_size_x = 750
        self.canvas_size_y = 750

        self.canvas = tk.Canvas(self.tab2_frame1, width=self.canvas_size_x, height=self.canvas_size_y, bg='#FFFFFF')
        self.canvas.pack(side=tk.TOP, padx=5, pady=5)
        # self.canvas = tk.Canvas(self.tab2_frame1, bg='#FFFFFF')
        # self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.square_size_r = 25
        self.square_size = 2 * self.square_size_r
        self.square_x = random.randint(self.square_size_r, self.canvas_size_x - self.square_size_r)
        self.square_y = random.randint(self.square_size_r, self.canvas_size_y - self.square_size_r)

        self.point_size_r = 4
        self.point_size = 2 * self.point_size_r
        self.point_x = random.randint(self.point_size_r, self.canvas_size_x - self.point_size_r)
        self.point_y = random.randint(self.point_size_r, self.canvas_size_y - self.point_size_r)

        self.draw_working_area()

        # координатные оси
        self.obj_x = self.canvas.create_line(self.square_x, 0, self.square_x, self.canvas_size_y, fill="#000000",
                                             width=1)
        self.obj_y = self.canvas.create_line(0, self.square_y, self.canvas_size_x, self.square_y, fill="#000000",
                                             width=1)
        # объект
        self.obj = self.canvas.create_rectangle(self.square_x - self.square_size_r, self.square_y - self.square_size_r,
                                                self.square_x + self.square_size_r, self.square_y + self.square_size_r,
                                                outline="#696969",
                                                fill="#2F4F4F")
        # точка
        self.point = self.canvas.create_oval(self.point_x - self.point_size_r, self.point_y - self.point_size_r,
                                             self.point_x + self.point_size_r,
                                             self.point_y + self.point_size_r, outline="#8B4513", fill="#D2691E",
                                             width=2)

        self.points = [(self.point_x, self.point_y)]
        self.objs = [(self.square_x, self.square_y)]
        # рамка с параметрами ==========================================================================================

        text_size_1 = 15
        text_size_2 = 15
        text_size_3 = 15

        # --------------------------------------------------------------------------------------------------------------
        # осн. характеристики ------------------------------------------------------------------------------------------
        self.tab2_frame21 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame21.pack(side=tk.TOP)
        self.tab2_frame211 = tk.Frame(self.tab2_frame21, bg='#DDDDDD')
        self.tab2_frame211.pack(anchor=tk.NW, expand=0)
        self.tab2_frame212 = tk.Frame(self.tab2_frame21, bg='#DDDDDD')
        self.tab2_frame212.pack(anchor=tk.NW, expand=0)

        # square label -------------------------------------------------------------------------------------------------
        self.square_size_str = tk.StringVar()
        self.tab2_frame21_lbl1 = tk.Label(self.tab2_frame211, textvariable=self.square_size_str,
                                          font=("Arial Bold", text_size_1),
                                          bg='#DDDDDD')
        self.square_size_str.set(f'размер квадрата = {self.square_size_r:02d}         ')
        self.tab2_frame21_lbl1.pack(side=tk.LEFT)

        # square scale -------------------------------------------------------------------------------------------------
        self.tab2_frame21_scale1 = tk.Scale(self.tab2_frame211, from_=1, to=100, orient="horizontal", bg='#DDDDDD',
                                            width=10, length=100, command=self.square_scale)
        self.tab2_frame21_scale1.pack(side=tk.LEFT)
        self.tab2_frame21_scale1.set(25)

        self.points_count = 1
        self.points_count_actual = self.points_count

        # points label -------------------------------------------------------------------------------------------------
        self.point_count_str = tk.StringVar()
        self.tab2_frame21_lbl2 = tk.Label(self.tab2_frame212, textvariable=self.point_count_str,
                                          font=("Arial Bold", text_size_1),
                                          bg='#DDDDDD')
        self.point_count_str.set(f'число экспериментов = {self.points_count:02d}   ')
        self.tab2_frame21_lbl2.pack(side=tk.LEFT, expand=0)

        # points scale -------------------------------------------------------------------------------------------------
        self.tab2_frame21_scale2 = tk.Scale(self.tab2_frame212, from_=1, to=100, orient="horizontal", bg='#DDDDDD',
                                            width=10, length=100, command=self.change_points_count)
        self.tab2_frame21_scale2.pack(side=tk.LEFT, expand=0)
        self.tab2_frame21_scale2.set(1)

        # trace --------------------------------------------------------------------------------------------------------
        self.chk_enabled = tk.IntVar()
        self.tab2_chk = ttk.Checkbutton(self.tab2_frame211, text="", variable=self.chk_enabled)
        self.tab2_chk.pack(side=tk.LEFT, padx=10)
        self.tab2_frame21_lbl1 = tk.Label(self.tab2_frame211, text="включить след", font=("Arial Bold", text_size_1),
                                          bg='#DDDDDD')
        self.tab2_frame21_lbl1.pack(side=tk.LEFT)

        self.chk2_enabled = tk.IntVar()
        self.tab2_chk2 = ttk.Checkbutton(self.tab2_frame212, text="", variable=self.chk2_enabled)
        self.tab2_chk2.pack(side=tk.LEFT, padx=10)
        self.tab2_frame21_lbl2 = tk.Label(self.tab2_frame212, text="ускорение", font=("Arial Bold", text_size_1),
                                          bg='#DDDDDD')
        self.tab2_frame21_lbl2.pack(side=tk.LEFT)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # распределения ------------------------------------------------------------------------------------------------
        self.raspr1 = 'гамма'
        self.raspr1_param1 = 0
        self.raspr1_param2 = 0
        self.raspr1_param3 = 0
        self.raspr1_param32 = 0
        self.raspr1_param4 = 0

        self.raspr2 = 'гамма'
        self.raspr2_param1 = 0
        self.raspr2_param2 = 0
        self.raspr2_param3 = 0
        self.raspr2_param32 = 0
        self.raspr2_param4 = 0

        self.tab2_frame22 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame22.pack(side=tk.TOP, pady=5)
        self.tab2_frame221 = tk.Frame(self.tab2_frame22, bg='#DDDDDD')
        self.tab2_frame221.pack(side=tk.LEFT)
        self.tab2_frame222 = tk.Frame(self.tab2_frame22, bg='#DDDDDD')
        self.tab2_frame222.pack(side=tk.LEFT)

        # combobox 1 ---------------------------------------------------------------------------------------------------
        self.tab2_frame221_combo1 = ttk.Combobox(self.tab2_frame221, font="Arial 16 bold")
        self.tab2_frame221_combo1['values'] = ('гамма', 'нормальное')
        self.tab2_frame221_combo1.current(0)  # установите вариант по умолчанию
        self.tab2_frame221_combo1.pack(side=tk.TOP)
        self.tab2_frame221_combo1.bind("<<ComboboxSelected>>", self.call_frame221_combo1)

        # combobox 2 ---------------------------------------------------------------------------------------------------
        self.tab2_frame222_combo1 = ttk.Combobox(self.tab2_frame222, font="Arial 16 bold")
        self.tab2_frame222_combo1['values'] = ('гамма', 'нормальное')
        self.tab2_frame222_combo1.current(0)  # установите вариант по умолчанию
        self.tab2_frame222_combo1.pack(side=tk.TOP)
        self.tab2_frame222_combo1.bind("<<ComboboxSelected>>", self.call_frame222_combo1)

        self.option_add('*TCombobox*Listbox.font', "Arial 16 bold")

        # распределение 1 параметр 1 label -----------------------------------------------------------------------------
        self.raspr1_param1_str = tk.StringVar()
        self.tab2_frame221_lbl1 = tk.Label(self.tab2_frame221, textvariable=self.raspr1_param1_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr1_param1_str.set(f'k = {self.raspr1_param1:02d}')
        self.tab2_frame221_lbl1.pack(side=tk.TOP, padx=5)

        # распределение 1 параметр 1 scale -----------------------------------------------------------------------------
        self.tab2_frame221_scale1 = tk.Scale(self.tab2_frame221, from_=0, to=10, orient="horizontal", bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr1_param1_scale)
        self.tab2_frame221_scale1.pack(side=tk.TOP)
        self.tab2_frame221_scale1.set(5)

        # распределение 1 параметр 2 label -----------------------------------------------------------------------------
        self.raspr1_param2_str = tk.StringVar()
        self.tab2_frame221_lbl2 = tk.Label(self.tab2_frame221, textvariable=self.raspr1_param2_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr1_param2_str.set(f'θ = {self.raspr1_param2:02d}')
        self.tab2_frame221_lbl2.pack(side=tk.TOP, padx=5)

        # распределение 1 параметр 2 scale -----------------------------------------------------------------------------
        self.tab2_frame221_scale2 = tk.Scale(self.tab2_frame221, from_=0, to=10, orient="horizontal", bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr1_param2_scale)
        self.tab2_frame221_scale2.pack(side=tk.TOP)
        self.tab2_frame221_scale2.set(5)

        # распределение 1 параметр 4 label -----------------------------------------------------------------------------
        self.raspr1_param4_str = tk.StringVar()
        self.tab2_frame221_lbl4 = tk.Label(self.tab2_frame221, textvariable=self.raspr1_param4_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr1_param4_str.set(f'весовой коэффициент = {self.raspr1_param4:.2f}')
        self.tab2_frame221_lbl4.pack(side=tk.TOP, padx=5)

        # распределение 1 параметр 4 scale -----------------------------------------------------------------------------
        self.tab2_frame221_scale4 = tk.Scale(self.tab2_frame221, from_=0, to=1, resolution=0.01, orient="horizontal",
                                             bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr1_param4_scale)
        self.tab2_frame221_scale4.pack(side=tk.TOP)
        self.tab2_frame221_scale4.set(0.5)

        # распределение 1 параметр 3 label -----------------------------------------------------------------------------
        self.tab2_frame2211 = tk.Frame(self.tab2_frame221, bg='#DDDDDD')
        self.tab2_frame2211.pack(side=tk.TOP)

        self.raspr1_param3_str = tk.StringVar()
        self.tab2_frame221_lbl3 = tk.Label(self.tab2_frame2211, textvariable=self.raspr1_param3_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr1_param3_str.set('смещение 1 =')
        self.tab2_frame221_lbl3.pack(side=tk.LEFT, padx=5)

        # распределение 1 параметр 3 scale -----------------------------------------------------------------------------
        # self.tab2_frame221_scale3 = tk.Scale(self.tab2_frame221, from_=-40, to=40, orient="horizontal", bg='#DDDDDD',
        #                                     width=10, length=150, resolution=0.1, command=self.raspr1_param3_scale)
        # self.tab2_frame221_scale3.pack(side=tk.TOP)

        self.tab2_frame221_spinbox3_text = tk.StringVar()

        self.tab2_frame221_spinbox3 = ttk.Spinbox(self.tab2_frame2211, from_=-100.0, to=100.0, increment=1,
                                                  textvariable=self.tab2_frame221_spinbox3_text)
        self.tab2_frame221_spinbox3.pack(side=tk.LEFT)
        self.tab2_frame221_spinbox3_text.trace('w', self.raspr1_param3_scale)
        self.tab2_frame221_spinbox3.set(0)


        # распределение 1 параметр 32 label ----------------------------------------------------------------------------
        self.tab2_frame2212 = tk.Frame(self.tab2_frame221, bg='#DDDDDD')
        self.tab2_frame2212.pack(side=tk.TOP)

        self.raspr1_param32_str = tk.StringVar()
        self.tab2_frame221_lbl32 = tk.Label(self.tab2_frame2212, textvariable=self.raspr1_param32_str,
                                            font=("Arial Bold", text_size_1),
                                            bg='#DDDDDD')
        self.raspr1_param32_str.set('смещение 2 =')
        self.tab2_frame221_lbl32.pack(side=tk.LEFT, padx=5)

        # распределение 1 параметр 32 scale ----------------------------------------------------------------------------
        # self.tab2_frame221_scale32 = tk.Scale(self.tab2_frame221, from_=-40, to=40, orient="horizontal", bg='#DDDDDD',
        #                                      width=10, length=150, resolution=0.1, command=self.raspr1_param32_scale)
        # self.tab2_frame221_scale32.pack(side=tk.TOP)

        self.tab2_frame221_spinbox32_text = tk.StringVar()

        self.tab2_frame221_spinbox32 = ttk.Spinbox(self.tab2_frame2212, from_=-100.0, to=100.0, increment=1,
                                                   textvariable=self.tab2_frame221_spinbox32_text)
        self.tab2_frame221_spinbox32.pack(side=tk.LEFT)
        self.tab2_frame221_spinbox32_text.trace('w', self.raspr1_param32_scale)
        self.tab2_frame221_spinbox32.set(0)

        # распределение 2 параметр 1 label -----------------------------------------------------------------------------
        self.raspr2_param1_str = tk.StringVar()
        self.tab2_frame222_lbl1 = tk.Label(self.tab2_frame222, textvariable=self.raspr2_param1_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr2_param1_str.set(f'k = {self.raspr2_param1:02d}')
        self.tab2_frame222_lbl1.pack(side=tk.TOP, padx=5)

        # распределение 2 параметр 1 scale -----------------------------------------------------------------------------
        self.tab2_frame222_scale1 = tk.Scale(self.tab2_frame222, from_=0, to=10, orient="horizontal", bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr2_param1_scale)
        self.tab2_frame222_scale1.pack(side=tk.TOP)
        self.tab2_frame222_scale1.set(5)

        # распределение 2 параметр 2 label -----------------------------------------------------------------------------
        self.raspr2_param2_str = tk.StringVar()
        self.tab2_frame222_lbl2 = tk.Label(self.tab2_frame222, textvariable=self.raspr2_param2_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr2_param2_str.set(f'θ = {self.raspr2_param2:02d}')
        self.tab2_frame222_lbl2.pack(side=tk.TOP, padx=5)

        # распределение 2 параметр 2 scale -----------------------------------------------------------------------------
        self.tab2_frame222_scale2 = tk.Scale(self.tab2_frame222, from_=0, to=10, orient="horizontal", bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr2_param2_scale)
        self.tab2_frame222_scale2.pack(side=tk.TOP)
        self.tab2_frame222_scale2.set(5)

        # распределение 2 параметр 4 label -----------------------------------------------------------------------------
        self.raspr2_param4_str = tk.StringVar()
        self.tab2_frame222_lbl4 = tk.Label(self.tab2_frame222, textvariable=self.raspr2_param4_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr2_param4_str.set(f'весовой коэффиициент = {self.raspr2_param4:.2f}')
        self.tab2_frame222_lbl4.pack(side=tk.TOP, padx=5)

        # распределение 2 параметр 4 scale -----------------------------------------------------------------------------
        self.tab2_frame222_scale4 = tk.Scale(self.tab2_frame222, from_=0, to=1, resolution=0.01, orient="horizontal",
                                             bg='#DDDDDD',
                                             width=10, length=150, command=self.raspr2_param4_scale)
        self.tab2_frame222_scale4.pack(side=tk.TOP)
        self.tab2_frame222_scale4.set(0.5)

        # распределение 2 параметр 3 label -----------------------------------------------------------------------------
        self.tab2_frame2221 = tk.Frame(self.tab2_frame222, bg='#DDDDDD')
        self.tab2_frame2221.pack(side=tk.TOP)

        self.raspr2_param3_str = tk.StringVar()
        self.tab2_frame222_lbl3 = tk.Label(self.tab2_frame2221, textvariable=self.raspr2_param3_str,
                                           font=("Arial Bold", text_size_1),
                                           bg='#DDDDDD')
        self.raspr2_param3_str.set('смещение 1 =')
        self.tab2_frame222_lbl3.pack(side=tk.LEFT, padx=5)

        # распределение 2 параметр 3 scale -----------------------------------------------------------------------------
        # self.tab2_frame222_scale3 = tk.Scale(self.tab2_frame222, from_=-40, to=40, orient="horizontal", bg='#DDDDDD',
        #                                     width=10, length=150, resolution=0.1, command=self.raspr2_param3_scale)
        # self.tab2_frame222_scale3.pack(side=tk.TOP)

        self.tab2_frame222_spinbox3_text = tk.StringVar()

        self.tab2_frame222_spinbox3 = ttk.Spinbox(self.tab2_frame2221, from_=-100.0, to=100.0, increment=1,
                                                  textvariable=self.tab2_frame222_spinbox3_text)
        self.tab2_frame222_spinbox3.pack(side=tk.LEFT)
        self.tab2_frame222_spinbox3_text.trace('w', self.raspr2_param3_scale)
        self.tab2_frame222_spinbox3.set(0)

        # распределение 2 параметр 32 label ----------------------------------------------------------------------------
        self.tab2_frame2222 = tk.Frame(self.tab2_frame222, bg='#DDDDDD')
        self.tab2_frame2222.pack(side=tk.TOP)

        self.raspr2_param32_str = tk.StringVar()
        self.tab2_frame222_lbl32 = tk.Label(self.tab2_frame2222, textvariable=self.raspr2_param32_str,
                                            font=("Arial Bold", text_size_1),
                                            bg='#DDDDDD')
        self.raspr2_param32_str.set('смещение 2 =')
        self.tab2_frame222_lbl32.pack(side=tk.LEFT, padx=5)

        # распределение 2 параметр 32 scale ----------------------------------------------------------------------------
        # self.tab2_frame222_scale32 = tk.Scale(self.tab2_frame222, from_=-40, to=40, orient="horizontal", bg='#DDDDDD',
        #                                      width=10, length=150, resolution=0.1, command=self.raspr2_param32_scale)
        # self.tab2_frame222_scale32.pack(side=tk.TOP)

        self.tab2_frame222_spinbox32_text = tk.StringVar()

        self.tab2_frame222_spinbox32 = ttk.Spinbox(self.tab2_frame2222, from_=-100.0, to=100.0, increment=1,
                                                   textvariable=self.tab2_frame222_spinbox32_text)
        self.tab2_frame222_spinbox32.pack(side=tk.LEFT)
        self.tab2_frame222_spinbox32_text.trace('w', self.raspr2_param32_scale)
        self.tab2_frame222_spinbox32.set(0)

        self.raspr1_param22_str = tk.StringVar()
        self.tab2_frame221_lbl21 = tk.Label(self.tab2_frame221, textvariable=self.raspr1_param22_str,
                                            font=("Arial Bold", text_size_1),
                                            bg='#DDDDDD')
        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.tab2_frame221_lbl21.pack(side=tk.TOP, padx=5, pady=5)

        self.raspr2_param22_str = tk.StringVar()
        self.tab2_frame221_lbl22 = tk.Label(self.tab2_frame222, textvariable=self.raspr2_param22_str,
                                            font=("Arial Bold", text_size_1),
                                            bg='#DDDDDD')
        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.tab2_frame221_lbl22.pack(side=tk.TOP, padx=5, pady=5)

        self.raspr1_param221_str = tk.StringVar()
        self.tab2_frame221_lbl211 = tk.Label(self.tab2_frame221, textvariable=self.raspr1_param221_str,
                                             font=("Arial Bold", text_size_1),
                                             bg='#DDDDDD')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')
        self.tab2_frame221_lbl211.pack(side=tk.TOP, padx=5, pady=5)

        self.raspr2_param221_str = tk.StringVar()
        self.tab2_frame221_lbl221 = tk.Label(self.tab2_frame222, textvariable=self.raspr2_param221_str,
                                             font=("Arial Bold", text_size_1),
                                             bg='#DDDDDD')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')
        self.tab2_frame221_lbl221.pack(side=tk.TOP, padx=5, pady=5)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # графики распределений ----------------------------------------------------------------------------------------
        self.tab2_frame23 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame23.pack(side=tk.TOP, pady=4)
        self.tab2_frame231 = tk.Frame(self.tab2_frame23, bg='#DDDDDD')
        self.tab2_frame231.pack(side=tk.LEFT)
        self.tab2_frame232 = tk.Frame(self.tab2_frame23, bg='#DDDDDD')
        self.tab2_frame232.pack(side=tk.LEFT)

        self.tab2_frame231_btn1 = tk.Button(self.tab2_frame231, text="центрировать", font=("Arial", 10),
                                            width=10, command=self.center_1)
        self.tab2_frame231_btn1.pack(side=tk.TOP, padx=0, pady=2)

        # график 1-го распределения ------------------------------------------------------------------------------------
        self.graf1_fig = Figure(figsize=(2, 2), dpi=100)
        self.graf1_plot = self.graf1_fig.add_subplot(1, 20, (4, 20))
        self.graf1_plot.set_title('Распределение по X', fontsize=10)
        self.graf1_canvas = FigureCanvasTkAgg(self.graf1_fig, master=self.tab2_frame231)
        self.graf1_canvas.draw()
        self.graf1_canvas.get_tk_widget().pack(side=tk.TOP, padx=5)

        self.tab2_frame232_btn1 = tk.Button(self.tab2_frame232, text="центрировать", font=("Arial", 10),
                                            width=10, command=self.center_2)
        self.tab2_frame232_btn1.pack(side=tk.TOP, padx=0, pady=2)

        # график 2-го распределения ------------------------------------------------------------------------------------
        self.graf2_fig = Figure(figsize=(2, 2), dpi=100)
        self.graf2_plot = self.graf2_fig.add_subplot(1, 20, (4, 20))
        self.graf2_plot.set_title('Распределение по Y', fontsize=10)
        self.graf2_canvas = FigureCanvasTkAgg(self.graf2_fig, master=self.tab2_frame232)
        self.graf2_canvas.draw()
        self.graf2_canvas.get_tk_widget().pack(side=tk.TOP, padx=5)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # вывод --------------------------------------------------------------------------------------------------------
        self.tab2_frame24 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame24.pack(side=tk.TOP, pady=0)
        self.tab2_frame242 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame242.pack(side=tk.TOP, pady=0)

        self.time_xy_str = tk.StringVar()
        self.time_x_str = tk.StringVar()
        self.time_y_str = tk.StringVar()

        # time_xy label ------------------------------------------------------------------------------------------------
        self.tab2_frame24_lbl1 = tk.Label(self.tab2_frame24, textvariable=self.time_xy_str,
                                          font=("Arial Bold", text_size_2), bg='#BBBBBB')
        self.time_xy_str.set(f'время:         {self.time_xy:.2f}')
        self.tab2_frame24_lbl1.pack(side=tk.LEFT, padx=5, pady=0)

        # time_x label -------------------------------------------------------------------------------------------------
        self.tab2_frame24_lbl2 = tk.Label(self.tab2_frame24, textvariable=self.time_x_str,
                                          font=("Arial Bold", text_size_2), bg='#BBBBBB')
        self.time_x_str.set(f'время до X: {self.time_x:.2f}')
        self.tab2_frame24_lbl2.pack(side=tk.LEFT, padx=5, pady=0)

        # time_y label -------------------------------------------------------------------------------------------------
        self.tab2_frame24_lbl3 = tk.Label(self.tab2_frame24, textvariable=self.time_y_str,
                                          font=("Arial Bold", text_size_2), bg='#BBBBBB')
        self.time_y_str.set(f'время до Y: {self.time_y:.2f}')
        self.tab2_frame24_lbl3.pack(side=tk.LEFT, padx=5, pady=0)
        # --------------------------------------------------------------------------------------------------------------

        self.points_count_str = tk.StringVar()
        self.tab2_frame24_lbl4 = tk.Label(self.tab2_frame242, textvariable=self.points_count_str,
                                          font=("Arial Bold", text_size_2), bg='#DDDDDD')
        self.points_count_str.set(f'осталось экспериментов: {self.points_count_actual:02d}')
        self.tab2_frame24_lbl4.pack(side=tk.TOP)

        # --------------------------------------------------------------------------------------------------------------
        # кнопки -------------------------------------------------------------------------------------------------------
        self.tab2_frame25 = tk.Frame(self.tab2_frame2, bg='#DDDDDD')
        self.tab2_frame25.pack(side=tk.TOP, pady=0)

        # кнопка 3 —-------------------------------------------------------------------------------------------------—
        self.tab2_frame25_btn3 = tk.Button(self.tab2_frame25, text="Стоп", font=("Arial", text_size_3),
                                           bg="#2F4F4F",
                                           fg="#FFFFFF", width=10, command=self.term_action)
        self.tab2_frame25_btn3.pack(side=tk.RIGHT, padx=5, pady=0)

        # кнопка 1 -----------------------------------------------------------------------------------------------------
        self.tab2_frame25_btn1 = tk.Button(self.tab2_frame25, text="Старт", font=("Arial", text_size_3), bg="#2F4F4F",
                                           fg="#FFFFFF", width=10, command=self.start_action)
        self.tab2_frame25_btn1.pack(side=tk.RIGHT, padx=5, pady=0)

        # кнопка 2 -----------------------------------------------------------------------------------------------------
        self.tab2_frame25_btn2 = tk.Button(self.tab2_frame25, text="Обновить", font=("Arial", text_size_3),
                                           bg="#2F4F4F",
                                           fg="#FFFFFF", width=10, command=self.rerun)
        self.tab2_frame25_btn2.pack(side=tk.RIGHT, padx=5, pady=0)
        # --------------------------------------------------------------------------------------------------------------

        # ==============================================================================================================

        # TAB3 =========================================================================================================
        # self.tab3_frame1 = tk.Frame(self.tab3)
        # self.tab3_frame1.pack(side=tk.TOP, pady=5, fill=tk.X)
        # self.tab3_frame11 = tk.Frame(self.tab3_frame1)
        # self.tab3_frame11.pack(side=tk.LEFT, pady=5)
        # self.tab3_frame12 = tk.Frame(self.tab3_frame1)
        # self.tab3_frame12.pack(side=tk.RIGHT, pady=5)
        # self.tab3_frame2 = tk.Frame(self.tab3)
        # self.tab3_frame2.pack(side=tk.TOP, pady=5)
        #
        # k = 2.5

        # self.img1 = Image.open("images/yu.jpeg")  # yu.jpeg
        # self.img1 = self.img1.resize((int(self.img1.size[0] / k), int(self.img1.size[1] / k)))
        # self.tatras1 = ImageTk.PhotoImage(self.img1)
        # canvas1 = tk.Canvas(self.tab3_frame11, width=self.img1.size[0] + 20, height=self.img1.size[1] + 20)
        #
        # canvas1.create_image(10, 10, anchor=tk.NW, image=self.tatras1)
        # canvas1.pack(fill=tk.BOTH, expand=1, padx=50)
        #
        # self.img2 = Image.open("images/se.jpeg")  # se.jpeg
        # self.img2 = self.img2.resize((int(self.img2.size[0] / k), int(self.img2.size[1] / k)))
        # self.tatras2 = ImageTk.PhotoImage(self.img2)
        #
        # canvas2 = tk.Canvas(self.tab3_frame12, width=self.img2.size[0] + 20, height=self.img2.size[1] + 20)
        #
        # canvas2.create_image(10, 10, anchor=tk.NW, image=self.tatras2)
        # canvas2.pack(fill=tk.BOTH, expand=1, padx=50)

        # self.tab3_lbl1 = tk.Label(self.tab3_frame2, text="Авторы:", font=("Arial Bold", 30))
        # self.tab3_lbl2 = tk.Label(self.tab3_frame11, text="Мельник Юрий 317", font=("Arial Bold", 30))
        # self.tab3_lbl3 = tk.Label(self.tab3_frame12, text="Грозный Сергей 317", font=("Arial Bold", 30))
        # self.tab3_lbl4 = tk.Label(self.tab3_frame2, text="Научный руководитель:", font=("Arial Bold", 30))
        # self.tab3_lbl5 = tk.Label(self.tab3_frame2, text="Чичигина Ольга Александровна", font=("Arial Bold", 30))
        #
        # self.tab3_lbl5.pack(side=tk.BOTTOM, pady=10)
        # self.tab3_lbl4.pack(side=tk.BOTTOM, pady=10)
        # self.tab3_lbl3.pack(side=tk.BOTTOM, pady=10)
        # self.tab3_lbl2.pack(side=tk.BOTTOM, pady=10)
        # self.tab3_lbl1.pack(side=tk.BOTTOM, pady=10)
        # ==============================================================================================================

    def draw_working_area(self):
        # сетка
        for i in range(self.canvas_size_x // self.square_size + 1):
            self.canvas.create_line(self.square_size * i, 0, self.square_size * i, self.canvas_size_y, fill="#C0C0C0",
                                    width=1)
        for i in range(self.canvas_size_y // self.square_size + 1):
            self.canvas.create_line(0, self.square_size * i, self.canvas_size_x, self.square_size * i, fill="#C0C0C0",
                                    width=1)

    def change_points_count(self, val):
        self.points_count = int(val)
        if self.points_count >= 100:
            self.point_count_str.set(f'число экспериментов = {self.points_count:02d} ')
        else:
            self.point_count_str.set(f'число экспериментов = {self.points_count:02d}   ')
        self.points_count_str.set(f'осталось экспериментов: {self.points_count:02d}')

    def square_scale(self, val):
        self.square_size_r = int(val)
        self.square_size = 2 * self.square_size_r
        if self.square_size_r >= 100:
            self.square_size_str.set(f'размер квадрата = {self.square_size_r:02d}       ')
        else:
            self.square_size_str.set(f'размер квадрата = {self.square_size_r:02d}         ')
        self.canvas.coords(self.obj, self.square_x - self.square_size_r, self.square_y - self.square_size_r,
                           self.square_x + self.square_size_r, self.square_y + self.square_size_r)

    def disp_x(self):
        w1 = self.raspr1_param4
        w2 = 1 - w1
        if self.raspr1 == "гамма":
            E1 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param3
            E2 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param32
            sigma2 = self.raspr1_param1 * (self.raspr1_param2 ** 2)
        else:
            E1 = self.raspr1_param1 + self.raspr1_param3
            E2 = self.raspr1_param1 + self.raspr1_param32
            sigma2 = self.raspr1_param2 ** 2
        E = w1 * E1 + w2 * E2
        return w1 * (E1 ** 2) + sigma2 + w2 * (E2 ** 2) - E ** 2

    def mean_x(self):
        w1 = self.raspr1_param4
        w2 = 1 - w1
        if self.raspr1 == "гамма":
            E1 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param3
            E2 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param32
        else:
            E1 = self.raspr1_param3
            E2 = self.raspr1_param32

        return w1 * E1 + w2 * E2

    def disp_y(self):
        w1 = self.raspr2_param4
        w2 = 1 - w1
        if self.raspr2 == "гамма":
            E1 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param3
            E2 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param32
            sigma2 = self.raspr2_param1 * (self.raspr2_param2 ** 2)
        else:
            E1 = self.raspr2_param1 + self.raspr2_param3
            E2 = self.raspr2_param1 + self.raspr2_param32
            sigma2 = self.raspr2_param2 ** 2
        E = w1 * E1 + w2 * E2
        return w1 * (E1 ** 2) + sigma2 + w2 * (E2 ** 2) - E ** 2

    def mean_y(self):
        w1 = self.raspr2_param4
        w2 = 1 - w1
        if self.raspr2 == "гамма":
            E1 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param3
            E2 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param32
        else:
            E1 = self.raspr2_param3
            E2 = self.raspr2_param32

        return w1 * E1 + w2 * E2

    def call_frame221_combo1(self, event):
        self.raspr1 = self.tab2_frame221_combo1.get()
        if self.raspr1 == 'гамма':
            self.tab2_frame221_scale1.config(state=tk.NORMAL)
            self.tab2_frame221_scale1.set(5)
            self.raspr1_param1_str.set(f'k = {self.raspr1_param1:02d}')
            self.raspr1_param2_str.set(f'θ = {self.raspr1_param2:02d}')
        else:
            self.tab2_frame221_scale1.set(0)
            self.tab2_frame221_scale1.config(state=tk.DISABLED)
            self.raspr1_param1_str.set(f'μ = {self.raspr1_param1:02d}')
            self.raspr1_param2_str.set(f'σ = {self.raspr1_param2:02d}')
        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')
        self.raspr1_param4_str.set(f'весовой коэффициент = {self.raspr1_param4:.2f}')
        self.print_graf1()

    def call_frame222_combo1(self, event):
        self.raspr2 = self.tab2_frame222_combo1.get()
        if self.raspr2 == 'гамма':
            self.tab2_frame222_scale1.config(state=tk.NORMAL)
            self.tab2_frame222_scale1.set(5)
            self.raspr2_param1_str.set(f'k = {self.raspr2_param1:02d}')
            self.raspr2_param2_str.set(f'θ = {self.raspr2_param2:02d}')
        else:
            self.tab2_frame222_scale1.set(0)
            self.tab2_frame222_scale1.config(state=tk.DISABLED)
            self.raspr2_param1_str.set(f'μ = {self.raspr2_param1:02d}')
            self.raspr2_param2_str.set(f'σ = {self.raspr2_param2:02d}')
        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')
        self.raspr2_param4_str.set(f'весовой коэффициент = {self.raspr2_param4:.2f}')
        self.print_graf2()

    def raspr1_param1_scale(self, val):
        self.raspr1_param1 = int(val)
        if self.raspr1 == 'гамма':
            self.raspr1_param1_str.set(f'k = {self.raspr1_param1:02d}')
        else:
            self.raspr1_param1_str.set(f'μ = {self.raspr1_param1:02d}')

        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

        self.print_graf1()

    def raspr1_param2_scale(self, val):
        self.raspr1_param2 = int(val)
        if self.raspr1 == 'гамма':
            self.raspr1_param2_str.set(f'θ = {self.raspr1_param2:02d}')
        else:
            self.raspr1_param2_str.set(f'σ = {self.raspr1_param2:02d}')

        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

        self.print_graf1()

    def raspr1_param3_scale(self, a, b, c):
        # self.raspr1_param3 = float(self.tab2_frame221_spinbox3.get())
        if self.tab2_frame221_spinbox3.get() is None:
            print('+0+')
        try:
            if float(self.tab2_frame221_spinbox3.get()) > self.canvas_size_y:
                self.tab2_frame221_spinbox3.set(self.canvas_size_x)
            if float(self.tab2_frame221_spinbox3.get()) < -self.canvas_size_x:
                self.tab2_frame221_spinbox3.set(-self.canvas_size_x)

            self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
            self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

            self.raspr1_param3 = float(self.tab2_frame221_spinbox3.get())
            self.print_graf1()
        except:
            print('+exc+')
            self.tab2_frame221_spinbox3.set(-50)
            self.raspr1_param3 = float(-50)

    def raspr1_param32_scale(self, a, b, c):
        if self.tab2_frame221_spinbox32.get() is None:
            print('+++')
        try:
            if float(self.tab2_frame221_spinbox32.get()) > self.canvas_size_x:
                self.tab2_frame221_spinbox32.set(self.canvas_size_x)
            if float(self.tab2_frame221_spinbox32.get()) < -self.canvas_size_x:
                self.tab2_frame221_spinbox32.set(-self.canvas_size_x)

            self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
            self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

            self.raspr1_param32 = float(self.tab2_frame221_spinbox32.get())
            self.print_graf1()
        except:
            print('+++')

    def raspr1_param4_scale(self, val):
        self.raspr1_param4 = float(val)
        self.raspr1_param4_str.set(f'весовой коэффициент = {self.raspr1_param4:.2f}')

        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

        self.print_graf1()

    def raspr2_param1_scale(self, val):
        self.raspr2_param1 = int(val)
        if self.raspr2 == 'гамма':
            self.raspr2_param1_str.set(f'k = {self.raspr2_param1:02d}')
        else:
            self.raspr2_param1_str.set(f'μ = {self.raspr2_param1:02d}')

        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

        self.print_graf2()

    def raspr2_param2_scale(self, val):
        self.raspr2_param2 = int(val)
        if self.raspr2 == 'гамма':
            self.raspr2_param2_str.set(f'θ = {self.raspr2_param2:02d}')
        else:
            self.raspr2_param2_str.set(f'σ = {self.raspr2_param2:02d}')

        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

        self.print_graf2()

    def raspr2_param3_scale(self, a, b, c):
        if self.tab2_frame222_spinbox3.get() is None:
            print('+++')
        try:
            if float(self.tab2_frame222_spinbox3.get()) > self.canvas_size_y:
                self.tab2_frame222_spinbox3.set(self.canvas_size_y)
            if float(self.tab2_frame222_spinbox3.get()) < -self.canvas_size_y:
                self.tab2_frame222_spinbox3.set(-self.canvas_size_y)

            self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
            self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

            self.raspr2_param3 = float(self.tab2_frame222_spinbox3.get())
            self.print_graf2()
        except:
            print('+exc+')
            self.tab2_frame222_spinbox3.set(-50)
            self.raspr2_param3 = float(-50)

    def raspr2_param32_scale(self, a, b, c):
        if self.tab2_frame222_spinbox32.get() is None:
            print('+++')
        try:
            if float(self.tab2_frame222_spinbox32.get()) > self.canvas_size_y:
                self.tab2_frame222_spinbox32.set(self.canvas_size_y)
            if float(self.tab2_frame222_spinbox32.get()) < -self.canvas_size_y:
                self.tab2_frame222_spinbox32.set(-self.canvas_size_y)

            self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
            self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

            self.raspr2_param32 = float(self.tab2_frame222_spinbox32.get())
            self.print_graf2()
        except:
            print('+++')

    def raspr2_param4_scale(self, val):
        self.raspr2_param4 = float(val)
        self.raspr2_param4_str.set(f'весовой коэффициент = {self.raspr2_param4:.2f}')

        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

        self.print_graf2()

    def center_1(self):
        if self.raspr1 == "гамма":
            w1 = self.raspr1_param4
            w2 = 1 - w1
            mu1 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param3
            mu2 = self.raspr1_param1 * self.raspr1_param2 + self.raspr1_param32
            mu = self.raspr1_param1 * self.raspr1_param2
        else:
            w1 = self.raspr1_param4
            w2 = 1 - w1
            mu1 = self.raspr1_param1 + self.raspr1_param3
            mu2 = self.raspr1_param1 + self.raspr1_param32
            mu = self.raspr1_param1

        if abs(self.raspr1_param3) < abs(self.raspr1_param32):
            self.tab2_frame221_spinbox32.set(-w1 * mu1 / w2 - mu)
            self.raspr1_param32 = -w1 * mu1 / w2 - mu
        else:
            self.tab2_frame221_spinbox3.set(-w2 * mu2 / w1 - mu)
            self.raspr1_param3 = -w2 * mu2 / w1 - mu

        self.raspr1_param22_str.set(f'общ. дисперсия = {self.disp_x():.2f}')
        self.raspr1_param221_str.set(f'общ. мат. ожидание = {self.mean_x():.2f}')

    def center_2(self):
        if self.raspr2 == "гамма":
            w1 = self.raspr2_param4
            w2 = 1 - w1
            mu1 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param3
            mu2 = self.raspr2_param1 * self.raspr2_param2 + self.raspr2_param32
            mu = self.raspr2_param1 * self.raspr2_param2
        else:
            w1 = self.raspr2_param4
            w2 = 1 - w1
            mu1 = self.raspr2_param1 + self.raspr2_param3
            mu2 = self.raspr2_param1 + self.raspr2_param32
            mu = self.raspr2_param1

        if abs(self.raspr2_param3) < abs(self.raspr2_param32):
            self.tab2_frame222_spinbox32.set(-w1 * mu1 / w2 - mu)
            self.raspr2_param32 = -w1 * mu1 / w2 - mu
        else:
            self.tab2_frame222_spinbox3.set(-w2 * mu2 / w1 - mu)
            self.raspr2_param3 = -w2 * mu2 / w1 - mu

        self.raspr2_param22_str.set(f'общ. дисперсия = {self.disp_y():.2f}')
        self.raspr2_param221_str.set(f'общ. мат. ожидание = {self.mean_y():.2f}')

    def print_graf1(self):
        self.graf1_plot.clear()
        self.graf1_plot.set_title('Распределение по X', fontsize=10)
        # if self.raspr1_param1 != 0 and self.raspr1_param2 != 0:
        if self.raspr1 == 'гамма':
            shape, scale = self.raspr1_param1, self.raspr1_param2
            mu1 = scale * shape + self.raspr1_param3
            mu2 = scale * shape + self.raspr1_param32
            weight1 = self.raspr1_param4
            weight2 = 1 - weight1
            if self.raspr1_param3 == 0 and self.raspr1_param32 == 0:
                weight1 = 1
            mx = max(mu1, mu2)
            mn = min(mu1, mu2)
            a = mn - 3 * scale * np.sqrt(shape)
            b = mx + 3 * scale * np.sqrt(shape)
            x = np.linspace(a, b, 1000)
            val1 = scipy.stats.gamma.pdf(x, a=shape, loc=self.raspr1_param3, scale=scale) * weight1
            val2 = scipy.stats.gamma.pdf(x, a=shape, loc=self.raspr1_param32, scale=scale) * weight2
            res = np.maximum(val1, val2)
            # self.graf1_plot.set_xticks(np.arange(a, b+1, 5))
            self.graf1_plot.plot(x, res)
            self.graf1_plot.set(ylabel=None)

        else:
            mu, sigma = self.raspr1_param1, self.raspr1_param2
            mu1 = mu + self.raspr1_param3
            mu2 = mu + self.raspr1_param32
            weight1 = self.raspr1_param4
            weight2 = 1 - weight1
            if self.raspr1_param3 == 0 and self.raspr1_param32 == 0:
                weight1 = 1
            mx = max(mu1, mu2)
            mn = min(mu1, mu2)
            a = mn - 3 * sigma
            b = mx + 3 * sigma
            x = np.linspace(a, b, 1000)
            val1 = scipy.stats.norm.pdf(x, mu1, sigma) * weight1
            val2 = scipy.stats.norm.pdf(x, mu2, sigma) * weight2
            res = np.maximum(val1, val2)
            # self.graf1_plot.set_xticks(np.arange(a, b+1, 5))
            self.graf1_plot.plot(x, res)
            self.graf1_plot.set(ylabel=None)

        self.graf1_canvas.draw()

    def print_graf2(self):
        self.graf2_plot.clear()
        self.graf2_plot.set_title('Распределение по Y', fontsize=10)
        # if self.raspr2_param1 != 0 and self.raspr2_param2 != 0:
        if self.raspr2 == 'гамма':
            shape, scale = self.raspr2_param1, self.raspr2_param2
            mu1 = scale * shape + self.raspr2_param3
            mu2 = scale * shape + self.raspr2_param32
            weight1 = self.raspr2_param4
            weight2 = 1 - weight1
            if self.raspr2_param3 == 0 and self.raspr2_param32 == 0:
                weight1 = 1
            mx = max(mu1, mu2)
            mn = min(mu1, mu2)
            a = mn - 3 * scale * np.sqrt(shape)
            b = mx + 3 * scale * np.sqrt(shape)
            x = np.linspace(a, b, 1000)
            val1 = scipy.stats.gamma.pdf(x, a=shape, loc=self.raspr2_param3, scale=scale) * weight1
            val2 = scipy.stats.gamma.pdf(x, a=shape, loc=self.raspr2_param32, scale=scale) * weight2
            res = np.maximum(val1, val2)
            # self.graf1_plot.set_xticks(np.arange(a, b+1, 5))
            self.graf2_plot.plot(x, res)
            self.graf2_plot.set(ylabel=None)

        else:
            mu, sigma = self.raspr2_param1, self.raspr2_param2
            mu1 = mu + self.raspr2_param3
            mu2 = mu + self.raspr2_param32
            weight1 = self.raspr2_param4
            weight2 = 1 - weight1
            if self.raspr2_param3 == 0 and self.raspr2_param32 == 0:
                weight1 = 1
            mx = max(mu1, mu2)
            mn = min(mu1, mu2)
            a = mn - 3 * sigma
            b = mx + 3 * sigma
            x = np.linspace(a, b, 1000)
            val1 = scipy.stats.norm.pdf(x, mu1, sigma) * weight1
            val2 = scipy.stats.norm.pdf(x, mu2, sigma) * weight2
            res = np.maximum(val1, val2)
            # self.graf1_plot.set_xticks(np.arange(a, b+1, 5))
            self.graf2_plot.plot(x, res)
            self.graf2_plot.set(ylabel=None)

        self.graf2_canvas.draw()

    def rerun(self):
        self.canvas.delete("all")
        self.draw_working_area()

        self.square_x = random.randint(self.square_size_r, self.canvas_size_x - self.square_size_r)
        self.square_y = random.randint(self.square_size_r, self.canvas_size_y - self.square_size_r)

        self.point_x = random.randint(self.point_size_r, self.canvas_size_x - self.point_size_r)
        self.point_y = random.randint(self.point_size_r, self.canvas_size_y - self.point_size_r)

        # координатные оси
        self.obj_x = self.canvas.create_line(self.square_x, 0, self.square_x, self.canvas_size_y, fill="#000000",
                                             width=1)
        self.obj_y = self.canvas.create_line(0, self.square_y, self.canvas_size_x, self.square_y, fill="#000000",
                                             width=1)
        # объект
        self.obj = self.canvas.create_rectangle(self.square_x - self.square_size_r, self.square_y - self.square_size_r,
                                                self.square_x + self.square_size_r, self.square_y + self.square_size_r,
                                                outline="#696969",
                                                fill="#2F4F4F")
        # точка
        self.point = self.canvas.create_oval(self.point_x - self.point_size_r, self.point_y - self.point_size_r,
                                             self.point_x + self.point_size_r,
                                             self.point_y + self.point_size_r, outline="#8B4513", fill="#D2691E",
                                             width=2)

        self.time_xy = 0
        self.time_x = 0
        self.time_y = 0
        self.time_xy_str.set(f'время:         {self.time_xy:.2f}')
        self.time_x_str.set(f'время до X: {self.time_x:.2f}')
        self.time_y_str.set(f'время до Y: {self.time_y:.2f}')
        self.points_count_actual = self.points_count
        self.points_count_str.set(f'осталось экспериментов: {self.points_count_actual:02d}')

    def term_action(self):
        # global stop
        #
        # if stop:
        #    self.tab2_frame25_btn3.config(text="стоп")
        #    stop = False
        # else:
        #    self.tab2_frame25_btn3.config(text="возобновить")
        #    stop = True
        #    print('stop x1')

        global stop
        global flag
        global stat

        stop = True
        flag = False
        stat = 0

    def start_action(self):
        global flag
        global flag_x
        global flag_y

        global stat
        global stat_x
        global stat_y

        global stop

        stop = False

        flag = True
        flag_x = True
        flag_y = True

        self.points_count_actual = self.points_count
        self.points_count_str.set(f'осталось экспериментов: {self.points_count_actual:02d}')
        stat = self.points_count - 1
        stat_x = self.points_count - 1
        stat_y = self.points_count - 1

        print('=====================================================')
        print(f'stat = {stat}')
        print(f'stat_x = {stat_x}')
        print(f'stat_y = {stat_y}')

        self.tab2_frame25_btn1.config(state=tk.DISABLED)
        self.tab2_frame25_btn2.config(state=tk.DISABLED)

        threaded = []
        for i in range(self.points_count - 1):
            threaded.append(threading.Thread(target=self.run_action_stat))

        threaded.append(threading.Thread(target=self.run_action))

        if stat > 0:
            thread2 = threading.Thread(target=self.run_time_stat)
        else:
            thread2 = threading.Thread(target=self.run_time)

        print(threading.main_thread().name)
        for i in range(self.points_count):
            threaded[i].start()

        thread2.start()

        self.check_thread(threaded)

    def check_thread(self, threaded):
        for thread in threaded:
            if thread.is_alive():
                continue
            else:
                threaded.remove(thread)
                self.points_count_actual -= 1
                self.points_count_str.set(f'осталось экспериментов: {self.points_count_actual:02d}')

        if threaded:
            self.after(100, lambda: self.check_thread(threaded))
        else:
            self.tab2_frame25_btn1.config(state=tk.NORMAL)
            self.tab2_frame25_btn2.config(state=tk.NORMAL)

    def run_action(self):
        print("Запуск длительного действия...")

        dim_x = 1
        dim_y = -1
        global flag
        global flag_x
        global flag_y
        global stop

        while flag and not stop:
            if abs(self.point_x - self.square_x) <= self.square_size_r and \
                    abs(self.point_y - self.square_y) <= self.square_size_r:
                break

            if abs(self.point_x - self.square_x) <= self.point_size_r:
                flag_x = False

            if abs(self.point_y - self.square_y) <= self.point_size_r:
                flag_y = False

            k = 5
            if self.chk_enabled.get() == 1:
                self.canvas.create_oval(self.point_x - self.point_size_r + k, self.point_y - self.point_size_r + k,
                                        self.point_x + self.point_size_r - k,
                                        self.point_y + self.point_size_r - k, outline="#87CEEB", fill="#87CEEB",
                                        width=2)

            if self.raspr1 == 'гамма':
                shape, scale = self.raspr1_param1, self.raspr1_param2
                val1 = gamma(shape, scale, 1)[0] + self.raspr1_param3
                val2 = gamma(shape, scale, 1)[0] + self.raspr1_param32
                x = dim_x * random.choices([val1, val2], weights=[self.raspr1_param4, 1 - self.raspr1_param4], k=1)[
                    0]
            else:
                mu, sigma = self.raspr1_param1, self.raspr1_param2
                val1 = normal(mu, sigma, 1)[0] + self.raspr1_param3
                val2 = normal(mu, sigma, 1)[0] + self.raspr1_param32
                x = dim_x * random.choices([val1, val2], weights=[self.raspr1_param4, 1 - self.raspr1_param4], k=1)[
                    0]

            if self.raspr2 == 'гамма':
                shape, scale = self.raspr2_param1, self.raspr2_param2
                val1 = gamma(shape, scale, 1)[0] + self.raspr2_param3
                val2 = gamma(shape, scale, 1)[0] + self.raspr2_param32
                y = dim_y * random.choices([val1, val2], weights=[self.raspr2_param4, 1 - self.raspr2_param4], k=1)[
                    0]
            else:
                mu, sigma = self.raspr2_param1, self.raspr2_param2
                val1 = normal(mu, sigma, 1)[0] + self.raspr2_param3
                val2 = normal(mu, sigma, 1)[0] + self.raspr2_param32
                y = dim_y * random.choices([val1, val2], weights=[self.raspr2_param4, 1 - self.raspr2_param4], k=1)[
                    0]

            if (self.point_x + x > self.canvas_size_x) or (self.point_x + x < 0):
                # dim_x *= -1
                x = -x
            if (self.point_y + y > self.canvas_size_y) or (self.point_y + y < 0):
                # dim_y *= -1
                y = -y

            self.point_x += x
            self.point_y += y

            self.canvas.move(self.point, x, y)

            if self.chk2_enabled.get() != 1:
                time.sleep(0.02)

        print("Длительное действие завершено!")
        flag = False

    def run_action_stat(self):
        print("Запуск статистики...")

        dim_x = 1
        dim_y = -1
        global stat
        global stat_x
        global stat_y

        flag_stat_x = True
        flag_stat_y = True

        square_x = random.randint(self.square_size_r, self.canvas_size_x - self.square_size_r)
        square_y = random.randint(self.square_size_r, self.canvas_size_y - self.square_size_r)

        point_x = random.randint(self.point_size_r, self.canvas_size_x - self.point_size_r)
        point_y = random.randint(self.point_size_r, self.canvas_size_y - self.point_size_r)

        while stat and not stop:
            if abs(point_x - square_x) <= self.square_size_r and \
                    abs(point_y - square_y) <= self.square_size_r:
                break

            if flag_stat_x and abs(point_x - square_x) <= self.point_size_r:
                stat_x -= 1
                flag_stat_x = False

            if flag_stat_y and abs(point_y - square_y) <= self.point_size_r:
                stat_y -= 1
                flag_stat_y = False

            if self.raspr1 == 'гамма':
                shape, scale = self.raspr1_param1, self.raspr1_param2
                val1 = gamma(shape, scale, 1)[0] + self.raspr1_param3
                val2 = gamma(shape, scale, 1)[0] + self.raspr1_param32
                x = dim_x * random.choices([val1, val2], weights=[self.raspr1_param4, 1 - self.raspr1_param4], k=1)[0]
            else:
                mu, sigma = self.raspr1_param1, self.raspr1_param2
                val1 = normal(mu, sigma, 1)[0] + self.raspr1_param3
                val2 = normal(mu, sigma, 1)[0] + self.raspr1_param32
                x = dim_x * random.choices([val1, val2], weights=[self.raspr1_param4, 1 - self.raspr1_param4], k=1)[0]

            if self.raspr2 == 'гамма':
                shape, scale = self.raspr2_param1, self.raspr2_param2
                val1 = gamma(shape, scale, 1)[0] + self.raspr2_param3
                val2 = gamma(shape, scale, 1)[0] + self.raspr2_param32
                y = dim_y * random.choices([val1, val2], weights=[self.raspr2_param4, 1 - self.raspr2_param4], k=1)[0]
            else:
                mu, sigma = self.raspr2_param1, self.raspr2_param2
                val1 = normal(mu, sigma, 1)[0] + self.raspr2_param3
                val2 = normal(mu, sigma, 1)[0] + self.raspr2_param32
                y = dim_y * random.choices([val1, val2], weights=[self.raspr2_param4, 1 - self.raspr2_param4], k=1)[0]

            if point_x + x > self.canvas_size_x:
                dim_x *= -1
                continue
            if point_x + x < 0:
                dim_x *= -1
                continue
            if point_y + y > self.canvas_size_y:
                dim_y *= -1
                continue
            if point_y + y < 0:
                dim_y *= -1
                continue

            point_x += x
            point_y += y

            if self.chk2_enabled.get() != 1:
                time.sleep(0.02)

        print("статистика завершена!")
        stat -= 1
        if flag_stat_x:
            stat_x -= 1
            flag_stat_x = False
        if flag_stat_y:
            stat_y -= 1
            flag_stat_y = False

    def run_time(self):
        print('run_time')
        global flag
        global flag_x
        global flag_y

        self.time_xy = 0
        self.time_x = 0
        self.time_y = 0
        while flag:
            time.sleep(0.01)
            self.time_xy += 0.01
            if flag_x:
                self.time_x += 0.01
            if flag_y:
                self.time_y += 0.01
            self.time_xy_str.set(f'время:         {self.time_xy:.2f}')
            self.time_x_str.set(f'время до X: {self.time_x:.2f}')
            self.time_y_str.set(f'время до Y: {self.time_y:.2f}')

        print('time is ', self.time_xy)

    def run_time_stat(self):
        print('run_time_stat')
        global stat
        global stat_x
        global stat_y
        global flag
        global flag_x
        global flag_y
        global stop

        t = 0
        tmp_stat = self.points_count - 1
        tmp_stat_x = self.points_count - 1
        tmp_stat_y = self.points_count - 1

        self.time_xy = 0
        self.time_x = 0
        self.time_y = 0

        self.time_xy_str.set(f'время:         {self.time_xy:.2f}')
        self.time_x_str.set(f'время до X: {self.time_x:.2f}')
        self.time_y_str.set(f'время до Y: {self.time_y:.2f}')

        count = 0
        count_x = 0
        count_y = 0

        flag_count = 1
        flag_x_count = 1
        flag_y_count = 1
        while not stop:
            time.sleep(0.01)
            t += 0.01
            if (tmp_stat > 0) and (stat != tmp_stat):
                print(f'count {count}, t {t}, tmp_stat {tmp_stat}, stat {stat}, XXX {tmp_stat - stat}')
                self.time_xy += (tmp_stat - stat) * t
                tmp_stat = stat
                count += 1
                # print(f'count {count}, t {t}, tmp_stat {tmp_stat}, stat {stat}, XXX {tmp_stat - stat}')
            if (tmp_stat_x > 0) and (stat_x != tmp_stat_x):
                print(
                    f'    count_x {count_x}, t {t}, tmp_stat_x {tmp_stat_x}, stat_x {stat_x}, XXX {tmp_stat_x - stat_x}')
                self.time_x += (tmp_stat_x - stat_x) * t
                tmp_stat_x = stat_x
                count_x += 1
                # print(f'    count_x {count_x}, t {t}, tmp_stat_x {tmp_stat_x}, stat_x {stat_x}, XXX {tmp_stat_x - stat_x}')
            if (tmp_stat_y > 0) and (stat_y != tmp_stat_y):
                print(
                    f'        count_y {count_y}, t {t}, tmp_stat_y {tmp_stat_y}, stat_y {stat_y}, XXX {tmp_stat_y - stat_y}')
                self.time_y += (tmp_stat_y - stat_y) * t
                tmp_stat_y = stat_y
                count_y += 1
                # print(f'        count_y {count_y}, t {t}, tmp_stat_y {tmp_stat_y}, stat_y {stat_y}, XXX {tmp_stat_y - stat_y}')

            if not flag and flag_count:
                self.time_xy += t
                flag_count -= 1
                print('main ', t)
            if not flag_x and flag_x_count:
                self.time_x += t
                flag_x_count -= 1
                print('    main_x ', t)
            if not flag_y and flag_y_count:
                self.time_y += t
                flag_y_count -= 1
                print('        main_y ', t)

            if not flag and (stat <= 0):
                break

        self.time_xy /= self.points_count
        self.time_x /= self.points_count
        self.time_y /= self.points_count

        # print('______time is ', self.time_xy)
        print('=====================================================')
        print(f'stat = {stat} tmp_stat = {tmp_stat}')
        print(f'stat_x = {stat_x} tmp_stat_x = {tmp_stat_x}')
        print(f'stat_y = {stat_y} tmp_stat_y = {tmp_stat_y}')
        print(f'count {count}')
        print(f'count_x {count_x}')
        print(f'count_y {count_y}')
        print(f'time = {self.time_xy}')
        print(f'time_x = {self.time_x}')
        print(f'time_y = {self.time_y}')

        self.time_xy_str.set(f'время:         {self.time_xy:.2f}')
        self.time_x_str.set(f'время до X: {self.time_x:.2f}')
        self.time_y_str.set(f'время до Y: {self.time_y:.2f}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
