BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 177, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH = 540
HEIGHT = 600
VELOCITY = 50
SHAPE = VELOCITY - 1
BOARD_COUNT = int((WIDTH - 40) / VELOCITY)
TEST_VEL = 25
TEST_SHAPE = TEST_VEL - 1
TEST_BOARD_COUNT = int((WIDTH - 40) / TEST_VEL)
FPS = 60

TAIL = 5
HEAD = 10
FOOD = 20

EMPTY = 0
# TAIL = 1
# HEAD = 2
# FOOD = 3

# 0: forward, 1: left, 2: right, 3: down
ACTION_SPACE = [0, 1, 2, 3]
FOOD_REWARD = 40
OUT_REWARD = -60
EMPTY_STEP_REWARD = 0

WINDOW_SIZE = 5


def pad_with(vector, pad_width, _, kwargs):
    pad_value = kwargs.get('padder', TAIL)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
