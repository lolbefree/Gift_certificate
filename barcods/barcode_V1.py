#!/usr/bin/python
# -*- coding: utf-8 -*-
#py -u test.py qwe
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import *
import code128
import mailsender
from datetime import date
import getpass
username = getpass.getuser()
import pyodbc
from barcode.writer import ImageWriter
from random import randint
import barcode
import os
import time

fullname = ""
randomint = ""

def check_id(randomint):
    server = '10.10.10.25'
    database = 'BD'
    username = 'sa'
    password = 'pw'
    driver = '{SQL Server}'  # Driver you need to connect to the database
    port = '1433'
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)

    cursor = cnn.cursor()

    sqlifexist = """
      if exists (
      select discid from amintegrations.dbo.ascertificates where discid={})                                               
      select 'true'
      else select 'none'
    """.format(randomint)                                                              # наличие в базе такой ид карточки


    sql_res = cursor.execute(sqlifexist)
    for row in sql_res:
        if (row[0]) =="true":
            os.remove(str(randomint) + ".png")
            create_barcode()
        else:
            return



def create_barcode():
    global randomint
    global fullname
    randomint = randint(10000000000000, 90000000000000)
    cd = code128.image('{}'.format(randomint))
    cd.save("C:\\AM\BAT\\Gift_certificate\\barcods\\{}.png".format(randomint))
    fullname = "{}.png".format(randomint)
    check_id(randomint)

create_barcode()



# создание приложения
app = tk.Tk()
app.configure(background='#E0E0E4')

app.title("Скидочные карты")
#app.configure(background="#ececec")
app.iconbitmap('C:\\AM\\BAT\\Gift_certificate\\barcods\\logo.ico')
app.minsize(480, 160)
app.maxsize(480, 160)
# создание текстовой надписи
search_label_card = ttk.Label(app, text="Выберете карту: ")
search_label_card.configure(background='#E0E0E4')
search_label_card.grid(row=7, column=0)

search_label_fio = ttk.Label(app, text="ФИО: ")
search_label_fio.grid(row=2, column=0)
search_label_fio.configure(background='#E0E0E4')
# создание поля для ввода информации

text_field_fio = ttk.Entry(app, width=50)
text_field_fio.grid(row=2,column=1)


search_label_tel = ttk.Label(app, text="Emeil: ")
search_label_tel.grid(row=3, column=0)
search_label_tel.configure(background='#E0E0E4')
# создание поля для ввода информации
text_field_tel = ttk.Entry(app, width=50)
text_field_tel.grid(row=3,column=1)

search_label_com = ttk.Label(app, text="Коментарии: ")
search_label_com.grid(row=5, column=0)
search_label_com.configure(background='#E0E0E4')
# создание поля для ввода информации
text_field_com = Text(app, height=5, width=38)
text_field_com.grid(row=5,column=1)

search_engine = StringVar()
search_engine.set("500")
today = date.today()


custno =""
tmp_for_wrkdno = ""

dict_with_data_for_sql = {"fullname":randomint, "custno":custno, "mail":text_field_tel.get(),
                          "tmp_for_wrkdno":tmp_for_wrkdno, "sum_of_dicount":search_engine.get(),
                          "salesman":getpass.getuser()}                 # словарь для подставки данных в скл и переменные

def m1(f1):


    var = f1
    server = '10.10.10.25'
    database = 'amprod'
    username = 'sa'
    password = 'Aut0m4ster'
    driver = '{SQL Server}'  # Driver you need to connect to the database
    port = '1433'
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnn.cursor()
    cursor .execute("""
select c.LNAME,c.WTEL,c.email,g.WRKORDNO, c.custno from GSALS01 g
join cust c on c.CUSTNO=g.CUSTNO
where g.GSALID=(select gsalid from GSALS01 where WRKORDNO={})
""".format(f1))  # select gsalid from GSALS01 where WRKORDNO=
    for row in cursor:
       # print(row)

        text_field_fio.insert(0, row[0])
        text_field_tel.insert(0, row[2])
        dict_with_data_for_sql["mail"] = row[2]
        dict_with_data_for_sql["tmp_for_wrkdno"] = row[3]
        dict_with_data_for_sql["custno"] = row[4]



