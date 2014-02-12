import bottle


@bottle.route('/')
def index():
    indexpage = """
         <head>
         <title>Hopitty</title>
        </head>
<body>

<h1>Hopitty</h1>

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
<a href="/index.html"><button>Home</button></a>
<a href="cgi-bin/start.py"><button>Run Control</button></a>
<a href="cgi-bin/status.py"><button>Status</button></a>
<a href="cgi-bin/stagesstatus.py"><button>Stages</button></a>
<a href="recipelist"><button>Recipe List</button></a>
<a href="cgi-bin/recipe.py"><button>Recipe</button></a>

</body>
    """
    return(indexpage)
