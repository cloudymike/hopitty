import bottle
import commonweb


def index():
    common = commonweb.commonweb()
    
    indexpage = """
<h2>How to brew</h2>
<ul>
<li>Go to the <b>Recipe List</b> and select a recipe. Make sure you click the
Set button </li>
<li>Go to the <b>Run Control</b> page and click on the green Start button.
If there is just a red Stop button, then a brew is in progress. Either wait
or cancel the
brew by clicking the Stop button.</li>
<li>The <b>Stages</b> page will show you what step in the brew process you
are on.</li>
<li>The <b>Status</b> page shows the status of the current stage in the brew
process.</li>
</ul>
"""
    indexpage = common.header('Hopitty') + indexpage + common.footer()
    indexpage = indexpage + "</body>"

    return(indexpage)
