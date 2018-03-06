#!/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
import glob
import json

images_path = 'images'
limit = 5
data_file = 'data.json'

emotions = ['angry', 'sad', 'happy']


def get_mudac_type(fn):
    for e in emotions:
        if e in fn:
            return e
    return 'unknown'


class MyHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global emotions
        global limit

        print('Files have changed ...')

        files = glob.glob(images_path + "/*.jpg")
        files.sort(key=os.path.getmtime, reverse=True)

        files = [f[2:] for f in files]

        data = [{'file': f, 'type': get_mudac_type(f)} for f in files]
        limited_data = []
        counts = [0, 0, 0]
        emotion_counts = dict(zip(emotions, counts))
        for d in data:
            if d['type'] in emotions and emotion_counts[d['type']] < limit:
                limited_data.append(d)
                emotion_counts[d['type']] += 1

        with open('data.json', 'w') as outfile:
            json.dump(limited_data, outfile)


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