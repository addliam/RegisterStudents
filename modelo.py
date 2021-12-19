#!usr/bin/env/python3
# -*- coding: utf-8 -*-
#@author: Quinones Carhuaz Liam

class Modelo():
    def __init__(self):
        f = open("datos.txt","a+")
        f.close() 
        self.lista_all = []
        self.refrescar_lista_all()
           
    def refrescar_lista_all(self):
        self.lista_all = []
        # recupera los datos q ya existen en datos.txt
        with open("datos.txt","r",encoding="utf-8") as f:
            content = f.read().splitlines()
            for k in content:
                k = eval(k)
                self.lista_all.append(k)

    def insert(self,x):
        # inserta el la data del objeto x a datos.txt
        with open("datos.txt","a",encoding="utf-8") as fi:
            self.lista_all.append(x.data())
            self.sobreescribir_archivo()
        self.refrescar_lista_all()
            
    def select(self,id_busqueda):
        self.refrescar_lista_all()
        for j in self.lista_all:
            if j[0] == str(id_busqueda):
                return j

    def delete(self,id_eliminar):
        new_lista = []
        for k in self.lista_all:
            if k[0] != str(id_eliminar):
                new_lista.append(k)
        self.lista_all = new_lista
        self.sobreescribir_archivo()

    def update(self,id_actualizar,nuevoObjeto):
        self.delete(id_actualizar)
        self.insert(nuevoObjeto)

    def select_codigos_all(self):
        self.refrescar_lista_all()
        codigos = []
        for k in self.lista_all:
            codigos.append(k[0])
        return codigos

    def select_all(self):
        return self.lista_all

    def select_all_reducido(self):
        self.refrescar_lista_all()
        retorno = []
        for k in self.lista_all:
            k = k[0:4]
            retorno.append(k)
        return retorno

    def sobreescribir_archivo(self):
        with open("datos.txt","w",encoding="utf-8") as fw:
            for k in self.lista_all:
                fw.write(str(k)+"\n")

""" 
m = Modelo()
al = Alumno("104","Ryze","Carhuaz","Si","San Juan de Lurigancho",["Español"])
print(m.select_all_reducido())
"""