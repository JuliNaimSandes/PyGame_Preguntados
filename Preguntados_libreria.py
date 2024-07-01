import pygame   #Importacion de la libreria.
import json as jsonFunciones
import os as SistemaOperativo

#############CONSTANTES###############
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

def validar_lista(lista : list, elementos_decididos : int, msg : str, val_pred : int = 0):

    '''
        Funcion para validar que la lista cumpla con un minimo de elementos.
        Args
        lista (list) : Lista en cuestion.
        elementos_decididos (int) : Cuantos elementos minimo debe contener la lista.
        msg (str) : El mensaje que se printeara en consola si ocurrio un error. Si no hay nada no se imprime nada.
        val_pred (int [0 pred.]) : Valor que se usara predeterminadamente en caso de indices faltantes.

        return
        ret (str) : La string del valor en el formato "000".
    '''

    if (type(lista) != list):
        lista = [lista]
    
    if (contar_elementos(lista) < elementos_decididos):
        #Si no cumple con lo minimo, entonces crearemos una nueva con elementos del valor predeterminado.
        lista = []
        for i in range(elementos_decididos):
            lista.append(val_pred)
        
        #Impresion del mensaje
        if (contar_elementos(msg) > 0):
            print(msg)
        
        #Aca retornaremos esta lista.
        return lista

    elif contar_elementos(lista) > elementos_decididos:
        #Caso de que se este pasando, entonces devolveremos una lista con solo la cantidad de elementos decididos.
        lista_nueva = []
        for i in range(elementos_decididos):
            lista_nueva.append(lista[i])

        return lista_nueva
    else:
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

def minimo_puntaje_ranking(ranking : dict) -> list:
    
    '''
        Se devolvera una lista de 2 dimensiones, el primer indice contiene el puntaje mas bajo
        y el 2do el indice de donde se encuentra.
        Devolvera false si el ranking esta vacio.
        Args
        ranking (dict) : Diccionario con el ranking

        Return
        minimo (list) : Lista con las caracteristicas antes mencionadas.
    '''

    minimo = False

    if (contar_elementos(ranking) > 0):
        minimo = [None, None]

        for i in range(contar_elementos(ranking['ranking'])):
            puntaje = ranking['ranking'][i]['puntaje']
            if (minimo[0] == None or puntaje < minimo[0]):
                minimo = [puntaje, i]
    
    return minimo

def borrar_ultimocaracter(cadena : str) -> str:
    
    '''
        Va a devolver una cadena con ultimo caracter suyo borrado.
        Args
        cadena (str) : La cadena en cuestion

        Return
        nueva_cadena (str) : La cadena pero sin el ultimo caracter.
    '''

    nueva_cadena = ""

    for i in range(len(cadena)-1):
        nueva_cadena += cadena[i]

    return nueva_cadena

#El puntaje va con 3 digitos, asi que para escribirlo usaremos este metodo.
def escribir_puntaje(puntj : int) -> str:

    '''
        Esto va a escribir un valor en el formato "000".
        Args
        puntj (int) : Valor en cuestion

        return
        ret (str) : La string del valor en el formato "000".
    '''

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

'''
FUNCIONES ORIENTADAS A PYGAME

Mas que nada dibujado de formas!
'''
def pg_dibujar_rectangulo(pantalla : pygame.surface, color : list, ubicacion : list, tamanio : list, radio_bordes : int = -1) -> pygame.rect:
    
    '''
        Va a dibujar un rectangulo de la forma que se dan los argumentos.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara el rectangulo.
        color (list [Maximo 3 Indices]) : El color, con sus respectivos valores RGB.
        ubicacion (list [Maximo 2 Indices]) : La ubicacion (X, Y).
        tamanio (list [Maximo 2 Indices]) : El tamaño (Ancho, Alto). Si en tamanio solo se da una lista de un solo indice, se creara un cuadrado.
        radio_bordes (int [-1 por pred.]) : El radio de las 4 esquinas del rectangulo.

        Return
        rect : El rectangulo ya dibujado, puede ser usado para detectar colisiones.
    '''

    #Verficaciones
    color = validar_lista(color, 3, "Color Invalido!")
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")
    if (contar_elementos(tamanio) == 1):
        tamanio.append(tamanio_r[0])
    else:
        tamanio = validar_lista(tamanio, 2, "Tamaño Invalido!")

    #Args: Pantalla a dibujar sobre, color, [X, Y, Ancho, Alto]
    return pygame.draw.rect(pantalla, color, [ubicacion[CX], ubicacion[CY], tamanio[0], tamanio[1]], 0, radio_bordes)

