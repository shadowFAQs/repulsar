import pygame as pg


class Button():
	def __init__(self, name:str, binding: int):
		self.binding = binding
		self.name    = name

		self.is_down    = False
		self.press_flag = False

	def press(self):
		self.press_flag = True
		self.is_down = True

	def release(self):
		self.press_flag = False
		self.is_down = False

	def update(self):
		self.press_flag = False


class Controller():
	def __init__(self, style: str):
		self.style = style  # wasd, arrows, controller

		self.buttons = []
		self.set_buttons_from_style()

	def button(self, name: str) -> Button:
		return next(b for b in self.buttons if b.name == name)

	def get_flags(self) -> list[Button]:
		return [b for b in self.buttons if b.press_flag]

	def get_pressed(self) -> list[Button]:
		return [b for b in self.buttons if b.is_down]

	def handle_keydown(self, key: int):
		try:
			button = next(b for b in self.buttons if b.binding == key)
			button.press()
		except StopIteration:
			pass

	def handle_keyup(self, key: int):
		try:
			button = next(b for b in self.buttons if b.binding == key)
			button.release()
		except StopIteration:
			pass

	def is_jump_pressed(self) -> bool:
		return self.button('JUMP').is_down

	def poll(self):
		"""Manually poll controller keys"""
		for button in self.buttons:
			if pg.key.get_pressed()[button.binding]:
				button.is_down = True

	def reset(self):
		for btn in self.buttons:
			btn.release()

	def set_buttons_from_style(self):
		match self.style:
			case 'wasd':
				buttons = ['JUMP', 'LEFT', 'RIGHT']
				bindings = [pg.K_w, pg.K_a, pg.K_d]
				for n in range(len(buttons)):
					self.buttons.append(Button(name=buttons[n], binding=bindings[n]))

	def update(self):
		for button in self.buttons:
			button.update()
