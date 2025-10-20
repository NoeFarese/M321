import requests
import json


def get_status_node1():
    response = requests.get('http://10.255.255.254:2032/status')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status. Status code: {response.status_code}")
        return None


def get_status_node2():
    response = requests.get('http://10.255.255.254:2033/status')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status. Status code: {response.status_code}")
        return None


def get_active_node_url():
    status_node1 = get_status_node1()
    status_node2 = get_status_node2()

    if status_node1 and status_node1['role'] == 'active':
        return 'http://10.255.255.254:2032'
    elif status_node2 and status_node2['role'] == 'active':
        return 'http://10.255.255.254:2033'
    else:
        print("No active node found.")
        return None


def get_limits():
    response = requests.get('http://10.255.255.254:2032/limits')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get limits. Status code: {response.status_code}")
        return None


def set_limits(new_limits):
    headers = {'Content-Type': 'application/json'}
    url = get_active_node_url()

    response = requests.put(f"{url}/limits", data=json.dumps(new_limits), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to set limits. Status code: {response.status_code}")
        return None


def set_limit_normal():
    set_limits({
        "thruster_back": 1,
        "thruster_front": 1,
        "thruster_bottom_left": 1,
        "thruster_front_right": 1,
        "thruster_bottom_right": 1,
        "thruster_front_left": 1,
        "cargo_bot": 1,
        "scanner": 1,
        "laser": 0,
        "sensor_atomic_field": 0,
        "matter_stabilizer": 0,
        "laser_amplifier": 0,
        "sensor_plasma_radiation": 0,
        "nuclear_reactor": 0,
        "jumpdrive": 0,
        "analyzer_alpha": 0,
        "analyzer_beta": 0,
        "shield_generator": 0,
        "sensor_void_energy": 0
    })


def mine():
    set_limits({
        "laser": 1,
        "cargo_bot": 1,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_bottom_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_right": 0,
        "thruster_front_left": 0,
        "scanner": 0,
        "sensor_atomic_field": 0,
        "matter_stabilizer": 0,
        "nuclear_reactor": 0,
        "jumpdrive": 0,
        "laser_amplifier": 0,
        "sensor_plasma_radiation": 0
    })


def set_energy_mine(matter_stabilizer, laser_amplifier):
    set_limits({
        "scanner": 0,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_bottom_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_right": 0,
        "thruster_front_left": 0,
        "cargo_bot": 0.3,
        "laser": 0.5,
        "sensor_atomic_field": matter_stabilizer,
        "matter_stabilizer": matter_stabilizer,
        "laser_amplifier": laser_amplifier,
        "sensor_plasma_radiation": laser_amplifier
    })
