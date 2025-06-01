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
GRAN = (25, 25, 112)
BLUE_LIGHT = (30, 144, 255)

FONT = pygame.font.SysFont("Arial", 24)
FONT1 = pygame.font.Font("pineapple_ofc_project/assets/fonts/CARDOVA.ttf", 24)

SLOT_POSITIONS = {
    'top': (100, 50),
    'middle': (100, 200),
    'bottom': (100, 350)
}


def draw_card_surface(card_str):
    surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)

    pygame.draw.rect(surf, (250, 250, 240), (0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=12)
    pygame.draw.rect(surf, BLACK, (0, 0, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=12)

    suit = card_str[-1]
    value = card_str[:-1]
    color = RED if suit in ['♥', '♦'] else BLACK

    val_font = pygame.font.Font("pineapple_ofc_project/assets/fonts/CARDOVA.ttf", 24)
    suit_font = pygame.font.SysFont("Arial", 24)

    val_text = val_font.render(value, True, color)
    suit_text = suit_font.render(suit, True, color)

    surf.blit(val_text, (8, 4))
    surf.blit(suit_text, (8, 30))

    big_suit = pygame.font.SysFont("Arial", 48)
    suit_center = big_suit.render(suit, True, color)
    surf.blit(suit_center, (CARD_WIDTH // 2 - 14, CARD_HEIGHT // 2 - 24))

    return surf



class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, x, y):
        super().__init__()
        self.card = card
        self.image = draw_card_surface(str(card))
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
        self.field_sprites = pygame.sprite.Group()
        self.delay_until = None
        self.next_turn_pending = False


    def run(self):
        while self.running:
            self.screen.fill(GRAN)
            self.draw_board()

            if not self.game_over:
                self.sprites.draw(self.screen)
            self.field_sprites.draw(self.screen)
    
            self.handle_events()
            now = pygame.time.get_ticks()
            if self.delay_until and now >= self.delay_until:
                self.delay_until = None
                if self.next_turn_pending:
                    self.next_turn_pending = False
                    self.controller.next_turn()
                else:
                    self.controller.end_game()

            pygame.display.flip()
            self.clock.tick(60)

    def draw_board(self):
        for name, (x, y) in SLOT_POSITIONS.items():
            pygame.draw.rect(self.screen, BLACK, (x, y, 500, CARD_HEIGHT), 2)
            self.draw_text(name.upper(), x, y - 30, WHITE)

            cards = getattr(self.controller.game_state, name)
            for i, card in enumerate(cards):
                self.draw_text(str(card), x + i * (CARD_WIDTH + 5) + 10, y + 35)

        pygame.draw.rect(self.screen, BLUE_LIGHT, (830, 250, 250, 100), border_radius=10)
        self.draw_text("Mnożniki punktów:", 850, 260, WHITE)
        self.draw_text("TOP     ×3", 850, 280, WHITE)
        self.draw_text("MIDDLE  ×2", 850, 300, WHITE)
        self.draw_text("BOTTOM  ×1", 850, 320, WHITE)
        self.field_sprites.draw(self.screen)

        pygame.draw.rect(self.screen, BLUE_LIGHT, (830, 10, 250, 230), border_radius=10)
        self.draw_text("Legenda punktacji:", 850, 20, WHITE)
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
            self.draw_text(text, 850, 50 + i * 20, WHITE)

        pygame.draw.rect(self.screen, BLUE_LIGHT, (WIDTH - 220, HEIGHT - 60, 180, 40), border_radius=10)
        self.draw_centered_text("Zagraj jeszcze raz", WIDTH - 220, HEIGHT - 60, 180, 40, WHITE)

    def draw_text(self, text, x, y, color=BLACK):
        label = FONT.render(text, True, color)
        self.screen.blit(label, (x, y))

    def draw_centered_text(self, text, rect_x, rect_y, rect_w, rect_h, color=BLACK):
        label = FONT.render(text, True, color)
        text_rect = label.get_rect(center=(rect_x + rect_w // 2, rect_y + rect_h // 2))
        self.screen.blit(label, text_rect)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    if WIDTH - 220 <= event.pos[0] <= WIDTH - 40 and HEIGHT - 60 <= event.pos[1] <= HEIGHT - 20:
                        self.controller.reset_game()
                        self.field_sprites.empty()
                        self.sprites.empty()
                        self.controller.hand_sprites.clear()
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
                                
                                cards_in_slot = len(getattr(self.controller.game_state, name))
                                x_pos = sx + (cards_in_slot - 1) * (CARD_WIDTH + 5)
                                y_pos = sy
                                new_card_sprite = CardSprite(self.dragged_card.card, x_pos, y_pos)
                                self.field_sprites.add(new_card_sprite)

                                if len(self.controller.hand_sprites) == 0:
                                    self.delay_until = pygame.time.get_ticks() + 500

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

    def schedule_next_turn(self):
        self.delay_until = pygame.time.get_ticks() + 500
        self.next_turn_pending = True


    def display_results(self, results):
        y = 600
        for line in results:
            self.draw_text(line, 600, y, RED)
            y += 30

        pygame.display.flip()
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
                        self.field_sprites.empty()
                        waiting = False
            self.clock.tick(60)

