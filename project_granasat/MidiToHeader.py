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
 *              Python code to obtain an Arduino Header file from a MIDI file
 *
 * ******************************************************************************************** *
 * Versions:
 *              V0 - Juan Andrés Peña Maldonado 12/05/2023
 * 
 * ******************************************************************************************** *
 * To do:
 *              Implementar un sistema nuevo de cabecera que ocupe menos espacio
 *              
 * ******************************************************************************************** *
 * Comments:
 * 
 *          
 * 
 * ******************************************************************************************** *       
 */
"""

import mido #Version 1.2.10
import numpy as np #Version 1.16.6



#midi_to_matrix se encarga de guardar la información relevante de un midi a una matriz numpy
def midi_to_matrix(mid):
    
    
    #La clase note_obj es una clase auxiliar que guarda la información necesaria de cada nota
    class note_obj():
        
        def __init__(self,track,note,start):
            #En que pista se encuentra esta nota
            self.track = track
            #El tono de dicha nota
            self.note = note
            #Cuando empieza a sonar (En decimas de segundo)
            self.start = start
            #Cuando termina de sonar (En decimas de segundo)
            self.end = None
        
        def __str__(self):
            return "{} {} {} {}".format(self.track,self.note,self.start,self.end-self.start)
    
    #Unfinished notes es un diccionario con las notas que sabemos cuando empiezan pero no cuando acaban.
    #Es un paso intermedio antes de ser guardadas en notes
    unfinished_notes = {}
    #Notes guarda las notas que tienen un inicio y un final definido.
    notes = []
    
    #Tempo determina el tempo de la pista y se usa para pasar de unidades de tiempo de MIDI a segundos
    tempo = 0
    #Track determina la pista actual que estamos leyendo
    track = 0
    #Leemos cada pista del archivo
    for i in mid.tracks:
        #Contamos el tiempo transcurrido desde el inicio de la canción
        #Se actualiza con cada mensaje leido y se mide en decimas de segundo
        absolute_timer = 0
        #Leemos cada mensaje de la pista
        for j in i:
            #Si es un mensaje meta, comprobamos si cambia el tempo de la pista
            if (j.is_meta):
                #En caso de que lo haga, actualizamos el tempo
                if (j.type == "set_tempo"):
                    tempo = j.tempo
            #En caso de que no sea un mensaje meta
            else:
                #Actualizamos el timer
                absolute_timer += mido.tick2second(j.time,mid.ticks_per_beat,tempo)*100
                #Comprobamos si el mensaje inicia una nota o la termina
                #Si es un mensaje note_on, inicia una nota y almacenamos la nota en unfinished
                if (j.type == "note_on"):
                    if (j.velocity != 0):
                        unfinished_notes[j.note] = note_obj(track,j.note,absolute_timer)
                #En caso de que sea un mensaje note_off o que la velocidad del mensaje note_on sea 0,
                #termina una nota, la sacamos de unfinished y la almacenamos en note
                    else:
                        new_note = unfinished_notes[j.note]
                        new_note.end = absolute_timer
                        notes.append(new_note)
                        unfinished_notes.pop(j.note)
                elif (j.type == "note_off"):
                    new_note = unfinished_notes[j.note]
                    new_note.end = absolute_timer
                    notes.append(new_note)
                    unfinished_notes.pop(j.note)
        track += 1
    
    #Ordenamos la lista de notas en función de cuando empiezan
    notes.sort(key= lambda x: x.start)
    
    #Pasamos la información almacenada en una lista de objetos a una matriz numpy
    matrix = np.zeros( (len(notes),4),dtype=int )
    line = 0
    for i in notes:
        matrix[line,0] = int(i.note)
        matrix[line,1] = int(i.start)
        matrix[line,2] = int(i.end - i.start)
        matrix[line,3] = int(i.track)
        line = line + 1
    
    return matrix


#tone_to_light se encarga de asignar una luz de la placa a cada una de las notas de la canción
def tone_to_light(m):
    
    #Primero, vamos a separar las canciones en función de cuantas pistas tenemos
    n_tracks =int(np.max(m[:,3]))
    tracks = []
    for i in range(n_tracks+1):
        track = m[np.where(m[:,3] == i)]
        tracks.append(track)
    
    #Vamos a pasar cada pista a un rango de luces
    #Las luces de la placa van del 0 al 31.
    #Cada pista tiene un rango de este intervalo en función de cuantas pistas haya
    #Cada nota se mapea sobre el rango asignado
    for track in tracks:
        notes_on_track = track[:,0]
        lowest_tone = np.min(notes_on_track)
        lights_on_track = (notes_on_track - lowest_tone)
        highest_tone = np.max(lights_on_track)
        lights_on_track = lights_on_track / highest_tone
        lights_on_track = lights_on_track * 31
        lights_on_track = np.round(lights_on_track,0).astype(int)
        
        track[:,0] = lights_on_track
    
    #Finalmente, volvemos a juntar todas las pistas en una sola matriz
    final_matrix = tracks[0]
    if (len(tracks) > 1):
        for i in range(1,len(tracks)):
            final_matrix = np.vstack(final_matrix,tracks[i])
    
    #Una vez terminado este proceso ya no necesitamos la columna pista por lo que podemos eliminarla
    return final_matrix[:,:3]


#matrix_to_header se encarga de guardar los datos de la matriz en forma de cabecera para Arduino
def matrix_to_header(m):
    
    #Convertimos la matriz a string
    m = m.astype(str)
    
    #Abrimos el archivo de la cabecera
    f = open("musiclights.h","w")
    
    #Escribimos los ifndef define
    f.write("#ifndef MUSICLIGHTS_H\n")
    f.write("#define MUSICLIGHTS_H\n\n")
    
    #Guardamos el número de notas
    f.write("\tconst int notes1 = "+str(len(m[:,0]))+";\n")
    
    #Las luces
    f.write("\tconst int light1 [] PROGMEM = {")
    first = True
    for i in m[:,0]:
        if first:
            f.write(i)
            first = False
        else:
            f.write(", " + i)
    f.write("};\n")
    
    #El momento en el que se tienen que encender
    f.write("\tconst int start1 [] PROGMEM = {")
    first = True
    for i in m[:,1]:
        if first:
            f.write(i)
            first = False
        else:
            f.write(", " + i)
    f.write("};\n")
    
    #El tiempo que tardan en apagarse
    f.write("\tconst int delay1 [] PROGMEM = {")
    first = True
    for i in m[:,2]:
        if first:
            f.write(i)
            first = False
        else:
            f.write(", " + i)
    f.write("};\n")
    
    #Cerramos los defines
    f.write("\n#endif")
    
    #Cerramos el archivo de la cabecera
    f.close()

#midi_to_header genera una cabecera para arduino a partir de un archivo MIDI
def midi_to_header(title):
    mid = mido.MidiFile(title,clip=True)


    m = midi_to_matrix(mid)
    
    m = tone_to_light(m)
    
    matrix_to_header(m)

def main():
    #Establecemos la ruta hacia el archivo MIDI
    title = "MIDIS/MiniMIDI.mid"
    
    midi_to_header(title)


if __name__ == "__main__":
    main()
    