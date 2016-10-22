#Código para mostrar la interfaz gráfica de nuestro Servidor, poder iniciarlo, entre otras cosas.
#By Jonayne  \( ͡° ͜ʖ ͡°)/ 

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from xmlrpc.server import SimpleXMLRPCServer
import random
import uuid

#Cargamos la interfaz gráfica hecha con QtDesigner.
servidor_ui = uic.loadUiType("servidor.ui")[0]

#Clase que muestra como se comportará nuestro Servidor (por lo menos el movimiento de la víbora, etc.)
class Servidor(QtGui.QMainWindow, servidor_ui):

	#Método que aumenta las columnas de nuestra TableWidget
	def modifica_columnas(self, m):
		self.tableWidget.setColumnCount(m)

	#Método que aumenta las lineas de nuestra TableWidget
	def modifica_lineas(self, n):
		self.tableWidget.setRowCount(n)

	#Método que empieza el juego, poniendo la vibora en la TableWidget, iniciando el timer, poniendo la opción de terminar el juego, etc.
	def empieza_juego(self):
		if self.pushButton_2.text() == "INICIA JUEGO" or self.pushButton_2.text() == "INICIAR OTRA PARTIDA":
			self.label_9.hide()
			self.pushButton_2.setText("PAUSAR JUEGO")
			self.timer= QTimer(self)
			self.timer.timeout.connect(self.handle)
			self.timer.start(100)
		elif self.pushButton_2.text() == "PAUSAR JUEGO":
			self.pushButton_2.setText("REAUNUDAR EL JUEGO")
			self.timer.stop()
		else:
			self.pushButton_2.setText("PAUSAR JUEGO")
			self.timer.start()

	#Método importantísimo que crea una nueva víbora en el juego, añadiendola a dos listas, una donde está la víbora en sí, y otra en dónde está la información de esta.
	def crea_vibora(self):
		color= self.crea_color_random()
		coords= self.asigna_coordenadas_random()
		identificador= self.asigna_identificador()
		nueva_vibora= Vibora(identificador, color, coords, 2) #Se mueve para abajo por defecto (por eso el 2).
		self.lista_viboras.append({"id": identificador, "camino": coords, "color": color})
		self.viboras_ingame.append(nueva_vibora)
		self.dibuja_vibora(nueva_vibora)

		return nueva_vibora

	#Método que se encarga de generar un color de forma aleatoria.
	def crea_color_random(self):
		r= random.randint(0, 255)
		g= random.randint(0, 255)
		b= random.randint(0, 255)

		return [r, g, b]

	#Método que se encarga de generar coordenadas aleatorias para una víbora.
	def asigna_coordenadas_random(self):
		cabezaY= random.randint(0, self.tableWidget.columnCount())
		cabezaX= random.randint(0, self.tableWidget.rowCount())
		cuerpo1X, cuerpo1Y, cuerpo2X, cuerpo2Y, cuerpo3X, cuerpo3Y, colaX, colaY= (cabezaX -1) % self.tableWidget.rowCount(), cabezaY, (cabezaX -2) % self.tableWidget.rowCount(), cabezaY, (cabezaX -3) % self.tableWidget.rowCount(), cabezaY, (cabezaX -4) % self.tableWidget.rowCount(), cabezaY

		return [cabezaX, cabezaY, cuerpo1X, cuerpo1Y, cuerpo2X, cuerpo2Y, cuerpo3X, cuerpo3Y, colaX, colaY]

	#Método que se encarga de dibujar a una víbora según sus coordenadas.
	def dibuja_vibora(self, vibora):
		self.tableWidget.setItem(vibora.coordenadas[8], vibora.coordenadas[9], vibora.cola)
		self.tableWidget.setItem(vibora.coordenadas[6], vibora.coordenadas[7], vibora.cuerpo3)
		self.tableWidget.setItem(vibora.coordenadas[4], vibora.coordenadas[5], vibora.cuerpo2)
		self.tableWidget.setItem(vibora.coordenadas[2], vibora.coordenadas[3], vibora.cuerpo1)
		self.tableWidget.setItem(vibora.coordenadas[0], vibora.coordenadas[1], vibora.cabeza)

	#Método que se encarga de generar un ID de forma aleatoria.
	def asigna_identificador(self):
		return str(uuid.uuid4())

	#Método que se encarga de borrar a una víbora del TablwWidget.
	def borra_vibora(self, vibora):
		self.tableWidget.takeItem(vibora.coordenadas[8], vibora.coordenadas[9])
		self.tableWidget.takeItem(vibora.coordenadas[6], vibora.coordenadas[7])
		self.tableWidget.takeItem(vibora.coordenadas[4], vibora.coordenadas[5])
		self.tableWidget.takeItem(vibora.coordenadas[2], vibora.coordenadas[3])
		self.tableWidget.takeItem(vibora.coordenadas[0], vibora.coordenadas[1])

	#Método que acaba el juego, quitando las serpientes y parando el timer.
	def vibora_ha_perdido(self, vibora):
		self.borra_vibora(vibora)
		for x in self.lista_viboras:
			if vibora.id == x["id"]:
				self.lista_viboras.remove(x)
				break
		self.viboras_ingame.remove(vibora)

	#Método que revisa si la serpiente ya ha chocado con ella misma (i.e, que siga viva)
	def esta_viva(self, vibora):
		return not((vibora.coordenadas[0] == vibora.coordenadas[8] and vibora.coordenadas[1] == vibora.coordenadas[9]) or self.ha_chocado(vibora))

	#Método que determina si una víbora ha chocado con alguna otra, i.e, ha perdido.
	def ha_chocado(self, vibora):
		cabeza= [vibora.coordenadas[0], vibora.coordenadas[1]]
		idd= vibora.id
		for otra_vib in self.lista_viboras:
			for i in range(9):
				if idd != otra_vib["id"] and cabeza[0] == otra_vib["camino"][i] and cabeza[1] == otra_vib["camino"][i+1]:
					return True
				i+=1
		return False
	
	#Métodos que mueven a la víbora a esa dirección.
	def mueve_a_izq(self, vibora):
		self.borra_vibora(vibora)
		vibora.actualiza_coords(3, self.tableWidget.columnCount(), self.tableWidget.rowCount())
		self.actualiza_coords_lista_vib()
		vibora.direccion= 3
		vibora.recrea_items()
		self.dibuja_vibora(vibora)
	def mueve_a_der(self, vibora):
		self.borra_vibora(vibora)
		vibora.actualiza_coords(1, self.tableWidget.columnCount(), self.tableWidget.rowCount())
		self.actualiza_coords_lista_vib()
		vibora.direccion= 1
		vibora.recrea_items()
		self.dibuja_vibora(vibora)
	def mueve_a_up(self, vibora):
		self.borra_vibora(vibora)
		vibora.actualiza_coords(0, self.tableWidget.columnCount(), self.tableWidget.rowCount())
		self.actualiza_coords_lista_vib()
		vibora.direccion= 0
		vibora.recrea_items()
		self.dibuja_vibora(vibora)
	def mueve_a_do(self, vibora):
		self.borra_vibora(vibora)
		vibora.actualiza_coords(2, self.tableWidget.columnCount(), self.tableWidget.rowCount())
		self.actualiza_coords_lista_vib()
		vibora.direccion= 2
		vibora.recrea_items()
		self.dibuja_vibora(vibora)

	#Método que se manda a llamar cada vez que se actualiza el juego, viendo en que dirección se tiene que mover la víbora y mandando a llamar al método correspondiente..
	def handle(self):
		for vibora in self.viboras_ingame:
			if vibora.direccion == 0:
				self.mueve_a_up(vibora)
			elif vibora.direccion == 3:
				self.mueve_a_izq(vibora)
			elif vibora.direccion == 1:
				self.mueve_a_der(vibora)
			else:
				self.mueve_a_do(vibora)
			if not self.esta_viva(vibora):
				self.vibora_ha_perdido(vibora)

	#Método que se encarga de buscar a una víbora por su ID, la regresa si esta está, sino, regresa None.
	def dame_vibora_por_id(self, idd):
		for x in self.viboras_ingame:
			if x.id == idd:
				return x

	#Método que actualiza las coordenadas de todas las serpientes que se encuentran en el servidor.
	def actualiza_coords_lista_vib(self):
		i= 0
		for vib in self.lista_viboras:
			vib["camino"] = self.viboras_ingame[i].coordenadas
			i+=1

	#Método que inicia un servidor, con sus funciones correspondientes.
	def inicia_servidor(self):
		if self.spinBox_4.value() == 0:
			self.spinBox_4.setValue(8000)
		self.servidor= SimpleXMLRPCServer((self.lineEdit.text() , self.spinBox_4.value()), allow_none= True)
		self.servidor.timeout= self.doubleSpinBox.value()
		self.servidor.register_function(self.ping)
		self.servidor.register_function(self.yo_juego)
		self.servidor.register_function(self.estado_del_juego)
		self.servidor.register_function(self.cambia_direccion)
		self.timer_server= QTimer(self)
		self.timer_server.timeout.connect(self.escucha_cliente)
		self.timer_server.start(100)
		self.pushButton.hide()

	#Función que se encarga de escuchar y trabajar peticiones que le lleguen al servidor.
	def escucha_cliente(self):
		self.servidor.handle_request()

	#Método que PING pero PONG.
	def ping(self):
			return "¡Pong!"

	#Método que crea una nueva víbora y regresa información de esta.
	def yo_juego(self):
		nueva_vib= self.crea_vibora()
		return {"id": nueva_vib.id, "color": {"r": nueva_vib.color[0], "g": nueva_vib.color[1], "b": nueva_vib.color[2]}}

	#Método que cambia la dirección de una víbora sí y sólo sí esta se encuentra en el tablero.
	def cambia_direccion(self, idd, dir):
		for x in self.lista_viboras:
			if idd == x["id"]:
				vib= self.dame_vibora_por_id(idd)
				vib.direccion = dir
				break

	def termina_partida(self):
		self.tableWidget.clear()
		self.lista_viboras.clear()
		self.viboras_ingame.clear()
		self.pushButton_3.hide()
		self.pushButton_2.setText("INICIAR OTRA PARTIDA")

	#Método que se encarga de regresar información importante sobre el juego, las víboras que contiene, tamaño del TableWidget, etc.
	def estado_del_juego(self):
		return {"espera": self.spinBox_3.value(), "tamX": self.tableWidget.columnCount(), "tamY": self.tableWidget.rowCount(), "viboras": self.lista_viboras}

	#Método que cambia los milisegundos que tarda en actualizarse el juego.
	def cambia_ms(self, n):
		self.timer.setInterval(n)

	#Método que cambia el timeout de nuestro servidor según la doubleSpinBox asociada. (Sólo funciona si el servidor ya ha sido iniciado!)
	def modifica_timeout(self, n):
		self.servidor.timeout= n

	#Constructor de el Juego de Snake (SERVIDOR)
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.pushButton_3.hide()
		self.dire= 2
		#acá hacemos que las celdas se adapten al tamaño de la TableWidget.
		self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Stretch)
		#Hacemos que se aumente/disminuya el tamaño de la TableWidget según los spinBox.
		self.spinBox.valueChanged.connect(self.modifica_columnas)
		self.spinBox_2.valueChanged.connect(self.modifica_lineas)
		self.spinBox_3.valueChanged.connect(self.cambia_ms)
		self.doubleSpinBox.valueChanged.connect(self.modifica_timeout)
		self.pushButton.clicked.connect(self.inicia_servidor)
		self.pushButton_2.clicked.connect(self.empieza_juego)
		self.pushButton_3.clicked.connect(self.termina_partida)
		self.label_9.hide()
		self.lista_viboras= []
		self.viboras_ingame= []
		self.servidor= None

