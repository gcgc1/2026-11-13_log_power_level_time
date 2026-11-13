'''
python -m venv .venv
.venv/scripts/activate

pip install psutil pyinstaller
pip install pyinstaller

pip freeze > requirements.txt
pip install -r requirements.txt

pyinstaller --onefile run.py
'''

import csv
import time
from datetime import datetime
import psutil


def log_battery_life(interval_seconds=60):
  print(
      f"Starting battery logger. Recording every {interval_seconds} seconds."
  )
  

  timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
  filename="battery_"+timestamp+".csv"
  print(f"Data will be saved to {filename}. Press Ctrl+C to stop.")
  
  with open(filename, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Timestamp",
        "Elapsed_Seconds",
        "Battery_Percent",
        "Power_Plugged",
    ])

    start_time = time.time()

    try:
      while True:
        battery = psutil.sensors_battery()
        if battery is None:
          print("Error: No battery detected on this system.")
          break

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed = int(time.time() - start_time)
        percent = battery.percent
        plugged = battery.power_plugged

        writer.writerow([timestamp, elapsed, percent, plugged])
        f.flush()

        print(
            f"[{timestamp}] Elapsed: {elapsed}s | Charge: {percent}% |"
            f" Plugged: {plugged}"
            f"| ctrl+c to stop"
        )

        time.sleep(interval_seconds)

    except KeyboardInterrupt:
      print("\nLogging stopped by user. CSV file saved successfully.")


if __name__ == "__main__":
  
  interval_seconds=5
  log_battery_life(interval_seconds)