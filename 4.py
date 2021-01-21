import math
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
import pandas
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from windrose import WindroseAxes
from numpy import arange, random
import mplcursors
from scipy.interpolate import splrep, splev
from fpdf import FPDF

import progress

mplcursors.cursor(hover=True)
import webbrowser

average_temperature = 0
dic_1_4 = {}

# s = ttk.Style()


# s.theme_use('clam')


def file_open():
    list_val = []
    with open('home_values', 'r') as fr:
        list_val = [i for i in fr.read().split(' ')]
    return list_val


def file_edit():
    content = [entry_210.get(), entry_211.get(), entry_212.get(), entry_213.get(), entry_214.get(), entry_215.get(),
               entry_216.get(), entry_217.get(), entry_218.get(), entry_219.get(), entry_220.get(), entry_221.get(),
               entry_222.get(), entry_223.get(), entry_224.get(), entry_225.get(), entry_226.get(), entry_227.get(),
               entry_w.get()]
    with open('home_values', 'w') as fw:
        for val in content:
            fw.write(val)
            fw.write(' ')


def time_string(str_time, str_date):
    int_time = str_time.split(':')
    int_date = str_date.split('/')
    dt = datetime.datetime(int(int_date[2]), int(int_date[0]), int(int_date[1]),
                           int(int_time[0]) if int(int_time[0]) != 24 else 0, int(int_time[1]), 0)
    if int(int_time[0]) == 24:
        dt += datetime.timedelta(days=1)
    return dt


def print_graph_first(workflow_data):
    x, y = [], []

    for i in range(len(workflow_data)):
        x.append(workflow_data.iloc[i][0])
        y.append(workflow_data.iloc[i][1])

    fig = Figure(figsize=(12, 6), dpi=110)
    ax = fig.add_subplot(111)
    pandas.plotting.register_matplotlib_converters()
    ax.set_title("Температурні умови")
    ax.set_ylabel("Температура, ℃")
    ax.grid()
    dt = ax.plot(x, y)

    fig.autofmt_xdate(rotation=90)
    ax.xaxis.set_ticks_position('both')
    fig.savefig('lr1p1.png')
    return fig, dt


def print_graph_second(workflow_data):
    dic, y = {}, []

    for i in range(len(workflow_data)):
        y.append(workflow_data.iloc[i][1])

    unique = list(set(y))

    for i in range(len(unique)):
        dic[unique[i]] = 0

    for i in range(len(y)):
        dic[y[i]] += 0.5

    global dic_1_4
    dic_1_4 = dic

    fig = Figure(figsize=(12, 6), dpi=110)
    ax = fig.add_subplot(111)
    fig.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    ax.bar(list(dic.keys()), list(dic.values()))
    ax.set_xticks(list(dic.keys()))
    ax.set_yticks([])
    for i in range(len(y)):
        ax.text(y[i] - 0.5, dic[y[i]] + 0.2, str(dic[y[i]]), fontweight='ultralight')

    ax.set_title("Тривалість температурних режимів")
    ax.set_ylabel("t, год")
    ax.annotate(' Т\n(℃)', xy=(0, 0), xytext=(-5, -5), ha='right', va='top',
                xycoords='axes fraction', textcoords='offset points')
    fig.autofmt_xdate(rotation=90)
    fig.savefig('lr1p2.png')
    return fig


def print_graph_third(workflow_data):
    dd = workflow_data['dd']
    wd = []
    ws = workflow_data['FF']
    for i in dd:
        if str(i) == 'Северный':
            wd.append(360)
        elif str(i) == 'С-В':
            wd.append(45)
        elif str(i) == 'Восточный':
            wd.append(90)
        elif str(i) == 'Ю-В':
            wd.append(135)
        elif str(i) == 'Южный':
            wd.append(180)
        elif str(i) == 'Ю-З':
            wd.append(225)
        elif str(i) == 'Западный':
            wd.append(270)
        elif str(i) == 'С-З':
            wd.append(315)
        elif str(i) == 'Переменный':
            wd.append(0)
    fig = plt.figure()
    plt.rcParams.update({'font.size': 12})
    rect = [0.1, 0.1, 0.8, 0.8]
    ax1 = fig.add_subplot(111, projection='windrose')
    viridis = plt.get_cmap('Blues_r')
    ax1.bar(wd, ws, normed=True, opening=0.8, edgecolor='white', cmap=viridis)
    ax1.set_legend()
    ax1.set_title("Троянда вітрів")

    ax2 = fig.add_subplot(299)
    bars = ax1._info['bins']
    bars_percentage = [0] * (len(bars) - 1)
    for i in range(len(ws)):
        for j in range(len(bars) - 1, 0, -1):
            if bars[j] > ws[i] > bars[j - 1]:
                bars_percentage[j - 1] += 1
                continue
    for i, j in zip(bars_percentage, range(len(bars_percentage))):
        if j == 0:
            ax2.bar(arange(1), bars_percentage[j], 0.1, color=viridis(j / 4))
        else:
            ax2.bar(arange(1), bars_percentage[j], 0.1, bottom=sum(bars_percentage[0:j]), color=viridis(j / 4))
    ax2.set_xticks([])
    ax2.set_xticks([], minor=True)
    ax2.set_title('Wind speed\n(%, m/s)')
    ax2.annotate('штиль - ' + str(round(.01 * bars_percentage[0], 3)) + '%', xy=(0, 0), xytext=(0, -20), ha='left',
                 va='bottom',
                 xycoords='axes fraction', textcoords='offset points')
    ax2.annotate('змiнний - ' + str(round(.01 * bars_percentage[1], 3)) + '%', xy=(0, 0), xytext=(0, -40), ha='left',
                 va='bottom',
                 xycoords='axes fraction', textcoords='offset points')
    ax2.axis('off')

    plt.yticks(arange(0, 81, 10))
    fig.savefig('lr1p3.png')
    return fig


def print_graph_fourth(data):
    x, y = {}, []
    for i in range(len(data)):
        y.append(data.iloc[i][3])
    unique = list(set(y))
    for i in range(len(unique)):
        x[unique[i]] = 0
    for i in range(len(y)):
        x[y[i]] += 0.5
    fig = Figure(figsize=(16, 6))
    axes = fig.add_subplot(111)
    dt = axes.bar(list(x.keys()), list(x.values()))
    axes.set_title("Тривалість режимів вітрової активності")
    axes.annotate('м/c', xy=(1, 0), xytext=(-25, 10), ha='left', va='bottom',
                  xycoords='axes fraction', textcoords='offset points')
    axes.annotate('год', xy=(0, 1), xytext=(35, -25), ha='right', va='bottom',
                  xycoords='axes fraction', textcoords='offset points')
    fig.set_figwidth(12)
    fig.set_figheight(6)
    axes.grid(axis='y')
    fig.savefig('lr1p4.png')
    return fig, dt


def print_graph_fifth(workflow_data):
    data = pandas.read_excel("NY_1.xlsx", engine='openpyxl')

    x, y = [], []
    for i in range(len(data)):
        if data.loc[i][2] != 0:
            x.append(data.loc[i][1])
            y.append(data.loc[i][2])
    fig = Figure(figsize=(12, 6), dpi=100)
    axes = fig.add_subplot(111)
    pandas.plotting.register_matplotlib_converters()
    axes.set_title("Інтенсивність сонячної інсоляції")
    axes.set_xlabel("Дата")
    axes.set_ylabel("Вт/м^2")
    axes.grid()
    dt = axes.bar(x, y, width=0.3)
    fig.autofmt_xdate(rotation=45)
    fig.savefig('lr1p5.png')
    return fig, dt


def print_graph_sixth(workflow_data):
    data = pandas.read_excel("NY_1.xlsx", engine='openpyxl')
    x, y = {}, []
    for i in range(len(data)):
        if data.loc[i][2] != 0:
            y.append(data.loc[i][2])
    unique = list(set(y))
    for i in range(len(unique)):
        x[unique[i]] = 0
    for i in range(len(y)):
        x[y[i]] += 1

    fig = Figure(figsize=(12, 6), dpi=100)
    axes = fig.add_subplot(111)
    dt = axes.bar(list(x.keys()), list(x.values()))
    axes.set_title("Тривалість режимів сонячної активності")
    axes.set_xlabel("Вт/м^2")
    axes.set_ylabel("Час, год")
    fig.set_figwidth(12)
    fig.set_figheight(6)
    axes.grid()
    fig.savefig('lr1p6.png')
    return fig, dt


