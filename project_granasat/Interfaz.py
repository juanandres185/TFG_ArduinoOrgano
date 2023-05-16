# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:13:50 2023

@author: JuanAndres
"""

import tkinter as tk #Versión 8.6.11
from tkinter.filedialog import askopenfile #Versión 8.6.11

#Obtiene la ruta de un archivo y la almacena en selected_file
def mfileopen():
    
    file = askopenfile()
    if file is not None:
        selected_file.insert(0,str(file).split("'")[1])
        
      
def main():
    
    #Los elementos de la interfaz deben ser globales para poder interactuar con ellos desde las funciones
    global root
    global title_label
    global selected_file
    global open_file_button
    
    
    root = tk.Tk()
    root.geometry("700x600")
    
    #Titulo
    title = "Organo de luces"
    title_label = tk.Label(root, text = title,padx=5,pady=5,font=("Arial",25))
    title_label.pack(fill=tk.X)
    
    #Seleccion de archivo
    select_file_frame = tk.Frame(root)
    select_file_frame.pack(fill=tk.X,padx = 10)
    
    #Texto
    selected_file = tk.Entry(select_file_frame)
    selected_file.pack(fill=tk.X,side=tk.LEFT,expand=True,padx = 5)
    selected_file.insert(0,"")
    
    #Boton
    open_file_button = tk.Button(select_file_frame,text = "Explorar",width = 30,command = mfileopen)
    open_file_button.pack(side=tk.LEFT)
    
    #Lista de canciones en la SD
    songs_list_frame = tk.Frame(root)
    songs_list_frame.pack(fill=tk.Y,pady= 10,padx= 10,side=tk.LEFT)
    
    #Etiqueta
    songs_list_title = tk.Label(songs_list_frame,text = "Canciones",padx=5,pady=5,font=("Arial",10))
    songs_list_title.grid(column=0,row=0)
    
    #Lista
    songs_list = tk.Listbox(songs_list_frame,width = 35, height = 12, selectmode = tk.SINGLE)
    for i in range(0,10):
        songs_list.insert(i,"Canción"+str(i))
    songs_list.grid(column=0,row=1)
    
    #Botones de cargar y eliminar canciones
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(fill=tk.Y,pady=100,padx = 100, side= tk.RIGHT)
    
    #Cargar
    load_button = tk.Button(buttons_frame,text = "Cargar", width = 30)
    load_button.grid(column=0,row=0,pady=10)
    
    #Eliminar
    delete_button = tk.Button(buttons_frame,text = "Eliminar", width = 30)
    delete_button.grid(column=0,row=1,pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()