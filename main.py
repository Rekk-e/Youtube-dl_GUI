import sys
import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pro import *


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.textChanged.connect(self.chose_url)
        self.ui.comboBox_2.activated.connect(self.chose_format)
        self.ui.lineEdit.textChanged.connect(self.chose_path)
        self.ui.pushButton.clicked.connect(self.download)



    def chose_url(self):

        global text
        text = self.ui.textEdit.toPlainText()

    def chose_format(self):
        global raar
        raar = []
        try:
            self.ui.tableWidget.setRowCount(0)
            box = self.ui.comboBox_2.currentText()
            ydl_opts = {'format': 'bestaudio/best'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    text, download=False)
                formats = meta.get('formats', [meta])
                title = meta.get('title', [meta])
            print(formats)
            for f in formats:
                if f['ext'] == box or (box == "Все форматы"):
                    try:
                        size = int(f['filesize']) / 1048576
                        size = float('{:.2f}'.format(size))
                        ei = ' Мб'
                    except:
                        size = 'Неизвестно'
                        ei = ''
                    rowPosition = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(rowPosition)
                    cell_widget = QWidget()
                    rad = QRadioButton()
                    rad.setObjectName(f['format_id'])
                    rad.setText(f['format_id'] + ' id')
                    rad.setStyleSheet('font: 6pt "MS Shell Dlg 2"')
                    lay_out = QHBoxLayout(cell_widget)
                    lay_out.addWidget(rad)
                    lay_out.setAlignment(Qt.AlignCenter)
                    lay_out.setContentsMargins(0, 0, 0, 0)
                    cell_widget.setLayout(lay_out)
                    self.ui.tableWidget.setCellWidget(rowPosition, 0, cell_widget)
                    self.ui.tableWidget.setToolTip('True')
                    self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(f['ext']))
                    self.ui.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(f['format'].split(' - ')[-1]))
                    self.ui.tableWidget.resizeColumnToContents(2)
                    self.ui.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(size) + '{}'.format(ei)))
                    self.ui.tableWidget.resizeColumnToContents(3)
                    self.ui.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(title))
                    self.ui.tableWidget.resizeColumnToContents(4)
                    raar.append(rad)
        except:
            print('ERROR')

    def chose_path(self):
        global path
        path = self.ui.lineEdit.text()

    def download(self):
        try:
            ids = []

            for i in raar:

                ydl_opts = {
                    'outtmpl': '{}/%(title)s-%(format_id)s.%(ext)s'.format(path)}
                if i.isChecked() == True:
                    ydl_opts['format'] = i.objectName()
                    print(ydl_opts)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([text])


        except NameError:
            pass


def mbox(self, body, title='Error'):
    dialog = QMessageBox(QMessageBox.Information, title, body)
    dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
