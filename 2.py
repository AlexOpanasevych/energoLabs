import math
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
import pandas
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from windrose import WindroseAxes
from numpy import arange
import mplcursors

mplcursors.cursor(hover=True)
import webbrowser

average_temperature = 0
dic_1_4 = {}


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
    return fig, dt


def print_graph_fifth(workflow_data):
    data = pandas.read_excel("NY_1.xlsx")
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
    return fig, dt


def print_graph_sixth(workflow_data):
    data = pandas.read_excel("NY_1.xlsx")
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
    data = pandas.read_excel(file_path)
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
        part_label['text'] = 'Файл прочитаний, дивiться нові вкладки'
        maine_frame = pandas_transforming(file_path)
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
    tab5_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    boiler_2_5(x, y)


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


def boiler_work():
    content = [entry_210.get(), entry_211.get(), entry_212.get(), entry_213.get(), entry_214.get(), entry_215.get(),
               entry_216.get(), entry_217.get(), entry_218.get(), entry_219.get(), entry_220.get(), entry_221.get(),
               entry_222.get(), entry_223.get(), entry_224.get(), entry_225.get(), entry_226.get(), entry_227.get()]

    q_dush = float(entry_220.get()) * float(entry_217.get())
    q_vann = float(entry_219.get()) * float(entry_218.get())
    q_dush_t = q_dush * (float(entry_214.get()) - float(entry_212.get())) / (
                float(entry_213.get()) - float(entry_212.get()))
    q_vann_t = q_vann * (float(entry_215.get()) - float(entry_212.get())) / (
                float(entry_213.get()) - float(entry_212.get()))
    q_overall = (q_dush_t - q_vann_t) / 998.23

    w_t = 1.163 * q_overall * (float(entry_213.get()) - float(entry_212.get()))
    r_gvp, t_nagr = 0, 0
    if w.get() == 'Потужність нагрівача':
        r_gvp = float(entry_w.get())
        t_nagr = w_t / r_gvp
    elif w.get() == 'Тривалість нагріву ємності':
        t_nagr = float(entry_w.get())
        r_gvp = w_t / t_nagr
    tab_child_2.tab(1, state='normal')
    label_2_1 = Label(tab22, text='Обсяги споживання води на прийом душу:', font=('bold', 10))
    label_2_1.place(relx=0.02, rely=0.02)
    entry_2_1 = Entry(tab22)
    entry_2_1.insert(0, q_dush)
    entry_2_1.configure(state='readonly')
    entry_2_1.place(relx=0.2, rely=0.02)

    label_2_2 = Label(tab22, text='Обсяги споживання води на прийом ван:', font=('bold', 10))
    label_2_2.place(relx=0.02, rely=0.1)
    entry_2_2 = Entry(tab22)
    entry_2_2.insert(0, str(q_vann))
    entry_2_2.configure(state='readonly')
    entry_2_2.place(relx=0.2, rely=0.1)

    label_2_3 = Label(tab22, text='Корегування витрати гарячої води для душа:', font=('bold', 10))
    label_2_3.place(relx=0.02, rely=0.18)
    entry_2_3 = Entry(tab22)
    entry_2_3.insert(0, str(round(q_dush_t)) + " л/добу")
    entry_2_3.configure(state='readonly')
    entry_2_3.place(relx=0.2, rely=0.18)

    label_2_4 = Label(tab22, text='Корегування витрати гарячої води для вани:', font=('bold', 10))
    label_2_4.place(relx=0.02, rely=0.26)
    entry_2_4 = Entry(tab22)
    entry_2_4.insert(0, str(round(q_vann_t)) + " л/добу")
    entry_2_4.configure(state='readonly')
    entry_2_4.place(relx=0.2, rely=0.26)

    label_2_5 = Label(tab22, text='Корегування витрати гарячої води всього:', font=('bold', 10))
    label_2_5.place(relx=0.02, rely=0.34)
    entry_2_5 = Entry(tab22)
    entry_2_5.insert(0, str(round(q_overall, 3)) + " м^3/добу")
    entry_2_5.configure(state='readonly')
    entry_2_5.place(relx=0.2, rely=0.34)

    label_2_6 = Label(tab22, text='Енергія необхідна для нагріву води:', font=('bold', 10))
    label_2_6.place(relx=0.02, rely=0.42)
    entry_2_6 = Entry(tab22)
    entry_2_6.insert(0, str(round(w_t, 3)) + " кВт*год")
    entry_2_6.configure(state='readonly')
    entry_2_6.place(relx=0.2, rely=0.42)

    label_2_7 = Label(tab22, text='Необхідна теплова потужність нагрівача:', font=('bold', 10))
    label_2_7.place(relx=0.02, rely=0.5)
    entry_2_7 = Entry(tab22)
    entry_2_7.insert(0, str(round(r_gvp, 3)) + " кВт")
    entry_2_7.configure(state='readonly')
    entry_2_7.place(relx=0.2, rely=0.5)

    label_2_8 = Label(tab22, text='Час нагрівання бака:', font=('bold', 10))
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
    # web_btn = Button(tab22, text='Знайти потрібний котел', height=1, font=('bold', 18), command=OpenUrl)
    # web_btn.place(relx=0.15, rely=0.8, anchor=CENTER)

    boiler_warmity()


