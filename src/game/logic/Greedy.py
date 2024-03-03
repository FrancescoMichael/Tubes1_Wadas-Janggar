from typing import Optional
import random
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def distance(A: Position, B: Position):
        return abs(A.x-B.x) + abs(A.y-B.y)

class GreedyLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position

        # teleport
        teleporter = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        dist_tele = [distance(d.position, current_position) for d in teleporter]
        if (dist_tele[0] > dist_tele[1]):
            near_tele = dist_tele[1]
            temp = teleporter[0]
            teleporter[0] = teleporter[1]
            teleporter[1] = temp
        else:
            near_tele = dist_tele[0]

        # red button
        distRedButton = 0
        positionRedButton = None
        for redButton in board.game_objects:
                if redButton.type == "DiamondButtonGameObject":
                    positionRedButton = redButton.position
                    distRedButton = abs(current_position.x-redButton.position.x) + abs(current_position.y-redButton.position.y)
                    if (near_tele + distance(teleporter[1].position, positionRedButton) <= distRedButton):
                        positionRedButton = teleporter[1].position
                        distRedButton = near_tele + distance(teleporter[1].position, positionRedButton)
                    break
        
        base = board_bot.properties.base
        dist_base = distance(current_position, base)
        # Analyze new state

        # Check diamond and time
        if (props.diamonds > 0 and board_bot.properties.milliseconds_left < 10000):
            # Move to base
            if ((near_tele + distance(teleporter[1].position, base)) >= dist_base):
                self.goal_position = base
            else:
                self.goal_position = teleporter[0].position

        # Tackle Algorithm
        bots = board.bots
        for bot in bots:
            if bot.properties.name != board_bot.properties.name and distance(current_position, bot.position) < 3 and bot.properties.diamonds > 2:
                delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                bot.position.x,
                bot.position.y,
                )
                return delta_x, delta_y

        if props.diamonds == 5 or (props.diamonds > 2 and dist_base < 2):
            # Move to base
            if ((near_tele + distance(teleporter[1].position, base)) >= dist_base):
                self.goal_position = base
            else:
                self.goal_position = teleporter[0].position
        else:
            # Look for diamonds
            min = 1000
            goal = base
            jumlahDiamond = 0
            for diamond in board.diamonds:
                jumlahDiamond += 1
                if not (diamond.properties.points == 2 and props.diamonds >= 4):
                    dist = distance(current_position, diamond.position)
                    dist_with_tele = near_tele + distance(teleporter[1].position, diamond.position)
                    if (dist < min):
                        if dist <= dist_with_tele:
                            goal = diamond.position
                            min = dist
                        else:
                            goal = teleporter[0].position
                            min = dist_with_tele
                    elif (dist_with_tele < min):
                        goal = teleporter[0].position
                        min = dist_with_tele
            
            if(jumlahDiamond <= 6 and distRedButton <= min):
                goal = positionRedButton

            self.goal_position = goal

        print(self.goal_position)
            
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        if delta_x == delta_y:
            delta_x = 0
            delta_y = pow(-1, random.randint(0, 1))
        return delta_x, delta_y
