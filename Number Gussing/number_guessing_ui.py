import random
import pygame
import sys
import math
from pygame import mixer

class NumberGuessingGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        mixer.init()
        
        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1000, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Number Guessing Game")
        
        # Colors
        self.DARK_BG = (15, 20, 35)
        self.PRIMARY = (0, 184, 255)
        self.SECONDARY = (255, 105, 180)
        self.ACCENT = (50, 215, 75)
        self.TEXT_COLOR = (240, 245, 255)
        self.INPUT_BG = (30, 40, 60)
        self.BUTTON_COLOR = (40, 130, 200)
        self.BUTTON_HOVER = (60, 170, 240)
        
        # Fonts
        self.title_font = pygame.font.SysFont("segoeui", 60, bold=True)
        self.subtitle_font = pygame.font.SysFont("segoeui", 32)
        self.normal_font = pygame.font.SysFont("segoeui", 28)
        self.small_font = pygame.font.SysFont("segoeui", 22)
        self.button_font = pygame.font.SysFont("segoeui", 26, bold=True)
        
        # Game states
        self.MENU = 0
        self.GAME = 1
        self.RESULT = 2
        self.current_state = self.MENU
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.guesses = []
        self.current_guess = ""
        self.message = ""
        self.difficulty = ""
        self.game_won = False
        self.score = 0
        self.animation_time = 0
        
        # Particle effects
        self.particles = []
        for i in range(100):
            self.particles.append({
                'x': random.randint(0, self.WIDTH),
                'y': random.randint(0, self.HEIGHT),
                'size': random.uniform(0.5, 3),
                'speed': random.uniform(0.1, 0.5),
                'color': (
                    random.randint(100, 200),
                    random.randint(100, 200),
                    random.randint(200, 255),
                    random.randint(50, 150)
                ),
                'angle': random.uniform(0, 2 * math.pi)
            })
            
        # Create buttons
        self.easy_button = self.Button(self.WIDTH//2 - 150, 250, 300, 60, "Easy Mode (10 attempts)")
        self.medium_button = self.Button(self.WIDTH//2 - 150, 330, 300, 60, "Medium Mode (7 attempts)")
        self.hard_button = self.Button(self.WIDTH//2 - 150, 410, 300, 60, "Hard Mode (5 attempts)")
        self.play_again_button = self.Button(self.WIDTH//2 - 150, 450, 300, 60, "Play Again")
        self.menu_button = self.Button(self.WIDTH//2 - 150, 530, 300, 60, "Main Menu")
        self.submit_button = self.Button(self.WIDTH//2 + 120, 350, 150, 50, "Submit")
        
        # Input box
        self.input_box = pygame.Rect(self.WIDTH//2 - 200, 350, 300, 50)
        
    class Button:
        def __init__(self, x, y, width, height, text, color=None, hover_color=None):
            if color is None:
                color = (40, 130, 200)
            if hover_color is None:
                hover_color = (60, 170, 240)
                
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.hover_color = hover_color
            self.is_hovered = False
            self.animation_progress = 0
            
        def draw(self, surface, font):
            # Smooth hover animation
            target_progress = 1.0 if self.is_hovered else 0.0
            self.animation_progress += (target_progress - self.animation_progress) * 0.2
            
            # Interpolate color
            r = int(self.color[0] + (self.hover_color[0] - self.color[0]) * self.animation_progress)
            g = int(self.color[1] + (self.hover_color[1] - self.color[1]) * self.animation_progress)
            b = int(self.color[2] + (self.hover_color[2] - self.color[2]) * self.animation_progress)
            current_color = (r, g, b)
            
            # Draw button with rounded corners and shadow
            shadow_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.rect.width, self.rect.height)
            pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=12)
            
            pygame.draw.rect(surface, current_color, self.rect, border_radius=12)
            
            # Add highlight effect
            highlight = pygame.Surface((self.rect.width, 15), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 30))
            surface.blit(highlight, (self.rect.x, self.rect.y))
            
            # Draw text with shadow
            text_surf = font.render(self.text, True, (240, 245, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            
            shadow_surf = font.render(self.text, True, (0, 0, 0, 100))
            shadow_rect = text_surf.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
            
            surface.blit(shadow_surf, shadow_rect)
            surface.blit(text_surf, text_rect)
            
        def check_hover(self, pos):
            self.is_hovered = self.rect.collidepoint(pos)
            
        def is_clicked(self, pos, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return self.rect.collidepoint(pos)
            return False

    def draw_animated_background(self):
        # Draw gradient background
        for y in range(self.HEIGHT):
            color = (
                max(10, min(25, 15 + y//50)),
                max(15, min(30, 20 + y//40)),
                max(25, min(45, 35 + y//30))
            )
            pygame.draw.line(self.screen, color, (0, y), (self.WIDTH, y))
        
        # Draw animated particles
        self.animation_time += 0.01
        
        for particle in self.particles:
            # Update position with subtle movement
            particle['x'] += math.cos(particle['angle'] + self.animation_time) * particle['speed']
            particle['y'] += math.sin(particle['angle'] + self.animation_time) * particle['speed']
            
            # Wrap around screen
            if particle['x'] < 0: particle['x'] = self.WIDTH
            if particle['x'] > self.WIDTH: particle['x'] = 0
            if particle['y'] < 0: particle['y'] = self.HEIGHT
            if particle['y'] > self.HEIGHT: particle['y'] = 0
            
            # Draw particle
            alpha_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                alpha_surface, 
                particle['color'], 
                (int(particle['size']), int(particle['size'])), 
                int(particle['size'])
            )
            self.screen.blit(alpha_surface, (int(particle['x']), int(particle['y'])))

    def draw_menu(self):
        self.draw_animated_background()
        
        # Draw title with gradient effect
        title_text = "Number Guessing Game"
        for i, char in enumerate(title_text):
            if char != " ":
                color = (
                    self.PRIMARY[0] + i * 2,
                    min(255, self.PRIMARY[1] + i * 3),
                    min(255, self.PRIMARY[2] + i)
                )
                char_surf = self.title_font.render(char, True, color)
                self.screen.blit(char_surf, (self.WIDTH//2 - self.title_font.size(title_text)[0]//2 + i * 32, 100))
        
        # Draw subtitle
        subtitle = self.subtitle_font.render("Guess the number between 1 and 100", True, self.TEXT_COLOR)
        subtitle_shadow = self.subtitle_font.render("Guess the number between 1 and 100", True, (0, 0, 0, 100))
        self.screen.blit(subtitle_shadow, (self.WIDTH//2 - subtitle.get_width()//2 + 2, 182))
        self.screen.blit(subtitle, (self.WIDTH//2 - subtitle.get_width()//2, 180))
        
        # Draw buttons
        self.easy_button.draw(self.screen, self.button_font)
        self.medium_button.draw(self.screen, self.button_font)
        self.hard_button.draw(self.screen, self.button_font)
        
        # Draw decorative elements
        pygame.draw.line(self.screen, self.PRIMARY, (self.WIDTH//2 - 180, 230), (self.WIDTH//2 + 180, 230), 2)
        pygame.draw.line(self.screen, self.PRIMARY, (self.WIDTH//2 - 180, 490), (self.WIDTH//2 + 180, 490), 2)
        
        # Draw instructions with fade-in effect
        instructions = [
            "• Use the number keys to enter your guess",
            "• Press Backspace to correct your input",
            "• Press Enter or click Submit to check your guess",
            "• The game will give you hints if you're close"
        ]
        
        for i, instruction in enumerate(instructions):
            alpha = min(255, int(200 + 55 * math.sin(self.animation_time * 2 + i)))
            text = self.small_font.render(instruction, True, (200, 200, 200, alpha))
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, 500 + i*30))

    def draw_game(self):
        self.draw_animated_background()
        
        # Draw title with subtle animation
        title = self.subtitle_font.render(f"Guess the Number - {self.difficulty} Mode", True, self.PRIMARY)
        title_y = 30 + 2 * math.sin(self.animation_time * 2)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, title_y))
        
        # Draw attempts with progress bar
        attempts_text = self.normal_font.render(f"Attempts: {self.attempts}/{self.max_attempts}", True, self.TEXT_COLOR)
        self.screen.blit(attempts_text, (self.WIDTH//2 - attempts_text.get_width()//2, 80))
        
        # Progress bar background
        pygame.draw.rect(self.screen, (40, 50, 70), (self.WIDTH//2 - 150, 120, 300, 15), border_radius=7)
        
        # Progress bar fill
        progress = self.attempts / self.max_attempts
        color = (
            int(200 * progress),
            int(200 * (1 - progress)),
            50
        )
        pygame.draw.rect(self.screen, color, (self.WIDTH//2 - 150, 120, 300 * progress, 15), border_radius=7)
        
        # Draw input box with glow effect
        pygame.draw.rect(self.screen, self.INPUT_BG, self.input_box, border_radius=8)
        
        # Add glow effect when focused
        glow_intensity = abs(math.sin(self.animation_time * 3)) * 100 + 50
        glow_surface = pygame.Surface((self.input_box.width + 20, self.input_box.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (self.PRIMARY[0], self.PRIMARY[1], self.PRIMARY[2], int(glow_intensity)), 
                        (10, 10, self.input_box.width, self.input_box.height), border_radius=12)
        self.screen.blit(glow_surface, (self.input_box.x - 10, self.input_box.y - 10))
        
        pygame.draw.rect(self.screen, self.PRIMARY, self.input_box, 2, border_radius=8)
        
        # Draw current guess
        guess_text = self.normal_font.render(self.current_guess, True, self.TEXT_COLOR)
        self.screen.blit(guess_text, (self.input_box.x + 15, self.input_box.y + 10))
        
        # Draw submit button
        self.submit_button.draw(self.screen, self.button_font)
        
        # Draw message with animation
        if self.message:
            msg_color = self.ACCENT if "Congratulations" in self.message else self.SECONDARY
            alpha = 200 + int(55 * math.sin(self.animation_time * 4))
            msg_text = self.normal_font.render(self.message, True, msg_color)
            msg_rect = msg_text.get_rect(center=(self.WIDTH//2, 250))
            self.screen.blit(msg_text, msg_rect)
        
        # Draw previous guesses
        if self.guesses:
            guesses_text = self.small_font.render("Your guesses: " + ", ".join(map(str, self.guesses)), True, self.TEXT_COLOR)
            self.screen.blit(guesses_text, (self.WIDTH//2 - guesses_text.get_width()//2, 420))
        
        # Draw hint if available
        if self.attempts > 0 and not self.game_won and self.current_guess:
            guess_num = int(self.current_guess) if self.current_guess.isdigit() else 0
            if guess_num > 0:
                difference = abs(self.secret_number - guess_num)
                if difference == 0:
                    hint = "Perfect! You found it!"
                    hint_color = self.ACCENT
                elif difference <= 5:
                    hint = "Very hot! You're almost there!"
                    hint_color = (255, 100, 100)
                elif difference <= 15:
                    hint = "Hot! Getting closer!"
                    hint_color = (255, 150, 50)
                elif difference <= 25:
                    hint = "Warm"
                    hint_color = (255, 200, 50)
                else:
                    hint = "Cold"
                    hint_color = (100, 150, 255)
                
                hint_text = self.normal_font.render(hint, True, hint_color)
                self.screen.blit(hint_text, (self.WIDTH//2 - hint_text.get_width()//2, 320))
                
                # Draw temperature indicator
                indicator_width = 300
                indicator_x = self.WIDTH//2 - indicator_width//2
                pygame.draw.rect(self.screen, (40, 50, 70), (indicator_x, 360, indicator_width, 20), border_radius=10)
                
                # Position based on difference (inverse)
                pos = indicator_x + indicator_width * (1 - min(50, difference) / 50)
                pygame.draw.circle(self.screen, hint_color, (int(pos), 370), 12)

    def draw_result(self):
        self.draw_animated_background()
        
        if self.game_won:
            # Draw victory message with animation
            result_text = self.subtitle_font.render("Congratulations! You guessed the number!", True, self.ACCENT)
            result_y = 150 + 5 * math.sin(self.animation_time * 3)
            self.screen.blit(result_text, (self.WIDTH//2 - result_text.get_width()//2, result_y))
            
            attempts_text = self.normal_font.render(f"It took you {self.attempts} attempts", True, self.TEXT_COLOR)
            self.screen.blit(attempts_text, (self.WIDTH//2 - attempts_text.get_width()//2, 200))
            
            score_text = self.normal_font.render(f"Your score: {self.score}", True, self.PRIMARY)
            self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 250))
            
            # Draw confetti effect
            for i in range(5):
                x = self.WIDTH//2 - 150 + i * 75
                y = 300 + 10 * math.sin(self.animation_time * 5 + i)
                pygame.draw.rect(self.screen, (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100)), 
                                (x, y, 30, 30))
        else:
            # Draw loss message
            result_text = self.subtitle_font.render("Game Over! You ran out of attempts.", True, self.SECONDARY)
            self.screen.blit(result_text, (self.WIDTH//2 - result_text.get_width()//2, 150))
            
            number_text = self.normal_font.render(f"The number was: {self.secret_number}", True, self.TEXT_COLOR)
            self.screen.blit(number_text, (self.WIDTH//2 - number_text.get_width()//2, 200))
        
        # Draw guesses
        guesses_text = self.normal_font.render("Your guesses: " + ", ".join(map(str, self.guesses)), True, self.TEXT_COLOR)
        self.screen.blit(guesses_text, (self.WIDTH//2 - guesses_text.get_width()//2, 300))
        
        # Draw buttons
        self.play_again_button.draw(self.screen, self.button_font)
        self.menu_button.draw(self.screen, self.button_font)

    def start_new_game(self, diff):
        self.difficulty = diff
        if self.difficulty == "Easy":
            self.max_attempts = 10
        elif self.difficulty == "Medium":
            self.max_attempts = 7
        else:  # Hard
            self.max_attempts = 5
            
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.guesses = []
        self.current_guess = ""
        self.message = ""
        self.game_won = False
        self.score = 0

    def check_guess(self):
        if not self.current_guess.isdigit():
            self.message = "Please enter a valid number!"
            return
            
        guess = int(self.current_guess)
        
        if guess < 1 or guess > 100:
            self.message = "Please enter a number between 1-100!"
            return
            
        self.attempts += 1
        self.guesses.append(guess)
        
        if guess == self.secret_number:
            self.message = f"Congratulations! You found it in {self.attempts} attempts!"
            self.game_won = True
            # Calculate score based on attempts and difficulty
            base_score = 1000
            multiplier = 1.0
            if self.difficulty == "Medium":
                multiplier = 1.5
            elif self.difficulty == "Hard":
                multiplier = 2.0
            self.score = int(base_score * multiplier / self.attempts)
            self.current_state = self.RESULT
        else:
            if self.attempts >= self.max_attempts:
                self.message = f"Game Over! The number was {self.secret_number}."
                self.current_state = self.RESULT
            else:
                if guess < self.secret_number:
                    self.message = "Try a higher number!"
                else:
                    self.message = "Try a lower number!"
        
        self.current_guess = ""

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.current_state == self.MENU:
                    self.easy_button.check_hover(mouse_pos)
                    self.medium_button.check_hover(mouse_pos)
                    self.hard_button.check_hover(mouse_pos)
                    
                    if self.easy_button.is_clicked(mouse_pos, event):
                        self.start_new_game("Easy")
                        self.current_state = self.GAME
                    elif self.medium_button.is_clicked(mouse_pos, event):
                        self.start_new_game("Medium")
                        self.current_state = self.GAME
                    elif self.hard_button.is_clicked(mouse_pos, event):
                        self.start_new_game("Hard")
                        self.current_state = self.GAME
                        
                elif self.current_state == self.GAME:
                    self.submit_button.check_hover(mouse_pos)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.check_guess()
                        elif event.key == pygame.K_BACKSPACE:
                            self.current_guess = self.current_guess[:-1]
                        elif event.unicode.isdigit():
                            if len(self.current_guess) < 3:  # Limit to 3 digits
                                self.current_guess += event.unicode
                                
                    if self.submit_button.is_clicked(mouse_pos, event):
                        self.check_guess()
                        
                elif self.current_state == self.RESULT:
                    self.play_again_button.check_hover(mouse_pos)
                    self.menu_button.check_hover(mouse_pos)
                    
                    if self.play_again_button.is_clicked(mouse_pos, event):
                        self.start_new_game(self.difficulty)
                        self.current_state = self.GAME
                    elif self.menu_button.is_clicked(mouse_pos, event):
                        self.current_state = self.MENU
            
            # Draw the appropriate screen based on current state
            if self.current_state == self.MENU:
                self.draw_menu()
            elif self.current_state == self.GAME:
                self.draw_game()
            elif self.current_state == self.RESULT:
                self.draw_result()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()