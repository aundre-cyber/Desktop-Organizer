import magic
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "E:/System/Users/User/Downloads"
dest_dir_documents = "E:/Users/OneDrive/Documents"
dest_dir_presentation = "E:/Users/OneDrive/Documents/Powerpoint Presentation"
dest_dir_music = "E:/System/Users/User/Music"
dest_dir_video = "E:/System/Users/User/Video"
dest_dir_image = "E:/Users/OneDrive/Pictures/Screenshots"


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(dest, entry, name):
    if exists(join(dest, name)):
        unique_name = make_unique(dest, name)
        move(entry.path, join(dest, unique_name))
    else:
        move(entry.path, join(dest, name))


def check_file_type(entry, name):
    try:
        file_type = magic.from_file(entry.path, mime=True)
        logging.info(f"File '{name}' is detected as type: {file_type}")
    except PermissionError:
        logging.error(f"Permission denied: {entry.path}")
        return

    if "audio" in file_type:
        move_file(dest_dir_music, entry, name)
        logging.info(f"Moved audio file: {name}")
    elif "video" in file_type:
        move_file(dest_dir_video, entry, name)
        logging.info(f"Moved video file: {name}")
    elif "image" in file_type:
        move_file(dest_dir_image, entry, name)
        logging.info(f"Moved image file: {name}")
    elif "application/pdf" in file_type:
        move_file(dest_dir_documents, entry, name)
        logging.info(f"Moved PDF document file: {name}")
    elif "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in file_type:
        move_file(dest_dir_documents, entry, name)
        logging.info(f"Moved Excel file: {name}")
    elif "application/vnd.ms-powerpoint" in file_type or "application/vnd.openxmlformats-officedocument.presentationml.presentation" in file_type:
        move_file(dest_dir_presentation, entry, name)
        logging.info(f"Moved presentation file: {name}")
    else:
        logging.warning(f"File '{name}' did not match any known file types.")


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                check_file_type(entry, name)

    def on_created(self, event):
        self.on_modified(event)


def move_existing_files():
    with scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            check_file_type(entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Move existing files first
    move_existing_files()

    # Set up monitoring for new files
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
