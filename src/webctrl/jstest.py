import bottle
import commonweb


def jstest():
    common = commonweb.commonweb()
    
    indexpage = """
<!DOCTYPE html>
<html>

<body>

  <script src="js/alert.js"></script>

</body>

</html>
"""

    return(indexpage)
