# main.py

import pygame
from controller.game_controller import GameController
from view.game_view import GameView
from model.game_state import GameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((1300, 900))

    # Inicjalizacja stanu gry
    game_state = GameState()

    # Inicjalizacja widoku (z tymczasowym None, bo kontroler potrzebuje widoku i odwrotnie)
    controller = GameController(game_state)
    view = GameView(controller, screen)

    # Powiązanie widoku z kontrolerem
    controller.view = view

    # Inicjalizacja pierwszego rozdania (ręki startowej)
    controller.draw_initial_hand()

    # Uruchomienie głównej pętli gry
    view.run()

    pygame.quit()

    #commited version

if __name__ == "__main__":
    main()
