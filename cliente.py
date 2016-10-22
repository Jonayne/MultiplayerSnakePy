#Código para mostrar nuestro Cliente para el juego de Snake, poder participar con otros jugadores.
#By Jonayne.  \( ͡° ͜ʖ ͡°)/ 

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from xmlrpc.client import ServerProxy

#Aquí lo cargamos.
cliente_gui = uic.loadUiType("cliente.ui")[0]

#Cliente de un juego de snake.
class Cliente(QtGui.QMainWindow, cliente_gui):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		#En las siguientes 5 lineas hacemos que las celdas de la TableWidget se adapten al tamaño de esta. 
		self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.verticalHeader().setStretchLastSection(True)
		self.label_3.hide()
		self.url_server= "http://" + self.lineEdit.text() + ":" + str(self.spinBox_4.value())
		self.server = ServerProxy(self.url_server)
		self.pushButton_2.clicked.connect(self.pingea)
		self.pushButton.clicked.connect(self.participa)
		self.tableWidget.keyPressEvent= self.keyPressEvent
		self.timer= QTimer(self)
		self.ant_coords= None
		self.primera_vez= False
		self.timer.timeout.connect(self.actualiza_juego)
		self.ms= self.server.estado_del_juego()["espera"]
		self.timer.start(self.ms)
		self.dire= 2
		
	#Método que actualiza el estado de el cliente, acorde al servidor. (Cambia lineas/columnas y dibuja a las víboras)
	def actualiza_juego(self):
			info= self.server.estado_del_juego()
			if info["espera"] != self.ms:
				self.ms= info["espera"]
				self.timer.setInterval(self.ms)
			if info["tamX"] != self.tableWidget.columnCount():
				self.tableWidget.setColumnCount(info["tamX"])
			if info["tamY"] != self.tableWidget.rowCount():
				self.tableWidget.setRowCount(info["tamY"])
			if self.primera_vez:
				if not self.esta_viva(info["viboras"]):
					self.label_3.show()
					self.lineEdit_2.setText("")
					self.lineEdit_3.setText("")
					self.pushButton.show()
					self.primera_vez= False
					self.dire= 2

			self.borra_viboras(self.ant_coords)
			self.dibuja_viboras(info["viboras"])
			self.ant_coords= info["viboras"]

	#Método que nos dice si la víbora de este cliente ya ha perdido.
	def esta_viva(self, lista_vibs):
		for vibora in lista_vibs:
			if vibora["id"] == self.lineEdit_2.text():
				return True
		return False

	#Método que se encarga de mandar a dibujar cada una de las serpientes del juego.
	def dibuja_viboras(self, info_vibs):
		for vibora in info_vibs:
			self.dibuja_vibora(vibora["camino"], vibora["color"])

	#Método que se encarga de mandar a borrar cada una de las serpientes del juego.
	def borra_viboras(self, info_vibs):
		if info_vibs == None: return
		for vibora in info_vibs:
			self.borra_vibora(vibora["camino"])

	#Método que se encarga de borrar una víbora en ciertas coordenadas.
	def borra_vibora(self, coords):
		self.tableWidget.takeItem(coords[8], coords[9])
		self.tableWidget.takeItem(coords[6], coords[7])
		self.tableWidget.takeItem(coords[4], coords[5])
		self.tableWidget.takeItem(coords[2], coords[3])
		self.tableWidget.takeItem(coords[0], coords[1])

	#Método que se encarga de dibujar a una víbora según sus coordenadas.
	def dibuja_vibora(self, coords, color):
		c1, c2, c3, c4, c5= QTableWidgetItem() , QTableWidgetItem() , QTableWidgetItem() , QTableWidgetItem() , QTableWidgetItem()
		c1.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		c2.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		c3.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		c4.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		c5.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.tableWidget.setItem(coords[8], coords[9], c1)
		self.tableWidget.setItem(coords[6], coords[7], c2)
		self.tableWidget.setItem(coords[4], coords[5], c3)
		self.tableWidget.setItem(coords[2], coords[3], c4)
		self.tableWidget.setItem(coords[0], coords[1], c5)

	#Método que te ingresa a la partida de snake.
	def participa(self):
			dic= self.server.yo_juego()
			
			self.label_3.hide()
			self.primera_vez= True
			self.lineEdit_2.setText(dic["id"])
			self.lineEdit_3.setText(str(dic["color"]["r"]) + "  " + str(dic["color"]["g"]) + "  " + str(dic["color"]["b"]))

	#Método que PING pero PONG.
	def pingea(self):
		self.pushButton_2.setText("Pinging...")
		try:
			pong= self.server.ping()
			self.pushButton_2.setText("¡Pong!")
		except:
			self.pushButton_2.setText("No PONG :(")

	#Overwrite de el método keyPressEvent para detectar cuando movemos a nuestra serpiente.
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Left and self.dire != 1: #Si se movió a la izq.
			self.server.cambia_direccion(self.lineEdit_2.text(), 3)
			self.dire= 3
		elif event.key() == QtCore.Qt.Key_Right and self.dire != 3: #Si se movió a la derecha.
			self.server.cambia_direccion(self.lineEdit_2.text(), 1)
			self.dire= 1
		elif event.key() == QtCore.Qt.Key_Down and self.dire != 0: #Si se movió abajo.
			self.server.cambia_direccion(self.lineEdit_2.text(), 2)
			self.dire= 2
		elif event.key() == QtCore.Qt.Key_Up and self.dire != 2: #Si se movió a arriba.
			self.server.cambia_direccion(self.lineEdit_2.text(), 0)
			self.dire= 0

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	ventana = Cliente(None)
	ventana.show()
	app.exec_()
#  \( ͡° ͜ʖ ͡°)/ 