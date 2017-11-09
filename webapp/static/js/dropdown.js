// Tested on JSFiddle

dropdown_on_headers('bandheader');

dropdown_on_headers('konsertheader');

// Funker bare på class, går gjennom alle elementene i classen og viser det
// Tips: slett cache hvis ikke funker og husk å legge til "hide" i css

function dropdown_on_headers(header) {

  header = document.getElementsByClassName(header);
  for(var i = 0; i < header.length;i++){
    header[i].addEventListener("click",function(){
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
}
