$(document).ready(function(){
    $("#buttonJoin").click(function(){
        window.location = ("game/vote/" + $("#joinId").val());
    });
  });