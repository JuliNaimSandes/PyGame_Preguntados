import pygame
import math
import sys
import random

#Importe de datos de otros archivos.
from Preguntados_datos import lista as lista_preguntas
from Preguntados_clases import *    #Importe de Clases
from Preguntados_libreria import *     #Las funciones!

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
botones_opcion_pos = [ub_boton_y, ub_boton_y+64, ub_boton_y+128]#Esto va a tener la ubicacion (y) de los botones de opciones.

#Definicion de botones
lista_botones = [
    claseBoton("Jugar", [ub_boton_x, ub_boton_y-tam_boton[1]-sep_botones], tam_boton, [2, 1], 0),
    claseBoton("Ver Puntajes", [ub_boton_x, ub_boton_y], tam_boton, [2, 3], 0),
    claseBoton("Salir", [ub_boton_x, ub_boton_y+(tam_boton[1]+sep_botones)*2], tam_boton, [0, 0], 0),
    claseBoton("Pregunta", [ub_boton_x, 120], tam_boton, [3, 0], 1),
    claseBoton("Reiniciar", [ub_boton_x + round((resolucion[0] / 2) / 2), 556], tam_boton, [4, 0], 1),
    claseBoton("Configuracion", [ub_boton_x, ub_boton_y+tam_boton[1]+sep_botones], tam_boton, [1, 2], 0),
    claseBoton("Volver", [64, 64], tam_boton, [1, 0], 2),
    claseBoton("Volver", [ub_boton_x, 556], tam_boton, [2, 0], 3),
    claseBotonOpcion("A", [(resolucion[0] / 2) - 240, botones_opcion_pos[0]], 1),
    claseBotonOpcion("B", [(resolucion[0] / 2) - 240, botones_opcion_pos[1]], 1),
    claseBotonOpcion("C", [(resolucion[0] / 2) - 240, botones_opcion_pos[2]], 1),
    claseBoton("Volver", [ub_boton_x - round((resolucion[0] / 2) / 2), 556], tam_boton, [2, 0], 1),
    claseBotonBandera(1, "Musica", [resolucion[0] / 2, 164], True, 2),
    claseBotonBandera(2, "Sonidos",[resolucion[0] / 2, 164+sep_botones_check], True, 2),
    claseBotonBandera(3, "Flash",[resolucion[0] / 2, 164+(sep_botones_check * 2)], True, 2),
    claseBotonBandera(4, "Modo Infinito",[resolucion[0] / 2, 164+(sep_botones_check * 3)], False, 2),
    claseBotonBandera(5, "Modo Aleatorio",[resolucion[0] / 2, 164+(sep_botones_check * 4)], False, 2)
]


#######################VARIABLES#######################
musica_actual = None            #Inicia en  None, contendra la musica correspondiente a pantalla_id.
trsc_transpariencia = 255       #Transparencia de la imagen de transicion
transicionando = True           #Bool para saber si estamos en medio de una transicion.
prox_pantallaid = 0             #Al final de cada transicion, se cambiara pantalla_id a este valor.
tipo_transicion = 0             #0 = Desvanacer; 1 = Aparecer
volumen = [1.0, 1.0]            #0 = Volumen para la musica; 1 = Volumen para los sonidos.
puntaje = 0                     #Se ira acumulando con cada pregunta contestada correctamente.
prg_actual = -1                 #Esta variable sera la que buscara el indice de preguntas,opciones y respuestas.
actualizar_botones = True       #Si esta en True, los botones de opciones actualizaran sus propiedades.
intentos_disponibles = 2        #Y esto contara los intentos que aun le quedan al jugador.
nombre_jugador = ""             #Nombre que se registre del jugador si es que su puntaje cumple para estar en los mejores. (3-20 caracteres)
flash_transpariencia = 0        #Transparencia del Flash en la pantalla de preguntas.
flash_habilitado = True         #Si es true, el flash podra ejecutarse con normalidad.
modo_infinito = False           #Si es true, la seccion de preguntas no parara hasta que el usuario pierda.
modo_aleatorio = False          #Si es true, la siguiente pregunta sera una aleatoria de las disponibles.
contador_preguntas = 0          #Cuantas preguntas vamos?
ingreso_nombre = False          #Si es true, en la pantalla de preguntas se le pedira al usuario ingresar el nombre.
tiempo_msj = 0                  #Contador usado para mostrar la notificacion de "Tu puntaje fue guardado!"
reorganizar_altitudes = False   #Si esta true, se va a reorganizar de forma aleatoria la posicion (Y) de los botones de opciones.

#Estas son variables de los datos obtenidos por el json (si es que el archivo existe)
datos_importados = leer_archivo_json("Preguntados_Ranking.json") #Esta variable tendra a los mejores puntajes registrados.
datos_importados['ranking'] = ordenar_ranking(datos_importados)       #Y esto ordenara directamente el ranking.

