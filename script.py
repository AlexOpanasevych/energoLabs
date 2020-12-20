import sys

import pandas as pd
from windrose import WindroseAxes
from spyre import server
import numpy as np
import matplotlib.pyplot as plt


# LIST_CITY = ["львов+","кривой_рог+","симферополь+","и_франк+","донецк+","харьков+","днепропетровськ+","киев+",
# "одесса+","луганськ+"] t = 0 for j in LIST_CITY:              # create df from files data_fr = pd.DataFrame() for i
# in range(1,13): data_fr = data_fr.append(pd.read_excel(j+"/2012-"+str(i)+".xlsx")) if i == 1: data_fr["Mon"] = 1
# else: data_fr["Mon"] = data_fr["Mon"].fillna(i) data_fr.to_csv(str(t) + ".csv") t += 1 # LIST_DF.append(data_fr)

# for i in range(10):          # fix date and clean db
#     df = pd.read_csv(str(i) + ".csv")
#     df = df.fillna("0")
#     df['Число месяца'] = df['Число месяца'].astype(int)
#     df['Mon'] = df['Mon'].astype(int)
#     df['UTC'] = df['Число месяца'].astype(str) + "." + df['UTC']
#     df['UTC'] = "2012." + df['Mon'].astype(str) + "." + df['UTC']
#     del df['Число месяца']
#     del df['Mon']
#     del df['U']
#     df['UTC'] = pd.to_datetime(df['UTC'],format='%Y.%m.%d.%H:%M:%S', errors='coerce')
#     df.to_csv(str(i) + ".csv")


