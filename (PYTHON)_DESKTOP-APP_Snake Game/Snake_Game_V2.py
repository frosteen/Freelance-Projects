#MADE_BY_PAMBID
#SNAKE_GAME_V2

import keyboard
import os
import time
import random
from colored import fg, bg, attr

class Game:
    #SETTINGS
    snake_symbol = "%s█%s" % (fg(2), attr(0))
    fence_symbol = "%s█%s" % (fg(19), attr(0))
    food_symbol = "%s●%s" % (fg(226), attr(0))
    width = 30
    height = 20
    board = []
    snake_pos_x = int(width/2)
    snake_pos_y = int(height/2)
    snake_bodies = 2
    snake_bodies_x = []
    snake_bodies_y = []
    snake_move = "UP"
    count = 0
    counter = 0
    food_exists = False
    food_pos_x = 0
    food_pos_y = 0
    score = 0
    #METHODS
    def set_board(self):
        for i in range(self.width):
            self.board.append([])
            for v in range(self.height):
                self.board[i].append('')
                
    def set_fences(self):
        for x in range(self.width):
            self.board[x][0] = self.fence_symbol
            self.board[x][self.height-1] = self.fence_symbol
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x][y] != self.fence_symbol and self.board[x][y] != self.food_symbol:
                    if x > 0 and x < (self.width-1):
                        self.board[x][y] = " "
                    else:
                        self.board[x][y] = self.fence_symbol
                for i in range(self.count):
                    if x == self.snake_bodies_x[i] and y == self.snake_bodies_y[i]:
                        self.board[x][y] = self.snake_symbol
        self.board[self.snake_pos_x][self.snake_pos_y] = self.snake_symbol

    def print_board(self):
        print("%sPAMBID\'S SNAKE GAME%s" % (fg(202), attr(0)))
        for y in range(self.height):
            for x in range(self.width):
                print(self.board[x][y], end = "")
            print()
            
    def append_snake_bodies(self):
        self.snake_bodies_x.append(self.snake_pos_x)
        self.snake_bodies_y.append(self.snake_pos_y)
        
    def set_snake_bodies(self):
        if  Game.count < self.snake_bodies:
            Game.count += 1
            self.append_snake_bodies()
        else:
            del self.snake_bodies_x[0]
            del self.snake_bodies_y[0]
            self.append_snake_bodies()
            
    def move(self):
        if self.snake_move == "UP":
            self.snake_pos_y -= 1
        if self.snake_move == "LEFT":
            self.snake_pos_x -= 1
        if self.snake_move == "DOWN":
            self.snake_pos_y += 1
        if self.snake_move == "RIGHT":
            self.snake_pos_x += 1
            
    def game_over(self):
        print("Game Over!")
        
    def snake_got_hit(self):
        if self.snake_pos_y <= 0 or self.snake_pos_y >= (self.height-1) or self.snake_pos_x <= 0 or self.snake_pos_x >= (self.width-1):
            self.game_over()
            input()
            quit()
        for i in range(self.count):
            if self.snake_bodies_x[i] == self.snake_pos_x and self.snake_bodies_y[i] == self.snake_pos_y:
                self.game_over()
                input()
                quit()
    def random_food_pos(self):
        self.food_pos_x = random.randint(1, self.width-2)
        self.food_pos_y = random.randint(1, self.height-2)
    def spawn_food(self):
        if self.food_exists == False:
            self.random_food_pos()
            for i in range(self.count):
                if (self.food_pos_x == self.snake_bodies_x[i] and self.food_pos_y == self.snake_bodies_y[i]):
                    self.random_food_pos()
            self.board[self.food_pos_x][self.food_pos_y] = self.food_symbol
            self.food_exists = True

    def snake_eats(self):
        if self.food_pos_x == self.snake_pos_x and self.food_pos_y == self.snake_pos_y:
            self.snake_bodies += 5
            self.food_exists = False
            self.score += 5

    def show_score(self):
        return self.score
    def __init__(self):
        os.system('mode con: cols='+str(self.width)+' lines='+str(self.height+3))
        while True:
            key = None
            if keyboard.is_pressed("up") and self.snake_move != "DOWN":
              self.snake_move = "UP"
            if keyboard.is_pressed("left") and self.snake_move != "RIGHT":
              self.snake_move = "LEFT"
            if keyboard.is_pressed("down") and self.snake_move != "UP":
              self.snake_move = "DOWN"
            if keyboard.is_pressed("right") and self.snake_move != "LEFT":
              self.snake_move = "RIGHT"
            os.system("cls")            
            self.move()
            self.set_board()
            self.set_fences()
            self.spawn_food()
            self.print_board()
            self.snake_got_hit()
            self.set_snake_bodies()
            self.snake_eats()
            print("Score: " + str(self.show_score()))
            time.sleep(0.1)
                          
if __name__ == "__main__":
    Game()
