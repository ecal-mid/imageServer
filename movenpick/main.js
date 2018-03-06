//$(function() {

  // todo keep polling the server for new data and create events
  // Simple version - one new image
  // Todo - complicated version, more images
document.addEventListener('gesturestart', function (e) {
    alert("hello");
    e.preventDefault();
});

 document.addEventListener('touchmove', function(event) {
  alert("moved");
    event = event.originalEvent || event;
    if(event.scale !== undefined && event.scale !== 1) {
      event.preventDefault();
    }
  }, false);




var containers = {
    'happy' : $('#container_happy'),
    'sad': $('#container_sad'),
    'angry': $('#container_angry')
};

var anim_functions = {
    'happy': happy,
    'angry': angry,
    'sad': sad
}

  var animDuration = 500;

  var data = [];

  function checkForNewData(){
    $.ajax({
     type: "GET",
     url: 'data.json?t=' + new Date(),
     success: function(response){
         //console.log(response);
         var new_data = response;
         // difference(A, B) - returns values present in A but not present in B
         //console.log(response);
         var new_images = _.differenceWith(new_data, data, _.isEqual).reverse(); // newest last
         var removed_images = _.differenceWith(data, new_data, _.isEqual);

        _.each(removed_images, function(d){
            removeImage(d.file);
        });

        _.each(new_images, function(d){
            addImage(d.file, d.type);
        });

        if (new_images.length > 0){
            var newest_img_data = new_images[new_images.length - 1];
            switch (newest_img_data.type){
            case 'sad':
                sad();
            break;
            case 'happy':
                happy();
            break;
            case 'angry':
                angry();
            break;
            }
        }

         data = new_data;
         // Remove old stuff
         // Check if new stuff is there
         // If it is add it in - start animation for the last one that is added
     }
    });
  }

setInterval(checkForNewData, 1000);

function removeImage(fn){
    $('#'+fn.slice(0, -4).replace('/', '')).remove();
}

function addImage(fn, type){
    //console.log('Add image')
    // Create new image in jquery
    var img = $('<img />', {
      id: fn.slice(0, -4).replace('/', ''), // remove.jpg
      src: fn,
      class: 'imagew'
    });

    //console.log(type);
    //console.log(containers[type]);
    img.prependTo(containers[type]);
}

  function happy() {
/* 120 sad, angry 0, happy -120 */
    $('.imageoverlay').removeClass('happy-img sad-img angry-img');
    $('.imageoverlay').addClass('happy-img');


    $( ".container" ).animate({
      "left": "-100vw"
    }, {
      duration: 500,
      complete: function() {
        //console.log("Finished!");
      }
    });
  }

  function sad() {
    $('.imageoverlay').removeClass('happy-img sad-img angry-img');
    $('.imageoverlay').addClass('sad-img');

    $( ".container" ).animate({
      "left": "0"
    }, {
      duration: 500,
      complete: function() {
        //console.log("Finished!");
      }
    });
  }

  function angry() {
    $('.imageoverlay').removeClass('happy-img sad-img angry-img');
    $('.imageoverlay').addClass('angry-img');

    $( ".container" ).animate({
      "left": "-200vw"
    }, {
      duration: 500,
      complete: function() {
        //console.log("Finished!");
      }
    });
  }
    
    //});