class StockExample(server.App):
    title = "Проектування кібер-енергетичних систем"

    inputs = [{"type": 'dropdown',
               "label": 'Місто',
               "options": [{"label": "Львів", "value": "львов"},
                           {"label": "Кривий Ріг", "value": "кривой_рог"},
                           {"label": "Сімферополь", "value": "симферополь"},
                           {"label": "Івана-Франківськ", "value": "и_франк"},
                           {"label": "Донецьк", "value": "донецк"},
                           {"label": "Харків", "value": "харьков"},
                           {"label": "Дніпропетровськ", "value": "днепропетровськ"},
                           {"label": "Київ", "value": "киев"},
                           {"label": "Одеса", "value": "одесса"},
                           {"label": "Луганськ", "value": "луганськ"}, ],
               "key": 'city',
               "action_id": "update_data"},
              {
                  "type": 'text',
                  "label": 'Date: ',
                  "value": '20.05-26.09',
                  "key": 'date',
                  "action_id": "refresh",
              },
              {"type": 'dropdown',
               "label": 'Завдання 1',
               "options": [
                   {"label": "-", "value": "-"}, {"label": "Температурні умови", "value": "T_plot"},
                   {"label": "Тривалість температурних режимів", "value": "T_val_plot"},
                   {"label": "Троянда вітрів ", "value": "Wind"},
                   {"label": "Тривалість режимів вітрової активності", "value": "val_wind"},
                   {"label": "Інтенсивність сонячної інсоляції", "value": "sun_izo"},
                   {"label": "Тривалість режимів сонячної активності", "value": "val_sun_izo"}, ],
               "key": 'exer',
               "action_id": "update_data"},
              {"type": 'dropdown',
               "label": 'Завдання 2',
               "options": [{"label": "2_1", "value": "2_1"},
                           {"label": "2_2", "value": "2_2"},
                           {"label": "2_3", "value": "2_3"},
                           {"label": "2_4", "value": "2_4"},
                           {"label": "2_5", "value": "2_5"},
                           {"label": "2_6", "value": "2_6"},
                           {"label": "2_7", "value": "2_7"}, ],
               "key": 'exer_2',
               "action_id": "update_data"},
              {
                  "type": 'text',
                  "label": '2.1 Вт/м2',
                  "value": '12',
                  "key": 's_one',
                  "action_id": "refresh",
              },
              {
                  "type": 'text',
                  "label": '2.1 S',
                  "value": '3',
                  "key": 's_one_s',
                  "action_id": "refresh",
              },
              {
                  "type": 'text',
                  "label": '2.2: Nд/Qд/Тд/Nв/Qв/Тв',
                  "value": '3/2/3/1/2/1',
                  "key": 's_s',
                  "action_id": "refresh",
              },
              {
                  "type": 'text',
                  "label": '2.2: T.вх/T.вих/Т.бака/t.нагр',
                  "value": '3/2/2/3',
                  "key": 's_s_s',
                  "action_id": "refresh",
              },
              {
                  "type": 'text',
                  "label": '2.3: T.роз/Q.тепла/S.буд',
                  "value": '3/2/2',
                  "key": 's_t',
                  "action_id": "refresh",
              },
              {
                  "type": 'slider',
                  "label": '2.5: T',
                  "value": '10',
                  "min": -30,
                  "max": 30,
                  "key": 'sli',
                  "action_id": "refresh",
              },
              {"type": 'dropdown',
               "label": '2.6',
               "options": [{"label": "теплозабезпечення від централізованої мережі;", "value": "1"},
                           {"label": "автономного теплозабезпечення від газового котла;", "value": "2"},
                           {"label": "автономного теплозабезпечення від вугільного котла;", "value": "3"},
                           {"label": "автономного теплозабезпечення від дров’яного котла;", "value": "4"},
                           {"label": "автономного теплозабезпечення від котла, що працює на деревних пелетах;",
                            "value": "5"},
                           {"label": "автономного теплозабезпечення від електричного котла.", "value": "6"}, ],
               "key": 's_six',
               "action_id": "update_data"},
              {
                  "type": 'text',
                  "label": '2.6: N топл',
                  "value": '302',
                  "key": 's_six_t',
                  "action_id": "refresh",
              }]

    controls = [{"type": "button", "label" : "Update Data",
                 "id": "update_data"}]

    tabs = ["Plot", "Second",]
    # Теплотехнічні характеристики будівлі, потреба у тепловій енергії на опалення, ГВП та вентилювання
    outputs = [{"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"},
               {"type": "html",
                "id": "simphtml",
                "control_id": "update_data",
                "tab": "Second",
                "on_page_load": True}, ]

    def getHTML(self, params):
        res = 1
        LIST_CITY = ["львов+", "кривой_рог+", "симферополь+", "и_франк+", "донецк+", "харьков+", "днепропетровськ+",
                     "киев+", "одесса+", "луганськ+"]
        if params["exer_2"] == "2_1":
            q = float(params["s_one"])
            w = float(params["s_one_s"])
            res = q * w
            return f"<font 'text-align: center; size=20' face='Arial'>Теплотехнічних характеристик будівлі:<br>Питомі " \
                   f"тепловтрати: {q} Вт/м²<br> Загальна площа: {w} м²<br> Результат : {res}</font> "
        elif params["exer_2"] == "2_2":
            List_str = params["s_s"] + "/" + params["s_s_s"]
            List_arg = List_str.split('/')
            List_arg = list(map(float, List_arg))
            try:
                Q_d = List_arg[0] * List_arg[1]
                Q_v = List_arg[3] * List_arg[4]
                Q_td = Q_d * float((List_arg[2] - List_arg[6]) / (List_arg[7] - List_arg[6]))
                Q_tv = Q_v * float((List_arg[5] - List_arg[6]) / (List_arg[7] - List_arg[6]))
                Q_tgv = ((Q_td - Q_tv) / 998.23)
                W_tgv = 1.163 * Q_tgv * (List_arg[8] - List_arg[6])
                P_gvp = W_tgv / List_arg[9]
            except ZeroDivisionError:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                return "<font 'text-align: center; size=20' face='Arial'>Поділено на нуль! Змініть вхідні дані! (Строка: {lineno})</font>".format(lineno=exc_tb.tb_lineno)
            return f"<font 'text-align: center; size=20' face='Arial'>Q душ  = {Q_d} Дж/кг·К<br>Q ванн  = {Q_v} Дж/кг·К<br>Qt душ = {Q_td} л/добу<br>Qt ванн = {Q_tv} л/добу<br>Qt г.води = {Q_tgv} м³/добу<br>W г.води = {W_tgv} кВт·год<br>P ГВП = {P_gvp} кВт</font>"
        elif params["exer_2"] == "2_3":
            List_arg = params["s_s"].split('/')
            List_arg = list(map(float, List_arg))
            Q_r_tp = List_arg[0] * List_arg[1] * List_arg[2]
            return f"<font 'text-align: center; size=20' face='Arial'>Потужність тепловтрат : {Q_r_tp} кВт</font>"
        elif params["exer_2"] == "2_4":
            return f""
        elif params["exer_2"] == "2_5":
            citys = params["city"]
            index = LIST_CITY.index(citys + "+")
            df = pd.read_csv(str(index) + ".csv", index_col=0)
            df['T'] = params["sli"]
            q = sum(df['T'])
            res = q * 18.23
            return "<font 'text-align: center; size=20' face='Arial'>Витрати енергії на опалення : {res} кВт·год</font>".format(res=res)
        elif params["exer_2"] == "2_6" or params["exer_2"] == "2_7":
            citys = params["city"]
            index = LIST_CITY.index(citys + "+")
            df = pd.read_csv(str(index) + ".csv", index_col=0)
            q = (df['T'] == params["sli"] - 30).sum()
            res = q * 18.23
            List_arg = (params["s_s"] + "/" + params["s_s_s"]).split('/')
            List_arg = list(map(float, List_arg))
            Q_d = List_arg[0] * List_arg[1]
            Q_v = List_arg[3] * List_arg[4]
            Q_td = Q_d * ((List_arg[2] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tv = Q_v * ((List_arg[5] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tgv = ((Q_td - Q_tv) / 998.23)
            W_tgv = 1.163 * Q_tgv * (List_arg[8] - List_arg[6])
            dict_cost = {"1": 16.784, "2": 12.76, "3": 19.20, "4": 23.20, "5": 17.74, "6": 12.80}
            f = float(params["s_six_t"])
            key = params["s_six"]
            res_this = res * W_tgv * f * dict_cost[key]
            List_cost = []
            for i in dict_cost:
                qu = res * W_tgv * f * dict_cost[i]
                List_cost.append(qu)
            if params["exer_2"] == "2_6":
                if key == "1":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: теплозабезпечення від " \
                           "централізованої мережі = {res_this:.2f} грн</font> ".format(res_this=res_this)
                elif key == "2":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: автономного теплозабезпечення від " \
                           "газового котла = {res_this:.2f} грн</font> ".format(res_this=res_this)
                elif key == "3":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: автономного теплозабезпечення від " \
                           "вугільного котла = {res_this:.2f} грн</font> ".format(res_this=res_this)
                elif key == "4":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: автономного теплозабезпечення від " \
                           "дров’яного котла = {res_this:.2f} грн</font> ".format(res_this=res_this)
                elif key == "5":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: автономного теплозабезпечення від " \
                           "котла, що працює на деревних пелетах = {res_this:.2f} грн</font> ".format(res_this=res_this)
                elif key == "6":
                    return "<font 'text-align: center; size=20' face='Arial'>За відомими обсягам споживання " \
                           "розрахувати вартість опалення та ГВП будівлі для умов: автономного теплозабезпечення від " \
                           "електричного котла = {res_this:.2f} грн</font> ".format(res_this=res_this)
                return "<a></a>"

        return "<a></a>"

    def getPlot(self, params):
        plt_obj = None
        LIST_CITY = ["львов+", "кривой_рог+", "симферополь+", "и_франк+", "донецк+", "харьков+", "днепропетровськ+",
                     "киев+", "одесса+", "луганськ+"]
        cities = params["city"]
        index = LIST_CITY.index(cities + "+")
        df = pd.read_csv(str(index) + ".csv", index_col=0)
        df = df.set_index(df['UTC'])
        date_f = params["date"].split("-")[0]
        date_s = params["date"].split("-")[1]
        day_f = date_f.split('.')[0]
        mon_f = date_f.split('.')[1]
        day_s = date_s.split('.')[0]
        mon_s = date_s.split('.')[1]
        df = df[(df['UTC'] > '2012-' + mon_f + '-' + day_f) & (df['UTC'] < '2012-' + mon_s + '-' + day_s)]
        if params["exer"] == "T_plot":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            plt_obj = df.plot(figsize=(30, 10))
            plt_obj.set_ylabel("Sun Izo", fontsize=18)
            plt_obj.set_xlabel("Date", fontsize=18)
            plt_obj.set_title("Температурні умови", fontsize=18)
        elif params["exer"] == "T_val_plot":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in range(-30, 35, 1):
                q = (df['T'] == i).sum()
                dict_val.update({i: q})
            dfc = pd.DataFrame.from_dict(dict_val, orient='index')
            plt_obj = dfc.plot.bar(color='green', figsize=(30, 10))
            plt_obj.set_ylabel("t, год", fontsize=18)
            plt_obj.set_xlabel("T, (°C)", fontsize=18)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
        elif params["exer"] == "sun_izo":
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["T"]
            del df["Unnamed: 0.1"]
            plt_obj = df.plot(figsize=(30, 10))
            plt_obj.set_ylabel("Вт/м²", fontsize=18)
            plt_obj.set_xlabel("Date", fontsize=18)
            plt_obj.set_title("Інтенсивність сонячної інсоляції", fontsize=18)
            plt.xticks(rotation=45, fontsize=18)
            plt.yticks(fontsize=18)
        elif params["exer"] == "val_wind":
            del df["T"]
            del df["N"]
            del df["PPP"]
            del df["hhh"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in range(0, 15, 1):
                q = (df['FF'] == i).sum()
                dict_val.update({i: q})
            dfc = pd.DataFrame.from_dict(dict_val, orient='index')
            plt_obj = dfc.plot.bar(figsize=(30, 10))
            plt_obj.set_ylabel("год", fontsize=18)
            plt_obj.set_xlabel("м/с", fontsize=18)
            plt_obj.set_title('Розподіл вітрового потенціалу за швидкостями, год', fontsize=18)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
        elif params["exer"] == "val_sun_izo":
            arr = df["hhh"].unique()
            del df["FF"]
            del df["N"]
            del df["PPP"]
            del df["T"]
            del df["Unnamed: 0.1"]
            dict_val = {}
            for i in arr:
                if i == 0:
                    continue
                else:
                    q = (df["hhh"] == i).sum()
                    dict_val.update({i: q})
            dfc = pd.DataFrame.from_dict(dict_val, orient='index')
            plt_obj = dfc.plot.bar(figsize=(30, 10))
            plt_obj.set_xlabel("Вт/м²", fontsize=18)
            plt_obj.set_ylabel("год", fontsize=18)
            plt_obj.set_title("Тривалість режимів сонячної активності", fontsize=18)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
        elif params["exer"] == "Wind":
            dd = df["dd"].to_numpy()
            wd = []
            ws = df["FF"].to_numpy()
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
            wdd = np.array(wd)
            wdd.resize(len(ws))
            # wd.resize(len(ws))
            # ws = np.random.random(1500) * 4
            # wd = np.random.random(1500) * 360
            ax = WindroseAxes.from_ax()
            ax.bar(wdd, ws, normed=True, edgecolor='white', bins=np.arange(0, 4, 1))

            ax.set_legend()
            ax.set_title("Троянда вітрів")
            fig = ax.get_figure()
            return fig
        elif params["exer_2"] == "2_7" or params["exer_2"] == "2_4":
            citys = params["city"]
            index = LIST_CITY.index(citys + "+")
            df = pd.read_csv(str(index) + ".csv", index_col=0)
            q = (df['T'] == params["sli"] - 30).sum()
            res = q * 18.23
            List_str = params["s_s"] + "/" + params["s_s_s"]
            List_arg = List_str.split('/')
            List_arg = list(map(int, List_arg))
            Q_d = List_arg[0] * List_arg[1]
            Q_v = List_arg[3] * List_arg[4]
            Q_td = Q_d * ((List_arg[2] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tv = Q_v * ((List_arg[5] - List_arg[6]) / (List_arg[7] - List_arg[6]))
            Q_tgv = ((Q_td - Q_tv) / 998.23)
            W_tgv = 1.163 * Q_tgv * (List_arg[8] - List_arg[6])
            if params["exer_2"] == "2_7":
                dict_cost = {"1": 16.784, "2": 12.76, "3": 19.20, "4": 23.20, "5": 17.74, "6": 12.80}
                f = int(params["s_six_t"])
                key = params["s_six"]
                List_cost = []
                for i in dict_cost:
                    qu = res * W_tgv * f * dict_cost[i]
                    List_cost.append(qu)
                dict_val = {i: List_cost[i] for i in range(0, len(List_cost))}
                dfc = pd.DataFrame.from_dict(dict_val, orient='index')
                plt_obj = dfc.plot.bar(figsize=(30, 10))
            elif params["exer_2"] == "2_4":
                dict_gr = {}
                for i in range(-20, 20):
                    dict_gr.update({i: i * W_tgv})
                dfc = pd.DataFrame.from_dict(dict_gr, orient='index')
                plt_obj = dfc.plot(figsize=(30, 10), marker='.', markersize=35)
                plt_obj.grid()
        if plt_obj is not None:
            fig = plt_obj.get_figure()
            return fig
        return None


    def getCustomCSS(self):
        return ".tab-content {background:#E2E2E2;} body {background:linear-gradient(90deg, rgba(0,0,0,1) 0%, " \
               "rgba(255,255,255,1) 100%)} "


port = 8090
if __name__ == '__main__':
    app = StockExample()
    app.launch(port=port)
