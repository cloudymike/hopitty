var url = 'apitest'
var allDisplays = document.querySelectorAll('pre');
var tempDisplay = allDisplays[0]
var myVar = setInterval(tempHWT, 1000);

function tempHWT() {tempAppliance('apitest', 'hwt'); }

function tempAppliance(url, key) {
    fetch(url).then(function(response){
        response.json().then(function(json) {
            tempJson = json
            tempHWT = tempJson[key]
            console.log(tempHWT)
            document.getElementById("tempHWT").innerHTML = tempHWT;
        });
    });
}