#m1(f1=2077107)          # точка входа передаваемая автомастером

def m2():


    server = '10.10.10.25'
    database = 'amprod'
    username = 'sa'
    password = 'Aut0m4ster'
    driver = '{SQL Server}'  # Driver you need to connect to the database
    port = '1433'
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    cursor = cnn.cursor()
    sqlquery = """
    insert into amintegrations.dbo.ascertificates (discid, custno, email, wrkordno, discsum, salesman, date, comment)
    VALUES ({},{},'{}',{},{},'{}',{}, '{}')""".format(int(dict_with_data_for_sql["fullname"]), int(dict_with_data_for_sql["custno"]),
                                                  dict_with_data_for_sql["mail"], int(dict_with_data_for_sql["tmp_for_wrkdno"]),
                                                  int(dict_with_data_for_sql["sum_of_dicount"]),
                                                  str(getpass.getuser()), "GETDATE()", text_field_com.get("1.0", END))
    #print(sqlquery)

    cursor.execute(sqlquery)
    cnn.commit()                            # заполняем колонки в базе если соблюдается условие

def check_info(sum_discount, mail, name, fullname):
    MsgBox = tk.messagebox.askquestion('Подведём итоги', """   Клиент: {}
   emeil: {}
   Сумма карты: {}
   Коментарий: {}
   """.format(text_field_fio.get(), text_field_tel.get(), sum_discount,(text_field_com.get("1.0", END)), icon='question'))
    if MsgBox == 'yes':
        if sum_discount == 500:
            mailsender.five_100(mail, name, fullname)
            m2()
            app.destroy()
        if sum_discount == 1000:
            m2()
            mailsender.One_1000(mail, name, fullname)
            app.destroy()
        #root.destroy()
    else:
        tk.messagebox.showinfo('Внимание', 'Перепроверьте заполненную информацию')

# button1 = tk.Button(root, text='Exit Application', command=ExitApplication)
# canvas1.create_window(150, 150, window=button1)
#
    # root.mainloop()


def search():
    #print(len(text_field_fio.get()))
    #print((text_field_tel.get()))
   # print(len(text_field_com.get("1.0", END)))

    if len(text_field_fio.get()) != 0 and '@' in (text_field_tel.get()) and len(text_field_com.get("0.0", END)) != 1:


        if search_engine.get() == "500":
            dict_with_data_for_sql["sum_of_dicount"] = 500
            mail = (text_field_tel.get())
            name = (text_field_fio.get())
           # mailsender.five_100(mail, name, fullname)

            check_info(dict_with_data_for_sql["sum_of_dicount"], mail, name, fullname)


        elif search_engine.get() == "1000":
            dict_with_data_for_sql["sum_of_dicount"] = 1000
            mail = (text_field_tel.get())
            name = (text_field_fio.get())
            check_info(dict_with_data_for_sql["sum_of_dicount"], mail, name, fullname)
           # mailsender.One_1000(mail, name, fullname)




btn_search = ttk.Button(app, text="Отправить", width=10, command=search)
btn_search.grid(row=7, column=2)


radio_500 = ttk.Radiobutton(app, text="500 грн", value="500", variable=search_engine)

radio_1000 = ttk.Radiobutton(app, text="1000 грн", value="1000", variable=search_engine)

radio_500.grid(row=7, column=1, sticky=W) # sticky от слова вест, слева
radio_1000.grid(row=7, column=1, sticky=E)# sticky от слова вест, справо

text_field_fio.focus() # фокусировка текстфилда

app.wm_attributes("-topmost", True)
# запуск приложения

args = sys.argv[1]
get_gsalid = m1(args) 
app.mainloop()
try:
    os.remove("C:\\AM\BAT\\Gift_certificate\\barcods\\{}.png".format(randomint))
except:
    print("fuck")
    time.sleep(4)