import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class TestBot(BaseLogic):
    def __init__(self):
        # kanan,atas, kiri, bawah
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def next_move(self, board_bot: GameObject, board:Board):
        delta_x = 0
        delta_y = 0
        prop = board_bot.properties
        self.goal_position = None

        # cari musuh
        distEnemy = 0
        distGoal = 0

        current_position = board_bot.position
        for bot in board.bots:
            distEnemy = abs(current_position.x - bot.position.x) + abs(current_position.y - bot.position.y)
            if(distEnemy == 1):
                self.goal_position = bot.position
                delta_x, delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
                break
        
        # jika tidak ada musuh
        if(self.goal_position == None):
            # jarak objek
            distDiamond = 10000
            distBase = 10000
            distStartTeleport = 10000
            distEndTeleport = 10000
            distEndTeleportDiamond = 10000
            distRedButton = 10000

            # jarak base
            distBase = abs(current_position.x-board_bot.properties.base.x) + abs(current_position.y-board_bot.properties.base.y)

            # jarak teleport
            teleport = [tele for tele in board.game_objects if tele.type == "TeleportGameObject"]
            # cari teleport terdekat
            # asumsi start teleport adalah teleport[0]
            # dan end teleport adalah teleport[1]
            distStartTeleport = abs(current_position.x-teleport[0].position.x) + abs(current_position.y-teleport[0].position.y)
            distEndTeleport = abs(current_position.x-teleport[1].position.x) + abs(current_position.y-teleport[1].position.y)
            #tukar teleport[0] dan teleport[1]
            if(distEndTeleport < distStartTeleport):
                temp = distStartTeleport
                distStartTeleport = distEndTeleport
                distEndTeleport = temp
                temp = teleport[0]
                teleport[0] = teleport[1]
                teleport[1] = temp

            # kalo diamond penuh, ke base   
            if prop.diamonds == 5:
                goal = None
                # ke base bisa langsung ke base atau menggunakan teleport
                distEndTeleportBase = abs(board_bot.properties.base.x-teleport[1].position.x) + abs(board_bot.properties.base.y-teleport[1].position.y)
                if(distStartTeleport + distEndTeleportBase < distBase):
                    self.goal_position = teleport[0].position
                else:
                    self.goal_position = board_bot.properties.base
                delta_x, delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            else:
                # print("Belum penuh")
                goal = None
                
                # jarak diamond
                tempAnsDiamond = None
                tempAnsTeleportDiamond = None
                # pilih diamond terdekat
                # pilih teleport + diamond terdekat
                # pilih opsi yang menguntungkan
                tempDistDiamond = 0
                tempDistEndTeleportDiamond = 0
                for diamond in board.diamonds:
                    # jarak langsung ke diamond
                    tempDistDiamond = abs(current_position.x-diamond.position.x) + abs(current_position.y-diamond.position.y)
                    if (tempDistDiamond < distDiamond):
                        distDiamond = tempDistDiamond
                        tempAnsDiamond = diamond
                    # jarak dari teleport ke diamond
                    tempDistEndTeleportDiamond = abs(diamond.position.x - teleport[1].position.x) + abs(diamond.position.y - teleport[1].position.y)
                    if(tempDistEndTeleportDiamond < distEndTeleportDiamond):
                        distEndTeleportDiamond = tempDistEndTeleportDiamond
                        tempAnsTeleportDiamond = diamond
                    
                # lebih dekat menggunakan teleport
                if (distEndTeleportDiamond + distStartTeleport < distDiamond):
                    goal = tempAnsTeleportDiamond.position
                    distGoal = distEndTeleportDiamond
                else:
                    goal = tempAnsDiamond.position
                    distGoal = distDiamond

                # jarak red button
                for redButton in board.game_objects:
                    if redButton.type == "DiamondButtonGameObject":
                        distRedButton = abs(current_position.x-redButton.position.x) + abs(current_position.y-redButton.position.y)
                        if(distGoal > distRedButton):
                            distGoal = distRedButton
                            goal = redButton.position
                        break
                
                # penentuan prioritas
                # ambil diamond
                # 1. langsung ke diamond
                # 2. teleport + diamond

                self.goal_position = goal

                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            
        # print("Current Position:", current_position)
        print("Goal Position:", self.goal_position)
        # print("Delta X:", delta_x)
        # print("Delta Y:", delta_y)

        return delta_x, delta_y