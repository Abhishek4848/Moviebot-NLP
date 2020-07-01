import imdb
ia = imdb.IMDb()

#Function to get all details of a movie searched by user
def searchbymovie(search):
    movies = ia.search_movie(search)
    id = movies[0].getID()
    movie = ia.get_movie(id)
    title = movie['title']
    year = movie['year']
    rating = movie['rating']
    directors = movie['directors']
    direcStr = ' '.join(map(str,directors))
    casting = movie['cast']
    actors = ', '.join(map(str, casting))
    genre = movie['genre']
    gnr = ' '.join(map(str,genre))
    plt = movie['plot']
    desc = " ".join(plt)
    lang = movie['languages']
    lng=", ".join(lang)
    imgurl = movie['cover url']
    movdetails = []
    movdetails.append(title)
    movdetails.append(year)
    movdetails.append(rating)
    movdetails.append(gnr)
    movdetails.append(lng)
    movdetails.append(direcStr)
    movdetails.append(actors)
    movdetails.append(desc)
    return (movdetails)

#Function to get the blockuster movies of a year   
def blockbuster(search):
    movlist = []
    topmovies = ia.get_top250_movies()
    for i in range (len(topmovies)): 
            if topmovies[i]['year'] == search:
                movlist.append(topmovies[i]['title'])

    return(movlist)
