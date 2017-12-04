import bottle
import commonweb


def jstest():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>

<body>

  <p>Temp HWT: <b id="tempHWT">Unknown</b><p>


  <script src="js/fetch.js"></script>

  <script>
  console.log("yup, that worked");
  </script>
  
  <p>Did something</p>

</body>

</html>
"""

    return(indexpage)