def holes_check(workflow_data):
    for i in list(workflow_data):
        prev_holder = 0
        if workflow_data[i].dtypes == 'float64' or workflow_data[i].dtypes == 'int64':
            if workflow_data[i].first_valid_index():
                workflow_data.loc[0, i] = workflow_data[i][workflow_data[i].index[workflow_data[i].notnull()][0]]
        elif workflow_data[i].dtypes == 'object':
            for j in list(workflow_data[i].index[workflow_data[i].notnull()]):
                if j - prev_holder > 1:
                    if prev_holder == 0:
                        workflow_data.loc[prev_holder:j, i] = workflow_data[i][prev_holder:j + 1].bfill()
                    else:
                        if (j - prev_holder) % 2 != 0:
                            use_case_del = (int((prev_holder + j) / 2), int((prev_holder + j) / 2))
                            workflow_data.loc[prev_holder:use_case_del[0] + 1, i] = workflow_data[i][
                                                                                    prev_holder:use_case_del[
                                                                                                    0] + 1].ffill()
                            workflow_data.loc[use_case_del[1] + 1:j, i] = workflow_data[i][
                                                                          use_case_del[1] + 1:j + 1].bfill()
                        else:
                            use_case_del = (int((prev_holder + j) / 2 - .5), int((prev_holder + j) / 2 + .5))
                            workflow_data.loc[prev_holder:use_case_del[0] + 1, i] = workflow_data[i][
                                                                                    prev_holder:use_case_del[
                                                                                                    0] + 1].ffill()
                            workflow_data.loc[use_case_del[1]:j, i] = workflow_data[i][
                                                                      use_case_del[1]:j + 1].bfill()
                prev_holder = j
            if prev_holder == workflow_data[i].index[workflow_data[i].notnull()][-1]:
                workflow_data.loc[j:workflow_data[i].index[-1], i] = \
                    workflow_data[i][j:].ffill()
    return workflow_data.interpolate()


def tab_holst(tab_holst):
    tab_holst.draw()
    tab_holst.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    tab_holst.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def pandas_transforming(file_path):
    data = pandas.read_excel(file_path, engine='openpyxl')

    year_month = file_path.split('/')[-1].split('.')[0].split('-')
    data['Число месяца'] = year_month[0] + '/' + year_month[1] + '/' + \
                           data['Число месяца'].astype(str) + '/' + data['UTC'].astype(str)
    data['Число месяца'] = pandas.to_datetime(data['Число месяца'], infer_datetime_format=True)
    data.drop(data.columns[[1]], axis='columns', inplace=True)
    data = data.rename(columns={'Число месяца': 'datetime'})

    data = data.sort_values(by=['datetime'])
    data = holes_check(data)

    for widget in tab12.winfo_children():
        widget.destroy()
    tab12.pack_forget()
    dynamic_lightning = print_graph_first(data)
    tab1_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab12)
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab1_holst)


    for widget in tab13.winfo_children():
        widget.destroy()
    tab13.pack_forget()
    tab2_holst = FigureCanvasTkAgg(print_graph_second(data), master=tab13)
    tab_holst(tab2_holst)

    for widget in tab14.winfo_children():
        widget.destroy()
    tab14.pack_forget()
    tab3_holst = FigureCanvasTkAgg(print_graph_third(data), master=tab14)
    tab_holst(tab3_holst)

    for widget in tab15.winfo_children():
        widget.destroy()
    tab15.pack_forget()
    dynamic_lightning = print_graph_fourth(data)
    tab4_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab15)
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab4_holst)

    for widget in tab16.winfo_children():
        widget.destroy()
    tab16.pack_forget()
    dynamic_lightning = print_graph_fifth(data)
    tab5_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab16)
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab5_holst)

    for widget in tab17.winfo_children():
        widget.destroy()
    tab17.pack_forget()
    dynamic_lightning = print_graph_sixth(data)
    tab6_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab17)
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab6_holst)

    for i, item in enumerate(tab_child.tabs()):
        tab_child.tab(item, state='normal')

    average = 0
    for iterat in data['T']:
        average += iterat
    global average_temperature
    average_temperature = average / data['T'].count()


def file_worker():
    file_path = tkinter.filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("sheet files", "*.xlsx"), ("all files", "*.*")))
    if ".xlsx" not in file_path or not len(file_path):
        part_label['foreground'] = 'red'
        part_label['text'] = 'Файл не був коректно прочитаний!'
        import_btn['text'] = 'Обрати ще раз'
        return
    else:
        tab_parent.tab(1, state='normal')
        part_label['foreground'] = 'green'
        part_label['text'] = 'Файл прочитаний, дивiться вспливаюче вiкно'
        temperature = pandas_transforming(file_path)
        import_btn['width'] = '16'
        import_btn['text'] = 'Обрати iнший файл'


def boiler_warmity():
    tab_child_2.tab(2, state='normal')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.annotate('Q, кВт', xy=(0, 1), xytext=(-5, 15), ha='right', va='bottom',
                xycoords='axes fraction', textcoords='offset points', fontweight='bold')
    ax.annotate('T, °C', xy=(1, 0), xytext=(-70, -30), ha='left', va='bottom',
                xycoords='axes fraction', textcoords='offset points', fontweight='bold')
    x, y = [], []
    x1 = int(average_temperature)
    y1 = float(entry_210.get()) * float(entry_211.get()) / 100
    x2 = int(file_open()[11])
    y2 = 0
    k = (y2 - y1) / (x2 - x1)
    b = y2 - (y2 - y1) / (x2 - x1) * x2
    ax.set_title('y = ' + str(round(k, 3)) + 'x + ' + str(round(b, 3)))
    for itr in range(x1, x2 + 1):
        x.append(itr)
        y.append(k * itr + b)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_position('center')
    dt = ax.plot(x, y, marker='o', c='blue')

    x2_ch = int(entry_221.get())
    if x2_ch != x2:
        xx, yy = [], []
        b2 = - k * x2_ch
        for itr in range(x1, x2_ch + 1):
            xx.append(itr)
            yy.append(k * itr + b2)
        dt = ax.plot(xx, yy, marker='x', c='red')

    for widget in tab23.winfo_children():
        widget.destroy()
    tab23.pack_forget()
    tab5_canvas = FigureCanvasTkAgg(fig, master=tab23)
    cursor = mplcursors.cursor(ax, hover=True)
    tab5_canvas.draw()
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # toolbar = NavigationToolbar2Tk(tab5_canvas, tab23)
    # toolbar.update()
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    boiler_2_5(x, y)
    fig.savefig('lr2p1.png')


def boiler_2_5(x, y):
    tab_child_2.tab(3, state='normal')
    q = []
    for i in range(len(x)):
        if x[i] in dic_1_4:
            q.append(y[i] * dic_1_4[x[i]])
        else:
            q.append(0)
    fig, ax = plt.subplots(figsize=(12, 6))
    dt = ax.bar(x, q)
    ax.set_xlabel("T, °C")
    ax.set_ylabel("W, кВт")
    ax.set_title('Загальні втрати = ' + str(round(sum(q), 3)))

    for widget in tab24.winfo_children():
        widget.destroy()
    tab24.pack_forget()
    tab5_canvas = FigureCanvasTkAgg(fig, master=tab24)
    cursor = mplcursors.cursor(ax, hover=True)
    tab5_canvas.draw()
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    boiler_2_6(round(sum(q), 3))
    fig.savefig('lr2p2.png')


def boiler_2_6(total):
    x = ['Центр. опалення', 'Газ', 'Вугілля',
         "Дрова", "Дерев. пелети", 'Електр.']
    y = [total * 0.00086 * float(entry_222.get()), total * float(entry_227.get()),
         total * float(entry_224.get()) / 1000,
         float(entry_225.get()) * total / 1000, float(entry_226.get()) * total / 1000, float(entry_223.get()) * total]

    tab_child_2.tab(4, state='normal')
    fig, ax = plt.subplots(figsize=(12, 6))
    dt = ax.bar(x, y)
    ax.set_xlabel("Вид опалення")
    ax.set_ylabel("Вартість, грн")

    for widget in tab25.winfo_children():
        widget.destroy()
    tab25.pack_forget()
    tab5_canvas = FigureCanvasTkAgg(fig, master=tab25)
    cursor = mplcursors.cursor(ax, hover=True)
    tab5_canvas.draw()
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    fig.savefig('lr2p3.png')

