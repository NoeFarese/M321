import navigation
import energy
import time
import scanner
import json
from datetime import datetime


def wait_for_captain_morris_at_center():
    navigation.travel_position_until_recive(0, 0)

    while True:
        scan_result = scanner.scan()

        if scan_result:
            for ship in scan_result:
                if ship.get("name") == "Captain Morris":
                    pos = ship.get("pos")
                    x, y = pos.get("x"), pos.get("y")
                    print("following Captain Morris")
                    return True, x, y

        time.sleep(1)
        print("waiting for Captain Morris")


def follow_morris_and_search_shady_shack():
    print("Starting continuous Morris following with Shady Shack search...")

    morris_lost_count = 0
    shady_shack_priority = False
    last_morris_pos = None

    while True:
        scan_result = scanner.scan()
        morris_found = False
        shady_shack_found = False

        if scan_result:
            for ship in scan_result:
                if ship.get("name") == "Shady Shack":
                    shady_shack_found = True
                    shady_pos = ship.get("pos")
                    sx, sy = shady_pos.get("x"), shady_pos.get("y")

                    log_shady_shack_position(ship)

                    print(f"SHADY SHACK FOUND! Position: {sx},{sy}")
                    print("SWITCHING TO SHADY SHACK - Higher priority target!")

                    navigation.travel_position(sx, sy)
                    shady_shack_priority = True

                    return follow_shady_shack_exclusively()

            if not shady_shack_found:
                for ship in scan_result:
                    if ship.get("name") == "Captain Morris":
                        morris_found = True
                        morris_lost_count = 0

                        pos = ship.get("pos")
                        x, y = pos.get("x"), pos.get("y")
                        last_morris_pos = (x, y)

                        print(f"Captain Morris: {x},{y} (searching for Shady Shack...)")
                        navigation.travel_position(x, y)
                        break

        if not morris_found and not shady_shack_found:
            morris_lost_count += 1
            print(f"Captain Morris not found (miss #{morris_lost_count})")

            if morris_lost_count >= 5:
                print("Lost Captain Morris! Attempting recovery...")

                if last_morris_pos:
                    print(f"🔍 Searching around last known Morris position: {last_morris_pos}")
                    found = search_around_position(last_morris_pos[0], last_morris_pos[1], "Captain Morris")

                    if found:
                        morris_lost_count = 0
                        print("✅ Recovered Captain Morris!")
                    else:
                        print("❌ Could not recover Captain Morris")
                        print("🔄 Returning to center (0,0) to wait for him again...")
                        return wait_for_captain_morris_at_center()
                else:
                    print("🔄 No last known position - returning to center (0,0)")
                    return wait_for_captain_morris_at_center()

        time.sleep(0.5)


def follow_shady_shack_exclusively():
    print("Now following Shady Shack exclusively!")

    shady_lost_count = 0
    last_shady_pos = None

    while True:
        scan_result = scanner.scan()
        shady_found = False

        if scan_result:
            for ship in scan_result:
                if ship.get("name") == "Shady Shack":
                    shady_found = True
                    shady_lost_count = 0

                    pos = ship.get("pos")
                    x, y = pos.get("x"), pos.get("y")
                    last_shady_pos = (x, y)

                    log_shady_shack_position(ship)

                    print(f"🏴‍☠️ Shady Shack: {x},{y}")
                    navigation.travel_position(x, y)
                    break

        if not shady_found:
            shady_lost_count += 1
            print(f"⚠️  Shady Shack not found (miss #{shady_lost_count})")

            if shady_lost_count >= 5:
                print("❌ Lost Shady Shack! Attempting recovery...")

                if last_shady_pos:
                    found = search_around_position(last_shady_pos[0], last_shady_pos[1], "Shady Shack")

                    if found:
                        shady_lost_count = 0
                        print("✅ Recovered Shady Shack!")
                    else:
                        print("❌ Could not recover Shady Shack")
                        print("🔄 Switching back to Captain Morris strategy...")
                        return follow_morris_and_search_shady_shack()
                else:
                    print("🔄 No last known position - switching back to Morris strategy")
                    return follow_morris_and_search_shady_shack()

        time.sleep(0.5)


def search_around_position(center_x, center_y, target_name, radius=3000):
    print(f"🔍 Searching for {target_name} around ({center_x}, {center_y})")

    search_offsets = [
        (0, 0),
        (radius, 0), (-radius, 0), (0, radius), (0, -radius),
        (radius, radius), (-radius, -radius), (radius, -radius), (-radius, radius)
    ]

    for i, (dx, dy) in enumerate(search_offsets):
        search_x = center_x + dx
        search_y = center_y + dy

        print(f"  Checking point {i + 1}/{len(search_offsets)}: ({search_x}, {search_y})")
        navigation.travel_position_until_recive(search_x, search_y)

        scan_result = scanner.scan()
        if scan_result:
            for ship in scan_result:
                if ship.get("name") == target_name:
                    pos = ship.get("pos")
                    found_x, found_y = pos.get("x"), pos.get("y")
                    print(f"🎯 Found {target_name} at: ({found_x}, {found_y})")
                    return True

        time.sleep(0.5)

    return False


def log_shady_shack_position(ship):
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ship_data": ship
        }

        with open("shady_shack_cords.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        pos = ship.get("pos", {})
        x, y = pos.get("x", "?"), pos.get("y", "?")
        print(f"📝 Logged Shady Shack position: ({x}, {y})")

    except Exception as e:
        print(f"❌ Error logging Shady Shack position: {e}")


def main_mission():
    print("🚀 Starting Shady Shack Communications Mission")
    print("Strategy: Wait at (0,0) → Follow Captain Morris → Search for Shady Shack → Prioritize Shady Shack if found")
    print("=" * 80)

    energy.set_limit_normal()

    while True:
        found, x, y = wait_for_captain_morris_at_center()

        if found:
            follow_morris_and_search_shady_shack()

        print("🔄 Mission restart - returning to center...")
        time.sleep(2)


if __name__ == "__main__":
    main_mission()