app = Tk()
app.title('Проектування кібер-енергетичних систем')
app.geometry('700x500+400+100')
app.resizable(True, True)

tab_parent = ttk.Notebook(app)
tab_parent.pack(expand=1, fill='both')

tab1 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Лабораторна 1")
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab2, text="Лабораторна 2", state='disable')

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

label_210 = Label(tab21, text='Питомі тепловтрати будівлі:', font=('bold', 10))
label_210.place(relx=0.02, rely=0.02)
entry_210 = Entry(tab21)
entry_210.insert(0, default_values[0])
entry_210.place(relx=0.2, rely=0.02)

label_211 = Label(tab21, text='Опалювальна площа:', font=('bold', 10))
label_211.place(relx=0.02, rely=0.1)
entry_211 = Entry(tab21)
entry_211.insert(0, default_values[1])
entry_211.place(relx=0.2, rely=0.1)

label_212 = Label(tab21, text='Т-ра вхідної води:', font=('bold', 10))
label_212.place(relx=0.02, rely=0.18)
entry_212 = Entry(tab21)
entry_212.insert(0, default_values[2])
entry_212.place(relx=0.2, rely=0.18)

label_213 = Label(tab21, text='Т-ра вихідної води:', font=('bold', 10))
label_213.place(relx=0.02, rely=0.26)
entry_213 = Entry(tab21)
entry_213.insert(0, default_values[3])
entry_213.place(relx=0.2, rely=0.26)

label_214 = Label(tab21, text='Т-ра води (прийом душу):', font=('bold', 10))
label_214.place(relx=0.02, rely=0.34)
entry_214 = Entry(tab21)
entry_214.insert(0, default_values[4])
entry_214.place(relx=0.2, rely=0.34)

label_215 = Label(tab21, text='Т-ра води (прийом ванної):', font=('bold', 10))
label_215.place(relx=0.02, rely=0.42)
entry_215 = Entry(tab21)
entry_215.insert(0, default_values[5])
entry_215.place(relx=0.2, rely=0.42)

label_216 = Label(tab21, text='К-сть людей:', font=('bold', 10))
label_216.place(relx=0.5, rely=0.02)
entry_216 = Entry(tab21)
entry_216.insert(0, default_values[6])
entry_216.place(relx=0.68, rely=0.02)

label_217 = Label(tab21, text='К-сть витраченої води (душ):', font=('bold', 10))
label_217.place(relx=0.5, rely=0.1)
entry_217 = Entry(tab21)
entry_217.insert(0, default_values[7])
entry_217.place(relx=0.68, rely=0.1)

