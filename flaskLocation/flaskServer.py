import utility
import os
from flask import Flask, request, redirect
from flask import render_template

from programLocation.bridge import search_initialize

app = Flask(__name__)

@app.route('/')
def testing():
    return render_template(utility.html_file)

@app.route('/', methods =["GET", "POST"])
def input():
    """Takes input from HTML and directs it to search initialzer"""   
    if request.method == 'POST':
        search_term = request.form.get("tterminput")
        service_selection = request.form.get("sserviceinput")
        sorting_selection = request.form.get("ssortinginput")
        review_sorting = request.form.get("rreviewinput")
        if str.isspace(search_term) == False:
            search_initialize(search_term, service_selection, sorting_selection, review_sorting)
        return redirect(utility.home_location)
    return render_template(utility.html_file)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)