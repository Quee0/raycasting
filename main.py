import pygame
import math

pygame.init()

width, height = 960, 540
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (157, 2, 8)
GREEN = (128, 185, 24)

map_tile_size = 52
map_width = 8
map_height = 8

level = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 1, 1, 0, 0, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 1, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]]

ys_list = list(range(0, 52 * map_height, map_tile_size))

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.angle = 1.4*math.pi
		self.delta_x = 1
		self.delta_y = 1

		self.image = pygame.Surface([map_tile_size//3, map_tile_size//3])
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center = pos)
	
	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]: 
			self.rect.x += self.delta_x
			self.rect.y += self.delta_y
		elif keys[pygame.K_DOWN]: 
			self.rect.x -= self.delta_x
			self.rect.y -= self.delta_y
		if keys[pygame.K_LEFT]: 
			self.angle -= math.pi/30
			self.delta_x = math.cos(self.angle)*5
			self.delta_y = math.sin(self.angle)*5
			
		elif keys[pygame.K_RIGHT]: 
			self.angle += math.pi/30
			self.delta_x = math.cos(self.angle)*5
			self.delta_y = math.sin(self.angle)*5

		if self.angle > 2*math.pi: self.angle = 0
		elif self.angle < 0: self.angle = 2*math.pi

	def cast_rays(self,walls):
		ray_angle = self.angle
		for ray in range(1):

			# --Check horisontal lines--
			ray_x, ray_y = 0, 0
			if ray_angle > math.pi: #Looking up
				ray_y = min(ys_list, key=lambda x: abs(x-self.rect.centery+map_tile_size))
				ray_x = self.rect.centerx - (1/math.tan(ray_angle-math.pi) * abs(ray_y-self.rect.centery))
				y_offset = -map_tile_size
				x_offset = y_offset*(1/math.tan(ray_angle))
				

			elif ray_angle < math.pi: #Looking down
				ray_y = min(ys_list, key=lambda x: abs(x-self.rect.centery-map_tile_size))
				ray_x = self.rect.centerx + (1/math.tan(ray_angle-math.pi) * abs(ray_y-self.rect.centery))
				y_offset = map_tile_size
				x_offset = y_offset*(1/(math.tan(ray_angle)+0.000001))

			found = False

			print(ray_angle)
			if ray_angle == 2*math.pi or ray_angle == math.pi or ray_angle == 0: 
				ray_x, ray_y = self.rect.centerx, self.rect.centery
				found = True
			
			limiter = 0
			while not found: # finding collisions
				if limiter >= 10: break
				for tile in walls:
					if not tile.rect.colliderect(pygame.Rect((ray_x-1, ray_y-1),(2,2))):
						pass
					else: 
						found = True
						break
				
				if not found:
					ray_y += y_offset
					ray_x += x_offset
				limiter += 1

			return [ray_x, ray_y]


class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,color):
		super().__init__()

		self.image = pygame.Surface([map_tile_size, map_tile_size])
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = pos)

def main():

	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('raycasting')

	running = True
	clock = pygame.time.Clock()


	walls = pygame.sprite.Group()
	for c_row, row in enumerate(level):
		for c_col, col in enumerate(row):
			if col == 1:
				walls.add(Tile((c_col*map_tile_size, c_row *map_tile_size),RED))

	player = pygame.sprite.GroupSingle()
	player.add(Player((200,200)))



	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		player.sprite.move()
		ray_l = player.sprite.cast_rays(walls)
		ray_x, ray_y = ray_l[0], ray_l[1]

		screen.fill(BLACK)
		
		walls.draw(screen)
		player.draw(screen)
		pygame.draw.line(screen, (0, 0, 255), (player.sprite.rect.centerx, player.sprite.rect.centery), (ray_x, ray_y), width=5)
		pygame.draw.line(screen, GREEN, (player.sprite.rect.centerx, player.sprite.rect.centery), (player.sprite.rect.centerx + player.sprite.delta_x*5, player.sprite.rect.centery+player.sprite.delta_y*5), width=3)

		pygame.draw.circle(screen, WHITE, (ray_x,ray_y), 1)
		pygame.display.update()


if __name__ == '__main__':
	main()
	pygame.quit()