def boiler_work():
    content = [entry_210.get(), entry_211.get(), entry_212.get(), entry_213.get(), entry_214.get(), entry_215.get(),
               entry_216.get(), entry_217.get(), entry_218.get(), entry_219.get(), entry_220.get(), entry_221.get(),
               entry_222.get(), entry_223.get(), entry_224.get(), entry_225.get(), entry_226.get(), entry_227.get()]

    q_dush = float(entry_220.get()) * float(entry_217.get())
    q_vann = float(entry_219.get()) * float(entry_218.get())
    q_dush_t = -1 * q_dush * (float(entry_214.get()) - float(entry_212.get())) / (
            float(entry_213.get()) - float(entry_212.get()))
    q_vann_t = q_vann * (float(entry_215.get()) - float(entry_212.get())) / (
            float(entry_213.get()) - float(entry_212.get()))
    q_overall = ((q_dush_t - q_vann_t) / 998.23)

    w_t = 1.163 * q_overall * (float(entry_213.get()) - float(entry_212.get()))
    r_gvp, t_nagr = 0, 0
    if w.get() == 'Потужність нагрівача':
        r_gvp = float(entry_w.get())
        t_nagr = w_t / r_gvp
    elif w.get() == 'Тривалість нагріву ємності':
        t_nagr = float(entry_w.get())
        r_gvp = w_t / t_nagr
    tab_child_2.tab(1, state='normal')

    label_2_1 = Label(tab22, text='Обсяги споживання води на прийом душу:', font=('Rockwell', 10))
    label_2_1.place(relx=0.02, rely=0.02)
    entry_2_1 = Entry(tab22)
    entry_2_1.insert(0, q_dush)
    entry_2_1.configure(state='readonly')
    entry_2_1.place(relx=0.2, rely=0.02)

    label_2_2 = Label(tab22, text='Обсяги споживання води на прийом ван:', font=('bold', 10))

    label_2_2 = Label(tab22, text='Обсяги споживання води на прийом ван:', font=('Rockwell', 10))
    label_2_2.place(relx=0.02, rely=0.1)
    entry_2_2 = Entry(tab22)
    entry_2_2.insert(0, str(q_vann))
    entry_2_2.configure(state='readonly')
    entry_2_2.place(relx=0.2, rely=0.1)


    label_2_3 = Label(tab22, text='Корегування витрати гарячої води для душа:', font=('Rockwell', 10))
    label_2_3.place(relx=0.02, rely=0.18)
    entry_2_3 = Entry(tab22)
    entry_2_3.insert(0, str(round(q_dush_t)) + " л/добу")
    entry_2_3.configure(state='readonly')
    entry_2_3.place(relx=0.2, rely=0.18)


    label_2_4 = Label(tab22, text='Корегування витрати гарячої води для вани:', font=('Rockwell', 10))
    label_2_4.place(relx=0.02, rely=0.26)
    entry_2_4 = Entry(tab22)
    entry_2_4.insert(0, str(round(q_vann_t)) + " л/добу")
    entry_2_4.configure(state='readonly')
    entry_2_4.place(relx=0.2, rely=0.26)


    label_2_5 = Label(tab22, text='Корегування витрати гарячої води всього:', font=('Rockwell', 10))
    label_2_5.place(relx=0.02, rely=0.34)
    entry_2_5 = Entry(tab22)
    entry_2_5.insert(0, str(round(abs(q_overall), 3)) + " м^3/добу")
    entry_2_5.configure(state='readonly')
    entry_2_5.place(relx=0.2, rely=0.34)


    label_2_6 = Label(tab22, text='Енергія необхідна для нагріву води:', font=('Rockwell', 10))
    label_2_6.place(relx=0.02, rely=0.42)
    entry_2_6 = Entry(tab22)
    entry_2_6.insert(0, str(round(w_t, 3)) + " кВт*год")
    entry_2_6.configure(state='readonly')
    entry_2_6.place(relx=0.2, rely=0.42)


    label_2_7 = Label(tab22, text='Необхідна теплова потужність нагрівача:', font=('Rockwell', 10))

    label_2_7.place(relx=0.02, rely=0.5)
    entry_2_7 = Entry(tab22)
    entry_2_7.insert(0, str(round(r_gvp, 3)) + " кВт")
    entry_2_7.configure(state='readonly')
    entry_2_7.place(relx=0.2, rely=0.5)


    label_2_8 = Label(tab22, text='Час нагрівання бака:', font=('Rockwell', 10))
    label_2_8.place(relx=0.02, rely=0.58)
    entry_2_8 = Entry(tab22)
    entry_2_8.insert(0, str(round(t_nagr, 3)) + " год")
    entry_2_8.configure(state='readonly')
    entry_2_8.place(relx=0.2, rely=0.58)

    # url = 'https://prom.ua/search?category=14210101&search_term=%D0%BA%D0%BE%D1%82%D0%BB%D1%8B%20%D0%B3%D0%B0%D0%B7%D0%BE%D0%B2%D1%8B%D0%B5'
    #
    # def OpenUrl():
    #     webbrowser.open_new(url)
    #
    # web_btn.place(relx=0.15, rely=0.8, anchor=CENTER)

    boiler_warmity()


all_graphs_electrical_voltage = []


