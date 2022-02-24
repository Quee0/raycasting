import pygame
import random

pygame.init()

width, height = 960, 540
WHITE = (255,255,255)

map_tile_size = 30

level = [[1, 1, 1, 1, 1, 1],
         [1, 0, 1, 1, 0, 1],
         [1, 0, 1, 0, 0, 1],
         [1, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1]]

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.image = pygame.Surface([50,50])
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center = pos)

def main():

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('raycasting')

	running = True



	player = pygame.sprite.GroupSingle()
	player.add(Player((500,500)))



	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		for c_row, row in enumerate(level):
			for c_col, col in enumerate(row):
				if col == 1: pygame.draw.rect(screen, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), (c_col*30, c_row*30, 30, 30))

		player.draw(screen)

		pygame.display.update()


if __name__ == '__main__':
	main()
	pygame.quit()
