# -*- coding: utf-8 -*-
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

import mido
import numpy as np

mid = mido.MidiFile("MIDIS/MiniMIDI.mid",clip=True)

print(mid.type)

f = open("midi2.txt","w")


class note_obj():
    
    def __init__(self,track,note,start):
        self.track = track
        self.note = note
        self.start = start
        self.end = None
    
    def __str__(self):
        return "{} {} {} {}".format(self.track,self.note,self.start,self.end-self.start)
        

unfinished = {}
notes = []

track = 0
for i in mid.tracks:
    print("Estamos en track:",track)
    
    absolute_timer = 0
    for j in i:
        if (not j.is_meta):
            absolute_timer += j.time
            if (j.type == "note_on"):
                if (j.velocity == 0):
                    new_note = unfinished[j.note]
                    new_note.end = absolute_timer
                    notes.append(new_note)
                    unfinished.pop(j.note)
                else:
                    unfinished[j.note] = note_obj(track,j.note,absolute_timer)
                    
            elif (j.type == "note_off"):
                new_note = unfinished[j.note]
                new_note.end = absolute_timer
                notes.append(new_note)
                unfinished.pop(j.note)
    track += 1

notes.sort(key= lambda x: x.start)

m = np.zeros( (len(notes),4) )
line = 0
for i in notes:
    m[line,0] = int(i.note)
    m[line,1] = int(i.start)
    m[line,2] = int(i.end - i.start)
    m[line,3] = int(i.track)
    line = line + 1




notas = np.unique(m[:,0])


def tone_to_note(m):
    
    n = m[:,0]
    minim = n.min()
    n = (n - minim)
    n = (n / n.max())
    n = (np.round(n*31,0)).astype(int)
    
    m[:,0] = n
    
    return m

m = tone_to_note(m)



notas = {}
for i in m:
    
    if i[1] in notas:
        notas[i[1]].append(i[0])
    else:
        notas[i[1]] = [i[0]]
    
    if (i[1] + i[2]) in notas:
        notas[i[1] + i[2] ].append(i[0])
    else:
        notas[i[1] + i[2] ] = [i[0]]


f = open("notas.txt","w")

delay = []
light = []
prev_nota = 0
for i in sorted(notas):
    f.write(str(i-prev_nota)[:-2])
    delay.append(str(i-prev_nota)[:-2])
    first = True
    for number in notas[i]:
        if first:
            f.write(" " + str(number)[:-2])
            light.append(str(number)[:-2])
            first = False
        else:
            f.write("\n0 "+str(number)[:-2])
            delay.append("0")
            light.append(str(number)[:-2])
    
    f.write("\n")
    prev_nota = i
    
f.close()

f = open("musiclights.h","w")

f.write("#ifndef MUSICLIGHTS_H\n")
f.write("#define MUSICLIGHTS_H\n\n")
f.write("\tconst int delay1 [] PROGMEM = {")
first = True
for i in delay:
    if first:
        f.write(i)
        first = False
    else:
        f.write(", " + i)
f.write("};\n")
f.write("\tconst int light1 [] PROGMEM = {")
first = True
for i in light:
    if first:
        f.write(i)
        first = False
    else:
        f.write(", " + i)
f.write("};\n")
f.write("\n#endif")


f.close()




