import sys, pygame, math
import random

DEBUG_MODE = True if '--debug' in sys.argv else False

# definicao de constantes para o jogo
FPS = 60
W_SIZE = W_WIDTH, W_HEIGHT = 1024, 768
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (20, 255, 140)
GREY = (210, 210, 210)
W_BGCOLOR = GREEN
SPEED = 5 # velocidade de movimento do carrinho do jogador
SPEED_OPPONENT1 = [0,3] # velocidade de movimento do carrinho oponente 1
SPEED_OPPONENT2 = [0,5] # velocidade de movimento do carrinho oponente 1
SPEED_LEVEL = 0.1 # Taxa de aumento da velocidade dos carrinhos
# próximo nível (valor sugerido: pode ser alterado conforme a sua lógica)
LEVEL = 10
# Usar essa quantidade de atualização das velocidades dos carrinhos oponentes.
# Isto é, a cada 10 carrinhos ultrapassados aumentar a velocidade destes.
LEVEL_FREQ = 10
# Variaveis relacionadas à pista
INICIO_PISTA = W_WIDTH // 100 * 15
FIM_PISTA = W_WIDTH // 100 * 45
FAIXAS = [
   [INICIO_PISTA, INICIO_PISTA * 2],
   [INICIO_PISTA * 2, INICIO_PISTA * 3],
   [INICIO_PISTA * 3, INICIO_PISTA * 4]
]
PISTA_FAIXAS = [FAIXAS[0][1], FAIXAS[2][0]]
# Lista contendo as imagens de arvores usadas no jogo
TREES = ["tree_1.png", "tree_2.png", "tree_3.png", "tree_4.png", "tree_5.png"]

# Habilita as funcoes do pygame e configura a Interface (não alterar)
pygame.init()
SCREEN = pygame.display.set_mode(W_SIZE)
pygame.display.set_caption('Car Racing')
pygame.display.set_icon(pygame.image.load('assets/images/gameicon.png'))
clock = pygame.time.Clock()

# define os textos para 'pontos' e mensagem do 'termino' do jogo (não alterar)
score = 0
game_over = False
font_score = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 50)

# X [TODO] carregar as imagens dos carrinhos
car = pygame.image.load("assets/images/white_car.png")
opponent_1 = pygame.image.load("assets/images/blue_car.png")
opponent_2 = pygame.image.load("assets/images/red_car.png")

