import code128
import mailsender
from datetime import date
import getpass
import notification
username = getpass.getuser()
import pyodbc
from barcode.writer import ImageWriter
from random import randint
import barcode
import os
import time
from PIL import Image
import cert_gui
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class BarcodeCreating(QtWidgets.QMainWindow, cert_gui.Ui_Certificates):

    def __init__(self, WRKORDNO):
        self.random_int = int()
        self.fullname = str()
        self.WRKORDNO = WRKORDNO
        super().__init__()
        self.setupUi(self)
        self.OK.clicked.connect(lambda x: self.clickMethod())
        server = ''
        database = 'DB'
        username = 'sa'
        password = 'PW'
        driver = '{SQL Server}'  # Driver you need to connect to the database
        port = '1433'
        self.cnn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        self.cursor = self.cnn.cursor()
        self.cursor.execute("""
        select c.LNAME,c.WTEL,c.email,g.WRKORDNO, c.custno from GSALS01 g
        join cust c on c.CUSTNO=g.CUSTNO
        where g.GSALID=(select gsalid from GSALS01 where WRKORDNO={})
        """.format(self.WRKORDNO))  # select gsalid from GSALS01 where WRKORDNO=
        for row in self.cursor:
            self.fio.setText(row[0])
            self.email.setText(row[2])
            self.custno = row[4]

    def clickMethod(self):
        print(len(self.textEdit.toPlainText()))
        if len(self.textEdit.toPlainText()) == 0:
            self.res.setText("Заполните комментарий")
            self.res.setStyleSheet('color: red')

        else:
            if "@" and "." in self.email.text():
                ret = QMessageBox.question(self, 'Подтвердите!',
                                           "Отправить на:  \n {}".format(self.email.text(), self.fio.text()),
                                           QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.Yes:
                    self.all_procedure()
            else:
                self.res.setText("Проверьте правильность написания почты")
                self.res.setStyleSheet('color: red')

    def create_barcode(self):
        self.random_int = randint(10000000000000, 90000000000000)
        cd = code128.image('{}'.format(self.random_int))
        cd.save("C:\\AM\\BAT\\Gift_certificate\\barcods_rent_car\\{}.png".format(self.random_int))
        img1 = Image.open('C:\\AM\\BAT\\Gift_certificate\\barcods_rent_car\\cert.jpg')  # main image
        barcd = Image.open("C:\\AM\\BAT\\Gift_certificate\\barcods_rent_car\\{}.png".format(self.random_int))

        img1.paste(barcd, (0, 850))  # paste barcode to main image
        img1.save("C:\\AM\\BAT\\Gift_certificate\\barcods_rent_car\\img_with_barcode.png")

    # sender(mail, name, "C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")

    def check_in_base(self, x):
        self.sqlifexist = f"""
          if exists (
          select discid from amintegrations.dbo.certificates_rent_car where discid={x})                                               
          select 'true'
          else select 'none'
        """
        self.cursor.execute(self.sqlifexist)
        for row in (self.cursor.execute(self.sqlifexist)):
            if row[0] == 'true':
                return "true"
        self.cursor.commit()

    def add_to_base(self):

        sql1 = """
        insert into amintegrations.dbo.certificates_rent_car (discid, custno, email, wrkordno, discsum, salesman, date, comment)
        VALUES ({},{},'{}',{},{},'{}',{}, '{}')""".format(self.random_int, self.custno,
                                                          self.email.text(), self.WRKORDNO,
                                                          500,
                                                          str(getpass.getuser()), "GETDATE()",
                                                          self.textEdit.toPlainText())
        self.cursor.execute(sql1)
        self.cursor.commit()


    def all_procedure(self):
        try:
            self.create_barcode()
            mailsender.sender(f"{self.email.text()}", f"{self.fio.text()}", "img_with_barcode.png")
            self.add_to_base()
            notification.my_notifier("Сертифіка успішно надісланий")
        except Exception as err:
            self.res.setText(err)
            self.res.setStyleSheet('color: red')
            notification.my_notifier("При відправці сертифікату виникла помилка")

        finally:
            print(self.fullname)
            time.sleep(3)
            os.remove(f"C:\\AM\\BAT\\Gift_certificate\\barcods_rent_car\\{self.fullname}")
            os.remove(r"C:\AM\BAT\Gift_certificate\barcods_rent_car\img_with_barcode.png")
            self.cnn.close()

            self.close()


def main(WRKORDNO):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BarcodeCreating(WRKORDNO)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    WRKORDNO = sys.argv[1] #2077107#
    main(WRKORDNO)
