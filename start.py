from game import *
pygame.font.init()

l1 = [
     ['x', 'x', '#', '#', '#', 'x', '2', '1'],
     ['2', 'x', '#', 'o', '#', '1' ,'x', 'x'],
     ['x', '1', '#', ' ', '#', '#', '#', '#'],
     ['#', '#', '#', ' ', ' ', ' ', 'o', '#'],
     ['#', 'o', ' ', ' ', ' ', '#', '#', '#'],
     ['#', '#', '#', '#', ' ', '#', 'x', '2'],
     ['2', 'x', 'x', '#', 'o', '#', '2', 'x'],
     ['x', '2', 'x', '#', '#', '#', 'x', '2']
    ]
l2 = [
    ['#', '#', '#', '#', '#', 'x', 'x', '2', 'x', '1'],
    ['#', ' ', ' ', ' ', '#', '2', 'x', 'x', 'x', '2'],
    ['#', ' ', ' ', ' ', '#', 'x', '#', '#', '#', 'x'],
    ['#', ' ', ' ', ' ', '#', '1', '#', 'o', '#', '2'],
    ['#', '#', '#', ' ', '#', '#', '#', 'o', '#', 'x'],
    ['1', '#', '#', ' ', ' ', ' ', ' ', 'o', '#', 'x'],
    ['x', '#', ' ', ' ', ' ', '#', ' ', ' ', '#', '2'],
    ['2', '#', ' ', ' ', ' ', '#', ' ', ' ', '#', 'x'],
    ['x', '#', ' ', ' ', ' ', '#', '#', '#', '#', 'x'],
    ['2',  '#', '#', '#', '#', '#', '1', 'x', 'x', 'x']
]
l3 = [
     ['x', '#', '#', '#', '#', 'x', 'x', 'x'],
     ['1', '#', ' ', ' ', '#', 'x' ,'x', 'x'],
     ['x', '#', ' ', ' ', '#', '#', '1', '2'],
     ['2', '#', ' ', ' ', '#', '#', 'x', '2'],
     ['#', '#', ' ', ' ', ' ', '#', '#', '#'],
     ['#', 'o', ' ', ' ', ' ', '#', '2', 'x'],
     ['#', 'o', 'o', 'o', 'o', '#', 'x', '2'],
     ['#', '#', '#', '#', '#', '#', '2', 'x']
    ]
l4 = [
     ['2', 'x', '#', '#', '#', '#', '#', '#'],
     ['x', '1', '#', ' ', ' ', ' ' ,' ', '#'],
     ['#', '#', '#', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', 'o', 'o', ' ', '#'],
     ['#', ' ', ' ', 'o', 'o', 'o', '#', '#'],
     ['#', '#', '#', '#', ' ', ' ', '#', '1'],
     ['x', 'x', '1', '#', '#', '#', '#', 'x'],
     ['2', 'x', 'x', '#', '#', '#', 'x', '2']
    ]

levelList = [l1,l2,l3,l4]
levelSize = [len(i) for i in levelList]
playerList = [ [4,4],[1,3],[2,2], [4,1]]
boxesList = [
[[3,3],[4,3],[3,5],[5,4]],
[ [2,2],[2,3],[3,2]],
[[2,3],[3,2],[4,3],[5,2],[6,3]],
[[2,3], [2,4],[2,5], [3,3],[4,2]]
]


if __name__ == "__main__":

    #texts
    WHITE = (255, 255, 255)
    BG_COLOR = (188, 143, 143)
    TEXT_COLOR = (165,42,42)
    fontObj = pygame.font.SysFont("comicsansms", 24)
    ghostseries = pygame.image.load('ghostseries.png')
    #ticking
    clock = pygame.time.Clock()
    delta = 0.0

    #start screen
    screen = pygame.display.set_mode((800, 600))  # display start view / settings
    pygame.display.set_caption('MENU')

    #sounds
    pygame.mixer.init()
    music = pygame.mixer.music.load('happytune.wav')
    #read settings
    f = open("settings.txt","r")
    sound = bool(int(f.readline()[-1]))
    f.close()
    if sound :
        pygame.mixer.music.play(-1, 0.0)

    #menu settings
    counter = 1

    while True:
        # start screen
        screen.fill(BG_COLOR)

        basicfont = pygame.font.SysFont("comicsansms", 72)
        text = basicfont.render("           SockoBunny          ", True, (255, 100, 100), (0, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = 150

        screen.blit(text, textrect)
        screen.blit(ghostseries, (50,450))

        #menu handling
        pressed = pygame.key.get_pressed()
        delta += clock.tick() / 1000.0
        while delta > 1 / 8:
            if pressed[pygame.K_DOWN] and counter < 3: counter += 1
            elif pressed[pygame.K_UP] and counter > 1: counter -= 1
            # stop music
            if counter == 2 and (pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]) :
                sound = not sound
                if sound:
                    pygame.mixer.music.play(-1, 0.0)
                else:
                    pygame.mixer.music.stop()
            delta -= 1 / 8



        if counter == 1:
            screen.blit(fontObj.render(' >  START   <', True, TEXT_COLOR),(300,250))
        else:
            screen.blit(fontObj.render(' START', True, TEXT_COLOR), (320, 250))
        if counter == 2 :
            if sound:
                screen.blit(fontObj.render('>  MUSIC : ON  <', True, TEXT_COLOR),(290,300))
            else:
                screen.blit(fontObj.render('>  MUSIC : OF  <', True, TEXT_COLOR), (290, 300))
        else:
            if sound:
                screen.blit(fontObj.render(' MUSIC : ON', True, TEXT_COLOR), (300, 300))
            else:
                screen.blit(fontObj.render(' MUSIC : OF', True, TEXT_COLOR), (300, 300))
        if counter == 3:
            screen.blit(fontObj.render('>  EXIT  <', True, TEXT_COLOR), (315, 350))
        else:
            screen.blit(fontObj.render(' EXIT ', True, TEXT_COLOR),(330,350))
        pygame.display.update()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and counter ==3 and event.key == pygame.K_RETURN:
                # zapisz w pliku txt
                f = open('settings.txt', 'w')
                f.write("'Sound' : " + str(int(sound)))
                f.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                f = open('settings.txt', 'w')
                f.write("'Sound' : " + str(int(sound)))
                f.close()
                sys.exit()


          # levele
        if counter == 1 and pressed[pygame.K_RETURN]:
            f = open("settings.txt", "w")
            f.write("Sound: " + str(int(sound)))
            f.close()

            for i in range(len(levelList)):
                restart = True
                while restart:
                   restart = not Game(i,boxesList[i], playerList[i], levelList[i],(levelSize[i]*50 + 100, levelSize[i]*50 +100), 60).isFinished()
            counter = 3
            pygame.display.set_mode((800, 600))
            pygame.display.set_caption('!!!Congratulation!!!')