def pg_crear_texto(pantalla : pygame.surface, texto : str, ubicacion : list, color : list = C_NEGRO, tamanio : int = 25, centrado : bool = False, fuente : str = "Arial Narrow"):
    
    '''
        Va a mostrar un determinado texto en la pantalla.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara el texto.
        texto (str) : Que quieres que se muestre en este texto?.
        ubicacion (list [Maximo 2 Indices]) : La ubicacion (X, Y).
        color (list [Maximo 3 Indices, [0, 0, 0] pred.]) : El color, con sus respectivos valores RGB.
        tamanio (int [25 pred.]) : El tamaño del texto.
        centrado (bool [False pred.]) : Si es true, se centrara con respecto a su posicion de origen.
        fuente (str ["Arial Narrow" pred.]) : La fuente del texto.
    '''
    
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

def pg_dibujar_boton(pantalla : pygame.surface, texto : str = "Boton", ubicacion : list = [0, 0], tamanio = [32, 24], color : list = C_BLANCO, color_borde : list = C_NEGRO, color_texto : list = C_NEGRO):
    
    '''
        Esto va a dibujar la forma predeterminada de un boton, alterar esto alterara cualquier boton.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara la imagen.
        texto (str) : Texto que aparecera dentro del boton, centrado.
        ubicacion (list [Maximo 2 Indices]) : La ubicacion (X, Y).
        tamanio (list [Maximo 2 Indices, [32, 24] pred.]) : El tamaño (Ancho, Alto).
        color (list [Maximo 3 Indices, [255, 255, 255] pred.]) : El color del bloque, con sus respectivos valores RGB.
        color_borde (list [Maximo 3 Indices, [0, 0, 0] pred.]) : El color del borde, con sus respectivos valores RGB.
        color_texto (list [Maximo 3 Indices, [0, 0, 0] pred.]) : El color del texto, con sus respectivos valores RGB.

        Return
        Rect : El boton ya dibujado, puede ser usado para detectar colisiones.
    '''
    
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

def pg_dibujar_imagen(pantalla : pygame.surface, imagen_ruta : str, ubicacion : list, escala : float = 1.0, transparencia : int = 255) -> pygame.rect:
    
    '''
        Va a dibujar una imagen en la pantalla.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara la imagen.
        imagen_ruta (str) : La ruta de la imagen
        ubicacion (list [Maximo 2 Indices]) : La ubicacion (X, Y).
        escala (float [1.0 pred.]) : La escala de la imagen.
        transparencia (int [255 pred.]) : La transpariencia de la imagen.

        Return
        Rect : La imagen ya dibujada, puede ser usado para detectar colisiones.
    '''
    
    #Verificaciones
    ubicacion = validar_lista(ubicacion, 2, "Ubicacion Invalida!")
    imagen = pygame.image.load(imagen_ruta)
    imagen = pygame.transform.scale_by(imagen, escala)
    imagen.set_alpha(transparencia)
    return pantalla.blit(imagen, ubicacion)

