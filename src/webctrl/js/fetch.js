var url = 'apitest'
var allDisplays = document.querySelectorAll('pre');
var tempDisplay = allDisplays[0]
var myVar = setInterval(tempHWT, 1000);

function tempHWT() {
    
    fetch(url).then(function(response){
        response.json().then(function(json) {
            tempJson = json
            tempHWT = tempJson['hwt']
            console.log(tempHWT)
            document.getElementById("tempHWT").innerHTML = tempHWT;
        });
    });
}