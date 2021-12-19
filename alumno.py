#!usr/bin/env/python3
# -*- coding: utf-8 -*-
#@author: Quinones Carhuaz Liam

class Alumno():
    def __init__(self,id,nombre,apellidos,becado,distrito,idiomas):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.becado = becado
        self.distrito = distrito
        self.idiomas = idiomas
    
    def data(self):
        languages = " - ".join(self.idiomas)
        datos = [
            self.id,
            self.nombre,
            self.apellidos,
            self.becado,
            self.distrito,
            languages,
        ]
        return str(datos)
if __name__ == "__main__":
    na = Alumno("Liam","Quinones Carhuaz","Si","SJL",["Español"])
    print(na.data())