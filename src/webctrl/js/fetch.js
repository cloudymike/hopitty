var url = 'apitest'
var allDisplays = document.querySelectorAll('pre');
var tempDisplay = allDisplays[0]

fetch(url).then(function(response){
    response.json().then(function(json) {
        tempJson = json
        tempHWT = tempJson['hwt']
        console.log(tempHWT)
        tempDisplay.textContent = tempHWT
    });
});