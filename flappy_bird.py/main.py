import pygame, sys, random, pygame.mixer #sound isch usgschaltet lan!!!
# boden zeichnen
def draw_floor():
    screen.blit(boden,(boden_x_pos,900))
    screen.blit(boden,(boden_x_pos + 576,900))
# erschafft röhren
def erstelle_röhre():
    zufällige_röhren_pos =  random.choice(röhren_höhe)
    untere_röhre = röhren.get_rect(midtop = (700, zufällige_röhren_pos))
    obere_röhre = röhren.get_rect(midbottom = (700, zufällige_röhren_pos - 245))
    return untere_röhre, obere_röhre
#bewege objekte
def röhre_bewegen(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
#zeichne röhren
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(röhren,pipe)
        else:
            flip_pipe = pygame.transform.flip(röhren,False,True)
            screen.blit(flip_pipe,pipe)
#kilisons funktion oder kilisons check
def kolisions_check(pipes):
    for pipe in pipes:
        if vogel_rect.colliderect(pipe):
            print("COLLISON")
            death_sound.play()
            return False
    if vogel_rect.top <= -100 or vogel_rect.bottom >= 900:
        print("colision")
        return False

    return True 
#rotations funktion
def rotiere_vogel(vogel):
    neuer_vogel = pygame.transform.rotozoom(vogel,-vogel_bewegung * 3,1)
    return neuer_vogel

def vogel_animation():
    neuer_vogel = vogel_frames[vogel_index]
    neuer_vogel_rect = neuer_vogel.get_rect(center = (100,vogel_rect.centery))
    return neuer_vogel,neuer_vogel_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,880))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size = 16, channels = 1, buffer = 768)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf",40)
#das bild auf ganzem bildschirm anzeigen
hintergrund = pygame.transform.scale2x(pygame.image.load('Assets/background-day.png').convert())

#spiel Variabeln
gravity = 0.25
vogel_bewegung = 0
game_active = True
score = 0
high_score = 0

boden = pygame.transform.scale2x(pygame.image.load('Assets/base.png').convert())
boden_x_pos = 0

vogel_runter = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-downflap.png').convert_alpha())
vogel_mitte = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-midflap.png').convert_alpha())
vogel_rauf = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-upflap.png').convert_alpha())
vogel_frames = [vogel_runter,vogel_mitte,vogel_rauf]
vogel_index = 0
vogel = vogel_frames[vogel_index]
vogel_rect = vogel.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)


'''vogel = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-midflap.png').convert_alpha())
vogel_rect = vogel.get_rect(center = (100, 512))'''

röhren = pygame.transform.scale2x(pygame.image.load('Assets/pipe-green.png').convert())
röhren_liste = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
röhren_höhe = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('Assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

#sound
flap_sound = pygame.mixer.Sound('Sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Sound/sfx_hit.wav')
'''whoosh_sound = pygame.mixer.Sound('Sound/sfx_swooshing.wav')
score_sound = pygame.mixer.Sound('Sound/sfx_point.wav')
score_sound_countdown = 100
'''

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                vogel_bewegung = 0
                vogel_bewegung -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                röhren_liste.clear()
                vogel_rect.center = (100,512)
                vogel_bewegung = 0
                score = 0
                                  
        if event.type == SPAWNPIPE:
            röhren_liste.extend(erstelle_röhre())

        if event.type == BIRDFLAP:
            if vogel_index > 2 :
                vogel_index += 1
            else:
                vogel_index = 0

            vogel,vogel_rect = vogel_animation()
            
    screen.blit(hintergrund,(0,0))
    if game_active:  
        #vogel
        vogel_bewegung += gravity
        rotierender_vogel = rotiere_vogel(vogel)
        vogel_rect.centery += vogel_bewegung
        screen.blit(rotierender_vogel,vogel_rect)
        screen.blit(vogel,(vogel_rect))
        game_active = kolisions_check(röhren_liste)

        #röhren
        röhren_liste = röhre_bewegen(röhren_liste)
        draw_pipes(röhren_liste)
        
        score += 0.01
        score_display('main_game')
        '''score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100'''
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        #whoosh_sound.play()

    #boden
    boden_x_pos -= 1
    draw_floor()
    if boden_x_pos <= -576:
        boden_x_pos = 0

    pygame.display.update()
    clock.tick(120)