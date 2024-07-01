import pygame
from Preguntados_libreria import *

#Todos los botones seran objetos con esta clase para una manipulacion de como funcionan mas facil.
class claseBoton():
    def __init__(self, texto : str, ubicacion : list, tamanio : list, accion : list, elemento_id : int): #Constructor
        self.texto_ = texto #Texto del boton
        self.ubicacion_ = [round(ubicacion[0]), round(ubicacion[1])]    #Ubicacion en pantalla.
        self.tamanio_ = tamanio #Tamaño del boton

        #Accion sera un valor List que contendra 2 valores, el primero indicara el efecto y el 2do sera para
        #diferenciar que hara con esa accion, algo asi como un definidor de como hara la accion.
        self.accion_ = validar_lista(accion, 2, f"Accion mal definida en {self.texto_}!", 0)
        self.elemento_id = elemento_id
        
        self.color_ = C_BLANCO #Color del rectangulo.
        self.color_borde_ = [0, 65, 255] #Color de los bordes
        self.color_aux_ = self.color_
        self.color_borde_aux_ = self.color_borde_
        self.mouse_encima = False

        #Se define el Rect del boton temporalmente, se modifica cuando se usa su metodo de dibujado.
        self.rect_ = None
        self.interactuable = False #Si esta en true, es posible de interactuar con el boton.
    
    def dibujar(self, pantalla : pygame.surface, pantalla_id : int):
        if (self.elemento_id == pantalla_id):
            if (self.interactuable == True):
                self.color_ = self.color_aux_
                self.color_borde_ = self.color_borde_aux_

                #Se ilumina el borde si esta el mouse encima.
                if (self.mouse_encima):
                    self.color_ = C_BLANCO
                    self.color_borde_ = C_BLANCO
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
        #self.texto_ = f"Opcion {self.opcion_}: {self.respuesta_}"
        self.texto_ = self.respuesta_
        claseBoton.dibujar(self, pantalla, pantalla_id)
    
    #Este metodo se va a fijar si era la respuesta correcta la suya.
    def tomar_decision(self, opcion_correcta : str, volumen : float):
        acierto = False
        if (self.opcion_.lower() == opcion_correcta):
            acierto = True

        #Reproducir sonido dependiendo de que si fue o no correcta la opcion decidida.
        if (acierto):
            pg_audio_reproducir("Recursos\Audio\sndAcierto.wav", False, volumen)
        else:
            pg_audio_reproducir("Recursos\Audio\sndError.wav", False, volumen * 0.75)

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
                imagen = pygame.image.load("Recursos\Imagenes\imgActivado.png")
                if (self.check_ == False):
                    imagen = pygame.image.load("Recursos\Imagenes\imgDesactivado.png")
            else:
                imagen = pygame.image.load("Recursos\Imagenes\imgCheckND.png")
                
            #Dibujado del texto y la imagen.
            pg_crear_texto(pantalla, self.texto_, [self.ubicacion_[0] - self.dist_txtb_, self.ubicacion_[1] + 24], [200, 255, 200], 42, True)
            self.rect_ = pg_dibujar_imagen(pantalla, imagen, [self.ubicacion_[0] + self.dist_txtb_, self.ubicacion_[1]], 3)

#Esto es para camnbiar el estado de interactuables de cualquier clase de boton.
def cambiar_interactuable_c(lista_botones : list, interactuable_arg : bool, clase_arg = claseBotonOpcion):
    for mis_botones in lista_botones:
        if type(mis_botones) == clase_arg:
            mis_botones.interactuable = interactuable_arg