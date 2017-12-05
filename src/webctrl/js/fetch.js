// stub functions to test java script

function getvalhwt() {pathAppliance('hwt', 'actual'); }
function getvalboiler() {pathAppliance('boiler', 'actual'); }

function initialize() {
    refreshTime('hwt', getvalhwt);
    refreshTime('boiler', getvalboiler);
    //var myVar = setInterval(tempHWT, hwtTime);
    //var myVar = setInterval(getvalboiler, 10000);
    
}

function refreshTime(appliance, myF) {
    var fullUrl = 'apipath' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var isActive = tempJson['active'];
            console.log("Value: " + isActive);
            if (isActive) {
                setInterval(myF, 1000);
            } else {
                setInterval(myF, 10000);
            }
        });
    });
}

function pathAppliance(appliance, key) {
    var fullUrl = 'apipath' + '/' + appliance;
    console.log(fullUrl);
    console.log(appliance, key);
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var tempVal = tempJson[key];
            console.log("Value: " + tempVal);
            document.getElementById(appliance).innerHTML = tempVal;
        });
    });
}

initialize();
