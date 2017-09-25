// Tested on JSFiddle

konsertheaders = document.getElementsByClassName('konsertheader');
for(var i = 0; i < konsertheaders.length;i++){
  konsertheaders[i].addEventListener("click",function(){
    if(this.nextSibling.innerHTML == undefined){
      if(window.getComputedStyle(this.nextSibling.nextSibling, null).getPropertyValue('display') == "block"){
        this.nextSibling.nextSibling.style.display = "none";
      }
      else if(window.getComputedStyle(this.nextSibling.nextSibling, null).getPropertyValue('display') == "none"){
        this.nextSibling.nextSibling.style.display = "block";
      }
    }
    else{
      if(window.getComputedStyle(this.nextSibling, null).getPropertyValue('display') == "block"){
        this.nextSibling.style.display = "none";
    }
    else if(window.getComputedStyle(this.nextSibling, null).getPropertyValue('display') == "none"){
      this.nextSibling.style.display = "block";
    }
  }
  })
}
