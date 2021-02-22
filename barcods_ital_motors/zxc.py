import code128
import mailsender
from datetime import date
import getpass
import notification
username = getpass.getuser()
import pyodbc
from random import randint
import barcode
from barcode.writer import ImageWriter
import os
import time
from PIL import Image
import cert_gui
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class BarcodeCreating(QtWidgets.QMainWindow, cert_gui.Ui_MainWindow):

    def __init__(self, WRKORDNO):
        self.random_int = int()
        self.fullname = str()
        self.WRKORDNO = WRKORDNO
        super().__init__()
        self.setupUi(self)
        self.OK.clicked.connect(lambda x: self.clickMethod())
        server = '10.10.10.25'
        database = 'DB'
        username = 'sa'
        password = 'pw'
        driver = '{SQL Server}'  # Driver you need to connect to the database
        port = '1433'
        self.cnn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        self.sm = int()
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
        if self.c100.isChecked():
            f_name = 'cert100'
            self.sm = 100
        if self.c350.isChecked():
            f_name = 'cert350'
            self.sm = 350
        if self.c500.isChecked():
            self.sm = 500
            f_name = 'cert500'
        if self.c750.isChecked():
            f_name = 'cert750'
            self.sm = 750


        img1 = Image.open(f'C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\{f_name}.png')  # main image

        cd = code128.image('{}'.format(self.random_int), height=250)
        cd.save("C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\{}.png".format(self.random_int))
        barcd = Image.open("C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\{}.png".format(self.random_int))

        img1.paste(barcd, (50, 725))  # paste barcode to main image
        img1.save("C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\img_with_barcode.png")

    # sender(mail, name, "C:\\AM\\BAT\\Gift_certificate\\barcods\\img_with_barcode.png")

    def check_in_base(self, x):
        self.sqlifexist = f"""
          if exists (
          select discid from amintegrations.dbo.cert_ital where discid={x})                                               
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
        insert into amintegrations.dbo.cert_ital (discid, custno, email, wrkordno, discsum, salesman, date, comment)
        VALUES ({},{},'{}',{},{},'{}',{}, '{}')""".format(self.random_int, self.custno,
                                                          self.email.text(), self.WRKORDNO,
                                                          self.sm,
                                                          str(getpass.getuser()), "GETDATE()",
                                                          self.textEdit.toPlainText())
        self.cursor.execute(sql1)
        self.cursor.commit()


    def all_procedure(self):
        try:
            self.create_barcode()
            mailsender.sender(f"{self.email.text()}", f"{self.fio.text()}", "img_with_barcode.png")
            self.add_to_base()
            notification.my_notifier("Сертифікат успішно надісланий")
        except Exception as err:
            self.res.setText(err)
            self.res.setStyleSheet('color: red')
            notification.my_notifier("При відправці сертифікату виникла помилка")

        finally:
            time.sleep(3)
            os.remove(f"C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\{self.random_int}.png")
            os.remove("C:\\AM\\BAT\\Gift_certificate\\barcods_ital_motors\\img_with_barcode.png")
            self.cnn.close()

            self.close()


def main(WRKORDNO):
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BarcodeCreating(WRKORDNO)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    WRKORDNO = sys.argv[1] #2004477#
    main(WRKORDNO)
#