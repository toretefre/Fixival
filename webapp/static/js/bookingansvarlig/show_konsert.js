// TODO: add document on load

var sjangerkonserter = document.getElementsByClassName('sjangerkonserter');
var sjangerpicker = document.getElementById('sjangerpicker');
var valgtSjanger;
if(sjangerpicker){
  sjangerpicker.addEventListener("change",function(){
    valgtSjanger = null
    for(var j = 0;j < sjangerkonserter.length;j++){
      if(sjangerpicker.options[sjangerpicker.selectedIndex].value == sjangerkonserter[j].id){
        valgtSjanger = sjangerkonserter[j];
      }
    }
    for(var i = 0; i < sjangerkonserter.length;i++){
      sjangerkonserter[i].style.display = "none";
    }
    if(valgtSjanger != null){
      valgtSjanger.style.display = "inline";
    }

  });
}
