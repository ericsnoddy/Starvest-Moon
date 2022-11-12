RES = WIDTH, HEIGHT = 1280, 720
TS = 64  # tilesize (px)
FPS = 60

# player
START_POS = (640, 360)
PLAYER_SPEED = 200
PLAYER_ANIM_RATE = 2

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, HEIGHT - 15), 
	'seed': (70, HEIGHT - 5)}

# These will be converted to pg.math.Vector2
PLAYER_TOOL_OFFSET = {
	'left': (-50,40),
	'right': (50,40),
	'up': (0,-10),
	'down': (0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}