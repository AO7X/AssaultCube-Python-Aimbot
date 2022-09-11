import math, keyboard
from pymeow import *


def read_values(proc):
    player_coords = read_vec3(proc, pointer_chain(proc, 0x50F4F4, [0x4], 4))
    enemies = {}
    enemies["count"] = read_int(proc, 0x50F500)
    enemies["list"] = []
    for i in range(1, enemies["count"]):
        enemy_ptr = pointer_chain(proc, 0x50F4F8, [i * 4], 4)
        enemy = {}
        enemy["health"] = read_int(proc, pointer_chain(proc, enemy_ptr, [0xF8], 4))
        enemy["coords"] = read_vec3(proc, pointer_chain(proc, enemy_ptr, [0x4], 4))
        enemies["list"].append(enemy)
    return player_coords, enemies


def get_best_target(player_coords, enemies):
    distance_list, valid_targets = [], []
    for i in range(enemies["count"] - 1):
        if enemies["list"][i]["health"] not in range(1, 101):
            distance_list.append(-1)
        else:
            distance = vec3_distance(player_coords, enemies["list"][i]["coords"])
            distance_list.append(distance)
            valid_targets.append(distance)
    return distance_list.index(min(valid_targets))


def calc_angles(src, dst):
    diff_x = dst["x"] - src["x"]
    diff_y = dst["y"] - src["y"]
    diff_z = dst["z"] - src["z"]
    yaw = -math.atan2(diff_x, diff_y) / math.pi * 180.0 + 180.0
    pitch = math.asin(diff_z / vec3_distance(dst, src)) * 180.0 / math.pi
    return yaw, pitch


def write_angles(proc, yaw, pitch):
    write_float(proc, pointer_chain(proc, 0x50F4F4, [0x40], 4), yaw)
    write_float(proc, pointer_chain(proc, 0x50F4F4, [0x44], 4), pitch)


def main():
    proc = process_by_name("ac_client.exe")
    while True:
        if keyboard.is_pressed("end"):
            break
        elif keyboard.is_pressed("ctrl"):
            player_coords, enemies = read_values(proc)
            print(
                "Player coords:",
                player_coords["x"],
                player_coords["y"],
                player_coords["z"],
            )
            target_index = get_best_target(player_coords, enemies)
            target_coords = enemies["list"][target_index]["coords"]
            print(
                "Target coords:",
                target_coords["x"],
                target_coords["y"],
                target_coords["z"],
            )
            print("Target distance:", vec3_distance(target_coords, player_coords))
            yaw, pitch = calc_angles(
                player_coords, enemies["list"][target_index]["coords"]
            )
            write_angles(proc, yaw, pitch)
            print("Yaw:", yaw)
            print("Pitch:", pitch)
            print()


if __name__ == "__main__":
    main()