def pg_dibujar_imagen_repetida(pantalla : pygame.surface, imagen_ruta : str, imagen_escala : float = 1.0, transparencia : int = 255):
    
    '''
        Va a dibujar una imagen por toda la pantalla repetidamente.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara la imagen.
        imagen_ruta (str) : La ruta de la imagen
        imagen_escala (float [1.0 pred.]) : La escala de la imagen.
        transparencia (int [255 pred.]) : La transpariencia de la imagen.
    '''
    
    #Esto va a dibujar una imagen repetidamente en toda la pantalla.
    #Va primero de arriba hacia abajo, pasando luego para la derecha.
    posicion = [0, 0]
    imagen = pygame.image.load(imagen_ruta)
    imagen = pygame.transform.scale_by(imagen, imagen_escala)
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

#Esto es para ya pre-dibujar los fondos sin mucho lio.
def dibujar_fondo(pantalla : pygame.surface, pantalla_id : int):

    '''
        Va a dibujar el fondo dependiendo de su pantalla_id.
        Args
        pantalla (pygame.surface) : La pantalla en donde se dibujara los fondos.
        pantalla_id (int) : Valor para identificar que dibujar.
    '''

    match(pantalla_id):
        case 0:
            pg_dibujar_imagen_repetida(pantalla, "Recursos\Imagenes\imgFondo2.png", 5)

        case 1: #Fondo de las preguntas
            pantalla.fill([12, 24, 13])
            pg_dibujar_imagen(pantalla, "Recursos\Imagenes\imgFondo3.png", [(pantalla.get_width() / 2) - 320, 0], 4)

        case 2: #Fondo de configuracion
            pantalla.fill([17, 18, 40])
            pg_dibujar_imagen(pantalla, "Recursos\Imagenes\imgFondo4.png", [(pantalla.get_width() / 2) - 320, 0], 4)

        case 3: #Fondo del ranking
            pantalla.fill([62, 42, 12])
            pg_dibujar_imagen(pantalla, "Recursos\Imagenes\imgFondo5.png", [(pantalla.get_width() / 2) - 320, 0], 4)

'''
APARTADO DE AUDIO

Aviso de que estas funciones solo podran ser usadas luego de haber inicializado el mixer.
'''
def pg_audio_reproducir(ruta_musica : str, bucle : bool = False, volumen : float = 1.0):

    '''
        Va a reproducir una pista de audio.
        Args
        ruta_musica (str) : La ruta del audio
        bucle (bool) : Si es true, se reproducira el sonido indefinidamente.
        volumen (float [1.0 pred.]) : El volumen, maximo 1.0.

        return
        sonido : El sonido ya reproducido, puede ser atajado.
    '''

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
    
    '''
        Detendra un sonido de su reproduccion, util con los que tienen bucle.
        Args
        sonido (pygame.mixer.Sound) : El sonido en cuestion, ya reproucido.
    '''
    
    if (sonido != None):
        sonido.stop()

def pg_audio_cambiarvolumen(sonido : pygame.mixer.Sound, volumen_nuevo : float = 0.0):
    
    '''
        Cambiara el volumen del audio (ya reproducido) dado.
        Args
        sonido (pygame.mixer.Sound) : Audio en cuestion.
        volumen_nuevo (float [0.0 pred.]) : Nuevo volumen.
    '''

    if (sonido != None):
        if (volumen_nuevo > 1.0):
            volumen_nuevo = 1.0
        elif (volumen_nuevo < 0.0):
            volumen_nuevo = 0.0
        
        sonido.set_volume(volumen_nuevo)

#Funcion para definir que musica usar segun la pantalla id.
def definir_musica(pista : int, volumen : float) -> pygame.mixer_music:
    '''
        Va a reproducir una musica dependiendo del valor dado de pista.
        Args
        pista (int) : Que pista reproducira dependiendo del valor.
        volumen (float) : Volumen de la musica.
    '''

    match(pista):
        case 1: #Musica de las preguntas (Solo se reproducira si las preguntas ya estan habilitadas!)
            musica = "Recursos\Audio\musPreguntas.wav"
        
        case 3: #Musica del Ranking
            musica = "Recursos\Audio\musPuntaje.wav"

        case _: #Por defecto se usa la musica del menu.
            musica = "Recursos\Audio\musMenu.wav"

    return pg_audio_reproducir(musica, True, volumen)