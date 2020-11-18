import os
import sys

from flask import (
    Flask,
    jsonify,
    abort,
    request
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import (
    setup_db,
    db,
    Actor,
    Movie,
    Role
)
from filters import (
    Actorfilter,
    Moviefilter,
    Rolefilter
)
from auth import (
    requires_auth,
    AuthError
)


ACTOR_COLUMNS = [
    'name', 'age', 'gender', 'location', 'passport',
    'driver_license', 'ethnicity', 'hair_color',
    'eye_color', 'body_type', 'height', 'description',
    'image_link', 'phone', 'email'
]

MOVIE_COLUMNS = ['title', 'release_date', 'company', 'description']

ROLE_COLUMNS = [
    'movie_id', 'actor_id', 'name',
    'gender', 'min_age', 'max_age', 'description'
]

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
setup_db(app)


cors = CORS(app, origins=['http://localhost:5000',
                          'https://duckcastingapi.herokuapp.com'])


@app.after_request
def after_request(response):
    allow_headers = 'Content-Type,Authorization'
    allow_methods = 'GET,POST,PATCH,DELETE,OPTIONS'
    response.headers.add('Access-Control-Allow-Headers', allow_headers)
    response.headers.add('Access-Control-Allow-Methods', allow_methods)
    return response


@app.route('/')
def index():
    return "Hello World!"


@app.route('/actors', methods=['GET'])
def get_actors():
    try:
        actor_filter = Actorfilter(request.args.to_dict(flat=False))
        total_actors_count, actors = actor_filter.get_results()
        actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': total_actors_count,
        })
    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>/roles', methods=['GET'])
def get_roles_of_actor(actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            raise AssertionError('Invalid actor id')
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e)
        }), 422
    try:
        roles = [role.format() for role in actor.roles]
        return jsonify({
            'success': True,
            'id': actor_id,
            'roles': roles
        })
    except Exception:
        abort(422)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(payload):
    body = request.get_json()
    actor_data = {column: body.get(column) for column in ACTOR_COLUMNS}
    try:
        new_actor = Actor(**actor_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            "error": 422,
            'message': str(e)
        }), 422
    try:
        new_actor.insert()
        return jsonify({
            'success': True,
            'id': new_actor.id,
        })
    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(payload, actor_id):
    body = request.get_json()
    actor_data = {column: body.get(column) for column in ACTOR_COLUMNS}
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            raise AssertionError('Invalid actor id')
        actor.update_by_dict(**actor_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e),
        }), 422
    try:
        actor.update()
        return jsonify({
            'success': True,
            'id': actor_id,
        })
    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            raise AssertionError('Invalid actor id')
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e),
        }), 422
    try:
        actor.delete()
        return jsonify({
            'success': True,
            'id': actor_id,
        })
    except Exception:
        abort(422)


@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        movie_filter = Moviefilter(request.args.to_dict(flat=False))
        total_movies_count, movies = movie_filter.get_results()
        movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': total_movies_count,
        })
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>/roles', methods=['GET'])
def get_roles_of_movie(movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            raise AssertionError('Invalid movie id')
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e)
        }), 422
    try:
        roles = [role.format() for role in movie.roles]
        return jsonify({
            'success': True,
            'id': movie_id,
            'roles': roles
        })
    except Exception:
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload):
    body = request.get_json()
    movie_data = {column: body.get(column) for column in MOVIE_COLUMNS}
    try:
        new_movie = Movie(**movie_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e)
        }), 422
    try:
        new_movie.insert()
        return jsonify({
            'success': True,
            'id': new_movie.id,
        })
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(payload, movie_id):
    body = request.get_json()
    movie_data = {column: body.get(column) for column in MOVIE_COLUMNS}
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            raise AssertionError('Invalid movie id')
        movie.update_by_dict(**movie_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e)
        }), 422
    try:
        movie.update()
        return jsonify({
            'success': True,
            'id': movie_id,
        })
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            raise AssertionError('Invalid movie id')
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e),
        }), 422

    try:
        movie.delete()
        return jsonify({
            'success': True,
            'id': movie_id,
        })
    except Exception:
        abort(422)


@app.route('/roles')
def get_roles():
    try:
        role_filter = Rolefilter(request.args.to_dict(flat=False))
        total_roles_count, roles = role_filter.get_results()
        roles = [role.format() for role in roles]
        return jsonify({
            'success': True,
            'roles': roles,
            'total_roles': total_roles_count,
        })
    except Exception:
        abort(422)


@app.route('/roles', methods=['POST'])
@requires_auth('post:roles')
def post_role(payload):
    body = request.get_json()
    role_data = {column: body.get(column) for column in ROLE_COLUMNS}
    try:
        new_role = Role(**role_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            "error": 422,
            'message': str(e)
        }), 422

    try:
        new_role.insert()
        return jsonify({
            'success': True,
            'id': new_role.id,
        })
    except Exception:
        abort(422)


@app.route('/roles/<int:role_id>', methods=['PATCH'])
@requires_auth('patch:roles')
def patch_role(payload, role_id):
    body = request.get_json()
    role_data = {column: body.get(column) for column in ROLE_COLUMNS}
    try:
        role = Role.query.filter(Role.id == role_id).one_or_none()
        if role is None:
            raise AssertionError('Invalid role id')
        role.update_by_dict(**role_data)
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e),
        }), 422

    try:
        role.update()
        return jsonify({
            'success': True,
            'id': role_id,
        })
    except Exception:
        abort(422)


@app.route('/roles/<int:role_id>', methods=['DELETE'])
@requires_auth('delete:roles')
def delete_role(payload, role_id):
    try:
        role = Role.query.filter(Role.id == role_id).one_or_none()
        if role is None:
            raise AssertionError('Invalid role id')
    except AssertionError as e:
        return jsonify({
            'success': False,
            'error': 422,
            'message': str(e),
        }), 422

    try:
        role.delete()
        return jsonify({
            'success': True,
            'id': role_id,
        })
    except Exception:
        abort(422)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
        }), 400


@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized error"
        }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
        }), 500


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    ex.error['success'] = False
    ex.error['error'] = ex.status_code
    ex.error['message'] = ex.error['description']
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run()