#Accion
bucleJuego = True
while bucleJuego:
    #ADVERTENCIA DE CHOCLASO!
    pygame.display.set_caption("Preguntados [Julian Naim Sandes]")

    #Musica
    if (musica_actual != None):
        pg_audio_cambiarvolumen(musica_actual, volumen[0] * 0.7)
    else:
        #Definir la musica
        if (pantalla_id != 1):
            musica_actual = definir_musica(pantalla_id, volumen[0] * 0.7)

    for pEvent in pygame.event.get():
        match pEvent.type:  #Eventos
            case pygame.USEREVENT:  #Ticks

                #Transiciones
                if (transicionando):
                    if (tipo_transicion == 0 and trsc_transpariencia > 0):
                        trsc_transpariencia -= 3
                    elif (tipo_transicion == 1 and trsc_transpariencia < 255):
                        trsc_transpariencia += 1
                    else:
                        if (tipo_transicion == 0):
                            transicionando = False #Terminar con la transicion si era un "Fade Out"
                        else:
                            #Esto cambia que elementos mostrar en caso de querer cambiarlo.
                            pantalla_id = prox_pantallaid
                            tipo_transicion = 0
                            musica_actual = None #Esto obligara a redefinir la musica.

                #Manejo del Flash
                if (pantalla_id == 1 and flash_transpariencia > 0):
                    #Esto es para evitar que se mantenga el bordeado de las opciones mientras se mueven
                    for boton in lista_botones:
                        if (type(boton) == claseBotonOpcion):
                            boton.mouse_encima = False

                    flash_transpariencia -= 3
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
                    if (boton.interactuable == True and transicionando == False):
                        reiniciar = False
                        if (boton.rect_ != None and boton.rect_.collidepoint(pEvent.pos)):
                            if (type(boton) == claseBoton) and (boton.rect_.collidepoint(pEvent.pos)):
                                #Nota: Los botones con efecto 0 no hacen NADA.
                                #Con esto comprobamos si el boton es un boton para reiniciar.
                                if (boton.accion_[0] == 4):
                                    reiniciar = True
                                    pg_audio_reproducir("Recursos\Audio\sndBoton.wav", False, volumen[1])
                                else:
                                    #Botones de transicion
                                    #Efecto 1: Cambiar pantalla_id de forma instantanea.
                                    #Efecto 2: Cambiar pantalla_id con transicion incluida.
                                    if (boton.accion_[0] == 1 or boton.accion_[0] == 2):
                                        if (boton.accion_[0] == 2): #Con transicion

                                            #Esto es para detener la musica
                                            if (musica_actual != None):
                                                pg_audio_detener(musica_actual)

                                            transicionando = True
                                            tipo_transicion = 1
                                            prox_pantallaid = boton.accion_[1]
                                        else:   #Sin Transicion
                                            pantalla_id = boton.accion_[1]

                                        #Si estamos en la pantalla vamos a reiniciar las preguntas.
                                        if (pantalla_id == 1):
                                            reiniciar = True
                                        
                                        pg_audio_reproducir("Recursos\Audio\sndBoton.wav", False, volumen[1])
                                    
                                    #Efecto 3: Comienzo del juego (solo funciona en la pantalla de preguntas)
                                    if (boton.accion_[0] == 3):
                                        if (prg_actual < 0 and pantalla_id == 1):
                                            if (modo_aleatorio):
                                                prg_actual = random.randint(0, contar_elementos(preguntas))
                                            else:
                                                prg_actual = 0
                                        
                                            #Esto reactiva la musica.
                                            if (musica_actual == None):
                                                musica_actual = definir_musica(1, volumen[0])

                                            cambiar_interactuable_c(lista_botones, True)
                                            pg_audio_reproducir("Recursos\Audio\sndBoton.wav", False, volumen[1])
                                            reorganizar_altitudes = True
                                    
                                    #Efecto 4: Reinicia el juego (arriba esta definido!)
                                    #Efecto 5: Salir del juego
                                    if (boton.accion_[0] == 5):
                                        bucleJuego = False         
                            elif (type(boton) == claseBotonOpcion):   #Evento de click para los botones de respuesta.

                                #Nos fijaremos si el boton pulsado dio que la respuesta correcta
                                if (boton.tomar_decision(respuestas[prg_actual], volumen[1]) == True):
                                    if (intentos_disponibles > 0):
                                        flash_transpariencia = 128
                                        puntaje += 10
                                        contador_preguntas += 1
                                        cambiar_interactuable_c(lista_botones, True)
                                        reorganizar_altitudes = True

                                        #Si ya nos quedamos sin preguntas y el modo infinito no esta activo, fin del juego.
                                        if (contador_preguntas >= contar_elementos(preguntas)):
                                            if (modo_infinito == False):
                                                prg_actual = -1
                                                contador_preguntas = 0
                                                cambiar_interactuable_c(lista_botones, False)
                                                pg_audio_detener(musica_actual)

                                                if (puntaje > minimo_puntaje_ranking(datos_importados)[0]):
                                                    ingreso_nombre = True
                                        else:
                                            #Decision de siguiente pregunta.
                                            if (modo_aleatorio == False):
                                                prg_actual += 1
                                            else:
                                                anterior_prg = prg_actual

                                                #Buscamos una pregunta aleatoria de las que hay disponibles
                                                while (prg_actual == anterior_prg):
                                                    prg_actual = random.randint(0, contar_elementos(preguntas))

                                else:   #Caso contrario a que la respuesta sea la correcta:
                                    #Mostrar que este boton esta deshabilitado si no era el correcto.
                                    boton.interactuable = False
                                    intentos_disponibles -= 1

                                    #Si se nos acabaron los intentos, detenemos el juego.
                                    if (intentos_disponibles <= 0):

                                        #Para ver si le pediremos o no al usuario su nombre, vamos a
                                        #fijarnos si su puntaje es superior al minimo encontrado del ranking.
                                        #Esto hay que hacerlo al momento porque el ranking cambia con cada nuevo puntaje.
                                        if (puntaje > minimo_puntaje_ranking(datos_importados)[0]):
                                            ingreso_nombre = True

                                        cambiar_interactuable_c(lista_botones, False)
                                        pg_audio_detener(musica_actual)
                                    
                                    actualizar_botones = True

                            #BOTONES DE CHECK
                            elif(type(boton) == claseBotonBandera):
                                boton.check_ = not(boton.check_) #El bool se invierte.
                                pg_audio_reproducir("Recursos\Audio\sndCheck.wav", False, volumen[1])

                                #Esto controlara que banderas alterara.
                                match(boton.id_):
                                    case 1 | 2: #Musicas/Sonidos
                                        indice = boton.id_ - 1

                                        #Muteado/Desmuteado de la musica/los sonidos.
                                        if (boton.check_):
                                            volumen[indice] = 1
                                        else:
                                            volumen[indice] = 0
                                
                                    case 3: #Estado del flash.
                                        flash_habilitado = boton.check_
                                    
                                    case 4: #Preguntas Infinitas
                                        modo_infinito = boton.check_
                                    
                                    case 5: #Preguntas Infinitas
                                        modo_aleatorio = boton.check_
                                            
                        #Reinicio del juego
                        if (reiniciar):
                            if (prg_actual > 0):
                                flash_transpariencia = 128

                            puntaje = 0

                            if (musica_actual != None):
                                pg_audio_detener(musica_actual)

                            musica_actual = None
                            prg_actual = -1
                            intentos_disponibles = 2
                            cambiar_interactuable_c(lista_botones, False)
                            actualizar_botones = True

            ###TECLADO###
            #Nota: KeyDown es usado para reconocer el Backspace y el Enter usando scancode. 
            #Todo lo demas se usado TextInput.
            case pygame.KEYDOWN | pygame.TEXTINPUT:
                if (ingreso_nombre):
                    if (pEvent.type == pygame.KEYDOWN):
                        if (pEvent.scancode == 42): #(Si se presiona Backspace)
                            nombre_jugador = borrar_ultimocaracter(nombre_jugador)  #Se le saca el ultimo caracter
                        elif (pEvent.scancode == 40):   #(Si se presiona Enter)
                            if (contar_elementos(nombre_jugador) > 0):
                                flash_transpariencia = 128
                                tiempo_msj = 360
                                pg_audio_reproducir("Recursos\Audio\sndCheck.wav", False, volumen[1])
                                datos_importados['ranking'].pop(minimo_puntaje_ranking(datos_importados)[1])
                                datos_importados['ranking'].append({'nombre': nombre_jugador, 'puntaje': puntaje})
                                ordenar_ranking(datos_importados)
                                ingreso_nombre = False
                    else:
                        #El nombre solo podra soportar 15 caracteres.
                        if (contar_elementos(nombre_jugador) < 15):
                            nombre_jugador += pEvent.text
                
            #Si el usuario quiere cerrar el juego, terminemos con el bucle!
            case pygame.QUIT:
                bucleJuego = False

    #Musica y Fondo
    pantalla.fill(C_NEGRO)    #Aca hay un filling para sobreponer todo lo que estaba antes.
    dibujar_fondo(pantalla, pantalla_id)  #Graficado de los fondos.

    #Logo de la primera pantalla
    if (pantalla_id == 0):
        pg_dibujar_imagen(pantalla, pygame.image.load("Recursos\Imagenes\imgLogo.png"), 
            [resolucion[0] / 2 - 320, 60], 0.5)
    
    #Pantalla de preguntas
    if (pantalla_id == 1):

        #"PUNAJE *** | INTENTOS *"
        pg_crear_texto(pantalla, f"PUNTAJE: {escribir_puntaje(puntaje)} | INTENTOS : {intentos_disponibles}", 
            [resolucion[0] / 2, 80], [255, 65, 65], 30, True)

        #Pregunta
        if (prg_actual >= 0 and prg_actual < contar_elementos(preguntas)):
            pg_crear_texto(pantalla, f"{preguntas[prg_actual]}", [resolucion[0] / 2, 220], [255, 255, 0], 42, True)

    #Texto del ranking y el mismo ranking
    if (pantalla_id == 3):
        pg_crear_texto(pantalla, f"--Los 7 mejores puntajes--", 
            [resolucion[0] / 2, 80], [250, 250, 45], 65, True)
        
        #Impresion de los mejores y sus nombres
        for i in range(contar_elementos(datos_importados['ranking'])):
            lista = datos_importados['ranking']

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
    altura_elegida = 0
    altitudes_disponibles = []
    for ypos in botones_opcion_pos:
        altitudes_disponibles.append(ypos)
    
    for boton in lista_botones:
        if (boton.elemento_id == pantalla_id):
            #Solo se volvera interactuable ahora si es un boton normal
            #Pero si es uno de opcion, entonces no se podra interactuar hasta
            #que las preguntas esten habilitadas.
            if (actualizar_botones):
                if (type(boton) == claseBotonOpcion):
                    #Esto es para cambiar la posicion (y) de las opciones de forma aleatoria.
                    #Un intento mio de evitar que hacer click en el mismo lugar de antes sea justo la respuesta correcta.
                    if (reorganizar_altitudes == True):
                        altura_elegida = random.randint(0, (contar_elementos(altitudes_disponibles)-1))
                        boton.ubicacion_ = [boton.ubicacion_[0], altitudes_disponibles[altura_elegida]]
                        altitudes_disponibles.pop(altura_elegida)

                    #Esto cambiara el texto de las opciones por las respuestas.
                    if (prg_actual > -1 and prg_actual < contar_elementos(preguntas)):
                        #Vamos a referenciar la opcion con el indice de la letra de la opcion en numero.
                        #Esto se puede calcular facil con una tabla ASCII, aca la "a" es 61.
                        boton.respuesta_ = opciones[prg_actual][ord(boton.opcion_)-65]
                    else:
                        boton.respuesta_ = ""
                else:
                    boton.interactuable = True
        else:
            boton.interactuable = False
        
        boton.dibujar(pantalla, pantalla_id)

    #Esto es para asegurar que no se vuelva a revolver.
    if (reorganizar_altitudes == True):
        reorganizar_altitudes = False
    
    if (pantalla_id == 1):
        #Dibujado del flash
        if (flash_habilitado):
            pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Recursos\Imagenes\imgFlash.png"), 
            1, flash_transpariencia)

        #Cuadro para poner el nombre.
        if (ingreso_nombre == True):

            #Esta imagen es para permitir enfocar mejor el recuadro del nombre.
            pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Recursos\Imagenes\imgDesvanecimiento.png"), 1, 225)
            pg_crear_texto(pantalla, "Porfavor Ingrese su nombre", [resolucion[0] / 2, resolucion[1] / 2 - 60], C_BLANCO, 60, True)
            pg_dibujar_rectangulo(pantalla, C_GRIS, [resolucion[0] / 2 - 168, resolucion[1] / 2 + 16], [400, 48], 1)
            pg_dibujar_rectangulo(pantalla, C_BLANCO, [resolucion[0] / 2 - 200, resolucion[1] / 2], [400, 48], 1)
            pg_crear_texto(pantalla, nombre_jugador, [resolucion[0] / 2, resolucion[1] / 2 + 25], C_NEGRO, 50, True)
            pg_crear_texto(pantalla, "Presione ENTER si termino", [resolucion[0] / 2, resolucion[1] / 2 + 120], C_BLANCO, 60, True)

    if (tiempo_msj > 0):
        pg_crear_texto(pantalla, "Tu puntaje ha sido guardado!", [0, 640-32], [0, 255, 0])
        
    pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Recursos\Imagenes\imgDesvanecimiento.png"), 1, trsc_transpariencia)
    pygame.display.flip()   #Actualiza el dibujado de la pantalla

#Esto va a modificar los datos que se obtuvieron antes del bucle por los nuevos.
crear_archivo_diccionario("Preguntados_Ranking", "json", datos_importados)

pygame.quit() # Fin