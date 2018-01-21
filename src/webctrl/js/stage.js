function initialize() {
    updateCurrentStage()
    var myVar = setInterval(updateCurrentStage, 5000);
    
}

// Should probably be an object to wrap the variable
var oldStageGlobalVariableWathOut = "This is totally bogus string"
function checkOldStage(stage){
    if (stage){
        if (stage == oldStageGlobalVariableWathOut) {
            return(false)
        } else {
            oldStageGlobalVariableWathOut = stage;
            return(true)
        }
    }
}

function updateCurrentStage() {
    var fullUrl = 'apipath/currentstage'
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var stage = tempJson['stage'];
            console.log("Value: " + stage);
            document.getElementById('currentstage').innerHTML = stage;
            drawTemperatures()
            //drawVolumes()
            if (checkOldStage(stage)) {
                document.getElementById('newstage').innerHTML = 'New stage';
            } else {
                document.getElementById('newstage').innerHTML = '...';
            }
        });
    });
}

initialize();
