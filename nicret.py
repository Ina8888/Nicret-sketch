import pygame
pygame.init()

fps = 60
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
activeSize = 0
activeColor = (255, 255, 255)
painting = []
clearClicked = False
saveClicked = False

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Nicret')

def drawMenu(size, color, clearClicked, saveClicked):
    pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 70])
    pygame.draw.line(screen, 'black', (0, 70), (WIDTH, 70), 3)

    xlBrush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    lBrush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    mBrush = pygame.draw.rect(screen, 'black', [130, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (155, 35), 10)
    sBrush = pygame.draw.rect(screen, 'black', [190, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (215, 35), 5)

    brushList = [xlBrush, lBrush, mBrush, sBrush]

    if size == 20:
        pygame.draw.rect(screen, 'green', [10, 10, 50, 50], 3)
    elif size == 15:
        pygame.draw.rect(screen, 'green', [70, 10, 50, 50], 3)
    elif size == 10:
        pygame.draw.rect(screen, 'green', [130, 10, 50, 50], 3)
    elif size == 5:
        pygame.draw.rect(screen, 'green', [190, 10, 50, 50], 3)

    pygame.draw.circle(screen, color, (400, 35), 30)
    pygame.draw.circle(screen, 'dark grey', (400, 35), 30, 3)

    blue = pygame.draw.rect(screen, (0, 0, 255), [WIDTH - 35, 10, 25, 25])
    red = pygame.draw.rect(screen, (255, 0, 0), [WIDTH - 35, 35, 25, 25])
    green = pygame.draw.rect(screen, (0, 255, 0), [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, (255, 255, 0), [WIDTH - 60, 35, 25, 25])
    teal = pygame.draw.rect(screen, (0, 255, 255), [WIDTH - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, (255, 0, 255), [WIDTH - 85, 35, 25, 25])
    white = pygame.draw.rect(screen, (255, 255, 255), [WIDTH - 110, 10, 25, 25])
    black = pygame.draw.rect(screen, (0, 0, 0), [WIDTH - 110, 35, 25, 25])

    colorRect = [blue, red, green, yellow, teal, purple, white, black]
    rgbList = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255), (0, 0, 0)]

    clearButton = pygame.draw.rect(screen, 'black', [WIDTH - 200, 10, 50, 50])
    if clearClicked:
        pygame.draw.rect(screen, 'green', [WIDTH - 200, 10, 50, 50], 3)
    else:
        pygame.draw.rect(screen, 'white', [WIDTH - 200, 10, 50, 50], 2)
    pygame.draw.line(screen, 'white', (WIDTH - 190, 20), (WIDTH - 160, 50), 3)
    pygame.draw.line(screen, 'white', (WIDTH - 190, 50), (WIDTH - 160, 20), 3)
    
    saveButton = pygame.draw.rect(screen, 'black', [WIDTH - 260, 10, 50, 50])
    if saveClicked:
        pygame.draw.rect(screen, 'green', [WIDTH - 260, 10, 50, 50], 3)
    else:
        pygame.draw.rect(screen, 'white', [WIDTH - 260, 10, 50, 50], 2)
    pygame.draw.polygon(screen, 'white', [(WIDTH - 250, 45), (WIDTH - 220, 45), (WIDTH - 235, 20)])
    pygame.draw.rect(screen, 'white', [WIDTH - 250, 45, 30, 5])

    return brushList, colorRect, rgbList, clearButton, saveButton

def drawPainting(paint):
    for circle in paint:
        pygame.draw.circle(screen, circle[0], circle[1], circle[2])

run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    mouse = pygame.mouse.get_pos()
    leftClick = pygame.mouse.get_pressed()[0]

    if mouse[1] > 70 and leftClick:
        painting.append((activeColor, mouse, activeSize))

    if mouse[1] > 70:
        pygame.draw.circle(screen, activeColor, mouse, activeSize)

    drawPainting(painting)

    brushes, colors, rgb, clearButton, saveButton = drawMenu(activeSize, activeColor, clearClicked, saveClicked)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    activeSize = 20 - (i * 5)
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    activeColor = rgb[i]
            if clearButton.collidepoint(event.pos):
                clearClicked = not clearClicked
                if clearClicked:
                    painting.clear()
            if saveButton.collidepoint(event.pos):
                saveClicked = not saveClicked

    pygame.display.flip()

pygame.quit()
