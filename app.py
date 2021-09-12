from flask import Flask, redirect, url_for, request, render_template
import json
app = Flask(__name__)   

# Take care of /data, I used it for a volume mount on multiple docker container

def getMovies():
    movies = {}

    file = open('data/database_1.txt', 'r')
    if not file.read(1):
        print('File Empty.')
        return movies
    file.seek(0)
    movies = json.loads(file.read())
    print("File Loaded into Memory.")
    file.close()

    if movies.get('true'):
        movies[True] = []
        movies[True] = movies['true']
        movies.pop('true')

    if movies.get('false'):
        movies[False] = []
        movies[False] = movies['false']
        movies.pop('false')
    print(f'Returning movies: {movies}')
    return movies

def setMovies(movies):
    file = open('data/database_1.txt','w')
    file.write(json.dumps(movies))
    print("Data written to File.")
    file.close()

@app.route('/')
def home_page():
    movies = getMovies()
    return render_template('index.html', result=movies, isEmpty=not bool(movies))

@app.route('/addmovie', methods=['POST'])
def addMovie():
    movies = getMovies()
    movieValues = list(movies.values())
    movieValues = [v for value in movieValues for v in value]
    movie = request.form['movie']
    watched = request.form['watched'] == 'yes'
    message = ""
    if not movie:
        message = 'Movie Name can not be empty!'
    elif (not movies) or (movieValues.count(movie) == 0):
        if not movies.get(watched):
            movies[watched] = [movie]
        else:
            movies[watched].append(movie)
        message='Movie Added successfully!'
    else:
        message='Movie Already in Database!'
    print(message)
    setMovies(movies)
    return json.dumps({"Status":message})

@app.route('/editmovie', methods=['PUT'])
def editMovie():
    movies = getMovies()
    movieValues = list(movies.values())
    movieValues = [v for value in movieValues for v in value]
    movie = request.form['movie']
    watched = request.form['watched'] == 'yes'
    message = ""
    if not movie:
        message = 'Movie Name can not be empty!'
    elif (movieValues.count(movie) == 0):
        message = "Movie Not Found! Please use /addMovie endpoint."
    elif movie in movies[watched]:
        message = "New Data can't be same as Old Data"
    else:
        movies[not watched].remove(movie)
        movies[watched].append(movie)
        message = "Movie Updated Successfully"
    setMovies(movies)
    return json.dumps({"Status":message})

@app.route('/removemovie', methods=['DELETE'])
def removeMovie():
    movies = getMovies()
    message = ''
    movie = request.form['movie']
    if not movie:
        message = 'Movie Name can not be empty!'
    elif movies.get(True) and movie in movies[True]:
        movies[True].remove(movie)
        message = 'Movie Removed Successfully!'
    elif movies.get(False) and movie in movies[False]:
        movies[False].remove(movie)
        message = 'Movie Removed Successfully!'
    else:
        message = 'Movie not Found! Please add the movie first using /addmovie endpoint.'
    setMovies(movies)
    return json.dumps({"Status":message})

@app.route('/info/<key>')
def info(key):
    movies = getMovies()
    if not movies:
        return "You haven't watched any movies yet!"
    elif key in movies.get(True):
        return f"You have watched the {key}."
    elif key in movies.get(False):
        return f"You haven't watched the {key}, but you plan on watching it."
    else:
        return f"You haven't watched the {key}, and you aren't planning on watching it."

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)