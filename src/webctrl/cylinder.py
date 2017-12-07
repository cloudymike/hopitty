def cylinderAM():

    mypage = """

<!-- Styles -->
<style>
#chartdiv {
	width		: 300px;
	height		: 300px;
	font-size	: 11px;
}															
</style>

<!-- Resources -->
<script src="https://www.amcharts.com/lib/3/amcharts.js"></script>
<script src="https://www.amcharts.com/lib/3/serial.js"></script>
<script src="https://www.amcharts.com/lib/3/plugins/export/export.min.js"></script>
<link rel="stylesheet" href="https://www.amcharts.com/lib/3/plugins/export/export.css" type="text/css" media="all" />
<script src="https://www.amcharts.com/lib/3/themes/light.js"></script>

  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<!-- Chart code -->
  <script type="text/javascript" src="js/vGauge.js"></script>

<!-- HTML -->
<!-- <div id="vol_hwt"></div> -->
<div style="width: 100%; display: table;">
    <div style="display: table-row">
    <div id="vol_hwt" style="width: 250px; height: 250px; display: table-cell;"></div>
    <div id="vol_boiler" style="width: 250px; height: 250px; display: table-cell;"></div>
  </div>
</div>

"""

    return(mypage)
											