#Clase que representa a una Víbora, de nuestro juego de Snake.
class Vibora():
	id= None
	color= []
	coordenadas= []
	cabeza= QTableWidgetItem()
	cuerpo1= QTableWidgetItem()
	cuerpo2= QTableWidgetItem()
	cuerpo3= QTableWidgetItem()
	cola= QTableWidgetItem()
	direccion= 2
	
	#Constructor de una Víbora.
	def __init__(self, idd, color, coordenadas, direccion):
		self.id= idd
		self.color= [color[0], color[1], color[2]]
		self.coordenadas= coordenadas
		self.cabeza.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpo1.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpo2.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.cuerpo3.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.cola.setBackground(QtGui.QColor(color[0],color[1],color[2]))
		self.direccion= direccion

	#Método que se encarga de actualizar las coordenadas según la dirección se haya movido la víbora.
	def actualiza_coords(self, direccion, columnas, lineas):
		if direccion == 3: #Cambia las coordenadas si nos movemos hacia la izquierd
			self.coordenadas= [ self.coordenadas[0], (self.coordenadas[1]-1) % columnas, self.coordenadas[0] , self.coordenadas[1] ,self.coordenadas[2] ,self.coordenadas[3] ,self.coordenadas[4] ,self.coordenadas[5] ,self.coordenadas[6] ,self.coordenadas[7]]
		elif direccion == 1: #Cambia las coordenadas si nos movemos hacia la derecha.
			self.coordenadas= [ self.coordenadas[0], (self.coordenadas[1]+1) % columnas, self.coordenadas[0] , self.coordenadas[1] ,self.coordenadas[2] ,self.coordenadas[3] ,self.coordenadas[4] ,self.coordenadas[5] ,self.coordenadas[6] ,self.coordenadas[7]]
		elif direccion == 0: #Cambia las coordenadas si nos movemos para arriba.
			self.coordenadas= [ (self.coordenadas[0]-1) % lineas, self.coordenadas[1] , self.coordenadas[0] , self.coordenadas[1] ,self.coordenadas[2] ,self.coordenadas[3] ,self.coordenadas[4] ,self.coordenadas[5] ,self.coordenadas[6] ,self.coordenadas[7]]
		else: #Cambia las coordenadas si nos movemos para abajo.
			self.coordenadas= [ (self.coordenadas[0]+1) % lineas, self.coordenadas[1] , self.coordenadas[0] , self.coordenadas[1] ,self.coordenadas[2] ,self.coordenadas[3] ,self.coordenadas[4] ,self.coordenadas[5] ,self.coordenadas[6] ,self.coordenadas[7]]

	#Método que recra a una víbora que ha sido quitada del TableWidget, de esta forma se puede volver a pintar.
	def recrea_items(self):
		self.cabeza= QTableWidgetItem()
		self.cuerpo1= QTableWidgetItem()
		self.cuerpo2= QTableWidgetItem()
		self.cuerpo3= QTableWidgetItem()
		self.cola= QTableWidgetItem()
		self.cabeza.setBackground(QtGui.QColor(self.color[0],self.color[1], self.color[2]))
		self.cuerpo1.setBackground(QtGui.QColor(self.color[0],self.color[1], self.color[2]))
		self.cuerpo2.setBackground(QtGui.QColor(self.color[0],self.color[1], self.color[2]))
		self.cuerpo3.setBackground(QtGui.QColor(self.color[0],self.color[1], self.color[2]))
		self.cola.setBackground(QtGui.QColor(self.color[0],self.color[1], self.color[2]))

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	ventana = Servidor(None)
	ventana.show() #Iniciamos el Juego!
	app.exec_()

#  \( ͡° ͜ʖ ͡°)/ 