#!/usr/bin/python
import cgi
import pickle
import cgitb
import memcache
#@PydevCodeAnalysisIgnore


# This is for debug, set the selected recipe
# directly in mem cache
def writeCurrentRecipe2Memcache(value):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set('currentRecipe', value)


# This is data that should be sent to controller
def writeSelectedRecipe2Memcache(value):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    mc.set('selectedRecipe', value)

if __name__ == "__main__":
    cgitb.enable()
    form = cgi.FieldStorage()  # instantiate only once!
    setRecipe = form.getfirst('recipe', 'empty')

    # Avoid script injection escaping the user input
    setRecipe = cgi.escape(setRecipe)

    writeCurrentRecipe2Memcache(setRecipe)
    writeSelectedRecipe2Memcache(setRecipe)
    print "Content-Type: text/html"
    print
    print '<html>'
    print '<meta HTTP-EQUIV="REFRESH" content="0; url=/index.html">'
    print """\
    <body><h1>RecipeReader</h1>
    <p>This is the page that should redirect</p>
    <p>The purpose of this page is to read form data and update data files.</p>
    <br><br>
    <p>Recipe selected: %s</p>
    """ % setRecipe

    print "</body></html>"
