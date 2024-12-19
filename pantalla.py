import tkinter as tk
import mido
import threading
import random
from pychord import Chord, utils
from PIL import Image, ImageTk

ventana=tk.Tk()
pianoBotones=[]
pianoActivo=True
nombreDispositivo=""
zonaPractica=""
notas=[]
hilo_1=""
estadoPractica=""
seccionMostrat=tk.Frame()
notasElegidas=[]
tipoArcodeElegido=[]
acorde=""

def funcionOpcionNota(boton):
    global notasElegidas
    if boton["relief"] == "raised":
        boton.config(relief="sunken")
        notasElegidas.append(boton["text"])
    else:
        boton.config(relief="raised")
        notasElegidas.remove(boton["text"])

def funcionAcorde(boton):
    global tipoArcodeElegido
    if boton["relief"] == "raised":
        boton.config(relief="sunken")
        tipoArcodeElegido.append(boton["text"])
    else:
        boton.config(relief="raised")
        tipoArcodeElegido.remove(boton["text"])

def comprobarAcorde(a):
    global acorde
    listaNotas = [utils.val_to_note(elemento) for elemento in a]
    if(isinstance(acorde,Chord)):
        if(len(listaNotas)>=len(acorde.components())):
            contador=0
            numnotas=0
            for notainb in acorde.components():
                notainbnor=utils.transpose_note(notainb, 0) 
                if(notainbnor in listaNotas):
                    numnotas+=1
                contador+=listaNotas.count(notainbnor)
            if(contador==len(listaNotas) and numnotas==len(acorde.components())):
                if(True):
                    funcionSiguienteAcorde()
                else:
                    print ("correcto")
    return False

def funcionSiguienteAcorde():
    global notasElegidas 
    global tipoArcodeElegido  
    global acorde
    global seccionMostrat
    if(notasElegidas and tipoArcodeElegido):
        acorde=Chord(notasElegidas[random.randrange(0,len(notasElegidas))]+tipoArcodeElegido[random.randrange(0,len(tipoArcodeElegido))])
        for labels in seccionMostrat.winfo_children():
            labels.destroy()
        labelAcorde=tk.Label(seccionMostrat, text=acorde, font=("Arial", 50), bg="white")
        labelAcorde.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        labelComponentes=tk.Label(seccionMostrat, text=acorde.components(), font=("Arial", 30), bg="white")
        labelComponentes.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        

