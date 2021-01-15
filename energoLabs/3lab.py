def electrical_voltage():
    def choices_open():
        list_val = []
        with open('choices_values.txt', 'r') as fr:
            list_val = [i for i in fr.read().split('.')]
        return list_val[1:]

    w_31 = ttk.Combobox(tab31, values=choices_open(), state='readonly', width=70)
    w_31.current(0)
    w_31.place(relx=0.02, rely=0.14)

    def choices_add():
        tree.insert('', 'end', values=(w_31.get(), 15, 10))

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
        insert_vals.title('Введення свого приладу')
        insert_vals.minsize(600, 250)
        insert_vals.resizable(False, False)

        label_31 = Label(insert_vals, text='Назва пристрою:', font=('bold', 10))
        label_31.place(relx=0.01, rely=0.1)
        entry_31 = Entry(insert_vals, width=15)
        entry_31.place(relx=0.2, rely=0.1)
        choices_custom = ['ручне вмикання та вимикання', 'ручне вмикання, автоматичне вимикання',
                          'автоматичне вмикання та вимикання']
        w_custom = ttk.Combobox(insert_vals, values=choices_custom, state='readonly', width=25)
        w_custom.current(0)
        w_custom.place(relx=0.45, rely=0.1)

        choices_custom = ['автоматичне регулювання параметрів споживання', 'ручне регулювання параметрів споживання']
        w_energy = ttk.Combobox(insert_vals, values=choices_custom, state='readonly', width=35)
        w_energy.current(0)
        w_energy.place(relx=0.45, rely=0.2)

        choices_days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']
        w_custom2 = ttk.Combobox(insert_vals, values=choices_days, state='readonly', width=10)
        w_custom2.current(0)
        w_custom2.place(relx=0.01, rely=0.85)

        graphs_electrical_voltage = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [],
                                     'friday': [], 'saturday': [], 'sunday': [], 'name': ''}

        def next_day_check():
            if graphs_electrical_voltage['name'] and graphs_electrical_voltage['monday']:
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

        def custom_add():
            if len(w_custom2['values']) != 0:
                if entry_31.get():
                    label_31.config(fg="black")
                    graphs_electrical_voltage['name'] = entry_31.get()
                    entry_31['state'] = 'disabled'
                    try:
                        check_val = int(entry_energy_active.get())
                        label_energy_active.config(fg="black")
                        if w_custom2.get() == 'Понеділок':
                            graphs_electrical_voltage['monday'].append({})
                            graphs_electrical_voltage['monday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['monday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['monday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())
                        elif w_custom2.get() == 'Вівторок':
                            graphs_electrical_voltage['tuesday'].append({})
                            graphs_electrical_voltage['tuesday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['tuesday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                     str(w_custom4.get())
                            graphs_electrical_voltage['tuesday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                   str(w_custom6.get())
                        elif w_custom2.get() == 'Середа':
                            graphs_electrical_voltage['wednesday'].append({})
                            graphs_electrical_voltage['wednesday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['wednesday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                       str(w_custom4.get())
                            graphs_electrical_voltage['wednesday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                     str(w_custom6.get())
                        elif w_custom2.get() == 'Четвер':
                            graphs_electrical_voltage['thursday'].append({})
                            graphs_electrical_voltage['thursday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['thursday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                      str(w_custom4.get())
                            graphs_electrical_voltage['thursday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                    str(w_custom6.get())
                        elif w_custom2.get() == 'П\'ятниця':
                            graphs_electrical_voltage['friday'].append({})
                            graphs_electrical_voltage['friday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['friday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['friday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())
                        elif w_custom2.get() == 'Субота':
                            graphs_electrical_voltage['saturday'].append({})
                            graphs_electrical_voltage['saturday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['saturday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                      str(w_custom4.get())
                            graphs_electrical_voltage['saturday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                    str(w_custom6.get())
                        elif w_custom2.get() == 'Неділя':
                            graphs_electrical_voltage['sunday'].append({})
                            graphs_electrical_voltage['sunday'][-1]['energy'] = [check_val]
                            graphs_electrical_voltage['sunday'][-1]['time_start'] = str(w_custom3.get()) + ":" + \
                                                                                    str(w_custom4.get())
                            graphs_electrical_voltage['sunday'][-1]['time_end'] = str(w_custom5.get()) + ":" + \
                                                                                  str(w_custom6.get())

                        if entry_energy_passive['state'] == 'normal':
                            try:
                                check_val = int(entry_energy_passive.get())
                                label_energy_passive.config(fg="black")
                                if w_custom2.get() == 'Понеділок':
                                    graphs_electrical_voltage['monday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Вівторок':
                                    graphs_electrical_voltage['tuesday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Середа':
                                    graphs_electrical_voltage['wednesday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Четвер':
                                    graphs_electrical_voltage['thursday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'П\'ятниця':
                                    graphs_electrical_voltage['friday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Субота':
                                    graphs_electrical_voltage['saturday'][-1]['energy'].append(check_val)
                                elif w_custom2.get() == 'Неділя':
                                    graphs_electrical_voltage['sunday'][-1]['energy'].append(check_val)
                            except ValueError:
                                label_energy_passive.config(fg="red")
                                # graphs_electrical_voltage.clear()
                    except ValueError:
                        label_energy_active.config(fg="red")
                        # graphs_electrical_voltage.clear()
                    # entry_31['state'] = 'disabled'
                    # w_custom2['values'] = [i for i in w_custom2['values'] if i != w_custom2.get()]
                    # if not len(w_custom2['values']):
                    #     w_custom2['values'] = ['']
                    #     w_custom2['state'] = 'disabled'
                    #     btn_inner_add['state'] = 'disabled'
                    #     btn_inner_end['state'] = 'normal'
                    #     all_graphs_electrical_voltage.append(graphs_electrical_voltage)
                    # w_custom2.current(0)
                else:
                    label_31.config(fg="red")
            else:
                btn_inner_add['state'] = 'disabled'
                btn_inner_end['state'] = 'normal'
            next_day_check()
            print(graphs_electrical_voltage)
            # print(graphs_electrical_voltage)
            # tree.insert('', 'end', values=(w_31.get(), 15, 10))

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

        btn_inner_add = Button(insert_vals, text='Додати', height=1, font=('bold', 10), command=custom_add)
        btn_inner_add.place(relx=0.2, rely=0.84)

        btn_inner_add_2 = Button(insert_vals, text='Наступний день', height=1, font=('bold', 10), command=next_day,
                                 state='disabled')
        btn_inner_add_2.place(relx=0.4, rely=0.84)

        btn_inner_end = Button(insert_vals, text='Завершити додання', height=1, font=('bold', 10),
                               command=custom_destroy,
                               state='disabled')
        btn_inner_end.place(relx=0.7, rely=0.84)

        label_turnon = Label(insert_vals, text='Ввімкнув:', font=('bold', 10))
        label_turnon.place(relx=0.01, rely=0.3)
        label_turnoff = Label(insert_vals, text='Вимкнув:', font=('bold', 10))
        label_turnoff.place(relx=0.01, rely=0.4)
        label_energy_active = Label(insert_vals, text='Потужність прибору (активний стан):', font=('bold', 10))
        label_energy_active.place(relx=0.01, rely=0.5)
        label_energy_passive = Label(insert_vals, text='Потужність прибору (пасивний стан):', font=('bold', 10))
        label_energy_passive.place(relx=0.01, rely=0.6)

        choices_hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08',
                         '09', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19', '20', '21', '22', '23']
        w_custom3 = ttk.Combobox(insert_vals, values=choices_hours, state='readonly', width=2)
        w_custom3.current(0)
        w_custom3.place(relx=0.15, rely=0.3)
        label_turnon = Label(insert_vals, text=':', font=('bold', 10))
        label_turnon.place(relx=0.21, rely=0.3)
        choices_mins = ['00', '05', '10', '15', '20', '25', '30', '35', '40',
                        '45', '50', '55']
        w_custom4 = ttk.Combobox(insert_vals, values=choices_mins, width=2)
        w_custom4.current(0)
        w_custom4.place(relx=0.23, rely=0.3)

        w_custom5 = ttk.Combobox(insert_vals, values=choices_hours, state='readonly', width=2)
        w_custom5.current(0)
        w_custom5.place(relx=0.15, rely=0.4)
        label_turnon = Label(insert_vals, text=':', font=('bold', 10))
        label_turnon.place(relx=0.21, rely=0.4)
        w_custom6 = ttk.Combobox(insert_vals, values=choices_mins, width=2)
        w_custom6.current(1)
        w_custom6.place(relx=0.23, rely=0.4)

        entry_energy_active = Entry(insert_vals)
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

    btn_31 = Button(tab31, text='Обрати', height=1, font=('bold', 10), command=choices_add)
    btn_31.place(relx=0.6, rely=0.155, anchor=CENTER)

    btn_32 = Button(tab31, text='Додати', height=1, font=('bold', 10), command=choices_insert)
    btn_32.place(relx=0.7, rely=0.155, anchor=CENTER)

    btn_33 = Button(tab31, text='Видалити', height=1, font=('bold', 10), command=choices_delete)
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

        y_sum = [0]*7
        for item in all_graphs_electrical_voltage:
            tabs3_inf.append(ttk.Frame(tab_child_3))
            tabs3_inf_notes.append(ttk.Notebook(tabs3_inf[-1]))
            tab_child_3.add(tabs3_inf[-1], text=item['name'])
            for week, it in zip(('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'), range(7)):
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
                ax.grid()  # включение отображение сетки
                dt = ax.bar(x, y)


                ax.xaxis.set_ticks_position('both')

                for widget in tabs33_inf[-1].winfo_children():
                    widget.destroy()
                tabs33_inf[-1].pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tabs33_inf[-1])  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                toolbar = NavigationToolbar2Tk(tab1_canvas, tabs33_inf[-1])
                toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            if len(all_graphs_electrical_voltage) > 1 and item == all_graphs_electrical_voltage[-1]:
                tab3_overall = ttk.Frame(tab_child_3)
                tab_child_3.add(tab3_overall, text="Загальне споживання ел. енергії")

                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                pandas.plotting.register_matplotlib_converters()
                ax.set_title('Всi пристроi')
                ax.set_ylabel("Електрична потужність, кВт")  # ось ординат
                ax.grid()  # включение отображение сетки
                dt = ax.bar(('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'), y_sum)


                ax.xaxis.set_ticks_position('both')

                for widget in tab3_overall.winfo_children():
                    widget.destroy()
                tab3_overall.pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tab3_overall)  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                toolbar = NavigationToolbar2Tk(tab1_canvas, tab3_overall)
                toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                tab3_overall = ttk.Frame(tab_child_3)
                tab_child_3.add(tab3_overall, text="По зонам")

                fig = Figure(figsize=(12, 6), dpi=100)
                ax = fig.add_subplot(111)
                pandas.plotting.register_matplotlib_converters()
                ax.set_title('Зони')
                ax.set_ylabel("Електрична потужність, кВт")  # ось ординат
                ax.grid()  # включение отображение сетки
                dt = ax.bar(('Однозонний тариф', 'Двозонний', 'Трьохзонний'), [sum(y_sum), sum(y_sum)*0.825, sum(y_sum)*0.8])

                ax.xaxis.set_ticks_position('both')

                for widget in tab3_overall.winfo_children():
                    widget.destroy()
                tab3_overall.pack_forget()
                tab1_canvas = FigureCanvasTkAgg(fig, master=tab3_overall)  # A tk.DrawingArea.
                tab1_canvas.draw()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                toolbar = NavigationToolbar2Tk(tab1_canvas, tab3_overall)
                toolbar.update()
                tab1_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

            tabs3_inf_notes[-1].pack(expand=1, fill="both")

    btn_34 = Button(tab31, text='Розрахувати', height=1, font=('bold', 10), command=choices_build, state='disabled')
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
