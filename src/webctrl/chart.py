import bottle
import commonweb


def chart():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <!--
  <script type="text/javascript" src="js/tGauge.js"></script>
  <script type="text/javascript" src="js/vGauge.js"></script>
  <script type="text/javascript" src="js/fetch.js"></script>
  -->
  <script type="text/javascript" src="js/stage.js"></script>

<body>
  <h2 id="currentstage">Let's brew</h2>
  <h3 id="newstage"></h3>
  <!--
  <div style="width: 100%; display: table;">
    <div style="display: table-row">
        <div id="title_HWT" style="width: 250px; height: 20px; font-size:200%; text-align:center;display: table-cell;">HWT  </div>
        <div id="title_mashTune" style="width: 250px; height: 20px; font-size:200%; text-align:center; display: table-cell;">Mash  </div>
        <div id="title_boiler" style="width: 250px; height: 20px; font-size:200%; text-align:center; display: table-cell;">Boil  </div>
    </div>
  <div style="display: table-row">
        <div id="chart_waterHeater" style="width: 250px; height: 250px; display: table-cell;"></div>
        <div id="chart_mashHeater" style="width: 250px; height: 250px; display: table-cell;"></div>
        <div id="chart_boiler" style="width: 250px; height: 250px; display: table-cell;"></div>
    </div>
    <div style="display: table-row">
        <div id="vol_waterHeater" style="width: 250px; height: 250px; display: table-cell;"></div>
        <div id="vol_mashHeater" style="width: 250px; height: 250px; display: table-cell;"></div>
        <div id="vol_boiler" style="width: 250px; height: 250px; display: table-cell;"></div>
    </div>
  -->
  </div>

  <!--
  <p>Temp HWT: <b id="hwt">Unknown</b><p>
  <p>Temp Boiler: <b id="boiler">Unknown</b><p>
  -->


  <script>
  console.log("Page is done");
  </script>
  
  <p>Brewtime!</p>

</body>

</html>
"""
    indexpage = common.header('Chart') + indexpage + common.footer()
    indexpage = indexpage + "</body>"

    return(indexpage)
