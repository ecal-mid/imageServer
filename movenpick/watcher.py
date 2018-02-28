#!/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
import glob
import json

images_path = 'images'
limit = 20
data_file = 'data.json'


class MyHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        print('Files have changed ...')
        print(images_path)
        files = glob.glob(images_path + "/*.jpg")
        print(files)
        files.sort(key=os.path.getmtime, reverse=True)
        print("changed files are")
        print(files)
        data = dict()
        data['angry'] = [f for f in files if 'angry' in f][:limit]
        data['sad'] = [f for f in files if 'sad' in f][:limit]
        data['happy'] = [f for f in files if 'happy' in f][:limit]

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    images_path = args[0] if args else './images'
    observer.schedule(MyHandler(), path=images_path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()