import pygame

class GameLog:
    def __init__(self, screen, width, height, max_lines=10):
        font = pygame.font.SysFont("Arial",12)
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.max_lines = max_lines
        self.logs = []  # Stores all lines of text
        self.scroll_offset = 0  # Keeps track of how much the text is scrolled
        self.auto_scroll = True  # Flag for auto-scrolling

    def add_log(self, text):
        """Add a new line of text to the log."""
        self.logs.append(text)
        # Keep the number of lines below the maximum allowed
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
        # Auto-scroll to the bottom when new logs are added
        if self.auto_scroll:
            self.scroll_offset = len(self.logs) - self.max_lines if len(self.logs) > self.max_lines else 0

    def draw(self):
        """Draw the scrollable game log on the screen."""
        # Draw background for log area
        text_title = self.font.render("Game Logs", True, (254, 250, 255))
        self.screen.blit(text_title, (10, 40))

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 60, self.width, self.height-100))
        
        # Draw the log lines
        for i, line in enumerate(self.logs[self.scroll_offset:self.scroll_offset + self.max_lines]):
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 65 + i * 20))

        # Draw the scrollbar

    def scroll_up(self):
        """Scroll the log up."""
        if self.scroll_offset > 0:
            self.scroll_offset -= 1

    def scroll_down(self):
        """Scroll the log down."""
        if self.scroll_offset < len(self.logs) - self.max_lines:
            self.scroll_offset += 1

    def handle_events(self, event):
        """Handle user input for scrolling."""
        if event.type == pygame.MOUSEWHEEL:
            if event.y < 0:  # Scroll down
                self.scroll_down()
            elif event.y > 0:  # Scroll up
                self.scroll_up()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Arrow up
                self.scroll_up()
            elif event.key == pygame.K_DOWN:  # Arrow down
                self.scroll_down()