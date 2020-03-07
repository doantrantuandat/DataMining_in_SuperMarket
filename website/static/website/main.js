$(document).ready(function(){
    var $regexname=/^([a-zA-Z]{3,16})$/;
    $('.name').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexname)) {
              // there is a mismatch, hence show the error message
                 $('.exception').removeClass('hidden');
                 $('.exception').show();
             }
           else{
                // else, do not display message
                $('.exception').addClass('hidden');
               }
         });
});