# define posicao inicial para o carrinho (não alterar)
car_rect = car.get_rect()
car_rect.center = (W_WIDTH // 3 + 40, W_HEIGHT - 100)

# define posicoes iniciais para os oponentes (não alterar)
# Repare que a coordenada ``y'' é negativa. Isso permite
# iniciar aos carrinhos em uma posição fora da tela.
opponent_1_rect = opponent_1.get_rect()
opponent_2_rect = opponent_2.get_rect()
opponent_1_rect.center = (random.randint(FAIXAS[0][0] + 25, FAIXAS[0][1] - 25), 100)
opponent_2_rect.center = (random.randint(FAIXAS[2][0] + 25, FAIXAS[2][1] - 25), 100)
faixa_opponent_1 = 0
faixa_opponent_2 = 2

# carrega as imagens das árvores, escolhendo-as aleatoriamente. Repare que apenas
# duas árvores são visíveis na tela a cada instante (não alterar).
trees_images = []
trees_images_rect = []
for i in range(0, len(TREES)):
   trees_images.append(pygame.image.load("assets/images/" + TREES[i]))
   trees_images_rect.append(trees_images[i].get_rect())
t1 = random.randint(0, 2)
t2 = random.randint(3, 4)

# define posicoes iniciais para as arvores (não alterar)
# Repare que a coordenada ``y'' é negativa. Isso permite
# iniciar as ávores em uma posição fora da tela.
trees_images_rect[t1].center = (random.randint(W_WIDTH - 350, W_WIDTH - 200), -250)
trees_images_rect[t2].center = (random.randint(W_WIDTH - 350, W_WIDTH - 200), -10)


# X [TODO] carregar a musica de fundo e deixá-la em execução
pygame.mixer.music.load("assets/sounds/top-Gear-Soundtrack.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

# Funções para o jogo
#

""" def captura_colisao_oponentes():
   global opponent_1_rect, opponent_2_rect


   [TODO] Detectar colisao entre os oponentes ('blocos'). Em caso de colisao,
       afastar um carrinho para o lado sem deixa-lo sair das pistas.
   """


def captura_colisao():
   global car_rect, opponent_1_rect, opponent_2_rect

   # Colisão com oponente 1
   if (min(car_rect.x, car_rect.x + car_rect.w) < max(opponent_1_rect.x, opponent_1_rect.x + opponent_1_rect.w)
      and min(car_rect.y, car_rect.y + car_rect.h) < max(opponent_1_rect.y, opponent_1_rect.y + opponent_1_rect.h)
      and max(car_rect.x, car_rect.x + car_rect.w) > min(opponent_1_rect.x, opponent_1_rect.x + opponent_1_rect.w)
      and max(car_rect.y, car_rect.y + car_rect.h) > min(opponent_1_rect.y, opponent_1_rect.y + opponent_1_rect.h)
   ):
      print('colisão oponente 1')
      return True

   # Colisão com oponente 2
   if (min(car_rect.x, car_rect.x + car_rect.w) < max(opponent_2_rect.x, opponent_2_rect.x + opponent_2_rect.w)
      and min(car_rect.y, car_rect.y + car_rect.h) < max(opponent_2_rect.y, opponent_2_rect.y + opponent_2_rect.h)
      and max(car_rect.x, car_rect.x + car_rect.w) > min(opponent_2_rect.x, opponent_2_rect.x + opponent_2_rect.w)
      and max(car_rect.y, car_rect.y + car_rect.h) > min(opponent_2_rect.y, opponent_2_rect.y + opponent_2_rect.h)
   ):
      print('colisão oponente 2')
      return True

   return False

   """
   X [TODO] Detectar colisao entre o carrinho e cada um de seus oponentes ('blocos'). Em caso
   de colisão, retornar True e parar o movimento de todos os elementos. Sem colisão detectada,
   então manter o jogo em execução e retornar False.
   """

def reinicia_oponente():
   global opponent_1_rect, opponent_2_rect, score, faixa_opponent_1, faixa_opponent_2

   # Reinicia oponente 1
   if(opponent_1_rect.y >= W_HEIGHT + 50):
      faixa_opponent_1 = random.randint(0, len(FAIXAS) - 1)

      while (faixa_opponent_1 == faixa_opponent_2):
         faixa_opponent_1 = random.randint(0, len(FAIXAS) - 1)

      opponent_1_rect.center = (random.randint(FAIXAS[faixa_opponent_1][0] + 25, FAIXAS[faixa_opponent_1][1] - 25), -50)
      score += 1

   # Reinicia oponente 2
   if(opponent_2_rect.y >= W_HEIGHT + 50):
      faixa_opponent_2 = random.randint(0, len(FAIXAS) - 1)

      while (faixa_opponent_2 == faixa_opponent_1):
         faixa_opponent_2 = random.randint(0, len(FAIXAS) - 1)

      opponent_2_rect.center = (random.randint(FAIXAS[faixa_opponent_2][0] + 25, FAIXAS[faixa_opponent_2][1] - 25), -50)
      score += 1

   """
   X [TODO] Se um oponente sai da tela, renicia-se a sua posicao aleatoriamente na tela
   """

def debug_mode():
   global car_rect, opponent_1_rect, opponent_2_rect

   for faixa in FAIXAS:
      pygame.draw.line(SCREEN, RED, (faixa[0], 0), (faixa[1], W_HEIGHT), 4)

   pygame.draw.rect(SCREEN, RED, (car_rect.x, car_rect.y, car_rect.w, car_rect.h))
   pygame.draw.rect(SCREEN, RED, (opponent_1_rect.x, opponent_1_rect.y, opponent_1_rect.w, opponent_1_rect.h))
   pygame.draw.rect(SCREEN, RED, (opponent_2_rect.x, opponent_2_rect.y, opponent_2_rect.w, opponent_2_rect.h))

# CODIGO PRINCIPAL
while True:
   # X [TODO] desenhar a imagem de fundo. Utilize os valores numéricos da tela e das pistas.
   # Define cor de background
   SCREEN.fill(GREEN)
   # Desenha fundo da pista
   fundo_pista_rect = pygame.draw.rect(SCREEN, GREY, (INICIO_PISTA, 0, FIM_PISTA, W_HEIGHT))
   # Desenha as faixas da pista
   for faixa in PISTA_FAIXAS:
      pygame.draw.line(SCREEN, WHITE, (faixa, 0), (faixa, W_HEIGHT), 4)

   # X [TODO] Capturar o evento de fechar o jogo na interface.
   # A musica deve ser finalizada antes do fechamento do jogo.
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.mixer.music.stop()
         pygame.mixer.music.unload()

         pygame.quit()
         sys.exit()

   # X [TODO mover as arvores em 1 pixel. Reposicionar quando as arvores saem da Interface.
   if game_over == False:
      trees_images_rect[t1].move_ip(0, 1)
      trees_images_rect[t2].move_ip(0, 1)

      if(trees_images_rect[t1].y >= W_HEIGHT + 25):
         t1 = random.randint(0, 2)
         trees_images_rect[t1].center = (random.randint(W_WIDTH - 350, W_WIDTH - 200), -250)
      if(trees_images_rect[t2].y >= W_HEIGHT + 25):
         t2 = random.randint(3, 4)
         trees_images_rect[t2].center = (random.randint(W_WIDTH - 350, W_WIDTH - 200), -10)

   # X [TODO] Capturar uma tecla pressionada para mover o carrinho. Usar as teclas
   # UP, DOWN, LEFT e RIGHT (setinhas). Para mover o carrinho use a velocidade na
   # coordenada correta.
   if pygame.key.get_focused() and game_over == False:
      key = pygame.key.get_pressed()

      if key[pygame.K_UP]:
         if key[pygame.K_LEFT]:
            car_rect.move_ip(-SPEED, -SPEED)
         elif key[pygame.K_RIGHT]:
            car_rect.move_ip(SPEED, -SPEED)
         else:
            car_rect.move_ip(0, -SPEED)
      elif key[pygame.K_DOWN]:
         if key[pygame.K_LEFT]:
            car_rect.move_ip(-SPEED, SPEED)
         elif key[pygame.K_RIGHT]:
            car_rect.move_ip(SPEED, SPEED)
         else:
            car_rect.move_ip(0, SPEED)
      elif key[pygame.K_LEFT]:
         car_rect.move_ip(-SPEED, 0)
      elif key[pygame.K_RIGHT]:
         car_rect.move_ip(SPEED, 0)



   # X [TODO] mover os carrinhos oponentes
   if game_over == False:
      opponent_1_rect.move_ip(SPEED_OPPONENT1)
      opponent_2_rect.move_ip(SPEED_OPPONENT2)

   # X [TODO] detectar colisão
   colisao = captura_colisao()

   # X [TODO] reiniciar oponentes quando
   score_antigo = score
   reinicia_oponente()

   # X [TODO] a cada intervalo de pontos a velocidade dos oponentes eh aumentada
   if (score_antigo // LEVEL_FREQ < score // LEVEL_FREQ):
      SPEED_OPPONENT1[1] = SPEED_OPPONENT1[1] + SPEED_OPPONENT1[1] * SPEED_LEVEL
      SPEED_OPPONENT2[1] = SPEED_OPPONENT2[1] + SPEED_OPPONENT2[1] * SPEED_LEVEL

      print(f'SPEED_OPPONENT1 {SPEED_OPPONENT1}')
      print(f'SPEED_OPPONENT2 {SPEED_OPPONENT2}')


   # X [TODO] manter o carrinho do jogador na tela. Use valores numéricos da tela e das pistas.
   car_rect.clamp_ip(fundo_pista_rect)

   # X [TODO] detectar colisao entre o carrinho do jogador e algum carrinho oponente.
   # Em caso de colisão mostrar a mensagem ''Fim de Jogo'' e carregar a imagem
   # de carrinho batido para o carrinho do jogador.
   if (colisao == True):
      game_over = True
      SCREEN.blit(font_score.render("GAME OVER", True, RED), (W_WIDTH // 3, W_HEIGHT // 4))
      car = pygame.image.load("assets/images/white_car_crashed.png")

   if DEBUG_MODE == True:
      debug_mode()

   # desenha os objetos em posicoes atualizadas (não alterar)
   SCREEN.blit(trees_images[t1], trees_images_rect[t1])
   SCREEN.blit(trees_images[t2], trees_images_rect[t2])

   text_surf_p = font_score.render(str(score), True, BLACK)
   SCREEN.blit(text_surf_p, (W_WIDTH-100, 20))

   SCREEN.blit(opponent_1, opponent_1_rect)
   SCREEN.blit(opponent_2, opponent_2_rect)

   SCREEN.blit(car, car_rect)
   pygame.display.update()
   clock.tick(FPS)
