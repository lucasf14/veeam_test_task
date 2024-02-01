import os
import shutil
import sys
import time
import logging


def logger_setup(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path)
        ]
    )


def create_directory_if_not_exists(directory):
    # Create the replica folder if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Folder created: {directory}")


def copy_files(source_file, replica_file):
    # Copy any missing files in the replica folder from the source folder
    if not os.path.exists(replica_file):
        shutil.copy(source_file, replica_file)
        logging.info(f"File copied: {source_file} -> {replica_file}")


def copy_subfolders_and_files(source_folder, replica_folder):
    # Copy any missing folders and files
    # in the replica folder from the source folder
    for root, dirs, files in os.walk(source_folder):
        for folder in dirs:
            source_subfolder = os.path.join(root, folder)
            replica_subfolder = os.path.join(
                replica_folder,
                os.path.relpath(source_subfolder, source_folder)
            )
            create_directory_if_not_exists(
                replica_subfolder
            )

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(
                replica_folder,
                os.path.relpath(source_file, source_folder)
            )
            copy_files(
                source_file,
                replica_file
            )


def remove_directory_if_not_exists(source_folder, replica_folder):
    # Remove any replica subfolder if it doesn't exist in source_folder anymore
    if not os.path.exists(source_folder):
        logging.info(f"Removing folder: {replica_folder}")

        # Logs the content of the folder to be removed
        for file in os.listdir(replica_folder):
            logging.info(f"Files in {replica_folder}: {file}")
        shutil.rmtree(replica_folder)
        logging.info(f"Folder removed: {replica_folder}")


def remove_files(replica_file, source_file):
    # Remove files in replica folder that don't exist in source folder
    if not os.path.exists(source_file):
        os.remove(replica_file)
        logging.info(f"File removed: {replica_file}")


def remove_subfolders_and_files(source_folder, replica_folder):
    # Remove any extra folders or files the replica folder
    for root, dirs, files in os.walk(replica_folder):
        for folder in dirs:
            replica_subfolder = os.path.join(root, folder)
            source_subfolder = os.path.join(
                source_folder,
                os.path.relpath(replica_subfolder, replica_folder)
            )
            remove_directory_if_not_exists(
                source_subfolder,
                replica_subfolder
            )

        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(
                source_folder,
                os.path.relpath(replica_file, replica_folder)
            )
            remove_files(
                replica_file,
                source_file
            )


def synchronize_folders(source_folder, replica_folder):
    try:
        create_directory_if_not_exists(replica_folder)
        copy_subfolders_and_files(source_folder, replica_folder)
        remove_subfolders_and_files(source_folder, replica_folder)

    except Exception as e:
        logging.error(f"Synchronization failed: {e}")


def main():
    if len(sys.argv) != 5:
        # Example: python3 folder_sync.py src_folder rep_folder 5 events.log
        print(
            'Usage: python3 main.py <source_folder>'
            '<replica_folder> <interval> <log_file>'
        )
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])
    log_file = sys.argv[4]

    logger_setup(log_file)
    logging.info(
        f"Folder synchronization started: {source_folder} -> {replica_folder}"
    )

    try:
        while True:
            synchronize_folders(source_folder, replica_folder)
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Execution interrupted via CTRL-C")


if __name__ == "__main__":
    main()