label_218 = Label(tab21, text='К-сть витраченої води (ванна):', font=('bold', 10))
label_218.place(relx=0.5, rely=0.18)
entry_218 = Entry(tab21)
entry_218.insert(0, default_values[8])
entry_218.place(relx=0.68, rely=0.18)

label_219 = Label(tab21, text='К-сть прийомів ванної:', font=('bold', 10))
label_219.place(relx=0.5, rely=0.26)
entry_219 = Entry(tab21)
entry_219.insert(0, default_values[9])
entry_219.place(relx=0.68, rely=0.26)

label_220 = Label(tab21, text='К-сть прийомів душу:', font=('bold', 10))
label_220.place(relx=0.5, rely=0.34)
entry_220 = Entry(tab21)
entry_220.insert(0, default_values[10])
entry_220.place(relx=0.68, rely=0.34)

label_221 = Label(tab21, text='Температура повітря всередині:', font=('bold', 10))
label_221.place(relx=0.5, rely=0.42)
entry_221 = Entry(tab21)
entry_221.insert(0, default_values[11])
entry_221.place(relx=0.68, rely=0.42)

label_222 = Label(tab21, text='Тариф на теплову енергію:', font=('bold', 10))
label_222.place(relx=0.02, rely=0.5)
entry_222 = Entry(tab21)
entry_222.insert(0, default_values[12])
entry_222.place(relx=0.2, rely=0.5)

label_223 = Label(tab21, text='Тариф на електричну енергію:', font=('bold', 10))
label_223.place(relx=0.02, rely=0.58)
entry_223 = Entry(tab21)
entry_223.insert(0, default_values[13])
entry_223.place(relx=0.2, rely=0.58)

label_224 = Label(tab21, text='Вартість 1т вугілля:', font=('bold', 10))
label_224.place(relx=0.02, rely=0.66)
entry_224 = Entry(tab21)
entry_224.insert(0, default_values[14])
entry_224.place(relx=0.2, rely=0.66)

label_225 = Label(tab21, text='Вартість 1т дров:', font=('bold', 10))
label_225.place(relx=0.5, rely=0.5)
entry_225 = Entry(tab21)
entry_225.insert(0, default_values[15])
entry_225.place(relx=0.68, rely=0.5)

label_226 = Label(tab21, text='Вартість 1т пелет:', font=('bold', 10))
label_226.place(relx=0.5, rely=0.58)
entry_226 = Entry(tab21)
entry_226.insert(0, default_values[16])
entry_226.place(relx=0.68, rely=0.58)

label_227 = Label(tab21, text='Вартість 1м^3 газу:', font=('bold', 10))
label_227.place(relx=0.5, rely=0.66)
entry_227 = Entry(tab21)
entry_227.insert(0, default_values[17])
entry_227.place(relx=0.68, rely=0.66)

choices = ['Потужність нагрівача']
w = ttk.Combobox(tab21, values=choices, state='readonly')
w.current(0)
w.place(relx=0.02, rely=0.74)
entry_w = Entry(tab21)
entry_w.insert(0, default_values[18])
entry_w.place(relx=0.2, rely=0.74)

calculate_btn = Button(tab21, text='Розрахувати', height=1, font=('normal', 16), command=boiler_work)
calculate_btn.place(relx=0.02, rely=0.9)
save_btn = Button(tab21, text='Зберегти нові значення', height=1, font=('normal', 16), command=file_edit)
save_btn.place(relx=0.64, rely=0.9)

part_text = StringVar()
part_label = Label(tab11, text='Оберiть лист таблиці Excel,\n з розширення xlsx', font=('bold', 20), pady=20)
part_label.place(relx=0.5, rely=0.4, anchor=CENTER)

import_btn = Button(tab11, text='Обрати', height=1, font=('bold', 18), command=file_worker)
import_btn.place(relx=0.5, rely=0.7, anchor=CENTER)

app.mainloop()
