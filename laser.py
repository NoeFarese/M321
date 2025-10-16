import requests
import time
import cargo_hold


def activate():
    response = requests.post("http://10.255.255.254:2018/activate")
    print(f"activate laser: {response.json()}")
    return response.status_code

def deactive():
    response = requests.post("http://10.255.255.254:2018/deactivate")
    print(f"deactivate laser: {response.json()}")

def set_angle(angle):
    url = "http://10.255.255.254:2018/angle"
    data = {"angle": angle}

    response = requests.put(url, json=data)
    print(f"set angle: {response.json()}")

def get_state():
    response = requests.get("http://10.255.255.254:2018/state")
    print(f"state: {response.json()}")
    return response.json()

def aim_laser(magnon=False):
    angle = 0
    restart_laser = 3

    while True:
        try:
            if restart_laser == 3:
                status_code = activate()
                if status_code == 403:
                    print("max request reached - hold on for one min")
                    time.sleep(60)
                    activate()
                restart_laser = 0

            time.sleep(1)
            set_angle(angle)
            restart_laser += 1
            state = get_state()

            if cargo_hold.must_move_item():
                if magnon:
                    cargo_hold.move_magnon()
                else:
                    cargo_hold.move_all_down(.5)

            if state.get("is_mining"):
                print("mining rn")
                print(angle)
                time.sleep(5)
            else:
                angle = (angle + 22) % 360
                set_angle(angle)
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            raise e
