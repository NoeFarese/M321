import time
import scanner
import navigation
import energy

TARGET_NAMES = {"Xyron Vex"}
START_COORDS = (-51829, -77616)

def _parse_xy(pos):
    if pos is None:
        return None
    if isinstance(pos, dict):
        x, y = pos.get("x"), pos.get("y")
        if x is None or y is None:
            return None
        return float(x), float(y)
    if isinstance(pos, str):
        s = pos.strip().replace(",", ".")
        if "/" in s:
            parts = s.split("/")
        elif ";" in s:
            parts = s.split(";")
        else:
            parts = s.split()
        if len(parts) >= 2:
            try:
                return float(parts[0]), float(parts[1])
            except ValueError:
                return None
    return None

def _find_vex(scan_result):
    if not scan_result:
        return None
    for obj in scan_result:
        if obj.get("name") in TARGET_NAMES:
            xy = _parse_xy(obj.get("pos"))
            if xy:
                return xy
    return None

def lock_and_spam(delay=0.01):
    print("[*] Locking on and spamming coordinates …")
    while True:
        hit = _find_vex(scanner.scan())
        if hit:
            x, y = hit
            print(f"[VEX] x={x:.2f} y={y:.2f}")
            navigation.travel_position(x, y)
        time.sleep(delay)

def run_task():
    x, y = START_COORDS
    print(f"[-] Jumping to start: x={x}, y={y}")
    navigation.travel_position_until_recive(x, y)
    lock_and_spam()

if __name__ == "__main__":
    try:
        run_task()
    except KeyboardInterrupt:
        print("\nScript gestoppt")