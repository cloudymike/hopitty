

google.charts.load('current', {packages: ['corechart', 'bar']});
//google.charts.setOnLoadCallback(drawVolHwt);
//google.charts.setOnLoadCallback(drawVolBoiler);

function drawVolumes() {
    drawWaterVolume();
    drawMashVolume()
    drawBoilerVolume();
}

function drawWaterVolume() {
    var chart = new google.visualization.ColumnChart(document.getElementById('vol_waterHeater'));
    drawVolChart(chart, 'waterVolume');
}

function drawMashVolume() {
    var chart = new google.visualization.ColumnChart(document.getElementById('vol_mashHeater'));
    drawVolChart(chart, 'mashVolume');
}

function drawBoilerVolume() {
    var chart = new google.visualization.ColumnChart(document.getElementById('vol_boiler'));
    drawVolChart(chart, 'boilerVolume');
}


function drawVolChart(chart, appliance) {

      var data = google.visualization.arrayToDataTable([
        ['bogus','actual', 'target'],
        [appliance, 10, 2]
      ]);

/*
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'vessel');
      data.addColumn('number', 'qts');
      data.addRows([['hwt', 1]])
*/
    var options = {
        width: 250,
        height: 250,
        bar: { groupWidth: '75%' },
        legend: {position: 'top'},
        isStacked: true
    };
    
    //chart.draw(data, options);
    
    volumeGaugeCallback(appliance, chart, data, options);
    var fullUrl = 'apipath' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var isActive = tempJson['active'];
            console.log("Value: " + isActive);
            if (isActive) {
                setInterval(volumeGaugeCallback, 1000, appliance, chart, data, options);
            } else {
                setInterval(volumeGaugeCallback, 10000, appliance, chart, data, options);
            }
        });
    });
//    setInterval(function() {
//        gaugeCallback(appliance, chart, data, options);
//    }, 1300);
}

function volumeGaugeCallback(appliance, chart, data, options) {
    var fullUrl = 'apipath' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var tempVal = tempJson['actual'];
            var tempTarget = tempJson['target'];
            console.log("Appliance:", appliance, "  Value:" + tempVal, "  Target:", tempTarget);
            var delta = 0;
            if (tempTarget > tempVal) {
               delta = tempTarget - tempVal;
               data.setValue(0, 1, tempVal);
               data.setValue(0, 2, delta);
               data.setColumnLabel(1, 'actual');
               data.setColumnLabel(2, 'target');
            } else {
               delta = tempVal - tempTarget;
               data.setValue(0, 1, tempTarget);
               data.setValue(0, 2, delta);
               data.setColumnLabel(1, 'target');
               data.setColumnLabel(2, 'actual');
            }
            chart.draw(data, options);
        });
    });
}

