import pygame   #Importacion de la libreria.
import json as jsonFunciones
import os as SistemaOperativo

#Constantes
#Para normalmente referenciar los ejes X e Y, voy a usar estas 2 constantes por si necesitamos algun cambio.
CX = 0
CY = 1

#Colores Basicos
C_NEGRO = [0, 0, 0]
C_GRIS = [128, 128, 128]
C_BLANCO = [255, 255, 255]

'''
FUNCIONES GENERALES

que no necesariamente tienen que ver mucho con las funciones orientadas a PyGame...
'''

def contar_elementos(elementos) -> int:
    '''
        Cuenta la cantidad de elementos dentro de un objeto iterable.
        Recibe string/lista.
        Retorna la cantidad de caracteres de una cadena o la cantidad de elementos de una lista.
    '''

    contador = 0
    for i in elementos:
        contador += 1

    return contador

#Funcion tomada de mi biblioteca original.
def crear_archivo_diccionario(nombre_archivo: str, formato_archivo: str, contenido : dict):
    '''
        Crea un archivo en base al contenido de un diccionario.

        Args
        nombre_archivo (str) : Nombre del archivo de salida.
        formato_archivo (str) : Formato del archivo de salida.
        contenido (dict) : El contenido del archivo, en esta funcion debe de ser un diccionario (DICT).
    '''

    if (type(contenido) != dict): #Solo se aceptara contenido que sea diccionario.
        print("El contenido dado no es un diccionario!")
    else:
        with open(f"{nombre_archivo}.{formato_archivo}","w") as archivo:
            if (formato_archivo.lower() == "json"):
                jsonFunciones.dump(contenido,archivo,indent=4,ensure_ascii=False)
            else:
                texto = ""
                for juego in contenido['juegos']:
                    texto += f"{juego['nombre']} - {juego['empresa']},"
                
                archivo.write(texto)

#Funcion tomada de mi biblioteca original.
def leer_archivo_json(ruta: str):
    '''
        Lee un archivo JSON, devolvera los datos leidos del JSON.

        Args
        ruta (str) : Ruta del archivo.
    '''
    datos_json = {}
    if (SistemaOperativo.path.exists(ruta)):
        with open(ruta,"r") as archivo:
            datos_json = jsonFunciones.load(archivo)
    
    return datos_json

def validar_lista(lista : list, max_elementos : int, msg : str, val_pred : int = 0):
    if (type(lista) != list):
        lista = [lista]
    
    if (len(lista) < max_elementos or len(lista) > max_elementos):
        lista = []
        for i in range(max_elementos):
            lista.append(val_pred)
        print(msg)
    
    return lista

def ordenar_ranking(diccionario: dict) -> list:
    '''
        Se devolvera una lista con el ranking ya ordenado.
        Args
        diccionario (dict) : Diccionario con el ranking

        Return
        ranking_ordenado (list) : Lista con el ranking ordenado.
    '''

    ranking_ordenado = []

    if (contar_elementos(diccionario) > 0):
        ranking_ordenado = diccionario['ranking']

        #Compararemos entre si todos los elementos. (Burbujeo)
        for i in range(contar_elementos(ranking_ordenado)-1):
            for j in range(i+1, contar_elementos(ranking_ordenado)):

                dato1 = ranking_ordenado[i]['puntaje']
                dato2 = ranking_ordenado[j]['puntaje']

                #Swapeo de datos.
                if (dato1 < dato2):
                    aux = ranking_ordenado[i]
                    ranking_ordenado[i] = ranking_ordenado[j]
                    ranking_ordenado[j] = aux
    
    return ranking_ordenado

'''
FUNCIONES ORIENTADAS A PYGAME

Mas que nada dibujado de formas!
'''
def pg_dibujar_circulo(pantalla : pygame.surface, color : list, ubicacion : list, radio : int):
    #Verficaciones
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")
    radio = int(radio)

    #Args: Pantalla a dibujar sobre, color, [X, Y], radio.
    pygame.draw.circle(pantalla, color, ubicacion, radio)

