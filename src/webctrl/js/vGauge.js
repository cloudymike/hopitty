

google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawVolHwt);
google.charts.setOnLoadCallback(drawVolBoiler);

function drawVolHwt() {
    var chart = new google.visualization.ColumnChart(document.getElementById('vol_hwt'));
    drawVolChart(chart, 'hwt');
}

function drawVolBoiler() {
    var chart = new google.visualization.ColumnChart(document.getElementById('vol_boiler'));
    drawVolChart(chart, 'boiler');
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
    
    gaugeCallback(appliance, chart, data, options);
    var fullUrl = 'apipath' + '/' + appliance;
    fetch(fullUrl).then(function(response){
        response.json().then(function(json) {
            var tempJson = json;
            var isActive = tempJson['active'];
            console.log("Value: " + isActive);
            if (isActive) {
                setInterval(gaugeCallback, 1000, appliance, chart, data, options);
            } else {
                setInterval(gaugeCallback, 10000, appliance, chart, data, options);
            }
        });
    });
//    setInterval(function() {
//        gaugeCallback(appliance, chart, data, options);
//    }, 1300);
}

function gaugeCallback(appliance, chart, data, options) {
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

function drawVolume() {
    var chartData = [ {
      "category": "Wine left in the barrel",
      "value1": 30,
      "value2": 70
    } ];
    
    var options = {
      "theme": "light",
      "type": "serial",
      "depth3D": 100,
      "angle": 30,
      "autoMargins": false,
      "marginBottom": 100,
      "marginLeft": 30,
      "marginRight": 10,
      "dataProvider": chartData,
      "valueAxes": [ {
        "stackType": "100%",
        "gridAlpha": 0
      } ],
      "graphs": [ {
        "type": "column",
        "topRadius": 1,
        "columnWidth": 1,
        "showOnAxis": true,
        "lineThickness": 2,
        "lineAlpha": 0.5,
        "lineColor": "#FFFFFF",
        "fillColors": "#8d003b",
        "fillAlphas": 0.8,
        "valueField": "value1"
      }, {
        "type": "column",
        "topRadius": 1,
        "columnWidth": 1,
        "showOnAxis": true,
        "lineThickness": 2,
        "lineAlpha": 0.5,
        "lineColor": "#cdcdcd",
        "fillColors": "#cdcdcd",
        "fillAlphas": 0.5,
        "valueField": "value2"
      } ],
    
      "categoryField": "category",
      "categoryAxis": {
        "axisAlpha": 0,
        "labelOffset": 40,
        "gridAlpha": 0
      },
      "export": {
        "enabled": true
      }
    }

    var chart = AmCharts.makeChart( "chartdiv", options );

}




//drawVolume();