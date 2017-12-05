var url = 'apitest'
var allDisplays = document.querySelectorAll('pre');
var tempDisplay = allDisplays[0]
var myVar = setInterval(tempHWT, 1000);
var myVar = setInterval(tempBoiler, 10000);

function tempHWT() {pathAppliance('apipath', 'hwt'); }
function tempBoiler() {pathAppliance('apipath', 'boiler'); }

function pathAppliance(url, key) {
    fullUrl = url + '/' + key
    console.log(fullUrl)
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            tempJson = json
            tempVal = tempJson['actual']
            console.log(tempVal)
            document.getElementById(key).innerHTML = tempVal;
        });
    });
}
