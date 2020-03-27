import time
from PyQt5 import QtCore, QtGui, QtWidgets
from song_analyzer import get_lyrics_from_AZwebsite, get_song_metadata, analyze_emotion

# Window class which will be imported in the main.py file. This sets up the GUI elements and handles the button clicks
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(682, 723)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("background-color: hsl(55,45%,90%);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.artist_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.artist_edit.setObjectName("artist_edit")
        self.gridLayout.addWidget(self.artist_edit, 1, 2, 1, 1)
        self.info_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.info_tab.setObjectName("info_tab")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_5)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.info_tab.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_6)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.horizontalLayout_3.addWidget(self.textBrowser_3)
        self.info_tab.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_7)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_2.addWidget(self.textBrowser_2)
        self.info_tab.addTab(self.tab_7, "")
        self.gridLayout.addWidget(self.info_tab, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.song_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.song_edit.setObjectName("song_edit")
        self.song_edit.setFocus()
        self.gridLayout.addWidget(self.song_edit, 0, 2, 1, 1)
        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setStyleSheet("background-color:#ffffff;\n"
"\n"
"\n"
"")
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.clicked.connect(self.analyze_clicked)
        self.gridLayout.addWidget(self.analyze_button, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 21))
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.info_tab.setCurrentIndex(0)
        self.results = []
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Song Name:</span></p></body></html>"))
        self.info_tab.setTabText(self.info_tab.indexOf(self.tab_5), _translate("MainWindow", "Lyrics"))
        self.info_tab.setTabText(self.info_tab.indexOf(self.tab_6), _translate("MainWindow", "Analysis"))
        self.info_tab.setTabText(self.info_tab.indexOf(self.tab_7), _translate("MainWindow", "Metadata"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Artist:</span></p></body></html>"))
        self.analyze_button.setText(_translate("MainWindow", "Analyze"))

    """
        Trying to make the function analyze_clicked faster by using threads so it doesn't block the main thread.

        After using the time.time() function to time the three functions used (and subtracting the variables to find the wall time 
        elapsed for the functions), the synchronous approach has given the following results:
        This is depending on how heavy the song lyrics are, but for colt 45 by afroman 
        lyrics_func = 0.7155203819274902 seconds
        emotion_func = 6.410402536392212 seconds 
        metadata_func = 1.3229737281799316 seconds 

        The multithreaded version gives these results on avergae:
        lyrics_func = 0.7155203819274902 seconds
        emotion_func = 4.743182182312012 seconds 
        metadata_func = 2.018028736114502 seconds 

    """

    # The results list holds results from the three functions used. I have created a new thread for analyze_emotion and 
    # get_song_metadata to reduce the time taken. The event handlers emotion_result and meta_result are connected to their 
    # respective signals, which are created in the classes EmotionThread and MetaThread. I use a final finished handler because 
    # the EmotionThread takes the longest to run, and I want to display all results at once.  
    
    def analyze_clicked(self):
        self.results = []
        song_name = self.song_edit.text() 
        artist_name = self.artist_edit.text()
        start1 = time.time()
        lyrics = get_lyrics_from_AZwebsite(artist_name, song_name)
        end1 = time.time()
        print("lyr_func = ", (end1 - start1), "\n")        
        self.emotion_function_thread = EmotionThread(lyrics)
        self.emotion_function_thread.start()
        self.emotion_function_thread.output.connect(self.emotion_result)
        self.emotion_function_thread.finished.connect(self.emotion_thread_finished)
        self.meta_function_thread = MetaThread(artist_name, song_name)
        self.meta_function_thread.output.connect(self.meta_result)
        self.meta_function_thread.start()
        self.results.append(lyrics)
    
    def emotion_result(self, text2):
        self.results.append(text2)

    def meta_result(self, text3):
        self.results.append(text3)

    def emotion_thread_finished(self):
        self.textBrowser.setText(self.results[0])
        self.textBrowser_2.setText(self.results[1])
        self.textBrowser_3.setText(self.results[2])


class EmotionThread(QtCore.QThread):
    
    output = QtCore.pyqtSignal('PyQt_PyObject')
    def __init__(self, lyrics, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.lyrics = lyrics 
    
    def run(self):
        start2 = time.time()
        emotion = analyze_emotion(self.lyrics)
        end2 = time.time()
        print("em_func = ", (end2 - start2), "\n")
        self.output.emit(emotion)

class MetaThread(QtCore.QThread):
    
    output = QtCore.pyqtSignal('PyQt_PyObject')
    def __init__(self, artist, song, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.artist_name = artist
        self.song_name = song 
    
    def run(self):
        start3 = time.time()
        meta = get_song_metadata(self.artist_name, self.song_name)
        end3 = time.time()
        print("met_func = ", (end3 - start3), "\n")
        self.output.emit(meta)


    
        
            
       
  