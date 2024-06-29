import pygame
import math
import sys
from datos import lista as lista_preguntas
from PYGame_MiLibreria import *
import random

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
        self.mouse_encima = False

        #Se define el Rect del boton temporalmente, se modifica cuando se usa su metodo de dibujado.
        self.rect_ = pygame.draw.rect(pantalla, self.color_, [ubicacion[0], ubicacion[1], tamanio[0], tamanio[1]])
        self.interactuable = False #Si esta en true, es posible de interactuar con el boton.
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        if (self.elemento_id == pantalla_id):
            if (self.interactuable == True):
                self.color_ = self.color_aux_
                self.color_borde_ = self.color_borde_aux_

                #Se ilumina el borde si esta el mouse encima.
                if (self.mouse_encima):
                    self.color_ = [255, 255, 255]
                    self.color_borde_ = [255, 255, 255]
            else:
                self.color_ = [64, 64, 64]
                self.color_borde_ = [32, 32, 32]
                self.mouse_encima = False

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
        self.mouse_encima = False
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        self.texto_ = f"Opcion {self.opcion_}: {self.respuesta_}"
        claseBoton.dibujar(self, pantalla, pantalla_id)
    
    #Este metodo se va a fijar si era la respuesta correcta la suya.
    def tomar_decision(self, opcion_correcta : str, volumen : float):
        acierto = (self.opcion_.lower() == opcion_correcta) #La condicion en si es un booleano.

        #Reproducir sonido dependiendo de que si fue o no correcta la opcion decidida.
        if (acierto):
            pg_audio_reproducir("Assets\Audio\sndAcierto.wav", False, volumen)
        else:
            pg_audio_reproducir("Assets\Audio\sndError.wav", False, volumen * 0.75)

        return acierto

class claseBotonBandera():
    def __init__(self, ch_id : int, texto : str, ubicacion : list, valor : bool, elemento_id : int): #Constructor
        self.texto_ = texto #Texto que saldra a la izquierda del boton.
        self.id_ = ch_id    #Con esta ID el click detectara que bandera cambiar.
        self.dist_txtb_ = 96  #Distancia entre el boton y el texto, normalmente 124.
        self.ubicacion_ = [round(ubicacion[0]), round(ubicacion[1])]
        self.check_ = valor
        self.elemento_id = elemento_id
        self.interactuable = False
        self.rect_ = None
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        if (self.elemento_id == pantalla_id):
            if (self.interactuable == True):
                imagen = pygame.image.load("Assets\Imagenes\imgActivado.png")
                if (self.check_ == False):
                    imagen = pygame.image.load("Assets\Imagenes\imgDesactivado.png")
            else:
                imagen = pygame.image.load("Assets\Imagenes\imgCheckND.png")
                
            #Dibujado del texto y la imagen.
            pg_crear_texto(pantalla, self.texto_, [self.ubicacion_[0] - self.dist_txtb_, self.ubicacion_[1] + 24], [200, 255, 200], 42, True)
            self.rect_ = pg_dibujar_imagen(pantalla, imagen, [self.ubicacion_[0] + self.dist_txtb_, self.ubicacion_[1]], 3)

#Decidi dejar este metodo aca por lo unico para este programa que es.
def buscar_check_por_id(lista_objetos : list, id_arg : int) -> claseBotonBandera:
    boton_encontrado = None
    if (contar_elementos(lista_objetos) > 0):
        for boton in lista_objetos:
            if (type(boton) == claseBotonBandera):
                if (boton.id_ == id_arg):
                    boton_encontrado = boton
                    break

    return boton_encontrado


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
sep_botones_check = 64  #Lo mismo de arriba pero para los botones bandera.

