import paths
from eip4844.setting import *
import sys
import subprocess

def main():
    if len(sys.argv) != 2:
        print("Usage: python insert_rollup_delay.py <rollup_name>")
        return

    rollup_name = sys.argv[1]
    
    if rollup_name == "optimism" or rollup_name == "base":
        script_name = f"insert_rollup_delay_optimism_base.py"
        try:
            subprocess.run(["python", script_name, rollup_name])
        except FileNotFoundError:
            print(f"Script for rollup '{rollup_name}' not found.")

    else:
        script_name = f"insert_rollup_delay_{rollup_name.lower()}.py"

        try:
            subprocess.run(["python", script_name])
        except FileNotFoundError:
            print(f"Script for rollup '{rollup_name}' not found.")

if __name__ == "__main__":
    main()




