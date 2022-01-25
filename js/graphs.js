
var graphArray = ["figV.html","figA.html", "figC.html","figAe.html"];

function displayGraph(){
      var click = document.getElementById("selectMenu");
      var newSrcInd = click.options[click.selectedIndex].value;
      var newSrc = "assets/img/maps/"+graphArray[newSrcInd];

      document.getElementById("map").src=newSrc;
     }