#Definicion de botones
lista_botones = [
    claseBoton("Jugar", [ub_boton_x, ub_boton_y-tam_boton[1]-sep_botones], tam_boton, 6, 0),
    claseBoton("Ver Puntajes", [ub_boton_x, ub_boton_y], tam_boton, 8, 0),
    claseBoton("Salir", [ub_boton_x, ub_boton_y+(tam_boton[1]+sep_botones)*2], tam_boton, 0, 0),
    claseBoton("Pregunta", [ub_boton_x, 120], tam_boton, 9, 1),
    claseBoton("Reiniciar", [ub_boton_x + round((resolucion[0] / 2) / 2), 556], tam_boton, 10, 1),
    claseBoton("Configuracion", [ub_boton_x, ub_boton_y+tam_boton[1]+sep_botones], tam_boton, 3, 0),
    claseBoton("Volver", [64, 64], tam_boton, 1, 2),
    claseBoton("Volver", [ub_boton_x, 556], tam_boton, 5, 3),
    claseBotonOpcion("A", [(resolucion[0] / 2) - 240, ub_boton_y], 1),
    claseBotonOpcion("B", [(resolucion[0] / 2) - 240, ub_boton_y+64], 1),
    claseBotonOpcion("C", [(resolucion[0] / 2) - 240, ub_boton_y+128], 1),
    claseBoton("Volver", [ub_boton_x - round((resolucion[0] / 2) / 2), 556], tam_boton, 5, 1),
    claseBotonBandera(1, "Musica", [resolucion[0] / 2, 164], True, 2),
    claseBotonBandera(2, "Sonidos",[resolucion[0] / 2, 164+sep_botones_check], True, 2),
    claseBotonBandera(3, "Flash",[resolucion[0] / 2, 164+(sep_botones_check * 2)], True, 2),
    claseBotonBandera(4, "Modo Infinito",[resolucion[0] / 2, 164+(sep_botones_check * 3)], False, 2),
    claseBotonBandera(5, "Modo Aleatorio",[resolucion[0] / 2, 164+(sep_botones_check * 4)], False, 2)
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
actualizar_botones = True       #Si esta en True, los botones de opciones actualizaran sus propiedades.
intentos_disponibles = 2        #Y esto contara los intentos que aun le quedan al jugador.
top_mejores = leer_archivo_json("Preguntados_Ranking.json") #Esta variable tendra a los mejores puntajes registrados.
top_mejores['ranking'] = ordenar_ranking(top_mejores)       #Y esto ordenara directamente el ranking.
juego_terminado = False         #Si esta en true, entonces le pedira de una el nombre al usuario.
nombre_jugador = ""             #Nombre que se registre del jugador si es que su puntaje cumple para estar en los mejores. (3-20 caracteres)
flash_transpariencia = 0        #Transparencia del Flash en la pantalla de preguntas.
flash = False                   #Si es true, se vera un flash en la pantalla. (Solo funcional en la pantalla de preguntas)
flash_habilitado = True         #Si es true, el flash podra ejecutarse con normalidad.
modo_infinito = False           #Si es true, la seccion de preguntas no parara hasta que el usuario pierda.
modo_aleatorio = False          #Si es true, la siguiente pregunta sera una aleatoria de las disponibles.
maximo_preguntas = contar_elementos(preguntas)
contador_preguntas = 0
ingreso_nombre = False          #Si es true, en la pantalla de preguntas se le pedira al usuario ingresar el nombre.
tiempo_msj = 0                  #Contador usado para mostrar la notificacion de "Tu puntaje fue guardado!"

#Accion
bucleJuego = True
while bucleJuego:
    pg_titulo("Preguntados [Julian Naim Sandes]")
    for pEvent in pygame.event.get():

        #Eventos
        match pEvent.type:

            #Ticks
            case pygame.USEREVENT:
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
                    

                #Manejo del Flash
                if (pantalla_id == 1):
                    if (flash_transpariencia > 0):
                        flash_transpariencia -= 4
                    else:
                        flash_transpariencia = 0
                else:
                    flash_transpariencia = 0
                
                #Esto es para lo de la notificacion.
                if (tiempo_msj > 0):
                    tiempo_msj -= 1
            
            ###MOUSE###
            #Movimiento del puntero
            case pygame.MOUSEMOTION:
                if (ingreso_nombre == False):
                    #Esto es para iluminar los botones que seran seleccionados
                    for boton in lista_botones:
                        if (boton.interactuable == True and transicionando == False):
                            if boton.rect_.collidepoint(pEvent.pos):
                                boton.mouse_encima = True
                            else:
                                boton.mouse_encima = False
            
            #Clicks
            case pygame.MOUSEBUTTONDOWN:
                for boton in lista_botones:

                    #Pulso de boton Normal
                    #Solo se ejecutara la accion si es interactuable.
                    if (boton.interactuable == True and transicionando == False and ingreso_nombre == False):
                        if boton.rect_.collidepoint(pEvent.pos):
                            activarOpciones = False

                            if (type(boton) == claseBoton):
                                reiniciar = (boton.accion_ == 10)   #Ya sabremos si es true o false si la condicion se cumple.
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
                                    
                                    #En caso de que vayamos al de preguntar o estemos volviendo de ahi, reiniciaremos 
                                    #todos sus valores.
                                    if (prox_pantallaid == 1 or pantalla_id == 1):
                                        reiniciar = True

                                elif (mi_accion == 9):     #Habilitacion de las preguntas.
                                    
                                    if (preguntas_habilitadas == False):
                                        preguntas_habilitadas = True
                                        prg_actual = 0

                                        if (modo_aleatorio):
                                            prg_actual = random.randint(0, maximo_preguntas)
                                    
                                        #Esto reactiva la musica.
                                        if (musica_actual == None):
                                            volumen_real[0] = volumen[0]
                                            musica_actual = definir_musica(1, volumen_real[0])

                                        activarOpciones = True
                                    else:
                                        reproducir_sonido = False

                                if (reproducir_sonido):
                                    pg_audio_reproducir("Assets\Audio\sndBoton.wav", False, volumen[1])

                            elif (type(boton) == claseBotonOpcion):   #Evento de click para los botones de respuesta.
                                if (boton.tomar_decision(respuestas[prg_actual], volumen[1]) == True):
                                    if (intentos_disponibles > 0):
                                        flash_transpariencia = 128
                                        flash = True
                                        puntaje += 10
                                        contador_preguntas += 1
                                        activarOpciones = True

                                        #Esto decidira la siguiente pregunta.
                                        if (contador_preguntas >= maximo_preguntas):
                                            if (modo_infinito == False):
                                                for botonOpcion in lista_botones:
                                                    if type(botonOpcion) == claseBotonOpcion:
                                                        botonOpcion.interactuable = False

                                                juego_terminado = True
                                                pg_audio_detener(musica_actual)

                                            prg_actual = 0
                                        else:

                                            #Decision de siguiente pregunta.
                                            if (not modo_aleatorio):
                                                prg_actual += 1
                                            else:
                                                anterior_prg = prg_actual

                                                #Buscamos una pregunta aleatoria de las que hay disponibles
                                                while (prg_actual == anterior_prg):
                                                    prg_actual = random.randint(0, maximo_preguntas)

                                else:
                                    #Mostrar que este boton esta deshabilitado si no era el correcto.
                                    boton.interactuable = False
                                    intentos_disponibles -= 1

                                    #Si se nos acabaron los intentos, detenemos el juego.
                                    if (intentos_disponibles <= 0):

                                        #Para ver si le pediremos o no al usuario su nombre, vamos a
                                        #fijarnos si su puntaje es superior al minimo encontrado del ranking.
                                        #Esto hay que hacerlo al momento porque el ranking cambia con cada nuevo puntaje.
                                        if (puntaje > minimo_puntaje_ranking(top_mejores)[0]):
                                            ingreso_nombre = True

                                        for botonOpcion in lista_botones:
                                            if type(botonOpcion) == claseBotonOpcion:
                                                botonOpcion.interactuable = False

                                        juego_terminado = True
                                        pg_audio_detener(musica_actual)
                                    
                                    actualizar_botones = True

                            #BOTONES DE CHECK
                            elif(type(boton) == claseBotonBandera):
                                boton.check_ = not(boton.check_) #El bool se invierte.
                                
                                #Esto controlara que banderas alterara.
                                match(boton.id_):
                                    case 1 | 2: #Musicas/Sonidos
                                        indice = boton.id_ - 1

                                        if (volumen[indice] == 0):
                                            volumen[indice] = 1
                                        else:
                                            volumen[indice] = 0
                                        
                                        #Esta multiplicacion asegura que solo sea 0.7 (el volumen original de musica) 
                                        #Si el volumen ahora no es 0.
                                        #Se redondea para arriba.
                                        if indice == 0:
                                            volumen[indice] = 0.7 * math.ceil(volumen[indice])
                                        
                                        volumen_ref[indice] = volumen[indice]
                                        volumen_real[indice] = volumen[indice]
                                
                                    case 3: #Estado del flash.
                                        flash_habilitado = boton.check_
                                    
                                    case 4: #Preguntas Infinitas
                                        modo_infinito = boton.check_
                                    
                                    case 5: #Preguntas Infinitas
                                        modo_aleatorio = boton.check_

                                pg_audio_reproducir("Assets\Audio\sndCheck.wav", False, volumen[1])
                                
                            
                            #Esto es para activar los botones de opciones, usados en diversas situaciones.
                            if (activarOpciones):
                                for botonOpcion in lista_botones:
                                    if type(botonOpcion) == claseBotonOpcion:
                                        botonOpcion.interactuable = True
                            
                            #Reinicio del juego
                            if (reiniciar):
                                if (prg_actual > 0 or preguntas_habilitadas):
                                    flash_transpariencia = 128
                                    flash = True

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

            ###TECLADO###
            #Nota: KeyDown es usado para reconocer la backspace y el enter. Todo lo demas se usado TextInput.
            case pygame.KEYDOWN | pygame.TEXTINPUT:
                if (ingreso_nombre):
                    if (pEvent.type == pygame.KEYDOWN):
                        if (pEvent.scancode == 42):
                            nombre_jugador = nombre_jugador[:-1]  #Se le saca el ultim caracter
                        elif (pEvent.scancode == 40):
                            if (contar_elementos(nombre_jugador) > 0):
                                flash = True
                                flash_transpariencia = 128
                                tiempo_msj = 360
                                pg_audio_reproducir("Assets\Audio\sndCheck.wav", False, volumen[1])
                                top_mejores['ranking'].pop(minimo_puntaje_ranking(top_mejores)[1])
                                top_mejores['ranking'].append({'nombre': nombre_jugador, 'puntaje': puntaje})
                                ordenar_ranking(top_mejores)
                                print(top_mejores)
                                ingreso_nombre = False


                    else:   #TextInput
                        if (contar_elementos(nombre_jugador) < 15):
                            nombre_jugador += pEvent.text
                
            #El usuario va a quiere la ventana.
            case pygame.QUIT:
                bucleJuego = False

    #Musica y Fondo
    pantalla.fill(C_NEGRO)    #Aca hay un filling para sobreponer todo lo que estaba antes.
    dibujar_fondo(pantalla, pantalla_id)  #Graficado de los fondos.
    if (musica_actual == None and pantalla_id != 1): #Musica
        musica_actual = definir_musica(pantalla_id, volumen_real[0])

    #Logo de la primera pantalla
    if (pantalla_id == 0):
        pg_dibujar_imagen(pantalla, pygame.image.load("Assets\Imagenes\imgLogo.png"), 
            [resolucion[0] / 2 - 320, 60], 0.5)
    
    #Pantalla de preguntas
    if (pantalla_id == 1):

        #"PUNAJE *** | INTENTOS *"
        pg_crear_texto(pantalla, f"PUNTAJE: {escribir_puntaje(puntaje)} | INTENTOS : {intentos_disponibles}", 
            [resolucion[0] / 2, 80], [255, 65, 65], 30, True)

        #Pregunta
        if (prg_actual >= 0 and prg_actual < len(preguntas)):
            pg_crear_texto(pantalla, f"{preguntas[prg_actual]}", [resolucion[0] / 2, 220], [255, 255, 0], 42, True)

    #Texto del ranking y el mismo ranking
    if (pantalla_id == 3):
        pg_crear_texto(pantalla, f"--Los 7 mejores puntajes--", 
            [resolucion[0] / 2, 80], [250, 250, 45], 65, True)
        
        #Impresion de los mejores y sus nombres
        for i in range(len(top_mejores['ranking'])):
            lista = top_mejores['ranking']

            #El color de texto va a variar dependiendo de que tan alto en el ranking esta el jugador.
            color_texto = [85, 0, 255]
            if (i == 0):    #Primero
                color_texto = [255, 255, 0]
            elif (i == 1):    #Segundo
                color_texto = [150, 150, 150]
            elif (i == 2):    #Tercero
                color_texto = [165, 55, 0]
            pg_crear_texto(pantalla, f"{i+1} . {lista[i]['nombre']}",[resolucion[0] / 2 - 220, 140+(48*i)], color_texto, 48, False)
            pg_crear_texto(pantalla, f"{escribir_puntaje(lista[i]['puntaje'])}",[resolucion[0] / 2 + 150, 140+(48*i)], color_texto, 48, False)

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

    if (pantalla_id == 1):
        pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Assets\Imagenes\imgFlash.png"), 1, flash_transpariencia)

        #Cuadro para poner el nombre.
        if (ingreso_nombre == True):
            #Esta imagen es para permitir enfocar mejor el recuadro del nombre.
            pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Assets\Imagenes\imgDesvanecimiento.png"), 1, 225)
            pg_crear_texto(pantalla, "Porfavor Ingrese su nombre", [resolucion[0] / 2, resolucion[1] / 2 - 60], C_BLANCO, 60, True)
            pg_dibujar_rectangulo(pantalla, C_GRIS, [resolucion[0] / 2 - 168, resolucion[1] / 2 + 16], [400, 48], 1)
            pg_dibujar_rectangulo(pantalla, C_BLANCO, [resolucion[0] / 2 - 200, resolucion[1] / 2], [400, 48], 1)
            pg_crear_texto(pantalla, nombre_jugador, [resolucion[0] / 2, resolucion[1] / 2 + 25], C_NEGRO, 50, True)
            pg_crear_texto(pantalla, "Presione ENTER si termino", [resolucion[0] / 2, resolucion[1] / 2 + 120], C_BLANCO, 60, True)

    if (tiempo_msj > 0):
        pg_crear_texto(pantalla, "Tu puntaje ha sido guardado!", [0, 640-32], [0, 255, 0])
        
    pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Assets\Imagenes\imgDesvanecimiento.png"), 1, trsc_transpariencia)
    pygame.display.flip()   #Actualiza el dibujado de la pantalla

#Esto va a modificar el ranking cuando termine el bucle del juego.
crear_archivo_diccionario("Preguntados_Ranking", "json", top_mejores)

pygame.quit() # Fin