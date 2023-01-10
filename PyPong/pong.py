import pygame
import random

from pygame.locals import QUIT

ANCHO = 800
ALTO = 600

FPS = 30
BLANCO = (255,255,255)
GRIS = (144,144,144)
NEGRO = (0,0,0)

class Pelota:
    golaso = False
    golaso_ia = False
    def __init__(self,imagen_fichero):
        self.imagen = pygame.image.load(imagen_fichero).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        
        #POSICION NEUTRA
        #self.posicion = self.x=(ANCHO/2 - self.ancho/2), self.y = (ALTO/2 - self.alto/2)
        
        self.x = ANCHO/2 - self.ancho/2
        self.y = ALTO/2 - self.alto/2
        #DONDE MIRA
        self.dir_x = 0
        self.dir_y = 0
        
        self.puntuacion = 0
        self.puntuacion_ia = 0
        self.last_winner = 0
        
    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y
    
    def colision(self):
        if self.x<=0:
            self.reset()
            self.golaso = True
            self.puntuacion_ia += 1
        if self.x + self.ancho >= ANCHO:
            self.reset()
            self.golaso_ia = True
            self.puntuacion += 1
        if self.y<=0:
            self.dir_y = -self.dir_y
        if self.y+self.alto >= ALTO:
            self.dir_y = -self.dir_y
    
    def reset(self):
        self.x = ANCHO/2 - self.ancho/2
        self.y = ALTO/2 - self.alto/2
        self.dir_x = - self.dir_x
        self.dir_y = random.choice([-5, 5])

class Raqueta:
    def __init__(self):
        self.image = pygame.image.load("Assets\\flex_tape.png").convert_alpha()
        pygame.sprite.Sprite
        
        self.ancho, self.alto = self.image.get_size()
        
        self.x = 0
        self.y = ALTO/2 - self.alto/2
        
        self.dir_y = 0
        
    def mover(self):
        self.y += self.dir_y
        if self.y <=0:
            self.y=0
        if self.y >= ALTO - self.alto:
            self.y=ALTO - self.alto
    
    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x * 1.1
            pelota.x = self.x + self.ancho
    
    def mover_ia(self,pelota):
        if self.y > pelota.y :
            self.dir_y = -4
        elif self.y < pelota.y :
            self.dir_y = 4
        else:
            self.dir_y = 0
            
        if self.y <=0:
            self.y=0
        if self.y >= ALTO - self.alto:
            self.y=ALTO - self.alto
            
        self.y += self.dir_y
        
    def golpear_ia(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x * 1.1
            pelota.x = self.x - self.ancho
        
def main():
    pygame.init()
    
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG")
    
    fuente = pygame.font.Font(None, 60)
    
    pelota = Pelota("Assets\\phil_swift.png")
    raquetaJugador = Raqueta()
    raquetaJugador.x = 5
    
    raquetaIA = Raqueta()
    raquetaIA.x = ANCHO - raquetaIA.ancho - 5
    
    jugando = True
    inicio = True
    amenaza = True
    amenaza_ia = True
    
    
    while jugando:
        pygame.mixer.init()
        if inicio:
            raquetaJugador.y = ALTO/2 - raquetaJugador.alto/2
            raquetaIA.y = ALTO/2 - raquetaJugador.alto/2
            pelota.x = ANCHO/2 - pelota.ancho/2
            pelota.y = ALTO/2 - pelota.alto/2
            pelota.dir_x = 0
            pelota.dir_y = 0
            pelota.puntuacion = 0
            pelota.puntuacion_ia = 0
        
        if pelota.golaso:
            raquetaJugador.y = ALTO/2 - raquetaJugador.alto/2
            raquetaIA.y = ALTO/2 - raquetaJugador.alto/2
            pelota.x = raquetaJugador.x + raquetaJugador.ancho
            pelota.y = ALTO/2 - pelota.alto/2
            pelota.dir_x = 0
            pelota.dir_y = 0
            
        if pelota.golaso_ia:
            raquetaJugador.y = ALTO/2 - raquetaJugador.alto/2
            raquetaIA.y = ALTO/2 - raquetaJugador.alto/2
            pelota.x = raquetaIA.x - raquetaIA.ancho
            pelota.y = ALTO/2 - pelota.alto/2
            pelota.dir_x = 0
            pelota.dir_y = 0
            
        pelota.mover()
        pelota.colision()
        
        raquetaJugador.mover()
        raquetaJugador.golpear(pelota)
        
        raquetaIA.mover_ia(pelota)
        raquetaIA.golpear_ia(pelota)
        
        ventana.fill(NEGRO)
        pygame.draw.line(ventana,(BLANCO),(ANCHO/2, ALTO),(ANCHO/2,0))
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raquetaJugador.image,(raquetaJugador.x, raquetaJugador.y))
        ventana.blit(raquetaIA.image,(raquetaIA.x, raquetaIA.y))
        
        if inicio == False:
            texto = f"{pelota.puntuacion}   {pelota.puntuacion_ia}" 
            letrero = fuente.render(texto, False, BLANCO)
            ventana.blit(letrero, (ANCHO/2 - fuente.size(texto)[0]/2, 50))
        elif inicio and pelota.last_winner == 0:
            texto = f"Press space to start"
            letrero = fuente.render(texto, False, BLANCO)
            ventana.blit(letrero, (ANCHO/2 - fuente.size(texto)[0]/2, 50))
        else:
            texto = f"Gana el jugador {pelota.last_winner}"
            letrero = fuente.render(texto, False, BLANCO)
            ventana.blit(letrero, (ANCHO/2 - fuente.size(texto)[0]/2, 50))
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                jugando=False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    raquetaJugador.dir_y = -10
                if evento.key == pygame.K_s:
                    raquetaJugador.dir_y = 10
                if evento.key == pygame.K_SPACE and inicio:
                    pelota.dir_x = random.choice([-5,5])
                    pelota.dir_y = random.choice([-5,5])
                    texto = f"{pelota.puntuacion}   {pelota.puntuacion_ia}"
                    pygame.mixer.Sound("Assets/bomb.mp3").play()
                    pygame.mixer.music.load("Assets/background-theme.mp3")
                    pygame.mixer.music.set_volume(0.15)
                    pygame.mixer.music.play()
                    inicio = False
                    pelota.golaso_ia = False
                if evento.key == pygame.K_SPACE and pelota.golaso:
                    pelota.dir_x = random.choice([-5,5])
                    pelota.dir_y = random.choice([-5,5])
                    pelota.golaso = False
                if evento.key == pygame.K_SPACE and pelota.golaso_ia:
                    pelota.dir_x = random.choice([-5,5])
                    pelota.dir_y = random.choice([-5,5])
                    pelota.golaso_ia = False
                if evento.key == pygame.K_r:
                    inicio = True
            
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w or evento.key == pygame.K_s:
                    raquetaJugador.dir_y = 0
        
        if pelota.puntuacion == 1 and amenaza:
            pygame.mixer.Sound("Assets/xokas-no-juego.mp3").play()
            amenaza = False
        if pelota.puntuacion_ia == 1 and amenaza_ia:
            pygame.mixer.Sound("Assets/xokas-no-juego.mp3").play()
            amenaza_ia = False

        if pelota.puntuacion == 7:
            pelota.last_winner = 1
            pygame.mixer.Sound("Assets/now-thats.mp3").play()
            inicio = True
        elif pelota.puntuacion_ia == 7:
            pelota.last_winner = 2
            pygame.mixer.Sound("Assets/now-thats.mp3").play()
            inicio = True
            
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()