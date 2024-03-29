# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Organo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import MidiToHeader
from midi2audio import FluidSynth
import subprocess
import pyduinocli

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Interface Layout Setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 458)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/GranaSAT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, -1, -1, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathToSong = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.pathToSong.sizePolicy().hasHeightForWidth())
        self.pathToSong.setSizePolicy(sizePolicy)
        self.pathToSong.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pathToSong.setToolTip("")
        self.pathToSong.setWhatsThis("")
        self.pathToSong.setAccessibleName("")
        self.pathToSong.setAccessibleDescription("")
        self.pathToSong.setStyleSheet("")
        self.pathToSong.setTabChangesFocus(True)
        self.pathToSong.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.pathToSong.setAcceptRichText(False)
        self.pathToSong.setObjectName("pathToSong")
        self.horizontalLayout.addWidget(self.pathToSong)
        self.pathToSongButton = QtWidgets.QPushButton(self.centralwidget)
        self.pathToSongButton.setToolTip("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/Carpeta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pathToSongButton.setIcon(icon1)
        self.pathToSongButton.setObjectName("pathToSongButton")
        self.horizontalLayout.addWidget(self.pathToSongButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.songListTitle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.songListTitle.setFont(font)
        self.songListTitle.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.songListTitle.setObjectName("songListTitle")
        self.verticalLayout_2.addWidget(self.songListTitle)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(50, -1, 50, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setMinimumSize(QtCore.QSize(0, 30))
        self.saveButton.setToolTip("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/Guardar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setMinimumSize(QtCore.QSize(0, 30))
        self.deleteButton.setToolTip("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/Eliminar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon3)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.compileButton = QtWidgets.QPushButton(self.centralwidget)
        self.compileButton.setMinimumSize(QtCore.QSize(0, 30))
        self.compileButton.setToolTip("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/Subir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.compileButton.setIcon(icon4)
        self.compileButton.setObjectName("compileButton")
        self.verticalLayout.addWidget(self.compileButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        self.selectMenu = QtWidgets.QMenu(self.menuBar)
        self.selectMenu.setObjectName("selectMenu")
        self.menuSeleccionArduino = QtWidgets.QMenu(self.selectMenu)
        self.menuSeleccionArduino.setObjectName("menuSeleccionArduino")
        MainWindow.setMenuBar(self.menuBar)
        self.actionBuscarSD = QtWidgets.QAction(MainWindow)
        self.actionBuscarSD.setObjectName("actionBuscarSD")
        self.selectMenu.addAction(self.actionBuscarSD)
        self.selectMenu.addAction(self.menuSeleccionArduino.menuAction())
        self.menuBar.addAction(self.selectMenu.menuAction())
        
        #Interface text setup
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #Interface logic setup
        self.savedPort = ""
        self.sdPath = ""
        self.arduino = pyduinocli.Arduino("./arduino-cli")
        self.actionBuscarSD.triggered.connect(self.searchSD)
        self.pathToSongButton.clicked.connect(self.searchMIDI)
        self.saveButton.clicked.connect(self.saveSong)
        self.deleteButton.clicked.connect(self.deleteSong)
        self.compileButton.clicked.connect(self.compileCode)
        self.menuSeleccionArduino.aboutToShow.connect(self.searchArduino)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Organo de luces"))
        self.pathToSong.setStatusTip(_translate("MainWindow", "Escribe aqui la ruta de la canción en formato MIDI"))
        self.pathToSong.setPlaceholderText(_translate("MainWindow", "/MIDI/Canción.mid"))
        self.pathToSongButton.setStatusTip(_translate("MainWindow", "Buscar la canción en el explorador"))
        self.pathToSongButton.setText(_translate("MainWindow", "Explorar Archivos"))
        self.songListTitle.setText(_translate("MainWindow", "Lista de canciones"))
        self.listWidget.setStatusTip(_translate("MainWindow", "Lista de canciones en la tarjeta SD"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Tarjeta SD no seleccionada"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.saveButton.setStatusTip(_translate("MainWindow", "Guardar la canción seleccionada a la tarjeta SD y en el código"))
        self.saveButton.setText(_translate("MainWindow", "Guardar Canción"))
        self.deleteButton.setStatusTip(_translate("MainWindow", "Eliminar la canción de la lista y el código"))
        self.deleteButton.setText(_translate("MainWindow", "Eliminar Canción"))
        self.compileButton.setStatusTip(_translate("MainWindow", "Compilar el código del organo en la placa"))
        self.compileButton.setText(_translate("MainWindow", "Compilar el código"))
        self.selectMenu.setTitle(_translate("MainWindow", "Seleccionar"))
        self.menuSeleccionArduino.setTitle(_translate("MainWindow", "Seleccion Arduino"))
        self.actionBuscarSD.setText(_translate("MainWindow", "Buscar SD"))
        
    #Se encarga de seleccionar la placa Arduino en la que compilar el código
    def searchArduino(self):
        
        brds = self.arduino.board.list()
        
        ports = []
        
        for i in brds["result"]:
            ports.append(i["port"]["address"])
        
        self.menuSeleccionArduino.clear()
        if (len(ports) != 0):
            for i in ports:
                self.menuSeleccionArduino.addAction(str(i))
            self.menuSeleccionArduino.triggered.connect(lambda action: self.savePort(action))
            
        else:
            self.Vacio = QtWidgets.QAction(MainWindow)
            self.Vacio.setEnabled(False)
            self.Vacio.setObjectName("Vacio")
            self.Vacio.setText("Vacio")
            self.menuSeleccionArduino.addAction(self.Vacio)
        
        return
    
    
    def savePort(self,port):
        self.savedPort = port.text()
        
        
        msg = QtWidgets.QMessageBox()
        msg.setText("Se utilizara el puerto: {}".format(port.text()))
        msg.setWindowTitle("Puerto Establecido")
        msg.exec_()
        
        return
    
    #Permite encontrar la raiz de la tarjeta SD en la que se almacenara la música
    def searchSD(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget,"Selecciona la raiz de la SD",".")
        self.sdPath = path
        self.openSD()
        
        return
    
    #Carga el directorio de la sd en la lista de canciones
    def openSD(self):
        self.listWidget.clear()
        MP3s = os.listdir(self.sdPath)
        for i in MP3s:
            if i.find(".mp3") != -1:
                item = QtWidgets.QListWidgetItem(i)
                self.listWidget.addItem(item)
        return
    
    #Busca la ruta del archivo MIDI
    def searchMIDI(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,"Selecciona el archivo MIDI",".","Archivos Midi (*.mid)")
        if fileName:
            self.pathToSong.setText(fileName)
    
    #Una vez seleccionado el MIDI y la SD, se guarda la canción tanto la SD como en el header
    def saveSong(self):
        
        msg = QtWidgets.QMessageBox()
        if (self.sdPath == ""):
            #Error, no hay tarjeta  (WIP)
            msg.setText("Error: No se ha seleccionado una ruta para la tarjeta SD")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        elif(not self.pathToSong.toPlainText().endswith(".mid")):
            #Error, el archivo seleccionado no es un midi (WIP)
            msg.setText("Error: El archivo seleccionado no es un MIDI")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        else:
            #Convertimos el archivo MIDI a MP3 con la nomenclatura correcta y lo guardamos en la SD    
            MIDI = self.pathToSong.toPlainText()
            title = "Song_{number}_{name}".format(number = self.listWidget.count()+1,name = MIDI.split("/")[-1][:-4] + ".mp3")
            out = self.sdPath +"/" + title 
            subprocess.call(["fluidsynth","-ni","soundfont.sf2",MIDI,"-F",out,"-r","44100"])
        
            #Convertimos el archivo MIDI para poder añadirlo a la cabecera del documento
                
            #Si no existe cabecera la creamos
            if not os.path.exists("musiclights.h"):
                MidiToHeader.construct_header()
            
            #Añadimos el archivo al header
            MidiToHeader.add_midi(self.pathToSong.toPlainText(), self.listWidget.count()+1)
            
            #Finalmente añadimos la canción a la lista
            self.openSD()
            
            
        return
    
    def deleteSong(self):
        
        selected = self.listWidget.selectedItems()
        


        msg = QtWidgets.QMessageBox()
        if (selected and self.sdPath != ""):
            selected_number = int(selected[0].text().split("_")[1])
            
            #Eliminar de la SD
            for i in os.listdir(self.sdPath):
                j = int(i.split("_")[1])
                if j==selected_number:
                    os.remove(self.sdPath+"/"+i)
                elif j> selected_number:
                    new_name = "Song_{}{}".format(j-1,i[6:])
                    os.rename(self.sdPath+"/"+i,self.sdPath+"/"+new_name)
            
            #Eliminar del header
            MidiToHeader.delete_song_from_header(selected_number)
            
            #Actualizar la lista
            self.openSD()
        else:
            if (self.sdPath == ""):
                msg.setText("Error: No se ha seleccionado una ruta para la tarjeta SD")
                msg.setWindowTitle("Error")
                msg.exec_()
            elif (not selected):
                msg.setText("Error: No se ha seleccionado ninguna canción")
                msg.setWindowTitle("Error")
                msg.exec_()

        return
    
    def compileCode(self):
        
        
        msg = QtWidgets.QMessageBox()
        if (self.savedPort != ""):
            
            brds = self.arduino.board.list()
            
            exists = False
            for i in brds["result"]:
                if (self.savedPort == i["port"]["address"]):
                    exists = True
                    if "matching boards" in i:
                        fqbn = i["matching boards"][0]["fqbn"]
                    else:
                        fqbn = "arduino:avr:uno"
            
            #Si el saved port existe:
            if (exists):
                
                
                
                self.arduino.compile(fqbn=fqbn,sketch="project_granasat.ino")
                self.arduino.upload(fqbn=fqbn, sketch="project_granasat.ino", port=self.savedPort)
                
                msg.setText("La compilación ha terminada")
                msg.setWindowTitle("Compilación terminada")
                msg.exec_()
            #En caso contrario, salta una excepción
            else:
                msg.setText("Error: El puerto seleccionado no esta disponible, intentelo de nuevo o seleccione un nuevo puerto")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg.setText("Error: No hay puerto Arduino seleccionado")
            msg.setWindowTitle("Error")
            msg.exec_()
        
        
        return
    
    
import Images_qr

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

