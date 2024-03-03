from typing import Optional
import random
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

# fungsi untuk menghitung jarak satu objek dengan objek lainnya
def distance(A: Position, B: Position):
    return abs(A.x-B.x) + abs(A.y-B.y)

class GreedyLogic(BaseLogic):
    # inisiasi
    def __init__(self):
        # inisiasi objek tujuan
        self.goal_position: Optional[Position] = None

    # menentukan langkah selanjutnya
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties    # properti dari bot
        current_position = board_bot.position   # posisi bot saat ini

        # menentukan posisi teleport dan jarak teleport
        teleporter = [d for d in board.game_objects if d.type == "TeleportGameObject"]   # mencari teleport
        dist_tele = [distance(d.position, current_position) for d in teleporter]    # jarak tiap teleport
        # menentukan teleport terdekat
        if (dist_tele[0] > dist_tele[1]):
            near_tele = dist_tele[1]
            temp = teleporter[0]
            teleporter[0] = teleporter[1]
            teleporter[1] = temp
        else:
            near_tele = dist_tele[0]

        # menentukan posisi dan jarak red button
        distRedButton = 0   # jarak ke red button
        positionRedButton = None    # posisi red button
        # mencari red button
        for redButton in board.game_objects:
                # ketemu red button
                if redButton.type == "DiamondButtonGameObject":
                    positionRedButton = redButton.position  # memberikan posisi red button
                    distRedButton = abs(current_position.x-redButton.position.x) + abs(current_position.y-redButton.position.y)  # jarak ke red button
                    # menentukan jarak terdekat ke red button apakah direct atau menggunakan teleport
                    if (near_tele + distance(teleporter[1].position, positionRedButton) <= distRedButton):
                        positionRedButton = teleporter[1].position
                        distRedButton = near_tele + distance(teleporter[1].position, positionRedButton)
                    break   # langsung break karena red button hanya ada 1 pada map
        
        # properti dari base
        base = board_bot.properties.base
        dist_base = distance(current_position, base)

        # Memeriksa jumlah diamond yang dibawa dan waktu yang tersisi
        # jika waktu kurang dari 10 detik, dan masih membawa diamond, kembali ke base
        if (props.diamonds > 0 and board_bot.properties.milliseconds_left < 10000):
            # Menentukan bergerak ke base direct atau menggunakan teleport
            if ((near_tele + distance(teleporter[1].position, base)) >= dist_base):
                self.goal_position = base   # direct ke base
            else:
                self.goal_position = teleporter[0].position # menggunakan teleport

        # Algoritma tackle bot musuh
        # mencari bot lawan
        bots = board.bots
        for bot in bots:
            # memnentukan kapan akan membunuh bot
            # syarat:
            # jika jarak ke bot = 1 atau (< 3 dan musuh memiliki diamond > 2), bunuh bot lawan
            if bot.properties.name != board_bot.properties.name and ((distance(current_position, bot.position) < 3 and bot.properties.diamonds > 2) or distance(current_position, bot.position) == 1) :
                # menentukan arah pergerakan bot
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    bot.position.x,
                    bot.position.y,
                )

                # return hasil
                return delta_x, delta_y
        # jika inventory penuh atau jarak ke base dekat dan diamond > 2, ke base
        if props.diamonds == 5 or (props.diamonds > 2 and dist_base < 2):
            # menentukan arah ke base
            if ((near_tele + distance(teleporter[1].position, base)) >= dist_base):
                self.goal_position = base   # direct ke base
            else:
                self.goal_position = teleporter[0].position # ke base menggunakan teleport
        else:   # Mencari diamond
            # inisiasi variabel
            min = 1000  # jarak terdekat
            goal = base # tujuan 
            jumlahDiamond = 0   # jumalh diamond
            for diamond in board.diamonds:
                jumlahDiamond += 1  # jumalh diamond bertambah
                # jumlah diamond sudah empat dan ada red diamond, akan diskip
                if not (diamond.properties.points == 2 and props.diamonds >= 4):
                    # jarak ke diamond
                    dist = distance(current_position, diamond.position) # direct
                    dist_with_tele = near_tele + distance(teleporter[1].position, diamond.position) # menggunakan teleport
                    # menentukan jarak terdekat
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
            
            # jika diamond tinggal sedikit dan jarak ke red diamond lebih dekat, akan ke red diamond
            if(jumlahDiamond <= 6 and distRedButton <= min):
                goal = positionRedButton

            # menentukan goal
            self.goal_position = goal
        
        # menentukan arah gerak bot
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        
        # jika gerakan sumbu x dan sumbu y sama
        if delta_x == delta_y:
            delta_x = 0
            delta_y = pow(-1, random.randint(0, 1))
        
        # return hasil
        return delta_x, delta_y
