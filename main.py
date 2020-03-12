from PyQt5 import QtWidgets
from song_layout import Ui_MainWindow
import sys

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.analyze_button.clicked.connect(self.analyze_clicked)
    
    def analyze_clicked(self):
        if self.ui.info_tab.isTabEnabled(0):
           self.ui.textBrowser.setText("Tab 1")
        elif self.ui.info_tab.isTabEnabled(1):
           self.ui.textBrowser_3.setText("Tab 2")
        else:
           self.ui.textBrowser_2.setText("Tab 3")

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())