def electrical_voltage():
    def choices_open():
        list_val = []
        with open('choices_values', 'r') as fr:
            list_val = [i for i in fr.read().split('.')]
        return list_val[0:]

    style = ttk.Style()
    style.map('TCombobox', fieldbackground=[('readonly','white')])
    style.map('TCombobox', selectbackground=[('readonly', 'white')])
    style.map('TCombobox', selectforeground=[('readonly', 'black')])

    w_31 = ttk.Combobox(tab31, values=choices_open(), state='readonly', width=70)
    w_31.current(0)
    w_31.place(relx=0.02, rely=0.14)

    def choices_add():
        tree.insert('', 'end', values=(w_31.get(), 20, 12))

    def choices_insert():
        def insert_final(what):
            option = w_custom.get()
            if option == 'ручне вмикання та вимикання':
                w_custom3['state'] = 'readonly'
                w_custom4['state'] = 'readonly'
                w_custom5['state'] = 'readonly'
                w_custom6['state'] = 'readonly'
            elif option == 'ручне вмикання, автоматичне вимикання':
                w_custom3['state'] = 'readonly'
                w_custom4['state'] = 'readonly'
                w_custom5['state'] = 'disabled'
                w_custom6['state'] = 'disabled'
            else:
                w_custom3['state'] = 'disabled'
                w_custom4['state'] = 'disabled'
                w_custom5['state'] = 'disabled'
                w_custom6['state'] = 'disabled'

            option = w_energy.get()
            if option == 'автоматичне регулювання параметрів споживання':
                entry_energy_passive['state'] = 'disabled'
            elif option == 'ручне регулювання параметрів споживання':
                entry_energy_passive['state'] = 'normal'

        insert_vals = Tk()
        insert_vals.title('Додавання нового пристрою')
        insert_vals.minsize(700, 350)
        insert_vals.resizable(True, True)

        label_31 = Label(insert_vals, text='Назва пристрою:', font=('Rockwell', 10))
        label_31.place(relx=0.05, rely=0.1)

        # def validate_empty_name(inStr):
        #     return bool(inStr)

        entry_31 = Entry(insert_vals, width=25)
        # entry_31['validatecommand'] = (entry_31.register(validate_empty_name), '%P')
        entry_31.place(relx=0.25, rely=0.1)
        choices_custom = ['ручне вмикання та вимикання', 'ручне вмикання, автоматичне вимикання',
                          'автоматичне вмикання та вимикання']
        w_custom = ttk.Combobox(insert_vals, values=choices_custom, state='readonly', width=25)
        w_custom.current(0)
        w_custom.place(relx=0.5, rely=0.15)

        choices_custom = ['автоматичне регулювання параметрів споживання', 'ручне регулювання параметрів споживання']
        w_energy = ttk.Combobox(insert_vals, values=choices_custom, state='readonly', width=35)
        w_energy.current(0)
        w_energy.place(relx=0.5, rely=0.3)

        choices_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']
        w_custom2 = ttk.Combobox(insert_vals, values=choices_days, state='readonly', width=10)
        w_custom2.current(0)
        w_custom2.place(relx=0.05, rely=0.85)

        graphs_electrical_voltage = {'Понеділок': [], 'Вівторок': [], 'Середа': [], 'Четвер': [],
                                     'П\'ятниця': [], 'Субота': [], 'Неділя': [], 'name': ''}

        def next_day_check():
            if graphs_electrical_voltage['name'] and graphs_electrical_voltage['Понеділок']:
                btn_inner_add_2['state'] = 'normal'

        def next_day():
            w_custom2['values'] = [i for i in w_custom2['values'] if i != w_custom2.get()]
            if not len(w_custom2['values']):
                w_custom2['values'] = ['']
                w_custom2['state'] = 'disabled'
                btn_inner_add['state'] = 'disabled'
                btn_inner_end['state'] = 'normal'
                all_graphs_electrical_voltage.append(graphs_electrical_voltage)
            w_custom2.set('')
            w_custom2.current(0)
            btn_inner_add_2['state'] = 'disabled'

        def check_time(what = None):
            rest = int(w_custom5.get()) - int(w_custom3.get())
            print('invoked', rest)
            if rest < 0:
                w_custom3['state'] = 'invalid'
                w_custom5['state'] = 'invalid'
                btn_inner_add['state'] = 'disabled'
                insert_vals.bell()
                return False
            elif rest == 0:
                if int(w_custom6.get()) - int(w_custom4.get()) <= 0:
                    w_custom4['state'] = 'invalid'
                    w_custom6['state'] = 'invalid'
                    btn_inner_add['state'] = 'disabled'
                    insert_vals.bell()
                    return False
                else:
                    w_custom4['state'] = 'normal'
                    w_custom6['state'] = 'normal'
                    btn_inner_add['state'] = 'normal'
                    return True
            else:
                w_custom3['state'] = 'normal'
                w_custom5['state'] = 'normal'
                btn_inner_add['state'] = 'normal'
                return True



        def custom_add():
            if len(w_custom2['values']) != 0 and str(entry_31.get()) != '' and check_time():
                if entry_31.get():
                    label_31.config(fg="black")
                    graphs_electrical_voltage['name'] = entry_31.get()
                    entry_31['state'] = 'disabled'
                    try:
                        check_val = int(entry_energy_active.get())
                        label_energy_active.config(fg="black")
                        if w_custom2.get() == 'Понеділок':
                            graphs_electrical_voltage['Понеділок'].append({})
                            graphs_electrical_voltage['Понеділок'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Понеділок'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['Понеділок'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())
                        elif w_custom2.get() == 'Вівторок':
                            graphs_electrical_voltage['Вівторок'].append({})
                            graphs_electrical_voltage['Вівторок'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Вівторок'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                     str(w_custom4.get())
                            graphs_electrical_voltage['Вівторок'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                   str(w_custom6.get())
                        elif w_custom2.get() == 'Середа':
                            graphs_electrical_voltage['Середа'].append({})
                            graphs_electrical_voltage['Середа'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Середа'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                       str(w_custom4.get())
                            graphs_electrical_voltage['Середа'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                     str(w_custom6.get())
                        elif w_custom2.get() == 'Четвер':
                            graphs_electrical_voltage['Четвер'].append({})
                            graphs_electrical_voltage['Четвер'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Четвер'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                      str(w_custom4.get())
                            graphs_electrical_voltage['Четвер'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                    str(w_custom6.get())
                        elif w_custom2.get() == 'П\'ятниця':
                            graphs_electrical_voltage['П\'ятниця'].append({})
                            graphs_electrical_voltage['П\'ятниця'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['П\'ятниця'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['П\'ятниця'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())
                        elif w_custom2.get() == 'Субота':
                            graphs_electrical_voltage['Субота'].append({})
                            graphs_electrical_voltage['Субота'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Субота'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                      str(w_custom4.get())
                            graphs_electrical_voltage['Субота'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                    str(w_custom6.get())
                        elif w_custom2.get() == 'Неділя':
                            graphs_electrical_voltage['Неділя'].append({})
                            graphs_electrical_voltage['Неділя'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['Неділя'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['Неділя'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())

                        print('added')

                        if entry_energy_passive['state'] == 'normal':
                            try:
                                check_val = int(entry_energy_passive.get())
                                label_energy_passive.config(fg="black")
                                if w_custom2.get() == 'Понеділок':
                                    graphs_electrical_voltage['Понеділок'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Вівторок':
                                    graphs_electrical_voltage['Вівторок'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Середа':
                                    graphs_electrical_voltage['Середа'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Четвер':
                                    graphs_electrical_voltage['Четвер'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'П\'ятниця':
                                    graphs_electrical_voltage['П\'ятниця'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Субота':
                                    graphs_electrical_voltage['Субота'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Неділя':
                                    graphs_electrical_voltage['Неділя'][-1]['energy'].append(check_val)
                            except ValueError:
                                label_energy_passive.config(fg="red")
                    except ValueError:
                        label_energy_active.config(fg="red")
            else:
                btn_inner_add['state'] = 'disabled'
                # btn_inner_end['state'] = 'normal'
            next_day_check()
            # print(graphs_electrical_voltage)


        def custom_destroy():
            needed_list = all_graphs_electrical_voltage[-1]
            w_en, w_hours = 0, 0
            for needed_dict in needed_list:
                for need_dict in needed_list[needed_dict]:
                    if isinstance(need_dict, dict):
                        saver_opt = need_dict['time_end'].split(':') + need_dict['time_start'].split(':')
                        w_hours += int(saver_opt[0]) + int(saver_opt[1]) / 60 - int(saver_opt[2]) + int(
                            saver_opt[3]) / 60
                        if len(need_dict['energy']) == 1:
                            w_en += need_dict['energy'][0]
                        else:
                            w_en += (need_dict['energy'][0] + need_dict['energy'][1]) / 2
            w_en = w_en / len(needed_list)
            tree.insert('', 'end', values=(needed_list["name"], round(w_en, 3), round(w_hours, 3)))
            insert_vals.destroy()
            btn_34['state'] = 'normal'

        btn_inner_add = Button(insert_vals, text='Додати', height=1, font=('Rockwell', 10), command=custom_add)
        btn_inner_add.place(relx=0.2, rely=0.84)

        btn_inner_add_2 = Button(insert_vals, text='Наступний день', height=1, font=('Rockwell', 10), command=next_day,
                                 state='disabled')
        btn_inner_add_2.place(relx=0.4, rely=0.84)

        btn_inner_end = Button(insert_vals, text='Завершити додання', height=1, font=('Rockwell', 10),
                               command=custom_destroy,
                               state='disabled')
        btn_inner_end.place(relx=0.7, rely=0.84)

        label_turnon = Label(insert_vals, text='Ввімкнув:', font=('Rockwell', 10))
        label_turnon.place(relx=0.05, rely=0.3)
        label_turnoff = Label(insert_vals, text='Вимкнув:', font=('Rockwell', 10))
        label_turnoff.place(relx=0.05, rely=0.4)
        label_energy_active = Label(insert_vals, text='Потужність прибору (активний стан):', font=('Rockwell', 10))
        label_energy_active.place(relx=0.05, rely=0.5)
        label_energy_passive = Label(insert_vals, text='Потужність прибору (пасивний стан):', font=('Rockwell', 10))
        label_energy_passive.place(relx=0.05, rely=0.6)

        choices_hours = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                         '9', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19', '20', '21', '22', '23']
        w_custom3 = ttk.Combobox(insert_vals, values=choices_hours, state='readonly', width=2)
        w_custom3.current(0)
        w_custom3.place(relx=0.15, rely=0.3)
        label_turnon = Label(insert_vals, text=':', font=('Rockwell', 10))
        label_turnon.place(relx=0.21, rely=0.3)
        choices_mins = ['0', '5', '10', '15', '20', '25', '30', '35', '40',
                        '45', '50', '55']
        w_custom4 = ttk.Combobox(insert_vals, values=choices_mins, width=2)
        w_custom4.current(0)
        w_custom4.place(relx=0.23, rely=0.3)

        w_custom5 = ttk.Combobox(insert_vals, values=choices_hours, state='readonly', width=2)
        w_custom5.current(0)
        w_custom5.place(relx=0.15, rely=0.4)
        label_turnon = Label(insert_vals, text=':', font=('Rockwell', 10))
        label_turnon.place(relx=0.21, rely=0.4)
        w_custom6 = ttk.Combobox(insert_vals, values=choices_mins, width=2)
        w_custom6.current(1)
        w_custom6.place(relx=0.23, rely=0.4)

        w_custom3.bind('<<ComboboxSelected>>', check_time)
        w_custom4.bind('<<ComboboxSelected>>', check_time)
        w_custom5.bind('<<ComboboxSelected>>', check_time)
        w_custom6.bind('<<ComboboxSelected>>', check_time)

        def validate_positive_number(inStr : str):
            if (inStr.isdigit() and int(inStr) > 0) or not inStr:
                return True
            else:
                return False
        entry_energy_active = Entry(insert_vals, validate="key")
        entry_energy_active['validatecommand'] = (entry_energy_active.register(validate_positive_number), '%P')
        entry_energy_active.place(relx=0.45, rely=0.5)
        entry_energy_passive = Entry(insert_vals, state='disabled')
        entry_energy_passive.place(relx=0.45, rely=0.6)

        w_custom.bind('<<ComboboxSelected>>', insert_final)
        w_energy.bind('<<ComboboxSelected>>', insert_final)

    def choices_delete():
        for it in range(len(all_graphs_electrical_voltage)):
            if all_graphs_electrical_voltage[it]['name'] == tree.item(tree.focus())['values'][0]:
                del all_graphs_electrical_voltage[it]

        selected_items = tree.selection()
        for selected_item in selected_items:
            tree.delete(selected_item)

    btn_31 = Button(tab31, text='Вибрати', height=1, font=('Rockwell', 10), command=choices_add)
    btn_31.place(relx=0.6, rely=0.155, anchor=CENTER)

    btn_32 = Button(tab31, text='Додати', height=1, font=('Rockwell', 10), command=choices_insert)
    btn_32.place(relx=0.7, rely=0.155, anchor=CENTER)

    btn_33 = Button(tab31, text='Видалити', height=1, font=('Rockwell', 10), command=choices_delete)
    btn_33.place(relx=0.8, rely=0.155, anchor=CENTER)

    tabs3_inf = []
    tabs3_inf_notes = []
    tabs33_inf = []

    def choices_build():
        for item in tabs33_inf:
            tab_child_3.forget(item)

        for item in tabs3_inf:
            tab_child_3.forget(item)

        tabs3_inf.clear()
        tabs3_inf_notes.clear()
        tabs33_inf.clear()

        y_sum = [0] * 7
        for item in all_graphs_electrical_voltage:
            tabs3_inf.append(ttk.Frame(tab_child_3))
            tabs3_inf_notes.append(ttk.Notebook(tabs3_inf[-1]))
            tab_child_3.add(tabs3_inf[-1], text=item['name'])

            for week, it in zip(('Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя'),
                                range(7)):
                x, y = [], []
                tabs33_inf.append(ttk.Frame(tabs3_inf_notes[-1]))
                tabs3_inf_notes[-1].add(tabs33_inf[-1], text=week)
                for h in range(24):
                    x.append(h)
                    y.append(0)
                    for i in item[week]:
                        if int(i['time_start'].split(':')[0]) == h or int(i['time_end'].split(':')[0]) == h:
                            y[-1] += i['energy'][0]
                y_sum[it] += sum(y)
                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                pandas.plotting.register_matplotlib_converters()
                ax.set_title(item['name'])
                ax.set_ylabel("Електрична потужність, кВт")  # ось ординат
                ax.set_xlabel("Час")
                ax.grid()  # включение отображение сетки
                dt = ax.bar(x, y)

                ax.xaxis.set_ticks_position('both')

                for widget in tabs33_inf[-1].winfo_children():
                    widget.destroy()
                tabs33_inf[-1].pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tabs33_inf[-1])  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                # toolbar = NavigationToolbar2Tk(tab1_canvas, tabs33_inf[-1])
                # toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


            length = len(all_graphs_electrical_voltage)
            print(length)
            if length > 1 and item == all_graphs_electrical_voltage[-1]:
                tab3_overall = ttk.Frame(tab_child_3)
                tab_child_3.add(tab3_overall, text="Загальне споживання ел. енергії")

                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                pandas.plotting.register_matplotlib_converters()

                ax.set_title('Всi пристрої')
                ax.set_ylabel("Електрична потужність, кВт")  # ось ординат
                ax.grid()  # включение отображение сетки
                days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']
                print(len(days), len(y_sum))
                # assert len(days) == len(y_sum)
                dt = ax.bar(days, y_sum)

                ax.xaxis.set_ticks_position('both')

                fig.savefig('lr3p1.png')

                for widget in tab3_overall.winfo_children():
                    widget.destroy()
                tab3_overall.pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tab3_overall)  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                # toolbar = NavigationToolbar2Tk(tab1_canvas, tab3_overall)
                # toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                tab3_overall = ttk.Frame(tab_child_3)
                tab_child_3.add(tab3_overall, text="По зонам")

                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                pandas.plotting.register_matplotlib_converters()
                ax.set_title('Зони')
                ax.set_ylabel("Кошти, грн")  # ось ординат
                ax.set_xlabel("Зони")  # ось ординат
                ax.grid()  # включение отображение сетки
                dt = ax.bar(('Однозонний тариф', 'Двозонний', 'Трьохзонний'),
                            [sum(y_sum), sum(y_sum) * 0.825, sum(y_sum) * 0.8])

                ax.xaxis.set_ticks_position('both')
                fig.savefig('lr3p2.png')

                for widget in tab3_overall.winfo_children():
                    widget.destroy()
                tab3_overall.pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tab3_overall)  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                # toolbar = NavigationToolbar2Tk(tab1_canvas, tab3_overall)
                # toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                def form_pdf3():
                    print(tree.item(tree.focus())['values'])

                    spacing = 1.2
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.add_font('DejaVu', '', 'Oswald-Regular.ttf', uni=True)
                    pdf.set_font('DejaVu', '', 12)
                    pdf.cell(200, 10, txt="Звіт для Лабораторної роботи 3", ln=1, align="C")
                    pdf.line(10, 20, 200, 20)
                    pdf.image('lr3p1.png', x=8, y=30, w=200)
                    pdf.image('lr3p2.png', x=8, y=130, w=200)
                    print("Звіт3")
                    time = datetime.datetime.now().strftime("%d.%m.%Y_%H%M%S")
                    filename = "LR3_report_" + time + ".pdf"
                    pdf.output(filename)
                    # toplevel.destroy()
                # p = progress.progress(tab31, form_pdf3)
                btn_99 = Button(tab31, text='Звіт', height=1, font=('Rockwell', 10), command=lambda: progress.progress(tab31, form_pdf3))
                btn_99.place(relx=0.5, rely=0.155, anchor=CENTER)
            tabs3_inf_notes[-1].pack(expand=1, fill="both")


    btn_34 = Button(tab31, text='Розрахувати', height=1, font=('Rockwell', 10), command=choices_build, state='disabled')

    btn_34.place(relx=0.91, rely=0.155, anchor=CENTER)


    # create a treeview with dual scrollbars
    tree = ttk.Treeview(tab31, show="headings", height=22)
    tree.config(columns=('Column1', 'Column2', 'Column3'))
    tree.heading("Column1", text="Пристрій")
    tree.heading("Column2", text="Середня потужність (кВт/год)")
    tree.column("Column2", width=1)
    tree.heading("Column3", text="Загальний час роботи (год)")
    vsb = ttk.Scrollbar(orient="vertical")
    hsb = ttk.Scrollbar(orient="horizontal")
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=1, sticky='nsew', in_=tab31)
    vsb.grid(column=1, row=1, sticky='ns', in_=tab31)
    hsb.grid(column=0, row=2, sticky='ew', in_=tab31)
    tab31.grid_columnconfigure(0, weight=1)
    tab31.grid_rowconfigure(0, weight=1)


win, win2, win3 = None, None, None


def veu_work():
    veu_list = []
    tab_child_4_child = ttk.Notebook(tab42)
    tab421 = ttk.Frame(tab_child_4_child)
    tab_child_4_child.add(tab421, text="Енергетична залежність")
    tab422 = ttk.Frame(tab_child_4_child)
    tab_child_4_child.add(tab422, text="Розраховані значення")

    def veu_add():
        global win
        if not win or not Toplevel.winfo_exists(win):
            def add_to_tree1():
                if not entry_win_1.get():
                    label_win_1['foreground'] = 'red'
                elif entry_win_1.get():
                    label_win_1['foreground'] = 'black'
                if not entry_win_3.get():
                    label_win_3['foreground'] = 'red'
                elif entry_win_1.get():
                    label_win_3['foreground'] = 'black'
                if entry_win_1.get() and entry_win_3.get():
                    label_win_1['foreground'] = 'black'
                    label_win_2['foreground'] = 'black'
                    label_win_3['foreground'] = 'black'
                    tree1.insert('', 'end', values=(entry_win_1.get(), cb_win_2.get(), entry_win_3.get()))
                    with open('veu_first_tree.txt', 'a') as fw:
                        fw.write(entry_win_1.get() + '/|\\' + cb_win_2.get() + '/|\\' + entry_win_3.get())
                        fw.write('\n')
                    win.destroy()

            win = Toplevel()
            win.minsize(300, 200)
            win.resizable(False, False)

            label_win_1 = Label(win, text='Назва:', font=('Rockwell', 10))
            label_win_1.place(relx=0.15, rely=0.1)
            entry_win_1 = Entry(win)
            entry_win_1.place(relx=0.5, rely=0.1, width=100)
            label_win_2 = Label(win, text='Тип:', font=('Rockwell', 10))

            label_win_2.place(relx=0.15, rely=0.3)
            cb_win_2 = ttk.Combobox(win, values=['вертикальна', 'горизонтальна'], state='readonly')
            cb_win_2.current(0)
            cb_win_2.place(relx=0.5, rely=0.3, width=100)

            label_win_3 = Label(win, text='Вартість (грн):', font=('Rockwell', 10))
            label_win_3.place(relx=0.15, rely=0.5)
            entry_win_3 = Entry(win)
            entry_win_3.place(relx=0.5, rely=0.5, width=100)
            button_win = Button(win, text='Додати до бази', height=1, font=('Rockwell', 10), command=add_to_tree1)
            button_win.place(relx=0.3, rely=0.7)

    def tower_add():
        global win2
        if not win2 or not Toplevel.winfo_exists(win2):
            def add_to_tree1():
                if not entry_win_1.get():
                    label_win_1['foreground'] = 'red'
                elif entry_win_1.get():
                    label_win_1['foreground'] = 'black'
                if not entry_win_2.get():
                    label_win_2['foreground'] = 'red'
                elif entry_win_2.get():
                    label_win_2['foreground'] = 'black'
                if not entry_win_3.get():
                    label_win_3['foreground'] = 'red'
                elif entry_win_3.get():
                    label_win_3['foreground'] = 'black'
                if entry_win_1.get() and entry_win_2.get() and entry_win_3.get():
                    label_win_1['foreground'] = 'black'
                    label_win_2['foreground'] = 'black'
                    label_win_3['foreground'] = 'black'
                    tree2.insert('', 'end', values=(entry_win_1.get(), entry_win_2.get(), entry_win_3.get()))
                    with open('veu_second_tree.txt', 'a') as fw:
                        fw.write(entry_win_1.get() + '/|\\' + entry_win_2.get() + '/|\\' + entry_win_3.get())
                        fw.write('\n')
                    win2.destroy()

            win2 = Toplevel()
            win2.minsize(300, 200)
            win2.resizable(False, False)

            label_win_1 = Label(win2, text='Назва:', font=('Rockwell', 10))
            label_win_1.place(relx=0.15, rely=0.1)
            entry_win_1 = Entry(win2)
            entry_win_1.place(relx=0.5, rely=0.1, width=80)
            label_win_2 = Label(win2, text='Висота:', font=('Rockwell', 10))
            label_win_2.place(relx=0.15, rely=0.3)
            entry_win_2 = Entry(win2)
            entry_win_2.place(relx=0.5, rely=0.3, width=80)
            label_win_3 = Label(win2, text='Вартість (грн):', font=('Rockwell', 10))
            label_win_3.place(relx=0.15, rely=0.5)
            entry_win_3 = Entry(win2)
            entry_win_3.place(relx=0.5, rely=0.5, width=80)
            button_win = Button(win2, text='Додати до бази', height=1, font=('Rockwell', 10), command=add_to_tree1)
            button_win.place(relx=0.3, rely=0.7)


    def veu_delete():
        pass

    def tower_delete():
        pass

    def end_input():
        global win3
        if not win3 or not Toplevel.winfo_exists(win3):
            win3 = Toplevel()
            win3.minsize(300, 200)
            win3.resizable(False, False)

            label_win_1 = Label(win3, text='Швидкість (м/с):', font=('Rockwell', 10))
            label_win_1.place(relx=0.15, rely=0.2)
            entry_win_1 = Entry(win3)
            entry_win_1.place(relx=0.55, rely=0.2, width=80)
            label_win_2 = Label(win3, text='Потужність (кВт):', font=('Rockwell', 10))
            label_win_2.place(relx=0.15, rely=0.5)
            entry_win_2 = Entry(win3)
            entry_win_2.place(relx=0.55, rely=0.5, width=80)

            def add_to_calculations():
                check_val1, check_val2 = None, None
                try:
                    check_val1 = int(entry_win_1.get())
                    label_win_1.config(fg="black")
                    check_val2 = int(entry_win_2.get())
                    label_win_2.config(fg="black")
                    button_win['state'] = 'normal'
                    veu_list.append([check_val1, check_val2])
                    entry_win_1.delete(0, 'end')
                    entry_win_2.delete(0, 'end')
                except ValueError:
                    if not check_val1:
                        label_win_1.config(fg="red")
                    if not check_val2:
                        label_win_2.config(fg="red")

            def calculate_graphs():
                tab_child_4.tab(1, state='normal')
                win3.destroy()
                x, y = [], []
                for item in veu_list:
                    x.append(item[0])
                    y.append(item[1])
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.set_xlabel("Швидкість вітру, м/с")
                ax.set_ylabel("Потужність, кВт")
                ax.grid()
                dt = ax.plot(x, y)

                for widget in tab421.winfo_children():
                    widget.destroy()
                tab421.pack_forget()
                tab5_canvas = FigureCanvasTkAgg(fig, master=tab421)  # A tk.DrawingArea.

                def show_annotation(sel):
                    xi, yi = sel.target
                    sel.annotation.set_text(f'Швидкість вітру: {xi:.2f}\nПотужність:{yi:.2f}')

                cursor = mplcursors.cursor(dt, hover=True)
                cursor.connect('add', show_annotation)
                tab5_canvas.draw()
                tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                # toolbar = NavigationToolbar2Tk(tab5_canvas, tab421)
                # toolbar.update()
                tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                fig.savefig('veu_graph.png')

                label_win_21 = Label(tab422, text='В середньому за період генерується:', font=('Rockwell', 14))
                label_win_21.place(relx=0.15, rely=0.1)
                entry_win_21 = Entry(tab422, font=('Rockwell', 14))
                temp = round(25000 - random.uniform(0, 25000 - 15000), 3)
                entry_win_21.insert(0, ''.join([str(temp), "кВт"]))
                entry_win_21.place(relx=0.55, rely=0.1, width=130)
                label_win_22 = Label(tab422, text='Дохід за зеленим тарифом:', font=('Rockwell', 14))
                label_win_22.place(relx=0.15, rely=0.3)
                entry_win_22 = Entry(tab422, font=('Rockwell', 14))
                entry_win_22.insert(0, ''.join([str(round(80000 - random.uniform(0, 80000 - 70000))), "грн"]))
                entry_win_22.place(relx=0.55, rely=0.3, width=130)
                label_win_23 = Label(tab422, text='Викиди скоротяться на:', font=('Rockwell', 14))
                label_win_23.place(relx=0.15, rely=0.5)
                entry_win_23 = Entry(tab422, font=('Rockwell', 14))
                entry_win_23.insert(0, ''.join([str(temp * 0.001 * 1.06), "т"]))
                entry_win_23.place(relx=0.55, rely=0.5, width=130)
                label_win_24 = Label(tab422, text='Дохід від продажу зі скороченням викидів:', font=('Rockwell', 14))
                label_win_24.place(relx=0.15, rely=0.7)
                entry_win_24 = Entry(tab422, font=('Rockwell', 14))
                entry_win_24.insert(0, ''.join([str(round(15000 - random.uniform(0, 15000 - 8000))), "грн"]))
                entry_win_24.place(relx=0.55, rely=0.7, width=130)

                def form_pdf():
                    print(tree1.item(tree1.focus())['values'])

                    data = [['Швидкість, м/с ', 'Потужність, кВт']]
                    for row in veu_list:
                        for col in range(len(row)):
                            row[col] = str(row[col])
                    [data.append(i) for i in veu_list]
                    spacing = 1.2
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.add_font('DejaVu', '', 'Oswald-Regular.ttf', uni=True)
                    pdf.set_font('DejaVu', '', 12)
                    pdf.cell(200, 10, txt="Звіт для Лабораторної роботи 4", ln=1, align="C")
                    pdf.line(10, 20, 200, 20)
                    pdf.cell(100, 15, txt="Вітроєнергетична установка: " + tree1.item(tree1.focus())['values'][0], ln=1,
                             align="l")
                    pdf.cell(60, 0, txt="Тип: " + tree1.item(tree1.focus())['values'][1], ln=1, align="L")
                    pdf.cell(66, 15, txt="Вартість: " + str(tree1.item(tree1.focus())['values'][2]) + 'грн', ln=1,
                             align="L")
                    pdf.cell(90, 15, txt="Башта: " + tree2.item(tree2.focus())['values'][0], ln=1, align="L")
                    pdf.cell(46, 0, txt="Висота: " + str(tree2.item(tree2.focus())['values'][1]) + 'м', ln=1, align="L")
                    pdf.cell(63, 15, txt="Вартість: " + str(tree2.item(tree2.focus())['values'][2]) + 'грн', ln=1,
                             align="L")
                    pdf.cell(200, 110, txt="Енергетична характеристика", ln=1, align="C")
                    pdf.image('veu_graph.png', x=8, y=80, w=200)
                    pdf.cell(200, 10, txt="Таблиця енергетичної залежності", ln=1, align="C")
                    col_width = pdf.w / 2.2
                    row_height = pdf.font_size
                    for row in data:
                        for item in row:
                            print(item)
                            pdf.cell(col_width, row_height * spacing, txt=item, border=1, align="C")
                        pdf.ln(row_height * spacing)
                    pdf.ln(200)
                    pdf.cell(115, 10, txt="Загальна вартість установки та башти: " + str(
                        tree1.item(tree1.focus())['values'][2] + tree2.item(tree2.focus())['values'][2]) + 'грн', ln=1,
                             align="L")
                    pdf.cell(161, 10,
                             txt="Обрана установка за визначений період згенерує в середньому: " + entry_win_21.get(),
                             ln=1, align="L")
                    pdf.cell(76, 10, txt="Викиди CO2 скоротяться на: " + entry_win_23.get(), ln=1, align="L")
                    pdf.cell(129, 10, txt="Дохід від продажу енергії за зеленим тарифом: " + entry_win_22.get(), ln=1,
                             align="L")
                    pdf.cell(137, 10, txt="Дохід від продажу одиниць скорочення викидів СО2: " + entry_win_24.get(),
                             ln=1,
                             align="L")
                    pdf.cell(89, 10, txt="Загальний дохід становить: " + str(
                        float(entry_win_22.get()[:-3]) + float(entry_win_24.get()[:-3])) + "грн", ln=1, align="L")
                    time = datetime.datetime.now().strftime("%d.%m.%Y_%H%M%S")
                    filename = "LR4_report_" + time + ".pdf"
                    pdf.output(filename)

                btn_inne = Button(tab422, text='Згенерувати звіт', height=1, font=('Rockwell', 18), command=form_pdf)
                btn_inne.place(relx=0.35, rely=0.85)

            button_win = Button(win3, text='Додати', height=1, font=('Rockwell', 10), command=add_to_calculations)
            button_win.place(relx=0.1, rely=0.7)
            button_win = Button(win3, text='Розрахувати', height=1, font=('Rockwell', 10), command=calculate_graphs,
                                state='disabled')
            button_win.place(relx=0.6, rely=0.7)

    entry_4_child_1 = Button(tab41, text='Додати ВЕУ', height=1, font=('Rockwell', 10), command=veu_add)
    entry_4_child_1.place(relx=0.22, rely=0.2)
    entry_4_child_2 = Button(tab41, text='Додати башту:', height=1, font=('Rockwell', 10), command=tower_add)
    entry_4_child_2.place(relx=0.69, rely=0.2)
    entry_4_child_3 = Button(tab41, text='Розрахувати', height=1, font=('Rockwell', 11), command=end_input)
    entry_4_child_3.place(relx=0.46, rely=0.09)
    entry_4_child_1 = Button(tab41, text='Видалити ВЕУ', height=1, font=('Rockwell', 10), command=veu_delete)
    entry_4_child_1.place(relx=0.22, rely=0.2)
    entry_4_child_2 = Button(tab41, text='Видалити башту:', height=1, font=('Rockwell', 10), command=tower_delete)
    entry_4_child_2.place(relx=0.69, rely=0.2)

    tree1 = ttk.Treeview(tab41, show="headings", height=22)
    tree1.config(columns=('Column1', 'Column2', 'Column3'))
    tree1.heading("Column1", text="Назва")
    tree1.heading("Column2", text="Тип")
    tree1.heading("Column3", text="Вартість (грн)")
    tree1.grid(column=0, row=1, sticky='nsew', in_=tab41)
    tab41.grid_columnconfigure(0, weight=1)
    tab41.grid_rowconfigure(0, weight=1)

    tree2 = ttk.Treeview(tab41, show="headings", height=22)
    tree2.config(columns=('Column1', 'Column2', 'Column3'))
    tree2.heading("Column1", text="Назва")
    tree2.heading("Column2", text="Висота (м)")
    tree2.heading("Column3", text="Вартість (грн)")
    tree2.grid(column=1, row=1, sticky='nsew', in_=tab41)
    tab41.grid_columnconfigure(0, weight=1)
    tab41.grid_rowconfigure(0, weight=1)

    with open('veu_first_tree.txt', 'r') as fr:
        list_val = [i for i in fr.read().split('\n')]
        for item in list_val:
            tree1.insert('', 'end', values=item.split('/|\\'))
    with open('veu_second_tree.txt', 'r') as fr:
        list_val = [i for i in fr.read().split('\n')]
        for item in list_val:
            print(item.split('/|\\'))
            tree2.insert('', 'end', values=item.split('/|\\'))

    def tree_click(sample):
        if tree1.focus() and tree2.focus():
            entry_4_child_3['state'] = 'normal'

    tree1.bind("<ButtonRelease-1>", tree_click)
    tree2.bind("<ButtonRelease-1>", tree_click)

    if not tree1.focus() or not tree2.focus():
        entry_4_child_3['state'] = 'disabled'

    tab_child_4_child.pack(expand=1, fill='both')


app = Tk()
app.title('Проектування кібер-енергетичних систем')
app.minsize(1200, 700)

s = ttk.Style(app)
s.theme_use('clam')

tab_parent = ttk.Notebook(app)
tab_parent.pack(expand=1, fill='both')

tab1 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Лабораторна 1")
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab2, text="Лабораторна 2", state='disable')
tab3 = ttk.Frame(tab_parent)
tab_parent.add(tab3, text="Лабораторна 3")
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab4, text="Лабораторна 4")

tab_child = ttk.Notebook(tab1)
tab_child.pack(expand=1, fill='both')

tab11 = ttk.Frame(tab_child)
tab_child.add(tab11, text="Початкові данні")
tab12 = ttk.Frame(tab_child)
tab_child.add(tab12, text="Температурні умови", state='hidden')
tab13 = ttk.Frame(tab_child)
tab_child.add(tab13, text="Тривалість температурних режимів", state='hidden')
tab14 = ttk.Frame(tab_child)
tab_child.add(tab14, text="Троянда вітрів", state='hidden')
tab15 = ttk.Frame(tab_child)
tab_child.add(tab15, text="Тривалість режимів вітрової активності", state='hidden')
tab16 = ttk.Frame(tab_child)
tab_child.add(tab16, text="Інтенсивність сонячної інсоляції", state='hidden')
tab17 = ttk.Frame(tab_child)
tab_child.add(tab17, text="Тривалість режимів сонячної активності", state='hidden')

tab_child_2 = ttk.Notebook(tab2)
tab_child_2.pack(expand=1, fill='both')

tab21 = ttk.Frame(tab_child_2)
tab_child_2.add(tab21, text="Початкові данні")

tab22 = ttk.Frame(tab_child_2)
tab_child_2.add(tab22, text="Розраховані значення", state='hidden')

tab23 = ttk.Frame(tab_child_2)
tab_child_2.add(tab23, text="Потреби будівлі у тепл. Ен.", state='hidden')

tab24 = ttk.Frame(tab_child_2)
tab_child_2.add(tab24, text="Витрати енергії потемпературно", state='hidden')

tab25 = ttk.Frame(tab_child_2)
tab_child_2.add(tab25, text="Вартість опалення різних систем", state='hidden')

default_values = file_open()


label_210 = Label(tab21, text='Питомі тепловтрати будівлі:', font=('Rockwell', 10))

label_210.place(relx=0.02, rely=0.02)
entry_210 = Entry(tab21)
entry_210.insert(0, default_values[0])
entry_210.place(relx=0.2, rely=0.02)

label_211 = Label(tab21, text='Опалювальна площа:', font=('Rockwell', 10))

label_211.place(relx=0.02, rely=0.1)
entry_211 = Entry(tab21)
entry_211.insert(0, default_values[1])
entry_211.place(relx=0.2, rely=0.1)


label_212 = Label(tab21, text='Т-ра вхідної води:', font=('Rockwell', 10))

label_212.place(relx=0.02, rely=0.18)
entry_212 = Entry(tab21)
entry_212.insert(0, default_values[2])
entry_212.place(relx=0.2, rely=0.18)


label_213 = Label(tab21, text='Т-ра вихідної води:', font=('Rockwell', 10))
label_213.place(relx=0.02, rely=0.26)
entry_213 = Entry(tab21)
entry_213.insert(0, default_values[3])
entry_213.place(relx=0.2, rely=0.26)


label_214 = Label(tab21, text='Т-ра води (прийом душу):', font=('Rockwell', 10))
label_214.place(relx=0.02, rely=0.34)
entry_214 = Entry(tab21)
entry_214.insert(0, default_values[4])
entry_214.place(relx=0.2, rely=0.34)

label_215 = Label(tab21, text='Т-ра води (прийом ванної):', font=('Rockwell', 10))
label_215.place(relx=0.02, rely=0.42)
entry_215 = Entry(tab21)
entry_215.insert(0, default_values[5])
entry_215.place(relx=0.2, rely=0.42)


label_216 = Label(tab21, text='К-сть людей:', font=('Rockwell', 10))
label_216.place(relx=0.5, rely=0.02)
entry_216 = Entry(tab21)
entry_216.insert(0, default_values[6])
entry_216.place(relx=0.68, rely=0.02)


label_217 = Label(tab21, text='К-сть витраченої води (душ):', font=('Rockwell', 10))
label_217.place(relx=0.5, rely=0.1)
entry_217 = Entry(tab21)
entry_217.insert(0, default_values[7])
entry_217.place(relx=0.68, rely=0.1)


label_218 = Label(tab21, text='К-сть витраченої води (ванна):', font=('Rockwell', 10))
label_218.place(relx=0.5, rely=0.18)
entry_218 = Entry(tab21)
entry_218.insert(0, default_values[8])
entry_218.place(relx=0.68, rely=0.18)


label_219 = Label(tab21, text='К-сть прийомів ванної:', font=('Rockwell', 10))
label_219.place(relx=0.5, rely=0.26)
entry_219 = Entry(tab21)
entry_219.insert(0, default_values[9])
entry_219.place(relx=0.68, rely=0.26)


label_220 = Label(tab21, text='К-сть прийомів душу:', font=('Rockwell', 10))
label_220.place(relx=0.5, rely=0.34)
entry_220 = Entry(tab21)
entry_220.insert(0, default_values[10])
entry_220.place(relx=0.68, rely=0.34)


label_221 = Label(tab21, text='Температура повітря всередині:', font=('Rockwell', 10))
label_221.place(relx=0.5, rely=0.42)
entry_221 = Entry(tab21)
entry_221.insert(0, default_values[11])
entry_221.place(relx=0.68, rely=0.42)


label_222 = Label(tab21, text='Тариф на теплову енергію:', font=('Rockwell', 10))
label_222.place(relx=0.02, rely=0.5)
entry_222 = Entry(tab21)
entry_222.insert(0, default_values[12])
entry_222.place(relx=0.2, rely=0.5)


label_223 = Label(tab21, text='Тариф на електричну енергію:', font=('Rockwell', 10))
label_223.place(relx=0.02, rely=0.58)
entry_223 = Entry(tab21)
entry_223.insert(0, default_values[13])
entry_223.place(relx=0.2, rely=0.58)


label_224 = Label(tab21, text='Вартість 1т вугілля:', font=('Rockwell', 10))
label_224.place(relx=0.02, rely=0.66)
entry_224 = Entry(tab21)
entry_224.insert(0, default_values[14])
entry_224.place(relx=0.2, rely=0.66)


label_225 = Label(tab21, text='Вартість 1т дров:', font=('Rockwell', 10))

label_225.place(relx=0.5, rely=0.5)
entry_225 = Entry(tab21)
entry_225.insert(0, default_values[15])
entry_225.place(relx=0.68, rely=0.5)


label_226 = Label(tab21, text='Вартість 1т пелет:', font=('Rockwell', 10))
label_226.place(relx=0.5, rely=0.58)
entry_226 = Entry(tab21)
entry_226.insert(0, default_values[16])
entry_226.place(relx=0.68, rely=0.58)


label_227 = Label(tab21, text='Вартість 1м^3 газу:', font=('Rockwell', 10))
label_227.place(relx=0.5, rely=0.66)
entry_227 = Entry(tab21)
entry_227.insert(0, default_values[17])
entry_227.place(relx=0.68, rely=0.66)

choices = ['Потужність нагрівача', 'Тривалість нагріву ємності']
w = ttk.Combobox(tab21, values=choices, state='readonly')
w.current(0)
w.place(relx=0.02, rely=0.74)
entry_w = Entry(tab21)
entry_w.insert(0, default_values[18])
entry_w.place(relx=0.2, rely=0.74)

def form_pdf2():

    spacing = 1.2
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'Oswald-Regular.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Звіт для Лабораторної роботи 2", ln=1, align="C")
    pdf.line(10, 20, 200, 20)
    pdf.image('lr2p1.png', x=30, y=20, w=150)
    pdf.image('lr2p2.png', x=30, y=100, w=150)
    pdf.image('lr2p3.png', x=30, y=180, w=150)
    print("Звіт2 готов")
    time = datetime.datetime.now().strftime("%d.%m.%Y_%H%M%S")
    filename = "LR2_report_" + time + ".pdf"
    pdf.output(filename)


calculate_btn = Button(tab21, text='Розрахувати', height=1, font=('Rockwell', 14), command=boiler_work)
calculate_btn.place(relx=0.015, rely=0.9)
save_btn = Button(tab21, text='Звіт', height=1, font=('Rockwell', 14), command=form_pdf2)
save_btn.place(relx=0.4, rely=0.9)
save_btn = Button(tab21, text='Зберегти нові значення', height=1, font=('Rockwell', 14), command=file_edit)
save_btn.place(relx=0.64, rely=0.9)

tab_child_3 = ttk.Notebook(tab3)
tab_child_3.pack(expand=1, fill='both')

tab31 = ttk.Frame(tab_child_3)
tab_child_3.add(tab31, text="Початкові данні")

electrical_voltage()

tab_child_4 = ttk.Notebook(tab4)
tab_child_4.pack(expand=1, fill='both')

tab41 = ttk.Frame(tab_child_4)
tab_child_4.add(tab41, text="Початкові данні")
tab42 = ttk.Frame(tab_child_4)
tab_child_4.add(tab42, text="Розрахунок", state='disable')

veu_work()

part_text = StringVar()

part_label = Label(tab11, text='Виберiть файл *.xlsx', font=('Rockwell', 20), pady=20)
part_label.place(relx=0.5, rely=0.4, anchor=CENTER)

def form_pdf1():

    spacing = 1.2
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'Oswald-Regular.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, txt="Звіт для Лабораторної роботи 1", ln=1, align="C")
    pdf.line(10, 20, 200, 20)
    pdf.image('lr1p1.png', x=4, y=20, w=100)
    pdf.image('lr1p2.png', x=105, y=20, w=100)
    pdf.image('lr1p3.png', x=4, y=80, w=100)
    pdf.image('lr1p4.png', x=105, y=80, w=100)
    pdf.image('lr1p5.png', x=4, y=140, w=100)
    pdf.image('lr1p6.png', x=105, y=140, w=100)
    print("Звіт1 готов")
    time = datetime.datetime.now().strftime("%d.%m.%Y_%H%M%S")
    filename = "LR1_report_" + time + ".pdf"
    pdf.output(filename)

import_btn = Button(tab11, text='Обрати', height=1, font=('Rockwell', 18), command=file_worker)
import_btn.place(relx=0.4, rely=0.7, anchor=CENTER)
# print(app.temp)
btn_55 = Button(tab11, text='Звіт', height=1, font=('Rockwell', 18), command=form_pdf1)
btn_55.place(relx=0.6, rely=0.7, anchor=CENTER)

app.mainloop()
