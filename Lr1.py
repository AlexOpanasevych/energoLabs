from tkinter import *
import tkinter.filedialog
from tkinter import ttk
import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from windrose import WindroseAxes
from numpy import arange
import mplcursors
mplcursors.cursor(hover=True)


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
    bars_percentage = [0]*(len(bars)-1)
    for i in range(len(ws)):
        for j in range(len(bars)-1, 0, -1):
            if bars[j] > ws[i] > bars[j - 1]:
                bars_percentage[j-1] += 1
                continue
    for i, j in zip(bars_percentage, range(len(bars_percentage))):
        if j == 0:
            ax2.bar(arange(1), bars_percentage[j], 0.1, color=viridis(j/4))
        else:
            ax2.bar(arange(1), bars_percentage[j], 0.1, bottom=sum(bars_percentage[0:j]), color=viridis(j/4))
    ax2.set_xticks([])
    ax2.set_xticks([], minor=True)
    ax2.set_title('Wind speed\n(%, m/s)')
    ax2.annotate('штиль - ' + str(round(.01*bars_percentage[0], 3)) + '%', xy=(0, 0), xytext=(0, -20), ha='left', va='bottom',
                 xycoords='axes fraction', textcoords='offset points')
    ax2.annotate('змiннi - ' + str(round(.01*bars_percentage[1], 3)) + '%', xy=(0, 0), xytext=(0, -40), ha='left', va='bottom',
                 xycoords='axes fraction', textcoords='offset points')
    ax2.axis('off')

    plt.yticks(arange(0, 61, 10))

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
                            workflow_data.loc[use_case_del[1]+1:j, i] = workflow_data[i][
                                                                        use_case_del[1]+1:j + 1].bfill()
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
    data['Число месяца'] = year_month[0] + '/' + year_month[1] + '/' + data['Число месяца'].astype(str) + '/' + data['UTC'].astype(str)
    data['Число месяца'] = pandas.to_datetime(data['Число месяца'], infer_datetime_format=True)
    data.drop(data.columns[[1]], axis='columns', inplace=True)
    data = data.rename(columns={'Число месяца': 'datetime'})

    data = data.sort_values(by=['datetime'])
    data = holes_check(data)

    for widget in tab12.winfo_children():
        widget.destroy()
    tab12.pack_forget()
    dynamic_lightning = print_graph_first(data)
    tab1_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab12)  # A tk.DrawingArea.
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab1_holst)

    for widget in tab13.winfo_children():
        widget.destroy()
    tab13.pack_forget()
    tab2_holst = FigureCanvasTkAgg(print_graph_second(data), master=tab13)  # A tk.DrawingArea.
    tab_holst(tab2_holst)


    for widget in tab14.winfo_children():
        widget.destroy()
    tab14.pack_forget()
    tab3_holst = FigureCanvasTkAgg(print_graph_third(data), master=tab14)  # A tk.DrawingArea.
    tab_holst(tab3_holst)

    for widget in tab15.winfo_children():
        widget.destroy()
    tab15.pack_forget()
    dynamic_lightning = print_graph_fourth(data)
    tab4_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab15)  # A tk.DrawingArea.
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab4_holst)

    for widget in tab16.winfo_children():
        widget.destroy()
    tab16.pack_forget()
    dynamic_lightning = print_graph_fifth(data)
    tab5_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab16)  # A tk.DrawingArea.
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab5_holst)

    for widget in tab17.winfo_children():
        widget.destroy()
    tab17.pack_forget()
    dynamic_lightning = print_graph_sixth(data)
    tab6_holst = FigureCanvasTkAgg(dynamic_lightning[0], master=tab17)  # A tk.DrawingArea.
    cursor = mplcursors.cursor(dynamic_lightning[1], hover=True)
    tab_holst(tab6_holst)

    for i, item in enumerate(tab_child.tabs()):
        tab_child.tab(item, state='normal')  # Does work

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
        part_label['foreground'] = 'green'
        part_label['text'] = 'Файл прочитаний, дивiться нові вкладки'
        main_frame = pandas_transforming(file_path)
        import_btn['width'] = '16'
        import_btn['text'] = 'Обрати iнший файл'


app = Tk()
app.title('Проектування кібер-енергетичних систем')
app.geometry('700x500+400+100')
app.resizable(True, True)


tab_parent = ttk.Notebook(app)
tab_parent.pack(expand=1, fill='both')

tab1 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Лабораторна 1")

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

part_text = StringVar()
<<<<<<< HEAD
part_label = Label(tab11, text='Оберiть лист таблиці Excel,\n з розширення xlsx', font=('bold', 20), pady=20)
part_label.place(relx=0.5, rely=0.4, anchor=CENTER)

import_btn = Button(tab11, text='Обрати', height=1, font=('bold', 18), command=file_worker)
=======
part_label = Label(tab11, text='Оберiть лист таблиці Excel,\n з розширення xlsx', font=('Rockwell', 20), pady=20)
part_label.place(relx=0.5, rely=0.4, anchor=CENTER)

import_btn = Button(tab11, text='Обрати', height=1, font=('Rockwell', 18), command=file_worker)
>>>>>>> origin/NewLabTest4
import_btn.place(relx=0.5, rely=0.7, anchor=CENTER)


app.mainloop()
