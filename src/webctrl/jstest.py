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

<body>
<div style="width: 100%; display: table;">
    <div style="display: table-row">
    <div id="chart_hwt" style="width: 120px; height: 120px; display: table-cell;"></div>
    <div id="chart_boiler" style="width: 120px; height: 120px; display: table-cell;"></div>
  </div>
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
