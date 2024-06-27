import pygame
import math
import sys
from datos import lista as lista_preguntas
from PYGame_MiLibreria import *

'''
A. Analizar detenidamente el set de datos (puede agregarle más preguntas si así lo desea).

B. Crear una pantalla de inicio, con 3 (tres) botones, “Jugar”, “Ver Puntajes”,
“Salir”, la misma deberá tener alguna imagen cubriendo completamente el
fondo y tener un sonido de fondo. Al apretar el botón jugar se iniciará el juego.
Opcional: Agregar un botón para activar/desactivar el sonido de fondo.

C. Crear 2 botones uno con la etiqueta “Pregunta”, otro con la etiqueta “Reiniciar”

D. Imprimir el Puntaje: 000 donde se va a ir acumulando el puntaje de las respuestas correctas. 
Cada respuesta correcta suma 10 puntos.

E. Al hacer clic en el botón “Pregunta” debe mostrar las preguntas comenzando
por la primera y las tres opciones, cada clic en este botón pasa a la siguiente
pregunta.

F. Al hacer clic en una de las tres palabras que representa una de las tres
opciones, si es correcta, debe sumar el puntaje, reproducir un sonido de
respuesta correcta y dejar de mostrar las otras opciones.

G. Solo tiene 2 intentos para acertar la respuesta correcta y sumar puntos, si
agotó ambos intentos, deja de mostrar las opciones y no suma puntos. Al
elegir una respuesta incorrecta se reproducirá un sonido indicando el error y
se ocultará esa opción, obligando al usuario a elegir una de las dos restantes.

H. Al hacer clic en el botón “Reiniciar” debe mostrar las preguntas comenzando
por la primera y las tres opciones, cada clic pasa a la siguiente pregunta.
También debe reiniciar el puntaje.

I. Una vez terminado el juego se deberá pedirle el nombre al usuario, guardar
ese nombre con su puntaje en un archivo, y volver a la pantalla de inicio.

J. Al ingresar a la pantalla “Ver Puntajes”, se deberá mostrar los 3 (tres) mejores
puntajes ordenados de mayor a menor, junto con sus nombres de usuario
correspondientes. Debe haber un botón para volver al menú principal.
'''

#Todos los botones seran objetos con esta clase para una manipulacion de como funcionan mas facil.
class claseBoton():
    def __init__(self, texto : str, ubicacion : list, tamanio : list, accion : int, elemento_id : int): #Constructor
        self.texto_ = texto #Texto del boton
        self.ubicacion_ = [round(ubicacion[0]), round(ubicacion[1])]    #Ubicacion en pantalla.
        self.tamanio_ = tamanio #Tamaño del boton
        self.accion_ = accion    #La accion que hara este boton, cada accion esta definida en mouseclickdown.
        self.elemento_id = elemento_id
        
        self.color_ = [255, 255, 255] #Color del rectangulo.
        self.color_borde_ = [0, 65, 255] #Color de los bordes
        self.color_aux_ = self.color_
        self.color_borde_aux_ = self.color_borde_

        #Se define el Rect del boton temporalmente, se modifica cuando se usa su metodo de dibujado.
        self.rect_ = pygame.draw.rect(pantalla, self.color_, [ubicacion[0], ubicacion[1], tamanio[0], tamanio[1]])
        self.interactuable = False #Si esta en true, es posible de interactuar con el boton.
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        if (self.elemento_id == pantalla_id and self.interactuable):
            self.rect_ = pg_dibujar_boton(pantalla, self.texto_, self.ubicacion_, self.tamanio_, self.color_, self.color_borde_, [0,0,0])
    
