#!/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys
import os
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image
import StringIO
import json
import copy



app = Flask(__name__)

images = []
newImages = []



HEIGHT = 800
WIDTH = 1000

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <meta charset="utf-8" />
    <style>
body {
    margin: 0;
    background-color: #333;
}

.image {
    display: block;
    margin: 2em auto;
    background-color: #444;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}

img {
    display: block;
}
    </style>
    <script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
    <!--<script src="http://luis-almeida.github.io/unveil/jquery.unveil.min.js" charset="utf-8"></script>-->
    <script>
$(document).ready(function() {
    console.log("Request new images");
    function requestNewImages(){

        $.ajax({
          url: '/reloadImg',
          type: 'POST',
          success: function(response) {
              console.log("Received : "+response);

              obj = JSON.parse(response);
              console.log(obj.images);
              obj.images.forEach(function(image) {
                $( ".container" ).prepend("<a class='image' href='"+image.src+"' style='width:"+image.width+"px; height:"+image.height+"px' ><img src='"+image.src+"' width='"+image.width+"' height='"+image.height+"' /></a>");

              });
              },
          error: function(error) {
              console.log(error);
          }
        });
    }
    setInterval(function(){ requestNewImages(); }, 3000);



});
    </script>
</head>
<body>
    <div class="container">
     </div>
    {% for image in images %}
        <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
            <img src="{{ image.src }}" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />

            <!--<img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />-->
        </a>
    {% endfor %}
</body>
'''

@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        print("image filename"+filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)

@app.route('/')
def index():
    print("images....")

    for root, dirs, files in os.walk('.'):
        for filename in [os.path.join(root, name) for name in files]:
            print("filename  : "+ filename)
            if not filename.endswith('.jpg'):
                continue
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })


    return render_template_string(TEMPLATE, **{
        'images': images,
    })

@app.route('/reloadImg', methods=['POST'])
def reloadImg():
    #print("reload images post")
    imagesToSend = copy.deepcopy(newImages)
    newImages[:] = []
    return json.dumps({"images":imagesToSend});

@app.route('/reloadImgs', methods=['POST'])
def reloadImgs():
    #print("reload images post")
    #imagesToSend = copy.deepcopy(newImages)
    #newImages[:] = []
    return json.dumps({"images":images});


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        print("filename = "+event.src_path)
        filename = event.src_path
        if filename.endswith('.jpg'):
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            #changed = newImages
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })

    def on_modified(self, event):
        print(".")

    def on_created(self, event):
        self.process(event)
        print("reloaded!")




if __name__ == '__main__':
    print("hello")
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()
    app.run(debug=True, host='::')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
