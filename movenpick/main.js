//$(function() {

  // todo keep polling the server for new data and create events
  // Simple version - one new image
  // Todo - complicated version, more images

  var data = {};

  console.log( "ready!" );
  
  var animDuration = 500;

  //$( ".container" ).translate('100vw',0);
    /*  $(".container").animateTransform("translate(100vw)", 750, function(){
  console.log("animation completed after 750ms");
});*/
      /*$( ".container" ).animate({ "left": "-100vw" }, 500 );
      $( ".container" ).animate({ "left": "0" }, 500 );
      $( ".container" ).animate({ "left": "-200vw" }, 500 );*/

      //angry();

/*
      $( ".overlay" ).animate({
        "left": "0vw",
        "top": "-60vw",
        'transform' : 'rotate(60deg)'
      }, {
        duration: 500,
        complete: function() {
          console.log("Finished!");
        }
      });
*/
      function happy() {
    /* 120 sad, angry 0, happy -120 */
        $('.imageoverlay').removeClass('happy-img sad-img angry-img');
        $('.imageoverlay').addClass('happy-img');
       

        $( ".container" ).animate({
          "left": "-100vw"
        }, {
          duration: 500,
          complete: function() {
            console.log("Finished!");
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
            console.log("Finished!");
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
            console.log("Finished!");
          }
        });
      }
    
    //});