def pg_dibujar_rectangulo(pantalla : pygame.surface, color : list, ubicacion : list, tamanio : list, radio_bordes : int = -1):
    #Verficaciones
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")
    if (len(tamanio) == 1):
        tamanio.append(tamanio_r[0])
    else:
        tamanio = validar_lista(tamanio, 2, "Tamaño Invalido!")

    #Args: Pantalla a dibujar sobre, color, [X, Y, Ancho, Alto]
    return pygame.draw.rect(pantalla, color, [ubicacion[CX], ubicacion[CY], tamanio[0], tamanio[1]], 0, radio_bordes)

def pg_dibujar_linea(pantalla : pygame.surface, color : list, ubicacion_in : list, ubicacion_fi : list, tamanio : int = 1):
    #Verficaciones
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion_in = validar_lista(ubicacion_in, 2, "Ubicacion Inicial Invalida!", 1)
    ubicacion_fi = validar_lista(ubicacion_fi, 2, "Ubicacion Final Invalida!", 1)
    tamanio = int(tamanio)

    pygame.draw.line(pantalla, color, ubicacion_in, ubicacion_fi, tamanio)

def pg_titulo(texto : str):
    pygame.display.set_caption(texto)

def pg_crear_texto(pantalla : pygame.surface, texto : str, ubicacion : list, color : list = [0, 0, 0], tamanio : int = 25, centrado : bool = False, fuente : str = "Arial Narrow"):
    #Verificaciones
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")
    
    #Creacion y Impresion del texto.
    fuente = pygame.font.SysFont(fuente, tamanio)
    texto_instancia = fuente.render(texto, True, color)

    if (centrado):
        pantalla.blit(texto_instancia, [ubicacion[CX] - fuente.size(texto)[CX] / 2, ubicacion[CY] - fuente.size(texto)[CY] / 2])
    else:
        pantalla.blit(texto_instancia, ubicacion)

def pg_dibujar_imagen(pantalla : pygame.surface, imagen : pygame.image, ubicacion : list, escala : float = 1.0, angulo : float = 0.0, transparencia : int = 255):
    #Verificaciones
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")

    imagen = pygame.transform.scale_by(imagen, escala)
    imagen = pygame.transform.rotate(imagen, angulo)
    imagen.set_alpha(transparencia)
    pantalla.blit(imagen, ubicacion)
    

def pg_extraer_frames(imagen : pygame.image, frames : int = 1, tamanio_frames : list = [16, 16]) -> list:
    tamanio_frames = validar_lista(tamanio_frames, 2, "Tamaño de frames Invalido!")
    frames_ = []
    frames_definidos = 0
    recortes = [imagen.get_width() / tamanio_frames[0], imagen.get_height() / tamanio_frames[1]]

    for i in range(round(recortes[0])):
        #Esto va a operar hasta que tengamos todos los frames definidos
        if (frames_definidos > frames):
            break
        for j in range(round(recortes[1])):
            if (frames_definidos > frames):
                break
            celday = tamanio_frames[CY] * i
            celdax = tamanio_frames[CX] * j
            frames_.append(imagen.subsurface(celdax, celday, tamanio_frames[CX], tamanio_frames[CY]))
            
            frames_definidos += 1
    
    return frames_

def pg_dibujar_boton(pantalla : pygame.surface, texto : str = "Boton", ubicacion : list = [0, 0], tamanio = [32, 24], color : list = C_BLANCO, color_borde : list = C_NEGRO, color_texto : list = C_NEGRO):
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion de boton Invalida!")
    tamanio = validar_lista(tamanio, 2, "Tamaño Invalido!")

    #Primero el borde (que es un rectangulo un poco mas garande detras del real) y el rectangulo.
    radio_rect = 25
    pg_dibujar_rectangulo(pantalla, color_borde, [ubicacion[CX] - 4, ubicacion[CY] - 4], [tamanio[CX] + 8, tamanio[CY] + 8], radio_rect)
    rect = pg_dibujar_rectangulo(pantalla, color, ubicacion, tamanio, radio_rect)

    #Esto obtendra los extremos del boton para ubicar el texto y las lineas.
    ub_derecha = ubicacion[CX] + tamanio[CX]
    ub_inferior = ubicacion[CY] + tamanio[CY]
    ub_centro = [ubicacion[CX] + (tamanio[CX] / 2), ubicacion[CY] + (tamanio[CY] / 2)]

    #Dibujado del texto
    pg_crear_texto(pantalla, texto, ub_centro, C_NEGRO, 32, True)

    #Esto va a retornar el Rect del boton para detectar colisiones.
    return rect

