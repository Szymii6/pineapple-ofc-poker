import pygame
from controller.game_controller import GameController
from view.game_view import GameView
from model.game_state import GameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((1300, 900))

    game_state = GameState()

    controller = GameController(game_state)
    view = GameView(controller, screen)


    controller.view = view

    controller.draw_initial_hand()

    view.run()

    pygame.quit()

    #commited version

if __name__ == "__main__":
    main()
