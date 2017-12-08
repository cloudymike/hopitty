import bottle
import commonweb


def jstest():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript" src="js/tGauge.js"></script>
  <!--
  <script type="text/javascript" src="js/fetch.js"></script>
  -->
  <script type="text/javascript" src="js/stage.js"></script>

<body>
  <h2 id="currentstage">Let's brew</h2>
  <h3 id="newstage"></h3>
  <div style="width: 100%; display: table;">
    <div style="display: table-row">
    <div id="chart_hwt" style="width: 250px; height: 250px; display: table-cell;"></div>
    <div id="chart_boiler" style="width: 250px; height: 250px; display: table-cell;"></div>
</div>

  <!--
  <p>Temp HWT: <b id="hwt">Unknown</b><p>
  <p>Temp Boiler: <b id="boiler">Unknown</b><p>
  -->


  <script>
  console.log("yup, that worked");
  </script>
  
  <p>Do something</p>

</body>

</html>
"""

    return(indexpage)
