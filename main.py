from flask import Flask, jsonify, request

from storage import all_movies, liked_movies, not_liked_movies, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-movie")
def get_movie():
    movie_data = [
        all_movies[0][19], #title
        all_movies[0][21], #vote count
        all_movies[0][20], #vote average
        all_movies[0][27] #poster link
    ]
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/liked-movie", methods=["POST"])
def liked_movie():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-movie", methods=["POST"])
def unliked_movie():
    movie = all_movies[0]
    not_liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/did-not-watch", methods=["POST"])
def did_not_watch_view():
    movie = all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-movies")
def popular_movies():
    return jsonify({
        "data": output,
        "status": "success"
    }), 200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    return jsonify({
        "data": all_recommended,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()