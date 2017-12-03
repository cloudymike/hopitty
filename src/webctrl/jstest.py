import bottle
import commonweb


def jstest():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>

<body>

  temp for HWT: <pre> </pre>

  <script src="js/fetch.js"></script>

  <script>
  console.log("yup, that worked");
  </script>
  
  <p>Did something</p>

</body>

</html>
"""

    return(indexpage)
