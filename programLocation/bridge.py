from programLocation.main import search

#recast variables to their correct input for main()
#all incoming variables are strings currently.
def search_initialize(term, website, sorting, review, post_type):

    if term != "":
        website = int(website)
        sorting = int(sorting)
        review = int(review)
        post_type = int(post_type)
        search(term, website, sorting, review, post_type)


