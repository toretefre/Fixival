// Tested on JSFiddle

konsertheaders = document.getElementsByClassName('konsertheader');
for(var i = 0; i < konsertheaders.length;i++){
  konsertheaders[i].addEventListener("click",function(){
    if(this.nextSibling.innerHTML == undefined){
      if(this.nextSibling.nextSibling.style.display == "inline"){
        this.nextSibling.nextSibling.style.display = "none";
      }
      else if(this.nextSibling.nextSibling.style.display == "none"){
        this.nextSibling.nextSibling.style.display = "inline";
      }
    }
    else{
      if(this.nextSibling.style.display == "inline"){
        this.nextSibling.style.display = "none";
    }
    else if(this.nextSibling.style.display == "none"){
      this.nextSibling.style.display = "inline";
    }
  }
  })
}
