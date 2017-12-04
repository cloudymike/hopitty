var url = 'apitest'
var allDisplays = document.querySelectorAll('pre');
var tempDisplay = allDisplays[0]
var myVar = setInterval(tempHWT, 1000);
var myVar = setInterval(tempBoiler, 10000);

function tempHWT() {tempAppliance('apitest', 'hwt'); }
function tempBoiler() {tempAppliance('apitest', 'boiler'); }

function tempAppliance(url, key) {
    fetch(url).then(function(response){
        response.json().then(function(json) {
            tempJson = json
            tempVal = tempJson[key]
            console.log(tempVal)
            document.getElementById(key).innerHTML = tempVal;
        });
    });
}