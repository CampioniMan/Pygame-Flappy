from pygame import *
import sys
from random import randint

init()

#
#	VARIÁVEIS GLOBAIS PARA O PRÓPRIO PYGAME
#

SCREEN_WIDTH, SCREEN_HEIGHT, CANO_WIDTH, CANO_HEIGHT, MARIO_WIDTH, MARIO_HEIGHT, ESPACO_ENTRE_CANOS, MINIMO_ALTURA_CANO, PORCENAGEM_ERRO_COLISAO = 640, 480, 50, 450, 48, 52, 150, 70, 95.0/100.0
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
display.set_caption('Flappy Mario')
surface = Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
screen.blit(surface, (0,0))

#
#	CLASSES DO PROGRAMA
#

class Mario(object):
	def __init__(self, inicioX, inicioY):
		self.indiceProX = 10
		self.myimage = [image.load("1.png").convert_alpha(), image.load("2.png").convert_alpha()]
		self.pos = [inicioX, inicioY]
		self.inicioX = inicioX
		self.inicioY = inicioY
		self.morreu = False

	def desenhar(self, surf):
		if self.indiceProX < 25:
			surf.blit(self.myimage[0], (self.pos[0], self.pos[1]))
		else:
			surf.blit(self.myimage[1], (self.pos[0], self.pos[1]))

	#-((indiceProX^2)/25) + indiceProX
	def cair(self):
		if not self.morreu:
			self.pos[1] -= -((self.indiceProX * self.indiceProX) / 25) + self.indiceProX
			self.indiceProX += 1

	def pular(self):
		if  (self.pos[1] >= -MARIO_HEIGHT):
			self.indiceProX = 10

	def bateuNumCano(self, cano):
		return (cano.pos[0] <= PORCENAGEM_ERRO_COLISAO * (self.pos[0] + MARIO_WIDTH) and PORCENAGEM_ERRO_COLISAO * (cano.pos[0] + CANO_WIDTH) >= self.pos[0]) and \
			   (cano.pos[1] <= PORCENAGEM_ERRO_COLISAO * (self.pos[1] + MARIO_HEIGHT) and PORCENAGEM_ERRO_COLISAO * (cano.pos[1] + CANO_HEIGHT) >= self.pos[1])

	def bateuNasBordas(self):
		return (self.pos[1] >= SCREEN_HEIGHT-MARIO_HEIGHT)

	def resetar(self):
		self.pos = [self.inicioX,self.inicioY]
		self.morreu = False
		self.indiceProX = 10

class Cano(object):
	def __init__(self, aImagem):
		self.myimage = image.load(aImagem).convert_alpha()
		self.pos = [SCREEN_WIDTH, SCREEN_HEIGHT-300]
		self.velocidade = 10.0

	def desenhar(self, surf):
		surf.blit(self.myimage, ((self.pos[0], self.pos[1])))

	def andar(self):
		self.pos[0] -= self.velocidade
		if self.pos[0] <= -CANO_WIDTH:
			self.pos[0] = SCREEN_WIDTH
			return True
		return False

	def set_altura(self, novaAltura):
		self.pos[1] = novaAltura

	def resetar(self):
		self.pos[0] = SCREEN_WIDTH
		self.velocidade = 10.0

	def aumentaVelocidade(self):
		if self.velocidade < 20:
			self.velocidade += 0.5

#
#	PARTE MAIN DO PROGRAMA
#

def main():

	# Variáveis para o funcionamento do jogo
	mario = Mario(0,100)
	canoCima = Cano("5.png")
	canoBaixo = Cano("4.png")
	fundo = (90,120,255)
	margem_calculo = -1
	pontos = 0
	jaPressionou = False

	# Criando as fontes para escrever na tela
	myfont = font.SysFont("Consolas", 25)
	myfontPequena = font.SysFont("Consolas", 10)

	# Labels que serão usados durante o jogo
	labelPerdeu = myfont.render("Você perdeu!", 1, (40,40,40))
	labelPerdeu2 = myfontPequena.render("Aperte [Espaço] para reiniciar", 1, (40,40,40))
	labelInicial = myfont.render("Aperta [UP] ou [W]!", 1, (40,40,40))

	canoCima.set_altura(-350)
	canoBaixo.set_altura(250)

	# O loop principal do jogo
	while True:
		# Limpando a tela
		screen.fill(fundo)

		# Verificando os eventos existentes
		for evento in event.get():
			if evento.type == QUIT:
				quit()
				sys.exit()
			elif evento.type == KEYDOWN:
				if evento.key == K_UP or evento.key == K_w:
					mario.pular()
					jaPressionou = True
				if evento.key == K_SPACE:
					if mario.morreu:
						canoCima.resetar()
						canoBaixo.resetar()
						mario.resetar()
						pontos = 0

		if not mario.morreu:
			mario.morreu = mario.bateuNumCano(canoCima) or mario.bateuNumCano(canoBaixo) or mario.bateuNasBordas()
			margem_calculo += 1
			if margem_calculo % 20 == 0:
				mario.cair()
				if canoCima.andar():
					pontos += 1
					canoCima.set_altura(randint(MINIMO_ALTURA_CANO - CANO_HEIGHT, SCREEN_HEIGHT - MINIMO_ALTURA_CANO - ESPACO_ENTRE_CANOS - CANO_HEIGHT))
					canoBaixo.set_altura(canoCima.pos[1] + ESPACO_ENTRE_CANOS + CANO_HEIGHT)
					canoCima.aumentaVelocidade()
					canoBaixo.aumentaVelocidade()
				canoBaixo.andar()
				margem_calculo = 0
		else:
			screen.blit(labelPerdeu, (100, canoCima.pos[1] + CANO_HEIGHT + 50))
			screen.blit(labelPerdeu2, (90, canoCima.pos[1] + CANO_HEIGHT + 80))

		if not jaPressionou:
			screen.blit(labelInicial, (0,0))

		# Desenhando o personagem, os canos e a pontuação
		mario.desenhar(screen)
		canoCima.desenhar(screen)
		canoBaixo.desenhar(screen)
		screen.blit(myfont.render(str(pontos), 1, (40,40,40)), (SCREEN_WIDTH - 40, 10))
		display.update()

#
#	CHAMANDO A MAIN
#

main()