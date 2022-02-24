import pygame
import random

pygame.init()

width, height = 960, 540
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (157, 2, 8)

map_tile_size = 30
speed = 2

level = [[1, 1, 1, 1, 1, 1],
         [1, 0, 1, 1, 0, 1],
         [1, 0, 1, 0, 0, 1],
         [1, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1]]

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.image = pygame.Surface([map_tile_size//3, map_tile_size//3])
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center = pos)
	
	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]: self.rect.y -= speed
		elif keys[pygame.K_DOWN]: self.rect.y += speed
		if keys[pygame.K_LEFT]: self.rect.x -= speed
		elif keys[pygame.K_RIGHT]: self.rect.x += speed

def main():

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('raycasting')

	running = True
	clock = pygame.time.Clock()



	player = pygame.sprite.GroupSingle()
	player.add(Player((50,50)))



	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		player.sprite.move()
		player.update()
	
		screen.fill(BLACK)

		for c_row, row in enumerate(level):
			for c_col, col in enumerate(row):
				if col == 1: pygame.draw.rect(screen, RED, (c_col*30, c_row*30, 30, 30))
		
		player.draw(screen)
		pygame.display.update()


if __name__ == '__main__':
	main()
	pygame.quit()