class claseBotonOpcion(claseBoton):
    def __init__(self, opcion : str, ubicacion : list, elemento_id : int): #Constructor
        self.opcion_ = opcion
        self.elemento_id = elemento_id
        self.ubicacion_ = [round(ubicacion[0]), round(ubicacion[1])]

        #Datos no Modificables
        self.respuesta_ = ""
        self.tamanio_ = [480, 48]
        self.color_ = [200, 128, 255]
        self.color_borde_ = [128, 16, 16]
        self.color_aux_ = self.color_
        self.color_borde_aux_ = self.color_borde_
        self.rect_ = None
        self.interactuable = False
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        self.texto_ = f"Opcion {self.opcion_}: {self.respuesta_}"

        if (self.elemento_id == pantalla_id):
            #Cambiar los colores si es que el boton esta disponible.
            if (self.interactuable == True):
                self.color_ = self.color_aux_
                self.color_borde_ = self.color_borde_aux_
            else:
                self.color_ = [64, 64, 64]
                self.color_borde_ = [32, 32, 32]

            self.rect_ = pg_dibujar_boton(pantalla, self.texto_, self.ubicacion_, self.tamanio_, self.color_, self.color_borde_, [0,0,0])
    
    #Este metodo se va a fijar si era la respuesta correcta la suya.
    def tomar_decision(self, opcion_correcta : str, volumen : float):
        acierto = (self.opcion_.lower() == opcion_correcta) #La condicion en si es un booleano.

        #Reproducir sonido dependiendo de que si fue o no correcta la opcion decidida.
        if (acierto):
            pg_audio_reproducir("Preguntados\Assets\Audio\sndAcierto.wav", False, volumen)
        else:
            pg_audio_reproducir("Preguntados\Assets\Audio\sndError.wav", False, volumen * 0.75)

        return acierto

#Inicializadores
pygame.init()       #Se inicializa pygame
pygame.mixer.init() #Junto al mixer.
pygame.time.set_timer(pygame.USEREVENT + 0, 6)

preguntas = []     #Cada indice contendra la pregunta.
opciones = []      #Cada indice contendra las opciones posibles en una lista de siempre 3 elementos.
respuestas = []    #Cada indice contendra la respuesta correcta de la pregunta X.

#Recorremos la lista obtenida para registrar todo.
for pregunta in lista_preguntas:
    preguntas.append(pregunta['pregunta'])
    opciones.append([pregunta['a'], pregunta['b'], pregunta['c']])
    respuestas.append(pregunta['correcta'])

#######################PANTALLA#######################
resolucion = [960, 640]
pantalla = pygame.display.set_mode(resolucion)
pantalla_id = 0   #Si cualquier ID de cada elemento coincide con la de esta variable, sera visible e interctuable.


#######################BOTONES#######################
tam_boton = [208, 40]   #Tamaño para cada boton.
ub_boton_x = (resolucion[0] / 2) - (tam_boton[0] / 2)   #Ubicacion predeterminada para los botones (X)
ub_boton_y = (resolucion[1] / 2) - (tam_boton[1] / 2)   #Ubicacion predeterminada para los botones (Y)
sep_botones = 32        #Cuanto separamos cada boton uno del otro en Y.

#Definicion de botones
lista_botones = [
    claseBoton("Jugar", [ub_boton_x, ub_boton_y-tam_boton[1]-sep_botones], tam_boton, 6, 0),
    claseBoton("Ver Puntajes", [ub_boton_x, ub_boton_y], tam_boton, 8, 0),
    claseBoton("Salir", [ub_boton_x, ub_boton_y+(tam_boton[1]+sep_botones)*2], tam_boton, 0, 0),
    claseBoton("Pregunta", [ub_boton_x, 120], tam_boton, 11, 1),
    claseBoton("Reiniciar", [ub_boton_x + round((resolucion[0] / 2) / 2), 500], tam_boton, 12, 1),
    claseBoton("Configuracion", [ub_boton_x, ub_boton_y+tam_boton[1]+sep_botones], tam_boton, 3, 0),
    claseBoton("Volver", [64, 64], tam_boton, 1, 2),
    claseBoton("Mutear Musicas", [ub_boton_x, 164], tam_boton, 9, 2),
    claseBoton("Mutear Sonidos", [ub_boton_x, 164+tam_boton[1]+sep_botones], tam_boton, 10, 2),
    claseBoton("Volver", [ub_boton_x, 556], tam_boton, 5, 3),
    claseBotonOpcion("A", [(resolucion[0] / 2) - 240, ub_boton_y], 1),
    claseBotonOpcion("B", [(resolucion[0] / 2) - 240, ub_boton_y+64], 1),
    claseBotonOpcion("C", [(resolucion[0] / 2) - 240, ub_boton_y+128], 1)
]


#######################VARIABLES#######################
musica_actual = None            #Inicia en none.
trsc_transpariencia = 255       #Transparencia de la imagen de transicion
transicionando = True           #Bool para saber si estamos en medio de una transicion.
prox_pantallaid = 0             #Al final de cada transicion, se cambiara pantalla_id a este valor.
tipo_transicion = 0             #0 = Desvanacer; 1 = Aparecer
volumen = [0.7, 1.0]            #0 = Volumen para la musica; 1 = Volumen para los sonidos.
volumen_real = [0.0, 1.0]       #Esta variable va a ser la que modifica constantemente el volumen en la musica.
volumen_ref = [volumen[0], volumen[1]]        #Y esta variable va a ser la referencia del volumen_real. Esta separada para las transiciones.
puntaje = 0                     #Se ira acumulando con cada pregunta contestada correctamente.
prg_actual = -1                 #Esta variable sera la que buscara el indice de preguntas,opciones y respuestas.
preguntas_habilitadas = False   #Se volvera true una vez que comenzamos con las preguntas.
actualizar_botones = True      #Si esta en True, los botones de opciones actualizaran sus propiedades.
intentos_disponibles = 2        #Y esto contara los intentos que aun le quedan al jugador.

