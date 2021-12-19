# -*- coding: utf-8 -*-
#@author: Quinones Carhuaz Liam

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from interfaz import Ui_MainWindow
from alumno import Alumno
from modelo import Modelo 
from time import sleep
import sys
    
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bd = Modelo()

        self.becado = ""
        self.idiomas = []
        self.actualizar_tabla_todos()
        self.setup_actividad_botones()
        self.validadores_input()
        
    def codigos_all(self):
        return self.bd.select_codigos_all()

    def actualizar_tabla_todos(self):
        self.poblar_tabla_widget_con_datos(self.ui.tableWidget,self.select_datosr_all())

    def select_datosr_all(self):
        lista_completa = self.bd.select_all_reducido()
        lista = []
        # mayusculas al nombre y apellido
        for item in lista_completa:
            id = item[0]
            nombre = item[1].capitalize()
            apellidos = item[2]
            apellidos_formateado = " ".join([k.capitalize() for k in apellidos.split()])
            becado = item[3]
            new_item = [id,nombre,apellidos_formateado,becado]
            lista.append(new_item)
        return lista

    def validadores_input(self):
        validator_text = QtGui.QRegExpValidator(QtCore.QRegExp("[a-z-A-Z_ÑñÁáÉéÍíÓóÚú]+"))
        validator_text_w_spaces = QtGui.QRegExpValidator(QtCore.QRegExp("[a-z-A-Z_ ÑñÁáÉéÍíÓóÚú]+"))
        self.ui.lineEdit_codigo.setValidator(QtGui.QIntValidator())
        self.ui.lineEdit_nombre.setValidator(validator_text)
        self.ui.lineEdit_apellidos.setValidator(validator_text_w_spaces)
        self.ui.lineEdit_codigo_eliminar.setValidator(QtGui.QIntValidator())
        self.ui.lineEdit_codigo_actualizar.setValidator(QtGui.QIntValidator())

    def setup_actividad_botones(self):
        self.ui.pushButton_registrar.clicked.connect(self.registrar_alumno)
        self.ui.pushButton_actualizar.clicked.connect(self.actualizar_alumno)
        self.ui.pushButton_eliminar.clicked.connect(self.eliminar_alumno)
        self.ui.pushButton_consultar.clicked.connect(self.consultar_alumno)
        self.ui.lineEdit_codigo_actualizar.editingFinished.connect(self.rellenar_datos_existentes)
        self.ui.pushButton_rellenar_actualizar.clicked.connect(self.rellenar_datos_existentes)

    def registrar_alumno(self):
        codigo = self.ui.lineEdit_codigo.text()
        nombre = self.ui.lineEdit_nombre.text().lower()
        apellidos = self.ui.lineEdit_apellidos.text().lower()
        if self.ui.radioButton_si.isChecked():
            self.becado = 'Si'
        elif self.ui.radioButton_no.isChecked():
            self.becado = 'No'
        becado = self.becado 
        idiomas = self.idiomas
        distrito = self.ui.comboBox_distritos.currentText()
        if self.ui.checkBox_espanol.isChecked():
            self.idiomas.append("Español")
        if self.ui.checkBox_aleman.isChecked():
            self.idiomas.append("Alemán")
        if self.ui.checkBox_frances.isChecked():
            self.idiomas.append("Francés")
        if self.ui.checkBox_ingles.isChecked():
            self.idiomas.append("Inglés")
        # comprobaciones de los campos
        if codigo in self.codigos_all():
            self.ui.label_data_error_registrar.setText("El código ya existe")
        else:
            if self.comprobaciones([codigo,nombre,apellidos,becado,idiomas],self.ui.label_data_error_registrar) == 1:
                nuevo_alumno = Alumno(codigo,nombre,apellidos,self.becado,distrito,self.idiomas)
                self.bd.insert(nuevo_alumno)
                self.ui.label_data_error_registrar.setText(f"SE REGISTRO {nombre.upper()} CORRECTAMENTE")
                # se vacia la lista de idiomas
                self.idiomas = []
                # se actualiza la tabla todos
                self.actualizar_tabla_todos()
    
    def comprobaciones(self, campos, label_error):
        codigo,nombre,apellidos,becado,idiomas = campos
        if codigo == "":
            label_error.setText("Escriba un código")
        elif nombre == "":
            label_error.setText("Nombre no puede estar vacio")
        elif apellidos.count(" ")<1:
            label_error.setText("Ingrese apellido paterno y materno correctamente")
        elif becado == "":
            label_error.setText("Marque la casilla becado")
        elif len(idiomas)<1:
            label_error.setText("Seleccione los idiomas")
        else:
            return 1
                
    def consultar_alumno(self):
        id_consulta = self.ui.lineEdit_codigo_consultar.text()
        if id_consulta not in self.codigos_all():
            self.ui.label_data_error_consultar.setText("El código no existe. Intenta de nuevo")
            self.ui.label_consulta_nombre.setText("")
            self.ui.label_consulta_apellidos.setText("")
            self.ui.label_consulta_becado.setText("")
            self.ui.label_consulta_distrito.setText("")
            self.ui.label_consulta_idiomas.setText("")
        else:
            datos = self.bd.select(id_consulta)
            id,nombre,apellidos,becado,distrito,idiomas = datos
            apellidos_w_formato = " ".join([k.capitalize() for k in apellidos.split()])
            self.ui.label_consulta_nombre.setText(nombre.capitalize())
            self.ui.label_consulta_apellidos.setText(apellidos_w_formato)
            self.ui.label_consulta_becado.setText(becado)
            self.ui.label_consulta_distrito.setText(distrito)
            self.ui.label_consulta_idiomas.setText(idiomas)
            
    def eliminar_alumno(self):
        id_eliminar = self.ui.lineEdit_codigo_eliminar.text()
        if id_eliminar not in self.codigos_all():
            self.ui.label_data_error_eliminar.setText("El código no existe. Intenta de nuevo")
        else:
            self.bd.delete(id_eliminar)
            self.ui.label_data_error_eliminar.setText("Se eliminó el alumno correctamente")
            self.actualizar_tabla_todos()

    def actualizar_alumno(self):
        # limpian las variables antes de reusarlas
        self.becado = ""
        self.idiomas = []
        id_actualizar = self.ui.lineEdit_codigo_actualizar.text()
        nombre = self.ui.lineEdit_nombre_2.text().lower()
        apellidos = self.ui.lineEdit_apellidos_2.text().lower()
        if self.ui.radioButton_si_2.isChecked():
            self.becado = 'Si'
        elif self.ui.radioButton_no_2.isChecked():
            self.becado = 'No'
        becado = self.becado 
        idiomas = self.idiomas
        distrito = self.ui.comboBox_distritos.currentText()
        if self.ui.checkBox_espanol_2.isChecked():
            self.idiomas.append("Español")
        if self.ui.checkBox_aleman_2.isChecked():
            self.idiomas.append("Alemán")
        if self.ui.checkBox_frances_2.isChecked():
            self.idiomas.append("Francés")
        if self.ui.checkBox_ingles_2.isChecked():
            self.idiomas.append("Inglés")
        # comprobaciones 
        if self.comprobaciones([id_actualizar,nombre,apellidos,becado,idiomas],self.ui.label_data_error_actualizar) == 1:
            nuevo_alumno = Alumno(id_actualizar,nombre,apellidos,self.becado,distrito,self.idiomas)
            self.bd.update(id_actualizar,nuevo_alumno)
            self.ui.label_data_error_actualizar.setText(f"SE ACTUALIZO EL ALUMNO CON CODIGO {id_actualizar} ")
            self.actualizar_tabla_todos()
                    
    def rellenar_datos_existentes(self):
        id_request = self.ui.lineEdit_codigo_actualizar.text()
        if id_request not in self.codigos_all():
            self.ui.label_data_error_actualizar.setText("El código no existe. Intenta de nuevo")
        else:
            datos = self.bd.select(id_request)
            id,nombre,apellidos,becado,distrito,idiomas = datos
            self.ui.lineEdit_nombre_2.setText(nombre)
            self.ui.lineEdit_apellidos_2.setText(apellidos)
            self.ui.comboBox_distritos_2.setCurrentText(distrito)
            if becado == "Si":
                self.ui.radioButton_si_2.setChecked(True)
            else:
                self.ui.radioButton_no_2.setChecked(True)
            idiomas = idiomas.split(" - ")
            for k in idiomas:
                if k == "Español":
                    self.ui.checkBox_espanol_2.setChecked(True)
                elif k == "Inglés":
                    self.ui.checkBox_ingles_2.setChecked(True)
                elif k == "Alemán":
                    self.ui.checkBox_aleman_2.setChecked(True)
                else:
                    self.ui.checkBox_frances_2.setChecked(True)

    def poblar_tabla_widget_con_datos(self, objeto, data):
        # el objeto debe ser de tipo QTableWidget y data un array con los datos
        row_numbers = len(data)
        objeto.setRowCount(row_numbers)
        row = 0
        for tup in data:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                objeto.setItem(row,col,cellinfo)
                col += 1
            row += 1

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
