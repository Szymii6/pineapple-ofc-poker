import pygame

pygame.init()

WIDTH, HEIGHT = 1300, 900
CARD_WIDTH, CARD_HEIGHT = 80, 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
GREY = (200, 200, 200)
RED = (255, 100, 100)
BLUE = (100, 100, 255)

FONT = pygame.font.SysFont("Arial", 24)

SLOT_POSITIONS = {
    'top': (100, 50),
    'middle': (100, 200),
    'bottom': (100, 400)
}


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, x, y):
        super().__init__()
        self.card = card
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.image.fill(GREY)
        text = FONT.render(str(card), True, BLACK)
        self.image.blit(text, (10, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_x + self.offset_x, mouse_y + self.offset_y)


class GameView:
    def __init__(self, controller, screen):
        self.controller = controller
        self.screen = screen
        pygame.display.set_caption("Pineapple OFC - MVC")
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.dragged_card = None
        self.running = True
        self.game_over = False

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            self.draw_board()
            self.sprites.draw(self.screen)
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_board(self):
        for name, (x, y) in SLOT_POSITIONS.items():
            pygame.draw.rect(self.screen, GREEN, (x, y, 500, CARD_HEIGHT), 2)
            self.draw_text(name.upper(), x, y - 30)

            cards = getattr(self.controller.game_state, name)
            for i, card in enumerate(cards):
                self.draw_text(str(card), x + i * (CARD_WIDTH + 5) + 10, y + 35)

        self.draw_text("Mnożniki punktów:", 850, 260)
        self.draw_text("TOP     ×3", 850, 280)
        self.draw_text("MIDDLE  ×2", 850, 300)
        self.draw_text("BOTTOM  ×1", 850, 320)

        self.draw_text("Legenda punktacji:", 850, 20)
        labels = [
            "Poker        8 pkt",
            "Kareta       7 pkt",
            "Full         6 pkt",
            "Kolor        5 pkt",
            "Strit        4 pkt",
            "Trójka       3 pkt",
            "Dwie pary    2 pkt",
            "Para         1 pkt",
            "Wys. karta   0 pkt"
        ]

        for i, text in enumerate(labels):
            self.draw_text(text, 850, 50 + i * 20)

        # Przycisk reset
        pygame.draw.rect(self.screen, BLUE, (WIDTH - 220, HEIGHT - 60, 180, 40))
        self.draw_text("Zagraj jeszcze raz", WIDTH - 210, HEIGHT - 50, WHITE)

    def draw_text(self, text, x, y, color=BLACK):
        label = FONT.render(text, True, color)
        self.screen.blit(label, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    if WIDTH - 220 <= event.pos[0] <= WIDTH - 40 and HEIGHT - 60 <= event.pos[1] <= HEIGHT - 20:
                        self.controller.reset_game()
                        self.game_over = False
                        return

                for card_sprite in self.controller.hand_sprites:
                    if card_sprite.rect.collidepoint(event.pos):
                        self.dragged_card = card_sprite
                        card_sprite.offset_x = card_sprite.rect.x - event.pos[0]
                        card_sprite.offset_y = card_sprite.rect.y - event.pos[1]
                        card_sprite.dragging = True
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragged_card:
                    self.dragged_card.dragging = False
                    placed = False
                    for name, (sx, sy) in SLOT_POSITIONS.items():
                        slot_rect = pygame.Rect(sx, sy, 500, CARD_HEIGHT)
                        if slot_rect.collidepoint(event.pos):
                            placed = self.controller.place_card(self.dragged_card.card, name)
                            if placed:
                                if self.dragged_card in self.sprites:
                                    self.sprites.remove(self.dragged_card)
                                if self.dragged_card in self.controller.hand_sprites:
                                    self.controller.hand_sprites.remove(self.dragged_card)

                            break
                    self.dragged_card = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragged_card:
                    self.dragged_card.update()

    def display_hand(self, hand):
        self.sprites.empty()
        self.controller.hand_sprites.clear()
        spacing = 20
        total_width = len(hand) * CARD_WIDTH + (len(hand) - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        y_pos = HEIGHT - CARD_HEIGHT - 20
        for i, card in enumerate(hand):
            sprite = CardSprite(card, start_x + i * (CARD_WIDTH + spacing), y_pos)
            self.sprites.add(sprite)
            self.controller.hand_sprites.append(sprite)

    def display_results(self, results):
        y = 600
        for line in results:
            self.draw_text(line, 600, y, RED)
            y += 30

        pygame.display.flip()  # <- natychmiast pokazuje wynik
        self.wait_for_restart()

    def wait_for_restart(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if WIDTH - 220 <= event.pos[0] <= WIDTH - 40 and HEIGHT - 60 <= event.pos[1] <= HEIGHT - 20:
                        self.controller.reset_game()
                        waiting = False
            self.clock.tick(60)

