
google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawTemperatures);
//google.charts.setOnLoadCallback(drawBoiler);

function drawTemperatures() {
    drawWaterHeater();
    drawMashHeater()
    drawBoiler();
}

function drawWaterHeater() {
    var chart = new google.visualization.Gauge(document.getElementById('chart_waterHeater'));
    drawChart(chart, 'waterHeater');
}
function drawMashHeater() {
    var chart = new google.visualization.Gauge(document.getElementById('chart_mashHeater'));
    drawChart(chart, 'mashHeater');
}
function drawBoiler() {
    var chart = new google.visualization.Gauge(document.getElementById('chart_boiler'));
    drawChart(chart, 'boiler');
}



function drawChart(chart, appliance) {
    var data = google.visualization.arrayToDataTable([
      ['Label', 'Value'],
       ['F', 68]
    ]);
    var options = {
      width: 250, height: 250,
      greenFrom: 160, greenTo: 170,
      minorTicks: 5, majorTicks: [60,80,100,120,140,160,180,200,220],
      min: 60, max: 220
    };
    
    chart.draw(data, options);
    
    temperatureGaugeCallback(appliance, chart, data, options);
    var fullUrl = 'apipath/appliance' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var isActive = tempJson['active'];
            console.log("Value: " + isActive);
            if (isActive) {
                setInterval(temperatureGaugeCallback, 1000, appliance, chart, data, options);
            } else {
                setInterval(temperatureGaugeCallback, 10000, appliance, chart, data, options);
            }
        });
    });
}

function temperatureGaugeCallback(appliance, chart, data, options) {
    var fullUrl = 'apipath/appliance' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var tempVal = tempJson['actual'];
            var tempTarget = tempJson['target'];
            var active = tempJson['active']
            options['greenFrom'] = tempTarget - 3;
            options['greenTo'] = tempTarget + 3;
            console.log("Appliance:", appliance, "  Value:" + tempVal, "  Target:", tempTarget, "  Active:", active);
            data.setValue(0, 1, tempVal);
            chart.draw(data, options);
        });
    });
}

