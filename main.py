import pygame as pg

from char import Char
from color import COLOR_REF
from controller import Controller


class Game():
	def __init__(self, screen_dims):
		self.stage_dims = screen_dims

		self.font           = pg.font.Font('FiraCode-Regular.ttf', 10)
		self.image          = pg.Surface(screen_dims)
		self.paused         = True
		self.robo           = None  # Char

		self.create_robo()

	def check_stage_boundaries(self, pos: pg.Vector2) -> tuple[bool]:
		out_of_bounds_x = False
		out_of_bounds_y = False

		if (pos.x < 0) or (pos.x > self.stage_dims[0] - self.robo.width):
			out_of_bounds_x = True

		if (pos.y < 0) or (pos.y > self.stage_dims[1] - self.robo.height):
			out_of_bounds_y = True

		return out_of_bounds_x, out_of_bounds_y

	def create_robo(self):
		self.robo = Char()
		self.robo.move((self.stage_dims[0] / 2 - self.robo.width / 2, self.stage_dims[1] - self.robo.height * 6))

	def draw(self):
		self.image.fill(COLOR_REF['black'])
		self.image.blit(self.robo.sprite, tuple(self.robo.pos))

		velocity = f'{round(self.robo.velocity.x, 1)}, {round(self.robo.velocity.y, 1)}'
		velocity_x = self.font.render(velocity, False, COLOR_REF['yellow'])
		self.image.blit(velocity_x, (100, 10))

		self.image.blit(self.font.render(str(self.robo.charge), False, COLOR_REF['cyan']), (130, 25))

	def unpause(self):
		self.paused = False

	def update(self, delta: int, controller: Controller):
		if not self.paused:
			self.robo.update(delta, controller)
			out_of_bounds_x, out_of_bounds_y = self.check_stage_boundaries(self.robo.get_rect_vector())
			if out_of_bounds_x or out_of_bounds_y:
				self.robo.stop_at_stage_boundary(out_of_bounds_x, out_of_bounds_y, self.stage_dims, controller)

			self.robo.advance_to_rect_pos()

		self.draw()


def main():
	screen_dims = (160, 240)
	screen = pg.display.set_mode(screen_dims, pg.SCALED)
	clock = pg.time.Clock()

	controller = Controller('wasd')

	game = Game(screen_dims)
	game.unpause()

	running = True
	while running:
		delta = clock.tick(30)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			elif event.type == pg.KEYDOWN:
				controller.handle_keydown(event.key)
			elif event.type == pg.KEYUP:
				controller.handle_keyup(event.key)

		game.update(delta, controller)
		controller.update()

		screen.fill(COLOR_REF['black'])
		screen.blit(game.image, (0, 0))
		pg.display.flip()


if __name__ == '__main__':
	pg.init()
	pg.display.set_caption('Repulsar')

	main()
