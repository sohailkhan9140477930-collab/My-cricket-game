import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        
        # मोबाइल स्क्रीन का साइज
        info = pygame.display.Info()
        self.WIDTH = info.current_w
        self.HEIGHT = info.current_h
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, int(self.WIDTH * 0.07))
        self.big_font = pygame.font.Font(None, int(self.WIDTH * 0.12))
        
        self.LANE_WIDTH = self.WIDTH // 3
        self.high_score = 0
        
        # --- बटनों को और भी ऊपर सेट किया गया है ---
        SAFE_MARGIN = 20
        # SAFE_BOTTOM को और बढ़ा दिया गया है (अब बटन्स स्क्रीन के काफी ऊपर होंगे)
        SAFE_BOTTOM = 300 
        btn_w = (self.WIDTH - (SAFE_MARGIN * 4)) // 3 
        btn_h = 120
        
        self.btn_left = pygame.Rect(SAFE_MARGIN, self.HEIGHT - SAFE_BOTTOM, btn_w, btn_h)
        self.btn_jump = pygame.Rect(SAFE_MARGIN * 2 + btn_w, self.HEIGHT - SAFE_BOTTOM, btn_w, btn_h)
        self.btn_right = pygame.Rect(SAFE_MARGIN * 3 + btn_w * 2, self.HEIGHT - SAFE_BOTTOM, btn_w, btn_h)
        
        # Game Over Restart Button
        self.btn_restart = pygame.Rect(self.WIDTH//2 - 120, self.HEIGHT//2 + 150, 240, 90)
        
        self.city_y = 0
        self.reset_game()

    def reset_game(self):
        self.player_lane = 1
        # प्लेयर को बटनों के ऊपर रखा गया है
        self.player_y = self.HEIGHT - 480 
        self.is_jumping = False
        self.jump_count = 10
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.speed = 12
        self.game_over = False

    def draw_city_area(self):
        # मुख्य सड़क
        self.screen.fill((50, 50, 50)) 
        
        # फुटपाथ (Sidewalks)
        pygame.draw.rect(self.screen, (120, 120, 120), (0, 0, 40, self.HEIGHT))
        pygame.draw.rect(self.screen, (120, 120, 120), (self.WIDTH - 40, 0, 40, self.HEIGHT))
        
        # सड़क की सफेद पट्टी (Road Markings)
        self.city_y = (self.city_y + self.speed) % 400
        for i in range(-400, self.HEIGHT, 100):
            pygame.draw.rect(self.screen, (200, 200, 200), (self.WIDTH//2 - 5, i + self.city_y, 10, 50))

        # सिटी बिल्डिंग्स और खिड़कियाँ
        for i in range(-400, self.HEIGHT, 250):
            # बाईं इमारत
            pygame.draw.rect(self.screen, (60, 60, 80), (0, i + self.city_y, 35, 200))
            pygame.draw.rect(self.screen, (255, 255, 150), (10, i + self.city_y + 40, 15, 25)) # खिड़की
            pygame.draw.rect(self.screen, (255, 255, 150), (10, i + self.city_y + 120, 15, 25)) # खिड़की
            
            # दाईं इमारत
            pygame.draw.rect(self.screen, (60, 60, 80), (self.WIDTH - 35, i + self.city_y, 35, 200))
            pygame.draw.rect(self.screen, (255, 255, 150), (self.WIDTH - 25, i + self.city_y + 40, 15, 25)) # खिड़की
            pygame.draw.rect(self.screen, (255, 255, 150), (self.WIDTH - 25, i + self.city_y + 120, 15, 25)) # खिड़की

    def draw_ui(self):
        # बटन्स को और चमकदार बनाया गया है
        pygame.draw.rect(self.screen, (220, 220, 220), self.btn_left, border_radius=15)
        pygame.draw.rect(self.screen, (0, 255, 100), self.btn_jump, border_radius=15)
        pygame.draw.rect(self.screen, (220, 220, 220), self.btn_right, border_radius=15)
        
        # बटन टेक्स्ट
        self.screen.blit(self.font.render("LEFT", True, (0,0,0)), (self.btn_left.centerx-30, self.btn_left.centery-15))
        self.screen.blit(self.font.render("JUMP", True, (0,0,0)), (self.btn_jump.centerx-35, self.btn_jump.centery-15))
        self.screen.blit(self.font.render("RIGHT", True, (0,0,0)), (self.btn_right.centerx-35, self.btn_right.centery-15))

        # स्कोर डिस्प्ले
        s_txt = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        h_txt = self.font.render(f"Best: {self.high_score}", True, (255, 215, 0))
        self.screen.blit(s_txt, (50, 60))
        self.screen.blit(h_txt, (self.WIDTH - h_txt.get_width() - 50, 60))

    def run(self):
        running = True
        while running:
            if self.game_over:
                self.screen.fill((10, 10, 20))
                if self.score > self.high_score: self.high_score = self.score
                
                over_txt = self.big_font.render("GAME OVER", True, (255, 50, 50))
                sc_txt = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
                best_txt = self.font.render(f"Best Score: {self.high_score}", True, (255, 215, 0))
                
                self.screen.blit(over_txt, (self.WIDTH//2 - over_txt.get_width()//2, self.HEIGHT//4))
                self.screen.blit(sc_txt, (self.WIDTH//2 - sc_txt.get_width()//2, self.HEIGHT//4 + 120))
                self.screen.blit(best_txt, (self.WIDTH//2 - best_txt.get_width()//2, self.HEIGHT//4 + 190))
                
                pygame.draw.rect(self.screen, (0, 255, 100), self.btn_restart, border_radius=20)
                res_txt = self.font.render("RESTART", True, (0, 0, 0))
                self.screen.blit(res_txt, (self.btn_restart.centerx - res_txt.get_width()//2, self.btn_restart.centery - res_txt.get_height()//2))
                
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.btn_restart.collidepoint(event.pos): self.reset_game()
                continue

            self.draw_city_area()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_left.collidepoint(event.pos) and self.player_lane > 0: self.player_lane -= 1
                    elif self.btn_right.collidepoint(event.pos) and self.player_lane < 2: self.player_lane += 1
                    elif self.btn_jump.collidepoint(event.pos) and not self.is_jumping: self.is_jumping = True

            # जंप लॉजिक
            y_off = 0
            if self.is_jumping:
                if self.jump_count >= -10:
                    y_off = (self.jump_count ** 2) * 1.5 * (1 if self.jump_count > 0 else -1)
                    self.jump_count -= 1
                else: self.is_jumping, self.jump_count = False, 10

            # प्लेयर
            px = self.player_lane * self.LANE_WIDTH + (self.LANE_WIDTH // 2) - 40
            pygame.draw.rect(self.screen, (0, 120, 255), (px, self.player_y - y_off, 80, 110), border_radius=12)
            pygame.draw.rect(self.screen, (200, 255, 255), (px+10, self.player_y - y_off + 20, 60, 20), border_radius=5) # आँखों वाला हिस्सा

            # बाधाएं और सिक्के
            if random.randint(1, 35) == 1: self.obstacles.append([random.randint(0, 2), -150])
            if random.randint(1, 50) == 1: self.coins.append([random.randint(0, 2), -100])

            for c in self.coins[:]:
                c[1] += self.speed
                pygame.draw.circle(self.screen, (255, 215, 0), (c[0]*self.LANE_WIDTH + self.LANE_WIDTH//2, int(c[1])), 22)
                if abs(c[1] - (self.player_y - y_off)) < 80 and c[0] == self.player_lane:
                    self.score += 10
                    self.coins.remove(c)

            for o in self.obstacles[:]:
                o[1] += self.speed
                pygame.draw.rect(self.screen, (255, 60, 60), (o[0]*self.LANE_WIDTH + 10, o[1], self.LANE_WIDTH-20, 80), border_radius=10)
                if not self.is_jumping and abs(o[1] - self.player_y) < 80 and o[0] == self.player_lane:
                    self.game_over = True
                if o[1] > self.HEIGHT: self.obstacles.remove(o); self.score += 1

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)
            self.speed += 0.002

        pygame.quit()

if __name__ == "__main__":
    Game().run()
