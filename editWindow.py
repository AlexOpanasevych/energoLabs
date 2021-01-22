from tkinter import *
from tkinter import ttk
from tkinter import messagebox
class editWindow:
    def __init__(self, parentWidget, data_device:dict, callback):
        self.data_device = data_device
        self.callback = callback
        self.window = Toplevel(parentWidget, height=480, width=640, background='darkgrey')
        self.window.title('Редагування приладу: ' + data_device['name'])
        print(data_device)
        for item in self.data_device:
            self.data_device[item] = []
        self.name_edit_label = ttk.Label(self.window, text='Введіть нове ім\'я')
        self.name_edit_label.place(relx=0.05, rely=0.05)
        self.name_edit_entry= ttk.Entry(self.window, width=30)
        self.name_edit_entry.place(relx=0.3, rely=0.05)
        # self.power_edit_label = ttk.Label(self.window, text='Введіть нову потужність')
        # self.power_edit_label.place(relx=0.05, rely=0.1)
        # self.power_edit_entry= ttk.Entry(self.window, width=20)
        # self.power_edit_entry.place(relx=0.3, rely=0.1)


        self.label_turnon = Label(self.window, text='Ввімкнув:', font=('Rockwell', 10))
        self.label_turnon.place(relx=0.05, rely=0.3)
        self.label_turnoff = Label(self.window, text='Вимкнув:', font=('Rockwell', 10))
        self.label_turnoff.place(relx=0.05, rely=0.4)
        self.label_energy_active = Label(self.window, text='Потужність прибору (активний стан):', font=('Rockwell', 10))
        self.label_energy_active.place(relx=0.05, rely=0.5)
        self.label_energy_passive = Label(self.window, text='Потужність прибору (пасивний стан):', font=('Rockwell', 10))
        self.label_energy_passive.place(relx=0.05, rely=0.6)

        choices_hours = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                         '9', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19', '20', '21', '22', '23']
        self.w_custom3 = ttk.Combobox(self.window, values=choices_hours, state='readonly', width=2)
        self.w_custom3.current(0)
        self.w_custom3.place(relx=0.15, rely=0.3)
        self.label_turnon = Label(self.window, text=':', font=('Rockwell', 10))
        self.label_turnon.place(relx=0.21, rely=0.3)
        choices_mins = ['0', '5', '10', '15', '20', '25', '30', '35', '40',
                        '45', '50', '55']
        self.w_custom4 = ttk.Combobox(self.window, values=choices_mins, width=2)
        self.w_custom4.current(0)
        self.w_custom4.place(relx=0.23, rely=0.3)

        self.w_custom5 = ttk.Combobox(self.window, values=choices_hours, state='readonly', width=2)
        self.w_custom5.current(0)
        self.w_custom5.place(relx=0.15, rely=0.4)
        self.label_turnon = Label(self.window, text=':', font=('Rockwell', 10))
        self.label_turnon.place(relx=0.21, rely=0.4)
        self.w_custom6 = ttk.Combobox(self.window, values=choices_mins, width=2)
        self.w_custom6.current(1)
        self.w_custom6.place(relx=0.23, rely=0.4)

        self.w_custom3.bind('<<ComboboxSelected>>', self.check_time)
        self.w_custom4.bind('<<ComboboxSelected>>', self.check_time)
        self.w_custom5.bind('<<ComboboxSelected>>', self.check_time)
        self.w_custom6.bind('<<ComboboxSelected>>', self.check_time)

        def validate_positive_number(inStr: str):
            if (inStr.isdigit() and int(inStr) > 0) or not inStr:
                return True
            else:
                return False

        self.entry_energy_active = Entry(self.window, validate="key")
        self.entry_energy_active['validatecommand'] = (self.entry_energy_active.register(validate_positive_number), '%P')
        self.entry_energy_active.place(relx=0.45, rely=0.5)
        self.entry_energy_passive = Entry(self.window, state='disabled', validate='key')
        self.entry_energy_passive['validatecommand'] = (self.entry_energy_passive.register(validate_positive_number), '%P')
        self.entry_energy_passive.place(relx=0.45, rely=0.6)


        self.days = ttk.Combobox(self.window, values=list(data_device.keys())[:-1], state='readonly', width=10)
        self.days.current(0)
        self.days.place(relx=0.05, rely=0.9)

        # self.days.bind('<<ComboboxSelected>>', self._change_time_combobox)

        # self.time_combobox = ttk.Combobox(self.window, values=[str(item) for item in data_device[self.days.get()]], state='readonly', width=50)
        # self.time_combobox.current(0)
        # self.time_combobox.place(relx=0.65, rely=0.3, anchor=CENTER)
        self.btn_inner_change_add = ttk.Button(self.window, text='Додати', command=self._add_or_change, width=15)
        self.btn_inner_change_add.place(relx=0.2, rely=0.9)


        self.confirm_day_button = ttk.Button(self.window, text='Наступний день', command=self._next_day, width=15)
        self.confirm_day_button.place(relx=0.4, rely=0.9)
        self.confirm_day_button['state'] = 'disabled'
        self.confirm_button = ttk.Button(self.window, text='Підтвердити', command=self._confirm_edit, width=15)
        self.confirm_button.place(relx=0.6, rely=0.9)

    def _confirm_edit(self):
        if self.name_edit_entry.get():
            self.data_device['name'] = str(self.name_edit_entry.get())
            self.window.destroy()
            self.callback(self.data_device)
        else:
            self.name_edit_label['foreground'] = 'red'

    def _next_day_check(self):
        return self.entry_energy_active.get()


    def _next_day(self):
        if self._next_day_check():
            self.days['values'] = [item for item in self.days['values'] if item != self.days.get()]
            self.days.set('')
            # self.time_combobox['values'] = []
            # self.time_combobox.set('')
            if len(self.days['values']):
                self.days.current(0)
                self.confirm_day_button['state'] = 'disabled'
                # self.time_combobox['values'] = [str(item) for item in self.data_device[self.days.get()]]
                # self.time_combobox.current(0)

    def check_time(self, what=None):
        rest = int(self.w_custom5.get()) - int(self.w_custom3.get())
        print('invoked', rest)
        if rest < 0:
            self.w_custom3['state'] = 'invalid'
            self.w_custom5['state'] = 'invalid'
            self.btn_inner_change_add['state'] = 'disabled'
            self.window.bell()
            return False
        elif rest == 0:
            if int(self.w_custom6.get()) - int(self.w_custom4.get()) <= 0:
                self.w_custom4['state'] = 'invalid'
                self.w_custom6['state'] = 'invalid'
                self.btn_inner_change_add['state'] = 'disabled'
                self.window.bell()
                return False
            else:
                self.w_custom4['state'] = 'normal'
                self.w_custom6['state'] = 'normal'
                self.btn_inner_change_add['state'] = 'normal'
                return True
        else:
            self.w_custom3['state'] = 'normal'
            self.w_custom5['state'] = 'normal'
            self.btn_inner_change_add['state'] = 'normal'
            return True

    def _add_or_change(self):

        day = self.days.get()
        if day:
            data_day = self.data_device[day]
            for session in data_day:
                if session['time_start'] == str(self.w_custom3.get()) + ":" + \
                        str(self.w_custom4.get()):
                    # session['time_end'] = str(self.w_custom5.get()) + ":" + str(self.w_custom6.get())
                    # session['energy'] = [str(self.entry_energy_active.get())]
                    return
            data_day.append({})
            data_day[-1]['energy'] = [int(self.entry_energy_active.get())]
            data_day[-1]['time_start'] = str(self.w_custom3.get()) + ":" + str(self.w_custom4.get())
            data_day[-1]['time_end'] = str(self.w_custom5.get()) + ":" + \
                                                                     str(self.w_custom6.get())
            self.data_device[day] = data_day
            print(data_day)
            self.confirm_day_button['state'] = 'normal'
            # for session in data_day[:-1]:
            #     tokens = session['time_end'].split(':')
            #     h = int(tokens[0])
            #     m = int(tokens[1])
            #     if h > int(self.w_custom5.get()) or (h == int(self.w_custom5.get()) and m > )