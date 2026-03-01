import pandas as pd

class Optimizer:

    @staticmethod
    def calculate_roi(labs, hostels, halls, days):
        lab_saving     = labs    * 0.40 * 570  * days
        hostel_saving  = hostels * 1500 * 12
        hall_saving    = halls   * 0.30 * 570  * days
        shuttle_saving = 3       * 950  * days

        annual  = int(lab_saving + hostel_saving + hall_saving + shuttle_saving)
        monthly = int(annual / 12)
        co2     = int(annual * 0.008)

        return {
            "annual":       annual,
            "monthly":      monthly,
            "co2":          co2,
            "shuttle_fuel": 28,
            "payback":      "IMMEDIATE (zero capex)"
        }

    @staticmethod
    def generate_actions(df):
        actions = []
        rooms = [
            ("Lab A",     0.15, "🔴 HIGH"),
            ("Lab C",     0.08, "🔴 HIGH"),
            ("Seminar 1", 0.12, "🔴 HIGH"),
            ("Seminar 2", 0.18, "🔴 HIGH"),
            ("Hall 2",    0.35, "🟡 MED"),
            ("Lab D",     0.60, "🟢 LOW"),
        ]
        
        for room, occ, priority in rooms:
            if occ < 0.20:
                daily = 570
                action = "Turn off AC + dim lights"
            elif occ < 0.50:
                daily = 320
                action = "Reduce AC to 26°C"
            else:
                daily = 120
                action = "Switch to eco lighting"
            
            actions.append({
                "priority": priority,
                "room": room,
                "occupancy": f"{int(occ*100)}%",
                "action": action,
                "daily_saving": daily,
                "monthly_saving": daily * 22
            })
        
        return pd.DataFrame(actions)
