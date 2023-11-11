import utility
from flask import Flask, request
from flask import render_template

from programLocation.bridge import search_initialize

app = Flask(__name__)

@app.route('/')
def testing():
    return render_template(utility.html_file)

@app.route('/', methods =["GET", "POST"])
def input():
    #this works for now, it feels bloated to me, can probably refine
    """Takes input from HTML and directs it to search initialzer"""   
    try:
        search_term = request.form.get("tterminput")
        service_selection = request.form.get("sserviceinput")
        if request.method == "POST" and search_term != "":
            search_initialize(search_term, service_selection)
    except:
        return render_template(utility.html_file)
    search_term = ""
    return render_template(utility.html_file)
