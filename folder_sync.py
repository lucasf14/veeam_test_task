import os
import shutil
import sys
import time


def synchronize_folders(source_folder, replica_folder):
    try:
        # Creates the directory and copies its content, if it doesn't exist
        if not os.path.exists(replica_folder):
            shutil.copytree(source_folder, replica_folder)

        # Removes the existing directory creates a new one
        shutil.rmtree(replica_folder)
        shutil.copytree(source_folder, replica_folder)
    except Exception as e:
        print(e)


def main():
    if len(sys.argv) != 4:
        # Example: python3 folder_sync.py "source_folder" "replica_folder"
        print('Usage: python3 main.py <source_folder> <replica_folder>')
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])

    while True:
        synchronize_folders(source_folder, replica_folder)
        time.sleep(interval)


if __name__ == "__main__":
    main()
