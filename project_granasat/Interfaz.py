# -*- coding: utf-8 -*-
"""
/*
 *      ________  ________  ________  ________   ________  ________  ________  _________
 *     |\   ____\|\   __  \|\   __  \|\   ___  \|\   __  \|\   ____\|\   __  \|\___   ___\
 *     \ \  \___|\ \  \|\  \ \  \|\  \ \  \\ \  \ \  \|\  \ \  \___|\ \  \|\  \|___ \  \_|
 *      \ \  \  __\ \   _  _\ \   __  \ \  \\ \  \ \   __  \ \_____  \ \   __  \   \ \  \
 *       \ \  \|\  \ \  \\  \\ \  \ \  \ \  \\ \  \ \  \ \  \|____|\  \ \  \ \  \   \ \  \
 *        \ \_______\ \__\\ _\\ \__\ \__\ \__\\ \__\ \__\ \__\____\_\  \ \__\ \__\   \ \__\
 *         \|_______|\|__|\|__|\|__|\|__|\|__| \|__|\|__|\|__|\_________\|__|\|__|    \|__|
 *  
 * Typing help from: http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
 * 
 * Webpage: https://granasat.ugr.es
 * Github:  https://github.com/granasat
 * 
 * ******************************************************************************************** *
 * Original Code:   https://github.com/juanandres185/TFG_ArduinoOrgano
 * Author:          juanandres185
 * 
 * ******************************************************************************************** *
 * Programmers:
 *              Juan Andrés Peña Maldonado 12/05/2023 (juanandres@correo.ugr.es)
 *  
 * ******************************************************************************************** *
 * Description: 
 *              Python interface to interact with Arduino code
 *
 * ******************************************************************************************** *
 * Versions:
 *              V0 - Juan Andrés Peña Maldonado 12/05/2023
 * 
 * ******************************************************************************************** *
 * To do:
 *              Añadir las funciones Carga y Elimina
 *              Leer las canciones que hay en la placa y añadirlas a songs_list
 *              
 * ******************************************************************************************** *
 * Comments:
 * 
 *          
 * 
 * ******************************************************************************************** *       
 */
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