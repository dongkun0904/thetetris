import pygame
import time
import thetetris.constants as constants
import thetetris.grid as grid
import thetetris.pieces as pieces
import thetetris.window as window


def run():
    # initialization
    pygame.init()
    win = window.createWindow(constants.width, constants.height)
    run = True
    usedSave = False
    g = grid.Grid()

    # pieces
    # curPiece = pieces.getPiece()
    # nextPiece = pieces.getPiece()
    curPiece = pieces.Piece(3, -1, 6, 0)
    nextPiece = pieces.Piece(3, -1, 6, 0)
    savedPiece = None

    # spaces that are already occupied
    placed = {}

    # texts on screen
    font = pygame.font.Font('data/fonts/raleway/Raleway-Black.ttf', 36)
    text = font.render(constants.TITLE, True, (0, 0, 0))

    clock = pygame.time.Clock()

    startTime = time.time()
    while run:
        clock.tick(60)
        if time.time() - startTime >= 0.5:
            if curPiece.tick(placed):
                curPiece.registerPiece(placed)
                curPiece = nextPiece
                nextPiece = pieces.getPiece()
                usedSave = False
            startTime = time.time()

        g.updateGrid(placed, curPiece)
        window.updateWindow(win, g, nextPiece, savedPiece, text)
        for event in pygame.event.get():

            # quit when we close the window
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            pressedKey = None
            if event.type == pygame.KEYDOWN:
                pressedKey = event.key

            if pressedKey == pygame.K_s and not usedSave:
                usedSave = True
                p = curPiece
                if savedPiece:
                    curPiece = savedPiece
                else:
                    curPiece = nextPiece
                    nextPiece = pieces.getPiece()
                savedPiece = p
                savedPiece.x = 3
                savedPiece.y = 0
                continue

            if curPiece.transform(pressedKey, placed):
                curPiece.registerPiece(placed)
                curPiece = nextPiece
                nextPiece = pieces.getPiece()
                usedSave = False

            if grid.lost(placed):
                run = False
                pygame.display.quit()
                print("You lost")

    pygame.quit()
