import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def distance( A: Position, B: Position):
        return abs(A.x-B.x) + abs(A.y-B.y)

class Move(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        bots = board.bots
        if len(bots) > 0:
            for bot in bots:
                if bot.id != board_bot.id and distance(board_bot.position, bot.position) < 2:
                    self.goal_position = bot.position
                    delta_x, delta_y = get_direction(board_bot.position.x, board_bot.position.y, self.goal_position.x, self.goal_position.y)
                    return delta_x, delta_y
        blueDist = 1000
        redDist = 1000
        isBlue = False
        isRed = False
        blueDiamond = None
        redDiamond = None
        withTele = False
        self.goal_position = board_bot.properties.base
        # Analyze new state
        teleporter = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        teleDist = [(abs(d.position.x-board_bot.position.x) + abs(d.position.y-board_bot.position.y)) for d in teleporter]
        if(teleDist[0] > teleDist[1]):
            near_tele = teleDist[1]
            temp = teleporter[0]
            teleporter[0] = teleporter[1]
            teleporter[1] = temp
        else:
            near_tele = teleDist[0]
        if props.diamonds >= 4 or (board_bot.properties.diamonds > 0 and board_bot.properties.milliseconds_left < 10000):
            # Move to base
            base = board_bot.properties.base
            baseDist = distance(current_position, base)
            if (near_tele + distance(teleporter[1].position, base) <= baseDist):
                self.goal_position = teleporter[0].position
            else:
                self.goal_position = base
        else:
            #Look for diamonds
            diamonds_list = board.diamonds  
            for diamond in diamonds_list:
                dist = distance(current_position, diamond.position)
                dist = abs(current_position.x - diamond.position.x) + abs(current_position.y - diamond.position.y)
                dist_with_tele = near_tele + abs(teleporter[1].position.x-diamond.position.x) + abs(teleporter[1].position.y-diamond.position.y)
                if diamond.properties.points == 1:  # Blue Diamonds
                    isBlue = True
                    if dist < blueDist:
                        blueDiamond = diamond
                        blueDist = dist
                        withTele = False
                    elif dist_with_tele < blueDist:
                        blueDist = dist_with_tele
                        withTele = True
                else:                               # Red Diamonds
                    isRed = True
                    if dist < redDist:
                        redDiamond = diamond
                        redDist = dist
                        withTele = False
                    elif dist_with_tele < blueDist:
                        redDist = dist_with_tele
                        withTele = True
            if isBlue and isRed:
                if(redDist < 1.5*blueDist):
                    if withTele:
                        goal = teleporter[0].position
                    else:
                        goal = redDiamond.position
                else:
                    if withTele:
                        goal = teleporter[0]
                    else:
                        goal = blueDiamond.position
            elif isRed:
                if withTele:
                    goal = teleporter[0].position
                else:
                    goal = redDiamond.position
            else:
                if withTele:
                    goal = teleporter[0].position
                else:
                    goal = blueDiamond.position
            self.goal_position = goal
        print(self.goal_position)
        delta_x, delta_y = get_direction(board_bot.position.x, board_bot.position.y, self.goal_position.x, self.goal_position.y)
        if delta_x == delta_y:
            delta_x == 0
            delta_y = pow(-1, random.randint(0, 1))
        return delta_x, delta_y