def pg_dibujar_imagen_repetida(pantalla : pygame.surface, imagen_arg : pygame.image, imagen_escala : float = 1.0, transparencia : int = 255):
    #Esto va a dibujar una imagen repetidamente en toda la pantalla.
    #Va primero de arriba hacia abajo, pasando luego para la derecha.
    posicion = [0, 0]
    imagen = pygame.transform.scale_by(imagen_arg, imagen_escala)
    imagen.set_alpha(transparencia)

    for i in range(pantalla.get_width()):
        for j in range(pantalla.get_height()):
            if (posicion[CY] > pantalla.get_height()):
                break

            #Dibujado de imagen.
            pantalla.blit(imagen, posicion)
            posicion[CY] += imagen.get_height()
        
        if (posicion[CX] > pantalla.get_width()):
            break

        posicion = [posicion[CX] + imagen.get_width(), 0]


'''
APARTADO DE AUDIO

Aviso de que estas funciones solo podran ser usadas luego de haber inicializado el mixer.
'''
def pg_audio_reproducir(ruta_musica : str, bucle : bool = False, volumen : float = 1.0):
    pygame.mixer.music.set_volume(volumen)
    sonido = pygame.mixer.Sound(ruta_musica)
    sonido.set_volume(volumen)

    #Esto evitara que el volumen se salga de 1 o 0.
    if (volumen > 1.0):
        volumen = 1.0
    elif (volumen < 0.0):
        volumen = 0.0
    
    if (bucle == True):
        sonido.play(-1)
    else:
        sonido.play()

    return sonido

def pg_audio_detener(sonido : pygame.mixer.Sound):
    sonido.stop()

def pg_audio_cambiarvolumen(sonido : pygame.mixer.Sound, volumen_nuevo : float = 0.0):
    if (volumen_nuevo > 1.0):
        volumen_nuevo = 1.0
    elif (volumen_nuevo < 0.0):
        volumen_nuevo = 0.0
    
    sonido.set_volume(volumen_nuevo)

#El puntaje va con 3 digitos, asi que para escribirlo usaremos este metodo.
def escribir_puntaje(puntj : int) -> str:
    ret = ""

    #Condiciones anidadas.
    if (puntj <= 9):
        ret = f"00{puntj}"
    else:
        if (puntj <= 99):
            ret = f"0{puntj}"
        else:
            if (puntj <= 999):
                ret = f"{puntj}"
            else:
                ret = "999"
    
    return ret

#Esto es para ya pre-dibujar los fondos sin mucho lio.
def dibujar_fondo(pantalla : pygame.surface, pantalla_id : int):
    match(pantalla_id):
        case 0:
            pg_dibujar_imagen_repetida(pantalla, pygame.image.load("Assets\Imagenes\imgFondo2.png"), 5)

        case 1: #Fondo de las preguntas
            pantalla.fill([12, 24, 13])
            pg_dibujar_imagen(pantalla, pygame.image.load("Assets\Imagenes\imgFondo3.png"), [(pantalla.get_width() / 2) - 320, 0], 4)

        case 2: #Fondo de configuracion
            pantalla.fill([17, 18, 40])
            pg_dibujar_imagen(pantalla, pygame.image.load("Assets\Imagenes\imgFondo4.png"), [(pantalla.get_width() / 2) - 320, 0], 4)

        case 3: #Fondo del ranking
            pantalla.fill([62, 42, 12])
            pg_dibujar_imagen(pantalla, pygame.image.load("Assets\Imagenes\imgFondo5.png"), [(pantalla.get_width() / 2) - 320, 0], 4)

#Funcion para definir que musica usar segun la pantalla id.
def definir_musica(pantalla_id : int, volumen : float) -> pygame.mixer_music:
    match(pantalla_id):
        case 1: #Musica de las preguntas (Solo se reproducira si las preguntas ya estan habilitadas!)
            musica = "Assets\Audio\musPreguntas.wav"
        
        case 3: #Musica del Ranking
            musica = "Assets\Audio\musPuntaje.wav"

        case _: #Por defecto se usa la musica del menu.
            musica = "Assets\Audio\musMenu.wav"

    return pg_audio_reproducir(musica, True, volumen)
