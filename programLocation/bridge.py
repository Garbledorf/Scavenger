from programLocation.main import search

#search is inefficient, should go directly to the service functions
#recast variables to their correct input for main()
#all incoming variables are strings currently.
def search_initialize(term, selector):
    #if statement probably shouldnt be here. 
    #should be a problem for flaskServer.py
    if term != "":
        selector = int(selector)
        search(term, selector)
        term = ""
        return term


