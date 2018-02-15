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
    //console.log("Request new images");
    var images = []

    function requestNewImages(){

        $.ajax({
            url: '/reloadImgs',
            type: 'POST',
            success: function(response) {
                //console.log("Received : "+response);
                obj = JSON.parse(response);

                if(images.length == 0){
                    images = obj.images;
                    obj.images.forEach(function(image) {
                        $( ".container" ).prepend("<a class='image' href='"+image.src+"' style='width:"+image.width+"px; height:"+image.height+"px' ><img src='"+image.src+"' width='"+image.width+"' height='"+image.height+"' /></a>");
                    });

                }else{
                    var tempImages = compareJSON(images,obj.images);
                    //console.log(tempImages);
                    if(tempImages.length != 0){
                        tempImages.forEach(function(image) {
                            $( ".container" ).prepend("<a class='image' href='"+image.src+"' style='width:"+image.width+"px; height:"+image.height+"px' ><img src='"+image.src+"' width='"+image.width+"' height='"+image.height+"' /></a>");
                        });
                    }
                }
                //console.log("json");
                //console.log(obj.images);
                //console.log("local");
                //console.log(images);
                //console.log("ARRAYDIFF");
                //console.log(compareJSON(images,obj.images))
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    requestNewImages();
    setInterval(function(){ requestNewImages(); }, 1000);

    function compareJSON(obj1, obj2) {
        var ret = [];
        for(var i in obj2) {
            if(!obj1.hasOwnProperty(i) || obj2[i].src !== obj1[i].src) {
                ret.push(obj2[i]);
            }
        }
        return ret;
    }

});
    </script>
</head>
<body>
    <div class="container">
     </div>

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
    for root, dirs, files in os.walk('.'):
        for filename in [os.path.join(root, name) for name in files]:
            print("filename  : "+ filename)
            if filename.endswith('.jpg') and filename.find("img_") != -1:
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

@app.route('/reloadImgs', methods=['POST'])
def reloadImgs():
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
        if filename.endswith('.jpg') and filename.find("img_") != -1:
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

    def on_modified(self, event):
        print(".")

    def on_created(self, event):
        self.process(event)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
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
        #app.stop()

    observer.join()
