import time, keyboard, math
from pymeow import *


def get_best_target(proc, player_coords):
    enemy_count = read_int(proc, 0x50F500)
    min_distance = -1
    for i in range(1, enemy_count):
        enemy_addr = pointer_chain(proc, 0x50F4F8, [i * 4], 4)
        enemy_health = read_int(proc, pointer_chain(proc, enemy_addr, [0xF8], 4))
        if enemy_health in range(1, 101):
            enemy_coords = read_vec3(proc, pointer_chain(proc, enemy_addr, [0x4], 4))
            if min_distance == -1:
                min_distance = vec3_distance(enemy_coords, player_coords)
                target_coords = enemy_coords
            else:
                distance = vec3_distance(enemy_coords, player_coords)
                if distance < min_distance:
                    min_distance = distance
                    target_coords = enemy_coords
    return target_coords


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


def aimbot(proc):
    player_coords = read_vec3(proc, pointer_chain(proc, 0x50F4F4, [0x4], 4))
    target_coords = get_best_target(proc, player_coords)
    yaw, pitch = calc_angles(player_coords, target_coords)
    write_angles(proc, yaw, pitch)


def main():
    proc = process_by_name("ac_client.exe")
    cheat_enabled = False
    while True:
        if keyboard.is_pressed("END"):
            break
        if keyboard.is_pressed("CTRL"):
            cheat_enabled = not cheat_enabled
            if cheat_enabled:
                print("Aimbot enabled")
            else:
                print("Aimbot disabled")
            time.sleep(0.25)
        if cheat_enabled:
            aimbot(proc)
            time.sleep(0.0001)


if __name__ == "__main__":
    main()
