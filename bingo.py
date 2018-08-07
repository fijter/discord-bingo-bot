import random
import csv
from PIL import Image,ImageDraw,ImageFont
import textwrap
from random import randint
import os


class BingoBoard:

    def __init__(self, bingo_board):
        self.bingo_board = bingo_board

    def generate_board_image(self, file_name='bingo', user_name='anon', user_id='12345'):

        y_position = 450
        cell_width = 265
        cell_height = 260
        margin = 10
        font = ImageFont.truetype("fonts/Rubik-Bold.ttf", 128, encoding="unic")
        canvas = Image.open("bingo_template.png")
        draw = ImageDraw.Draw(canvas)
        file_name = 'bingo_boards/' + file_name + '_' + user_id + '.png'

        if os.path.exists(file_name):
            return file_name

        for y, row in enumerate(self.bingo_board):
            x_position = 100
            for x, cell in enumerate(row):

                if x == 2 and y == 2:
                    x_position += cell_width
                    continue

                text = textwrap.fill(cell, 13)
                w, h = draw.textsize(text, font)
                newx = x_position + ((cell_width - w) / 2)
                print(w, newx, x_position)
                draw.text((newx-10, y_position-30), text, 'black', font)
                x_position += cell_width
            y_position += cell_height


        namefont = ImageFont.truetype("fonts/PermanentMarker-Regular.ttf", 96, encoding="unic")

        draw.text((380, 1685), textwrap.shorten(user_name, width=18, break_on_hyphens=False, placeholder='...') + '   ', 'white', namefont)

        canvas.save(file_name, "PNG")

        return file_name


class Bingo:

    def __init__(self, grid_size = 5):
        self.grid_size = grid_size

    def generate_board(self, user_name, user_id):
        board_layout = self.generate_board_layout()
        bingo_board = BingoBoard(board_layout)
        board_image = bingo_board.generate_board_image(user_name=user_name, user_id=user_id)
        return board_image

    def generate_board_layout(self):

        board = []

        for i in range(5):
            options = range((i*15)+1, (i*15)+16)
            numbers = random.sample(options, 5)
            board.append(list(map(lambda x: str(x), numbers)))

        board = list(zip(*reversed(board[::-1])))

        return board
