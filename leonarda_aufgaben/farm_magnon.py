import navigation
import energy
import laser
import cargo_hold as cargo
import time


energy.set_limit_normal()
navigation.travel_position_until_recive(-51368, -52550)

energy.mine()
laser.aim_laser(True)

"""
energy.mine()
laser.set_angle(330)

while True:
    if cargo.must_move_item():
        cargo.move_magnon()

    laser.activate()
    time.sleep(7)
"""