def practAcordes():
    global zonaPractica
    global estadoPractica
    global seccionMostrat
    estadoPractica="Acordes"
    listaNota=["C","C#","Db","D","D#","Eb","E","x","x","F","F#","Gb","G","G#","Ab","A","A#","Bb","B"]
    tipoAcordes=["maj","m","7","m7","maj7","dim","aug","sus4","sus2","6","m6","9","m9","add9"]
    margen=tk.Frame(zonaPractica,width=250, height=300)
    margen.grid(row=0,rowspan=3,column=0)
    opcion=tk.Frame(zonaPractica)
    opcion.grid(row=1,column=1)
    opcionNotaLabel=tk.Label(opcion, text="Elegir Fundamentales")
    opcionNotaLabel.grid(row=0,column=0,columnspan=3)
    for i,opcionNotas in enumerate(listaNota):
        if(opcionNotas!="x"):
            opcionNotaBoton=tk.Button(opcion, text=opcionNotas, width=7) 
            opcionNotaBoton.config(command=lambda b=opcionNotaBoton: funcionOpcionNota(b))
            opcionNotaBoton.grid(row=((i+1)//3)+1,column=((i+1)%3))        
    opcionAcordeBoton=tk.Label(opcion, text="Elegir Tipo de Acorde")
    opcionAcordeBoton.grid(row=0,column=3,columnspan=1+len(tipoAcordes)//7)
    for i,opcionAcordes in enumerate(tipoAcordes):
        opcionAcordeBoton=tk.Button(opcion, text=opcionAcordes, width=7)
        opcionAcordeBoton.config(command=lambda b=opcionAcordeBoton: funcionAcorde(b))
        opcionAcordeBoton.grid(row=i+1-(i//7*7),column=3+i//7)
    seccionMostrat=tk.Frame(zonaPractica,width=400, height=200,bg="white")
    seccionMostrat.grid(row=1,column=2,padx=10)
    seccionMostrat.grid_propagate(False)
    otrasOpciones=tk.Frame(zonaPractica)
    otrasOpciones.grid(row=1,column=3,padx=5)
    opcionAcordeAutomaticoBoton=tk.Button(otrasOpciones, text="Pasar Acordes Automaticamente")
    opcionAcordeAutomaticoBoton.grid(row=0)
    opcionPasarAcordeBoton=tk.Button(otrasOpciones, text="Generar Acorde")
    opcionPasarAcordeBoton.config(command=lambda: funcionSiguienteAcorde())
    opcionPasarAcordeBoton.grid(row=1)

def practEscalas():
    print("Practicar Escalas")
def practPartituras():
    print("Practicar Partituras")
def libre():  
    print("libre")

def coloTecla(presionada,numeroNota):
    numeroNota-=21
    if(presionada):
        if(pianoBotones[numeroNota]["width"]==20):
            pianoBotones[numeroNota].config(bg="Indian Red")
            pianoBotones[numeroNota].config(relief="sunken")
        else:
            pianoBotones[numeroNota].config(bg="Light Coral")
            pianoBotones[numeroNota].config(relief="sunken")
    else:
        if(pianoBotones[numeroNota]["width"]==20):
            pianoBotones[numeroNota].config(bg="black")
            pianoBotones[numeroNota].config(relief="raised")
        else:
            pianoBotones[numeroNota].config(bg="white")
            pianoBotones[numeroNota].config(relief="raised")

def escucharPiano():
    global nombreDispositivo
    global notas
    global pianoActivo
    global estadoPractica
    while pianoActivo:
        if(nombreDispositivo!=""):
            with mido.open_input(nombreDispositivo) as inport:
                for msg in inport:
                    if msg.type == 'note_on':
                        notas.append(msg.note)
                        coloTecla(True,msg.note)
                        if(estadoPractica=="Acordes"):
                            comprobarAcorde(notas)
                    elif msg.type == 'note_off':
                        
                        notas.remove(msg.note) #agregar un if contains?
                        coloTecla(False,msg.note)

def elegirDispositivo():
    dispositivos=mido.get_input_names()
    ventanaEmergente = tk.Toplevel(ventana)
    ventanaEmergente.title("Dispositivos")
    ventanaEmergente.geometry("300x"+str((len(dispositivos)+1)*50))
    label=tk.Label(ventanaEmergente, text="Selecciona un dispositivo")
    label.pack(pady=5)
    for dispositivo in dispositivos:
        boton=tk.Button(ventanaEmergente, text=dispositivo, command=lambda:setNombreDispositivo(dispositivo,ventanaEmergente))
        boton.pack(pady=5)

def setNombreDispositivo(dispositivo,ventanaEmergente):
    global nombreDispositivo
    global ventana
    nombreDispositivo = dispositivo
    ventana.title(dispositivo)
    ventanaEmergente.destroy()

def dibujarOpciones():
    global ventana
    boton = tk.Button(ventana, text="Practicar acordes", command=practAcordes)
    boton.grid(row=0, column=0, pady=5)
    boton = tk.Button(ventana, text="Practicar Escalas", command=practEscalas)
    boton.grid(row=0, column=1, pady=5)
    boton = tk.Button(ventana, text="Practicar Partituras", command=practPartituras)
    boton.grid(row=0, column=2, pady=5)
    boton = tk.Button(ventana, text="Libre", command=libre)
    boton.grid(row=0, column=3, pady=5)
    boton = tk.Button(ventana, text="Cambiar midi", command=elegirDispositivo)
    boton.grid(row=0, column=9, pady=5)

def dibujarPiano():
    j=1
    aux=5
    global pianoBotones
    global ventana
    for i in range(88):
        if(((12*j+2)//5)==i+1):
            j+=1
            tecla = tk.Frame(ventana, bg="black", width=20, height=96,borderwidth=1, relief="raised")
            tecla.place(x=aux-(20/2), y=350)
            tecla.lift()
        else:
            tecla = tk.Frame(ventana, bg="white", width=32, height=160,borderwidth=1, relief="raised")
            tecla.place(x=aux, y=350)
            tecla.lower() 
            aux+=32
        pianoBotones.append(tecla)

def cerrarVentana():
    global pianoActivo
    pianoActivo=False
    ventana.destroy()  
    
def main():
    global ventana
    global nombreDispositivo
    global zonaPractica
    ventana.geometry("1674x515")
    ventana.title("")
    ventana.protocol("WM_DELETE_WINDOW", cerrarVentana)
    zonaPractica=tk.Frame(ventana,width=1674, height=300)
    zonaPractica.grid(row=1, rowspan=4, column=0, columnspan=10)
    zonaPractica.grid_propagate(False)
    dibujarOpciones()
    dibujarPiano()
    #if(nombreDispositivo==""):
    #    elegirDispositivo()
    ventana.mainloop()

if __name__=="__main__":
    hilo_1 = threading.Thread(target=escucharPiano)
    hilo_1.start()
    main()