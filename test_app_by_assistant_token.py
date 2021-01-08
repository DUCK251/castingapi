import os
import sys
import unittest
import json

from app import app
from models import (
    db,
    Actor,
    Movie,
    Role
)

'''
ASSISTANT_TOKEN can be expired
'''
ASSISTANT_TOKEN = str(os.environ['ASSISTANT'])
HEADER = {'Authorization': f'Bearer {ASSISTANT_TOKEN}'}


class AppTestCase(unittest.TestCase):
    test_actor = {
        'name': 'test_name',
        'age': 22,
        'gender': 'male',
        'location': 'LA'
    }

    test_movie = {
        'title': 'test_movie',
        'release_date': '2021-01-01',
        'company': 'test_company',
        'description': 'test movie'
    }

    test_role = {
        'name': 'test_role',
        'gender': 'male',
        'min_age': 20,
        'max_age': 25,
        'description': 'test role'
    }

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

        movies = Movie.query.filter(Movie.title == 'test_movie').all()
        for movie in movies:
            movie.delete()
        actors = Actor.query.filter(Actor.name == 'test_name').all()
        for actor in actors:
            actor.delete()

    def tearDown(self):
        movies = Movie.query.filter(Movie.title == 'test_movie').all()
        for movie in movies:
            movie.delete()
        actors = Actor.query.filter(Actor.name == 'test_name').all()
        for actor in actors:
            actor.delete()

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['page'] == 1)

    def test_get_actors_filtered_by_two_id(self):
        actor_one = Actor(**AppTestCase.test_actor)
        actor_one.insert()
        actor_one_id = actor_one.id
        actor_two = Actor(**AppTestCase.test_actor)
        actor_two.insert()
        actor_two_id = actor_two.id
        actor_id_list = [actor_one_id, actor_two_id]

        res = self.client().get(f'/actors?id={actor_one_id}&id={actor_two_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['page'] == 1)
        self.assertTrue(data['total_actors'] == 2)
        self.assertTrue(data['actors'][0]['id'] in actor_id_list)
        self.assertTrue(data['actors'][1]['id'] in actor_id_list)

        actor_one.delete()
        actor_two.delete()

    def test_get_actors_by_name_search_term(self):
        actor = Actor(**AppTestCase.test_actor)
        actor.insert()
        search_term = 'es'

        res = self.client().get(f'/actors?search_term={search_term}')
        data = json.loads(res.data)

        actor.delete()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for actor in data['actors']:
            self.assertTrue(search_term in actor['name'])

    def test_get_male_actors(self):
        res = self.client().get(f'/actors?gender=male')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for actor in data['actors']:
            self.assertEqual(actor['gender'], 'male')

    def test_get_actors_having_passport(self):
        res = self.client().get(f'/actors?passport=t')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for actor in data['actors']:
            self.assertTrue(actor['passport'])

    def test_get_roles_of_actor(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        new_role = Role(**AppTestCase.test_role)
        new_role.movie = new_movie
        new_role.actor = new_actor
        new_role.insert()

        res = self.client().get(f'/actors/{actor_id}/roles')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor_id)
        self.assertTrue('actor_id' not in data['roles'][0])

    def test_error_get_roles_of_actor_by_invalid_id(self):
        actor_id = 987654321

        res = self.client().get(f'/actors/{actor_id}/roles')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid actor id')

    def test_create_actor(self):
        res = self.client().post('/actors',
                                 json=AppTestCase.test_actor,
                                 headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

    def test_patch_actor_to_change_age(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        change_data = {
            'age': 23
        }

        res = self.client().patch(f'/actors/{actor_id}',
                                  json=change_data,
                                  headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_actor.delete()

    def test_delete_actor(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().delete(f'/actors/{actor_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_actor.delete()

    def test_get_movies(self):
        res = self.client().get('/movies?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertTrue(data['success'])

    def test_get_movies_by_id(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().get(f'/movies?id={movie_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'][0]['id'], movie_id)

        new_movie.delete()

    def test_get_movies_by_min_release_date(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        min_release_date = '2020-11-25'

        res = self.client().get(f'/movies?min_release_date={min_release_date}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'][0]['release_date'] >= min_release_date)

        new_movie.delete()

    def test_get_movies_by_title_search_term(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        search_term = 'test'

        res = self.client().get(f'/movies?search_term={search_term}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for movie in data['movies']:
            self.assertTrue(search_term in movie['title'])

        new_movie.delete()

    def test_get_movies_with_page_and_page_size(self):
        res = self.client().get(f'/movies?page=2&page_size=4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['movies']), 4)

    def test_get_roles(self):
        res = self.client().get('/roles?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['page'], 2)
        self.assertTrue(data['success'])

    def test_get_roles_of_movie(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id
        new_role = Role(**AppTestCase.test_role)
        new_role.movie = new_movie
        new_role.insert()

        res = self.client().get(f'/movies/{movie_id}/roles')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movie_id' not in data['roles'][0])
        self.assertEqual(data['movie_id'], movie_id)

    def test_error_get_roles_of_movie_by_invalid_id(self):
        movie_id = 987654321

        res = self.client().get(f'/movies/{movie_id}/roles')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid movie id')

    def test_create_movie(self):
        res = self.client().post(
            '/movies',
            json=AppTestCase.test_movie,
            headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

    def test_patch_movie_to_change_title(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        change_data = {
            'title': 'changed_test_movie'
        }

        res = self.client().patch(f'/movies/{movie_id}',
                                  json=change_data,
                                  headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_movie.delete()

    def test_delete_movie(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete(f'/movies/{movie_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_movie.delete()

    def test_get_roles_by_min_age(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()

        new_role = Role(movie_id=movie_id, **AppTestCase.test_role)
        new_role.actor = new_actor
        new_role.insert()

        min_age = 20
        res = self.client().get(f'/roles?min_age={min_age}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for role in data['roles']:
            self.assertTrue(role['min_age'] >= min_age)

        new_movie.delete()
        new_actor.delete()

    def test_create_role(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        valid_test_role = AppTestCase.test_role.copy()
        valid_test_role['movie_id'] = movie_id

        res = self.client().post('/roles',
                                 json=valid_test_role,
                                 headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_movie.delete()

    def test_patch_role_to_provide_actor_id(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_role = Role(movie_id=movie_id, **AppTestCase.test_role)
        new_role.insert()
        role_id = new_role.id

        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch(f'/roles/{role_id}',
                                  json={'actor_id': actor_id},
                                  headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_movie.delete()
        new_actor.delete()

    def test_delete_role(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_role = Role(movie_id=movie_id, **AppTestCase.test_role)
        new_role.insert()
        role_id = new_role.id

        res = self.client().delete(f'/roles/{role_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

        new_movie.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
