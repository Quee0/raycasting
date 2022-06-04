import pygame
import math

pygame.init()

width, height = 1024, 540
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (157, 2, 8)
GREEN = (128, 185, 24)
LIGHT_GREEN = (217, 237, 146)
YELLOW = (255, 255, 0)

map_tile_size = 64
map_width = 8
map_height = 8
shade = 1
shade_intensity = 25000

level = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 1, 1, 0, 0, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 1, 1],
         [1, 0, 1, 0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]]

cord_list_x = list(range(0, 64 * map_width, map_tile_size))
cord_list_y = list(range(0, 64 * map_height, map_tile_size))

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.angle = 1.4*math.pi
		self.delta_x = 1
		self.delta_y = 1

		self.image = pygame.Surface([map_tile_size//3, map_tile_size//3])
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center = pos)

		self.last_x = self.rect.x
		self.last_y = self.rect.y
	
	def move(self):
		queue_x, queue_y = 0, 0
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			queue_x += self.delta_x
			queue_y += self.delta_y
		elif keys[pygame.K_s]: 
			self.rect.x -= self.delta_x
			queue_y -= self.delta_y
		# P_range = math.sqrt(self.delta_x**2 + self.delta_y**2) ALWAYS 3
		P_range = 3
		self.cos_range = P_range * math.cos(self.angle-math.pi/2)
		self.sin_range = P_range * math.sin(self.angle-math.pi/2)
		if keys[pygame.K_a]:
			queue_x += self.cos_range
			queue_y += self.sin_range
		if keys[pygame.K_d]:
			queue_x -= self.cos_range
			queue_y -= self.sin_range
		if keys[pygame.K_LEFT]:
			self.angle -= math.pi/60
			self.delta_x = math.cos(self.angle)*3
			self.delta_y = math.sin(self.angle)*3
			
		elif keys[pygame.K_RIGHT]:
			self.angle += math.pi/60
			self.delta_x = math.cos(self.angle)*3
			self.delta_y = math.sin(self.angle)*3

		if self.angle > 2*math.pi: self.angle = 0
		if self.angle < 0: self.angle = 2*math.pi

		if queue_x > 2: queue_x = 2
		elif queue_x < -2: queue_x = -2 
		if queue_y > 2: queue_y = 2
		elif queue_y < -2: queue_y = -2 
		self.rect.x += queue_x
		self.rect.y += queue_y


	def cast_rays(self,walls):
		ray_angle = self.angle-30*0.0175
		list_of_rays = []
		for i in range(60):
			ray_angle += (2*math.pi/360)
		
			#fix angle
			if ray_angle > 2*math.pi: ray_angle -= 2*math.pi
			if ray_angle < 0: ray_angle += 2*math.pi 
			# --Check horisontal lines--
			ray_x, ray_y = 0, 0
			if ray_angle > math.pi: #Looking up
				ray_y = min(cord_list_y, key=lambda x: abs(x-self.rect.centery+30))
				ray_x = self.rect.centerx - (1/math.tan(ray_angle-math.pi) * abs(ray_y-self.rect.centery))
				y_offset = -map_tile_size
				x_offset = y_offset*(1/math.tan(ray_angle))
				

			elif ray_angle < math.pi: #Looking down
				ray_y = min(cord_list_y, key=lambda x: abs(x-self.rect.centery-30))
				ray_x = self.rect.centerx + (1/math.tan(ray_angle-math.pi) * abs(ray_y-self.rect.centery))
				y_offset = map_tile_size
				x_offset = y_offset*(1/(math.tan(ray_angle)+0.000001))

			found = False
			if ray_angle == 2*math.pi or ray_angle == math.pi or ray_angle == 0: 
				ray_x, ray_y = 1000000000, 1000000000
				found = True
			
			limiter = 0
			while not found: # finding collisions
				if limiter >= 10: break
				for tile in walls:
					if not tile.rect.colliderect(pygame.Rect((ray_x-2, ray_y-2),(4,4))):
						pass
					else: 
						found = True
						break
				
				if not found:
					ray_y += y_offset
					ray_x += x_offset
				limiter += 1

			ray_length = math.sqrt( abs(self.rect.centerx-ray_x)**2.0 + abs(self.rect.centery-ray_y)**2.0 )

			#--Check Vertical lines--
			ray2_x, ray2_y = 0, 0
			if ray_angle > 0.5*math.pi and ray_angle < 1.5*math.pi:  # Looking left
				ray2_x = min(cord_list_x, key=lambda x: abs(x-self.rect.centerx+30))
				ray2_y = self.rect.centery - (math.tan(ray_angle-math.pi) * abs(ray2_x-self.rect.centerx))
				x_offset2 = -map_tile_size
				y_offset2 = x_offset2*(math.tan(ray_angle))

			elif (ray_angle > 0 and ray_angle < 0.5*math.pi) or (ray_angle > 1.5*math.pi and ray_angle < 2*math.pi):  # Looking right
				ray2_x = min(cord_list_x, key=lambda x: abs(x-self.rect.centerx-30))
				ray2_y = self.rect.centery + (math.tan(ray_angle-math.pi) * abs(ray2_x-self.rect.centerx))
				x_offset2 = map_tile_size
				y_offset2 = x_offset2*(math.tan(ray_angle))

			found2 = False
			if ray_angle == 1.5*math.pi or ray_angle == 0.5*math.pi or ray_angle == 0:
				ray2_x, ray2_y = 1000000000, 1000000000
				found2 = True

			limiter2 = 0
			while not found2:  # finding collisions
				if limiter2 >= 10:
					break
				for tile in walls:
					if not tile.rect.colliderect(pygame.Rect((ray2_x-2, ray2_y-2), (4, 4))):
						pass
					else:
						found2 = True
						break

				if not found2:
					ray2_y += y_offset2
					ray2_x += x_offset2
				limiter2 += 1

			ray2_length = math.sqrt( abs(self.rect.centerx-ray2_x)**2.0 + abs(self.rect.centery-ray2_y)**2.0 )

			if ray_length < ray2_length: ray_b_x, ray_b_y, ray_b_length = ray_x, ray_y, ray_length
			if ray_length > ray2_length: ray_b_x, ray_b_y, ray_b_length = ray2_x, ray2_y, ray2_length

			ca = self.angle - ray_angle
			if ca > 2*math.pi: ca -= 2*math.pi
			if ca < 0: ca += 2*math.pi
			ray_b_length = ray_b_length * math.cos(ca)
			
			list_of_rays.append([ray_b_x, ray_b_y, ray_b_length, ray2_x, ray2_y, ray_x, ray_y])
		return list_of_rays

	def collisions(self,objects):
		for object in objects:
			if object.rect.colliderect(pygame.Rect(self.rect.topleft[0], self.rect.topleft[1], self.image.get_width(), 1)) or object.rect.colliderect(pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1], self.image.get_width(), 1)):
				self.rect.y = self.last_y
			if object.rect.colliderect(pygame.Rect(self.rect.topleft[0], self.rect.topleft[1], 1, self.image.get_height())) or object.rect.colliderect(pygame.Rect(self.rect.topright[0], self.rect.topright[1], 1, self.image.get_height())):
				self.rect.x = self.last_x
		self.last_x = self.rect.x
		self.last_y = self.rect.y


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
	player.add(Player((220,220)))



	while running:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		player.sprite.move()
		player.sprite.collisions(walls)
		rays = player.sprite.cast_rays(walls)

		screen.fill(BLACK)

		walls.draw(screen)
		player.draw(screen)
		for ray_counter, ray in enumerate(rays):
			pygame.draw.line(screen, (0, 0, 255), (player.sprite.rect.centerx, player.sprite.rect.centery), (ray[0], ray[1]), width=1)
			line_height = (1/(ray[2]+0.0000001))*15000+100
			if ray[2] < 20: line_height = 1000
			shade = int((1/line_height)*shade_intensity)
			if shade > 255: shade = 255
			pygame.draw.rect(screen, (255-shade, 255-shade, 255-shade), pygame.Rect((ray_counter*8+512, line_height/2-500), (8, line_height+500)))
		
		pygame.draw.line(screen, GREEN, (player.sprite.rect.centerx, player.sprite.rect.centery), (player.sprite.rect.centerx + player.sprite.delta_x*5, player.sprite.rect.centery+player.sprite.delta_y*5), width=3)
		pygame.draw.rect(screen, GREEN, pygame.Rect(player.sprite.cos_range-2+player.sprite.rect.centerx, player.sprite.sin_range-2+player.sprite.rect.centery, 4,4))
		pygame.display.update()


if __name__ == '__main__':
	main()
	pygame.quit()
