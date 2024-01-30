import paths
from eip4844.setting import *
from pymongo import MongoClient
import subprocess

if __name__ == "__main__":
    files_to_execute = ["insert_block.py", "insert_slot.py", "insert_tx.py"]

    for file_name in files_to_execute:
        try:
            print(f"Executing {file_name}...")
            subprocess.run(["python", file_name], check=True)

            print(f"{file_name} executed successfully.\n")

        except subprocess.CalledProcessError as e:
            print(f"Error executing {file_name}: {e}\n")

