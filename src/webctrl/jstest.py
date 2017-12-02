import bottle
import commonweb


def jstest():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>

<body>

  <script src="js/alert.js"></script>

  <script>
  console.log("yup, that worked");
  </script>

</body>

</html>
"""

    return(indexpage)
