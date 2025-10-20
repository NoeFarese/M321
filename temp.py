import navigation as nav
import energy
import cargo_hold as cargo

# ---------- Energy Management ----------

energy.set_limit_normal()

"""
energy.set_limits({
    "nuclear_reactor": 1,
    "jumpdrive": 0.6,
    "scanner": 0,
    "laser": 0,
    "sensor_atomic_field": 0,
    "matter_stabilizer": 0,
    "cargo_bot": 0,
    "thruster_back": 0,
    "thruster_front": 0,
    "thruster_bottom_left": 0,
    "thruster_front_right": 0,
    "thruster_bottom_right": 0,
    "thruster_front_left": 0,
})
"""

"""
energy.set_limits({
    "nuclear_reactor": 0,
    "jumpdrive": 0,
    "scanner": 0,
    "laser": 0,
    "cargo_bot": 1,
    "sensor_atomic_field": 1,
    "matter_stabilizer": 1,
    "thruster_back": 1,
    "thruster_front": 1,
    "thruster_bottom_left": 1,
    "thruster_front_right": 1,
    "thruster_bottom_right": 1,
    "thruster_front_left": 1
})
"""

# ---------- Navigation ----------

# relief station - mechatrix task
# nav.travel_position_until_recive(150000, 150000)

# architect colony - uran kaufen
# nav.travel_position_until_recive(-108503, -108888)

# nuku - nuclear waste verkaufen
# nav.travel_position_until_recive(-96486, -80625)

# Station 61-B
# nav.travel_position_until_recive(-19762.0,19354.0)

# Station 30-B
# nav.travel_position_until_recive(-12834.0,18751.0)