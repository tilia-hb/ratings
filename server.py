"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/movies')
def movies():
    movies = Movie.query.order_by(Movie.title).all()
    print(movies)
    return render_template('movies.html', movies=movies)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/user/<user_id>')
def get_user_info(user_id):
    user_object = User.query.get(user_id)
    print(user_object)
    print(user_object.zipcode)
    return render_template("user_details.html",
                           display_user=user_object)

@app.route('/movie/<movie_id>')
def get_movie_info(movie_id):
    movie_object = Movie.query.get(movie_id)
    print(movie_object)
    total_score = 0
    for movie in movie_object.ratings:
        total_score += movie.score
    print("total score is: ", total_score)
    average_score = round(total_score / len(movie_object.ratings),2)
    print("average score is: ", average_score)
    num_ratings = len(movie_object.ratings)

    return render_template("movie_details.html",
                           current_movie=movie_object,
                           ave = average_score,
                           num_ratings = num_ratings)


@app.route('/movie/<movie_id>', methods=['POST'])
def rate_movie(movie_id):
    rating = request.form.get('rating')
    current_user_id = session["current_user"]

    movie_object = Movie.query.get(movie_id)
    movie_rating = movie_object.ratings
    print("movie obj is: ", movie_object)
    print("movie rating by current user is: ", movie_rating)

    redirect_route = 'movie/' + str(movie_id)

    return redirect(redirect_route)

@app.route('/registration',methods = ['GET'])
def registration():
    if request.form:
        return redirect('/registration-confirm')
    else:
        return render_template ('registration-form.html')

@app.route('/registration', methods = ['POST'])
def registration_confirm():

    new_email = request.form.get("email")


    #check if email in Users
    if User.query.filter_by(email=new_email).first():
        return redirect('/registration')
    else:   
        pwd = request.form.get('password')
        user = User(
                # user_id = user_id,
                email = new_email,
                password = pwd
                )
        db.session.add(user)
        db.session.commit()

        # print("user id is: ",user_id)
        print(user)
    return render_template('registration-confirm.html',
                            email=new_email)


@app.route('/login')
def login():
    print("shows the login form")
    return render_template('login.html')

@app.route('/login_confirm', methods = ['GET'])
def login_confirm():
    print("processes the login get request")
    new_email = request.args.get('email')
    pwd = request.args.get('password')

    if User.query.filter_by(email=new_email).first():
        current_user = User.query.filter_by(email=new_email).first()
        user_id = str(current_user.user_id)
        user_pwd = current_user.password
        print("cur_user object is: ",current_user)
        print("cur_user_id is: ",user_id)
        print("cur_user password is: ",user_pwd)
        print("entered passowrd is: ", pwd)
        if user_pwd == pwd:
            session["current_user"] = user_id
            redirect_route = 'user/' + user_id
            return redirect(redirect_route)
        else:
            flash("Login failed")
        return render_template('login.html')
# @app.route('/users/<user_id>')
# def user_page(user_id):
#     user_id = user.
    # return render_template('users.html', users=users)
@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out")
    return redirect('/')
    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
