var $;

(function($) {
  "use strict";

  $("#email").on("blur", function(event){
    if (!/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(this.value)) {
      $("#email-error").css("display","inline");
    }
  });

  $("#email").on("focus", function(){
    $("#email-error").css("display","none");
  });

})($);