#Accion
bucleJuego = True
while bucleJuego:
    pg_titulo("Preguntados [Julian Naim Sandes]")
    for pEvent in pygame.event.get():

        #Se verifica si el usuario quiere cerrar la ventana
        if pEvent.type == pygame.QUIT:
            bucleJuego = False

        #Ticks
        if (pEvent.type == pygame.USEREVENT): #Tick
            #Manejo de Musica
            if (musica_actual != None):
                if (volumen_real[0] < volumen_ref[0]):
                    volumen_real[0] += 0.001
                elif (volumen_real[0] > volumen_ref[0]):
                    volumen_real[0] -= 0.005

                pg_audio_cambiarvolumen(musica_actual, volumen_real[0])
            else:
                volumen_real[0] = 0

            #Transiciones
            if (transicionando):
                if (tipo_transicion == 0 and trsc_transpariencia > 0):
                    trsc_transpariencia -= 2
                elif (tipo_transicion == 1 and trsc_transpariencia < 255):
                    trsc_transpariencia += 1
                else:
                    if (tipo_transicion == 0):
                        transicionando = False
                    else:
                        #Esto cambia que elementos mostrar en caso de querer cambiarlo.
                        pantalla_id = prox_pantallaid
                        tipo_transicion = 0
                        volumen_ref[0] = volumen[0]
                        musica_actual = None

        if (pEvent.type == pygame.MOUSEMOTION):
            #Esto es para iluminar los botones que seran seleccionados
            for boton in lista_botones:
                if (boton.interactuable == True and transicionando == False):
                    if boton.rect_.collidepoint(pEvent.pos):
                        boton.color_borde_ = [255, 255, 255]
                    else:
                        boton.color_borde_ = boton.color_borde_aux_
        
        #Evento de clickeo de mouse.
        if pEvent.type == pygame.MOUSEBUTTONDOWN:
            for boton in lista_botones:

                #Pulso de boton Normal
                #Solo se ejecutara la accion si es interactuable.
                if (boton.interactuable == True and transicionando == False):
                    if boton.rect_.collidepoint(pEvent.pos):
                        activarOpciones = False

                        if (type(boton) == claseBoton):
                            reiniciar = (boton.accion_ == 12)
                            reproducir_sonido = True

                            #La accion del boton dependera de su valor de accion.
                            #Esto originalmente estaba hecho con un match, pero debido a la gran cantidad de lineas
                            #que usaba lo decidi reducir a unas condicionales. Espero se entienda!
                            mi_accion = boton.accion_
                            if (mi_accion > 0 and mi_accion < 9):
                                #Esto es para decidir correctamente a que pantalla_id iremos.
                                if (mi_accion < 5):
                                    pantalla_id = mi_accion - 1
                                else:
                                    transicionando = True
                                    tipo_transicion = 1
                                    volumen_ref[0] = 0
                                    prox_pantallaid = mi_accion - 5
                                    
                            elif (mi_accion == 9 or mi_accion == 10):  #Manejo de Volumenes
                                indice = mi_accion - 9

                                if (volumen[indice] == 0):
                                    volumen[indice] = 1
                                    boton.texto_ = boton.texto_.replace("Desmutear", "Mutear")
                                else:
                                    volumen[indice] = 0
                                    boton.texto_ = boton.texto_.replace("Mutear", "Desmutear")
                                    
                                #Esta multiplicacion asegura que solo sea 0.7 (el volumen original de musica) 
                                #Si el volumen ahora no es 0.
                                #Se redondea para arriba.
                                if indice == 0:
                                    volumen[indice] = 0.7 * math.ceil(volumen[indice])
                                
                                volumen_ref[indice] = volumen[indice]
                                volumen_real[indice] = volumen[indice]
                            elif (mi_accion == 11):     #Habilitacion de las preguntas.
                                
                                if (preguntas_habilitadas == False):
                                    preguntas_habilitadas = True
                                    prg_actual = 0
                                
                                    #Esto reactiva la musica.
                                    if (musica_actual == None):
                                        volumen_real[0] = volumen[0]
                                        musica_actual = definir_musica(1, volumen_real[0])

                                    activarOpciones = True
                                else:
                                    reproducir_sonido = False

                            if (reproducir_sonido):
                                pg_audio_reproducir("Preguntados\Assets\Audio\sndBoton.wav", False, volumen[1])

                        elif (type(boton) == claseBotonOpcion):   #Evento de click para los botones de respuesta.
                            if (boton.tomar_decision(respuestas[prg_actual], volumen[1]) == True):
                                if (intentos_disponibles > 0):
                                    puntaje += 10
                                    prg_actual += 1
                                    activarOpciones = True
                            else:
                                #Mostrar que este boton esta deshabilitado si no era el correcto.
                                boton.interactuable = False
                                intentos_disponibles -= 1

                                #Si se nos acabaron los intentos, detenemos el juego.
                                if (intentos_disponibles <= 0):
                                    for botonOpcion in lista_botones:
                                        if type(botonOpcion) == claseBotonOpcion:
                                            botonOpcion.interactuable = False

                                    pg_audio_detener(musica_actual)
                                
                                actualizar_botones = True
                            
                        
                        #Esto es para activar los botones de opciones, usados en diversas situaciones.
                        if (activarOpciones):
                            for botonOpcion in lista_botones:
                                if type(botonOpcion) == claseBotonOpcion:
                                    botonOpcion.interactuable = True
                        
                        #Reinicio del juego
                        if (reiniciar):
                            puntaje = 0

                            if (musica_actual != None):
                                pg_audio_detener(musica_actual)

                            musica_actual = None
                            preguntas_habilitadas = False
                            prg_actual = -1
                            intentos_disponibles = 2

                            for botonOpcion in lista_botones:
                                if type(botonOpcion) == claseBotonOpcion:
                                    botonOpcion.interactuable = False
                            
                            actualizar_botones = True

    #Musica y Fondo
    pantalla.fill([0, 0, 0])    #Aca hay un filling para sobreponer todo lo que estaba antes.
    dibujar_fondo(pantalla, pantalla_id)  #Graficado de los fondos.
    if (musica_actual == None and pantalla_id != 1): #Musica
        musica_actual = definir_musica(pantalla_id, volumen_real[0])

    #Logo de la primera pantalla
    if (pantalla_id == 0):
        pg_dibujar_imagen(pantalla, pygame.image.load("Preguntados\Assets\Imagenes\imgLogo.png"), 
            [resolucion[0] / 2 - 320, 60], 0.5)
    
    #Puntaje (y intentos restantes) y Pregunta de la pantalla de preguntas.
    if (pantalla_id == 1):

        pg_crear_texto(pantalla, f"PUNTAJE: {escribir_puntaje(puntaje)} | INTENTOS : {intentos_disponibles}", 
            [resolucion[0] / 2, 80], [255, 65, 65], 30, True)

        if (prg_actual >= 0 and prg_actual < len(preguntas)):
            pg_crear_texto(pantalla, f"{preguntas[prg_actual]}", [resolucion[0] / 2, 220], [255, 255, 0], 42, True)

    #Dibujado de botones.
    for boton in lista_botones:
        #Dibujado de botones.
        if (boton.elemento_id == pantalla_id):

            #Solo se volvera interactuable ahora si es un boton normal
            #Pero si es uno de opcion, entonces no se podra interactuar hasta
            #que las preguntas esten habilitadas.
            if (actualizar_botones):
                if (type(boton) == claseBotonOpcion):
                    #Esto cambiara el texto de las opciones por las respuestas.
                    if (preguntas_habilitadas and (prg_actual > -1 and prg_actual < len(preguntas))):
                        #Vamos a referenciar la opcion con el indice de la letra de la opcion en numero.
                        #Esto se puede calcular facil con una tabla ASCII, aca la "a" es 61.
                        #boton.interactuable = True
                        boton.respuesta_ = opciones[prg_actual][ord(boton.opcion_)-65]
                    else:
                        boton.respuesta_ = ""
                else:
                    boton.interactuable = True
        else:
            boton.interactuable = False
        
        boton.dibujar(pantalla, pantalla_id)


    pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Preguntados\Assets\Imagenes\imgDesvanecimiento.png"), 1, trsc_transpariencia)
    pygame.display.flip()   #Actualiza el dibujado de la pantalla

pygame.quit() # Fin