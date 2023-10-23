import pygame as pg

from color import COLOR_REF
from controller import Controller


class Char(pg.sprite.Sprite):
	def __init__(self):
		self.acceleration   = pg.Vector2(1, .9)
		self.air_decel      = .9
		self.charge           = 0
		self.ground_decel   = .6
		self.grounded       = False
		self.grounding_dist = 1
		self.height         = 0
		self.image          = None  # pg.Surface
		self.jump_buffer    = .2
		self.jump_force     = -5
		self.max_charge       = 60
		self.max_velocity   = pg.Vector2(5, 10)
		self.pos            = pg.Vector2(0, 0)
		self.rect           = None  # pg.Rect
		self.repulse_force  = -1.8
		self.sprite         = None  # pg.Surface
		self.velocity       = pg.Vector2(0, 0)
		self.width          = 0

		self.load_image()

	def advance_to_rect_pos(self):
		self.pos = self.get_rect_vector()

	def apply_movement(self):
		if abs(self.velocity.x) < .1:
			self.velocity.x = 0
		if abs(self.velocity.y) < .1:
			self.velocity.y = 0

		self.rect.x += self.velocity.x
		self.rect.y += self.velocity.y

	def decelerate(self):
		deceleration = self.ground_decel if self.grounded else self.air_decel
		self.velocity.x *= deceleration

	def draw(self):
		self.image.fill(COLOR_REF['transparent'])
		self.image.blit(self.sprite, (0, 0))

	def get_rect_vector(self) -> pg.Vector2:
		return pg.Vector2(self.rect.x, self.rect.y)

	def handle_direction(self, delta: int, controller: Controller):
		if controller.button('LEFT').is_down and controller.button('RIGHT').is_down:
			self.decelerate()
			return

		if controller.button('LEFT').is_down:
			if self.velocity.x > -self.max_velocity.x:
				self.velocity.x -= self.acceleration.x

		elif controller.button('RIGHT').is_down:
			if self.velocity.x < self.max_velocity.x:
				self.velocity.x += self.acceleration.x

		else:
			self.decelerate()

	def handle_gravity(self, delta: int):
		if not self.grounded:
			if self.velocity.y < self.max_velocity.y:
				self.velocity.y += self.acceleration.y

	def handle_jump(self, controller: Controller):
		if controller.button('JUMP').press_flag and self.grounded:
			self.velocity.y += self.jump_force
			self.grounded = False
		elif controller.button('JUMP').is_down:
			if self.charge > 0:
				self.charge -= 1

				if -self.velocity.y < self.max_velocity.y:
					self.velocity.y += self.repulse_force
				else:
					self.velocity.y = -self.max_velocity.y

	def land(self):
		self.velocity.y = 0
		self.grounded = True
		self.charge = self.max_charge

	def load_image(self):
		self.sprite = pg.image.load('img/char.png')
		self.sprite.set_colorkey(COLOR_REF['transparent'])
		self.image = pg.Surface(self.sprite.get_size())
		self.image.fill(COLOR_REF['transparent'])

		self.rect = self.sprite.get_rect()
		self.height = self.rect.h
		self.width = self.rect.w

	def move(self, pos: tuple[int|float]):
		self.pos = pg.Vector2(pos)
		self.move_rect_to_pos()

	def move_rect_to_pos(self):
		self.rect.move(tuple(self.pos))

	def recharge(self):
		self.charge = self.max_charge

	def set_next_pos(self, x: float=None, y: float=None):
		if x is not None:
			self.rect.x = x
		if y is not None:
			self.rect.y = y

	def stop_at_stage_boundary(self, x: bool, y: bool, stage_dims: tuple[int], controller: Controller):
		if x:
			if self.velocity.x > 0:
				self.set_next_pos(x=stage_dims[0] - self.width)
			else:
				self.set_next_pos(x=0)

			self.velocity.x *= -.5
		if y:
			if self.velocity.y > 0:
				self.set_next_pos(y=stage_dims[1] - self.height)
				if controller.button('JUMP').is_down:
					self.velocity.y = 0
				else:
					self.land()
			else:
				self.set_next_pos(y=0)
				self.velocity.y *= -.5

	def update(self, delta: int, controller: Controller):
		# self.handle_collisions()
		if self.grounded:
			self.recharge()

		self.handle_jump(controller)
		self.handle_direction(delta, controller)
		self.handle_gravity(delta)
		self.apply_movement()

		self.draw()
