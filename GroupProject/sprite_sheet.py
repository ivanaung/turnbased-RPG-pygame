import pygame

class SpriteSheet:
    def __init__(self, file_path):
        self.sheet = pygame.image.load(file_path).convert_alpha()

    def extract_frames(self, frame_width, frame_height):
        sheet_width, sheet_height = self.sheet.get_size()
        frames = []
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = self.sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)
        return frames