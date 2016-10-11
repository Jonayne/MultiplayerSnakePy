#Código para mostrar la interfaz gráfica de nuestro Servidor (y empezar juego de Snake).
#Escrito por Jonayne :).
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Cargamos la interfaz gráfica hecha con QtDesigner.
servidor_gui = uic.loadUiType("servidor.ui")[0]

#Clase que muestra como se comportará nuestro Servidor (por lo menos el movimiento de la víbora, etc.)
class Servidor(QtGui.QMainWindow, servidor_gui):

	#Método que aumenta las columnas de nuestra TableWidget
	def modificaColumnas(self, m):
		self.tableWidget.setColumnCount(m)

	#Método que aumenta las lineas de nuestra TableWidget
	def modificaLineas(self, n):
		self.tableWidget.setRowCount(n)

	#Método que empieza el juego, poniendo la vibora en la TableWidget, iniciando el timer, poniendo la opción de terminar el juego, etc.
	def empiezaJuego(self):
		if self.pushButton_2.text() == "INICIA JUEGO" or self.pushButton_2.text() == "INICIAR OTRA PARTIDA":
			self.label_9.hide()
			self.pushButton_2.setText("PAUSAR JUEGO")
			self.vibora_1, self.vibora_2, self.vibora_3, self.vibora_4, self.vibora_5= QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem()
			self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= 4, 0, 3, 0, 2, 0, 1, 0, 0, 0
			self.vibora_1.setBackground(QtGui.QColor(200,100,100))
			self.vibora_2.setBackground(QtGui.QColor(200,100,100))
			self.vibora_3.setBackground(QtGui.QColor(200,100,100))
			self.vibora_4.setBackground(QtGui.QColor(200,100,100))
			self.vibora_5.setBackground(QtGui.QColor(200,100,100))
			self.tableWidget.setItem(self.coordX5, self.coordY5, self.vibora_5)
			self.tableWidget.setItem(self.coordX4, self.coordY4, self.vibora_4)
			self.tableWidget.setItem(self.coordX3, self.coordY3, self.vibora_3)
			self.tableWidget.setItem(self.coordX2, self.coordY2, self.vibora_2)
			self.tableWidget.setItem(self.coordX1, self.coordY1, self.vibora_1)
			self.timer= QTimer(self)
			self.timer.timeout.connect(self.handle)
			self.timer.start(100)
		elif self.pushButton_2.text() == "PAUSAR JUEGO":
			self.pushButton_2.setText("REAUNUDAR EL JUEGO")
			self.timer.stop()
		else:
			self.pushButton_2.setText("PAUSAR JUEGO")
			self.timer.start()

	#Método que se encarga de actualizar las coordenadas según la dirección se haya movido la víbora.
	def actualizaCoords(self, direccion):
		if direccion == "IZQUIERDA": #Cambia las coordenadas si nos movemos hacia la izquierda.
			if self.coordY1 == 0:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1, self.tableWidget.columnCount()-1 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
			else:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1, self.coordY1 - 1 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
		elif direccion == "DERECHA": #Cambia las coordenadas si nos movemos hacia la derecha.
			if self.coordY1 == self.tableWidget.columnCount()-1:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1, 0 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
			else:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1, self.coordY1 + 1 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
		elif direccion == "ARRIBA": #Cambia las coordenadas si nos movemos para arriba.
			if self.coordX1 == 0:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.tableWidget.rowCount()-1, self.coordY1 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
			else:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1 - 1, self.coordY1, self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
		else: #Cambia las coordenadas si nos movemos para abajo.
			if self.coordX1 == self.tableWidget.rowCount()-1:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= 0, self.coordY1 , self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4
			else:
				self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4, self.coordX5, self.coordY5= self.coordX1 + 1 , self.coordY1, self.coordX1, self.coordY1, self.coordX2, self.coordY2, self.coordX3, self.coordY3, self.coordX4, self.coordY4

	#Método que acaba el juego, quitando las serpientes y parando el timer.
	def terminaJuego(self):
		self.tableWidget.takeItem(self.coordX5, self.coordY5)
		self.tableWidget.takeItem(self.coordX4, self.coordY4)
		self.tableWidget.takeItem(self.coordX3, self.coordY3)
		self.tableWidget.takeItem(self.coordX2, self.coordY2)
		self.tableWidget.takeItem(self.coordX1, self.coordY1)
		self.timer.stop()
		self.pushButton_2.setText("INICIAR OTRA PARTIDA")
		self.label_9.show()

	#Método que revisa si la serpiente ya ha chocado con ella misma (i.e, que siga viva)
	def estaViva(self):
		return not(self.coordX1 == self.coordX5 and self.coordY1 == self.coordY5)

	#Método que actualiza la posición de la víbora en la TableWidget
	def actualizaPosicion(self):
		self.vibora_1, self.vibora_2, self.vibora_3, self.vibora_4, self.vibora_5= QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem()
		self.vibora_1.setBackground(QtGui.QColor(200,100,100))
		self.vibora_2.setBackground(QtGui.QColor(200,100,100))
		self.vibora_3.setBackground(QtGui.QColor(200,100,100))
		self.vibora_4.setBackground(QtGui.QColor(200,100,100))
		self.vibora_5.setBackground(QtGui.QColor(200,100,100))
		self.tableWidget.setItem(self.coordX5, self.coordY5, self.vibora_5)
		self.tableWidget.setItem(self.coordX4, self.coordY4, self.vibora_4)
		self.tableWidget.setItem(self.coordX3, self.coordY3, self.vibora_3)
		self.tableWidget.setItem(self.coordX2, self.coordY2, self.vibora_2)
		self.tableWidget.setItem(self.coordX1, self.coordY1, self.vibora_1)

	#Método que quita la víbora de la tableWidget (ya sea para después moverla a otra posición después, o para finalizar el juego)
	def remuevePosicion(self):
		self.tableWidget.takeItem(self.coordX5, self.coordY5)
		self.tableWidget.takeItem(self.coordX4, self.coordY4)
		self.tableWidget.takeItem(self.coordX3, self.coordY3)
		self.tableWidget.takeItem(self.coordX2, self.coordY2)
		self.tableWidget.takeItem(self.coordX1, self.coordY1)

	#Métodos que mueven a la víbora a esa dirección.
	def mueveAIzq(self):
		self.remuevePosicion()
		self.actualizaCoords("IZQUIERDA")
		self.actualizaPosicion()
	def mueveADer(self):
		self.remuevePosicion()
		self.actualizaCoords("DERECHA")
		self.actualizaPosicion()
	def mueveAU(self):
		self.remuevePosicion()
		self.actualizaCoords("ARRIBA")
		self.actualizaPosicion()
	def mueveAD(self):
		self.remuevePosicion()
		self.actualizaCoords("ABAJO")
		self.actualizaPosicion()

	#Overwrite de el método keyPressEvent para detectar cuando movemos a nuestra serpiente.
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Left and not self.derecha: #Si se movió a la izq.
			self.arriba, self.abajo, self.derecha, self.izquierda= False, False, False, True
		elif event.key() == QtCore.Qt.Key_Right and not self.izquierda: #Si se movió a la derecha.
			self.arriba, self.abajo, self.derecha, self.izquierda= False, False, True, False
		elif event.key() == QtCore.Qt.Key_Down and not self.arriba: #Si se movió abajo.
			self.arriba, self.abajo, self.derecha, self.izquierda= False, True, False, False
		elif event.key() == QtCore.Qt.Key_Up and not self.abajo: #Si se movió a arriba.
			self.arriba, self.abajo, self.derecha, self.izquierda= True, False, False, False

	#Método que se manda a llamar cada vez que se actualiza el juego, viendo en que dirección se tiene que mover la víbora y mandando a llamar al método correspondiente..
	def handle(self):
		if self.arriba:
			self.mueveAU()
		elif self.izquierda:
			self.mueveAIzq()
		elif self.derecha:
			self.mueveADer()
		else:
			self.mueveAD()
		if not self.estaViva():
			self.terminaJuego()
			self.pushButton_3.hide()
			

	#Método que cambia los milisegundos que tarda en actualizarse el juego.
	def cambiaMS(self, n):
		self.timer.setInterval(n)

	#Constructor de el Juego de Snake (SERVIDOR)
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.pushButton_3.hide()
		self.arriba, self.abajo, self.derecha, self.izquierda= False, False, False, False
		#acá hacemos que las celdas se adapten al tamaño de la TableWidget.
		self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch)
		#Hacemos que se aumente/disminuya el tamaño de la TableWidget según los spinBox.
		self.spinBox.valueChanged.connect(self.modificaColumnas)
		self.spinBox_2.valueChanged.connect(self.modificaLineas)
		self.spinBox_3.valueChanged.connect(self.cambiaMS)
		self.pushButton_2.clicked.connect(self.empiezaJuego)
		self.pushButton_3.clicked.connect(self.terminaJuego)
		self.label_9.hide()
		self.tableWidget.keyPressEvent= self.keyPressEvent
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	ventana = Servidor(None)
	ventana.show() #Iniciamos el Juego!
	app.exec_()