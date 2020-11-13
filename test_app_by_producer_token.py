import os, sys
import unittest
import json

from app import app
from models import db, Actor, Movie, Role

'''
PRODUCER_TOKEN can be expired
'''
PRODUCER_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktpQ3ZwMmZaZXdfMlJwemxaSUR2QiJ9.eyJpc3MiOiJodHRwczovL2Rldi1ocm12dmE5Yi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTY3MTg5NTY4ODEwMjExNDc0MjEiLCJhdWQiOlsiY2FzdGluZyIsImh0dHBzOi8vZGV2LWhybXZ2YTliLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDUwOTQ1MjksImV4cCI6MTYwNTE4MDkyOSwiYXpwIjoiMmxPRHliNExwZk5RaldRdVA3emUyTFpUSXdyN1VTUDkiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6cm9sZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImdldDpyb2xlcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBhdGNoOnJvbGVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInBvc3Q6cm9sZXMiXX0.YZpmXx9AFst3oFU2A6BUrHrOLGTguVa78loqI2luNvh7oW3o6dAC0Gx1KmIuEsMHFdccv5912foCw6z4TdRr_-kKf_EUiWZSezezGt5lZ2V_SWli4NwYKs9Sl97vEU0w17x3zAP-5wSNW2RaJ8fqX-bLmC8siqyctynvF05poV2vfeJ9pdwz4Olg38s_qqwohR8ikHf2PWNk6gEWBzxh29BFdBUSyRVHWy4OavV3NUMvoudoNniTlGjo1fAJIh-mGLLSDXM-Wwp_acJ4pxgHL7yVeeYomE5BLp2-sUM4u5E1MeRb_MxhHy0WW253GxfPZEqflh3WGmBIJUZqa4-oBQ'
PRODUCER_HEADER = {'Authorization': PRODUCER_TOKEN}
HEADER = PRODUCER_HEADER


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

    def test_get_actors_filtered_by_two_id(self):
        actor_one = Actor(**AppTestCase.test_actor)
        actor_one.insert()
        actor_one_id = actor_one.id
        actor_two = Actor(**AppTestCase.test_actor)
        actor_two.insert()
        actor_two_id = actor_two.id

        res = self.client().get(f'/actors?id={actor_one_id}&id={actor_two_id}')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_actors'] == 2)
        self.assertTrue(data['actors'][0]['id'] in [actor_one_id, actor_two_id])
        self.assertTrue(data['actors'][1]['id'] in [actor_one_id, actor_two_id])

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

    def test_create_actor(self):
        res = self.client().post('/actors', json=AppTestCase.test_actor, headers=HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actor = Actor.query.filter(Actor.name == 'test_name').one_or_none()
        actor.delete()

    def test_create_actor_error_by_not_providing_name(self):
        invalid_test_actor = {
            'age': 22,
            'gender': 'male',
            'location': 'LA'
        }

        res = self.client().post('/actors', json = invalid_test_actor, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No name provided')

    def test_patch_actor_to_change_age(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        change_data = {
            'age': 23
        }

        res = self.client().patch(f'/actors/{actor_id}', json=change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.get(actor_id)
        self.assertEqual(actor.age, 23)
        actor.delete()
    
    def test_patch_actor_to_change_passport(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        change_data = {
            'passport': True
        }

        res = self.client().patch(f'/actors/{actor_id}', json=change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.get(actor_id)
        self.assertTrue(actor.passport)

        change_data = {
            'passport': False
        }

        res = self.client().patch(f'/actors/{actor_id}', json=change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.get(actor_id)
        self.assertFalse(actor.passport)

    def test_patch_actor_error_by_invalid_gender(self):
        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()

        change_data = {
            'gender': 'femalee'
        }

        res = self.client().patch(f'/actors/{new_actor.id}', json=change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        new_actor.delete()

    def test_delete_actor(self):
        new_actor = Actor(name = 'test_name', age = 22, gender = 'male', location = 'LA')
        new_actor.insert()

        res = self.client().delete(f'/actors/{new_actor.id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.filter(Actor.name == 'test_name').one_or_none()
        self.assertIsNone(actor)

    def test_delete_actor_error_by_providing_invalid_id(self):
        actor_id = 0
        res = self.client().delete(f'/actors/{actor_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid actor id')

    def test_get_movies_by_id(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().get(f'/movies?id={movie_id}')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movies'][0]['id'], movie_id)

    def test_get_movies_by_min_release_date(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        min_release_date = '2020-11-25'

        res = self.client().get(f'/movies?min_release_date={min_release_date}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movies'][0]['release_date'] >= min_release_date)

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

    def test_get_movies_with_page_and_page_size(self):
        res = self.client().get(f'/movies?page=2&page_size=4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['movies']), 4)

    def test_create_movie(self):
        res = self.client().post(
            '/movies', 
            json=AppTestCase.test_movie, 
            headers=PRODUCER_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movie = Movie.query.filter(Movie.title == 'test_movie').one_or_none()
        self.assertEqual(data['id'], movie.id)
        movie.delete()

    def test_create_movie_error_by_invalid_release_date(self):
        invalid_test_movie = {
            'title': 'test_movie',
            'release_date': '12-12-2020',
            'company': 'test_company',
            'description': 'test movie'
        }

        res = self.client().post(
            '/movies', 
            json=invalid_test_movie, 
            headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Provided release_date does not match format %Y-%m-%d')

    def test_create_movie_error_by_not_providing_release_date(self):
        invalid_test_movie = {
            'title': 'test_movie',
            'company': 'test_company',
            'description': 'test movie'
        }

        res = self.client().post(
            '/movies', 
            json=invalid_test_movie,
            headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No release date provided')

    def test_patch_movie_to_change_title(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        change_data = {
            'title': 'changed_test_movie'
        }
        
        res = self.client().patch(f'/movies/{movie_id}', json=change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movie = Movie.query.get(movie_id)
        self.assertEqual(movie.title, 'changed_test_movie')
        movie.delete()

    def test_patch_movie_error_by_invalid_release_date(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        change_data = {
            'release_date': '12-12-2020'
        }
        
        res = self.client().patch(f'/movies/{movie_id}', json = change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Provided release_date does not match format %Y-%m-%d')
        movie = Movie.query.get(movie_id)
        movie.delete()

    def test_delete_movie(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        res = self.client().delete(f'/movies/{movie_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        self.assertIsNone(movie)

    def test_delete_movie_error_by_providing_invalid_id(self):
        movie_id = 0
        res = self.client().delete(f'/movies/{movie_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid movie id')

    def test_get_roles_by_min_age(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()

        new_role = Role(movie_id = movie_id, **AppTestCase.test_role)
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
        
        res = self.client().post('/roles', json = valid_test_role, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        role = Role.query.filter(Role.name == 'test_role').one_or_none()
        self.assertEqual(data['id'], role.id)
 
        new_movie.delete()

    def test_create_role_error_by_invalid_movie_id(self):
        invalid_test_role = {
            'movie_id': 987654321,
            'name': 'test_role',
            'gender': 'male',
            'min_age': 20,
            'max_age': 25,
            'description': 'test role'
        }
        
        res = self.client().post('/roles', json = invalid_test_role, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid movie id')

    def test_patch_role_to_provide_actor_id(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_role = Role(movie_id = movie_id, **AppTestCase.test_role)
        new_role.insert()
        role_id = new_role.id

        new_actor = Actor(**AppTestCase.test_actor)
        new_actor.insert()
        actor_id = new_actor.id

        res = self.client().patch(f'/roles/{role_id}', json = {'actor_id': actor_id}, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], role_id)
        role = Role.query.get(role_id)
        self.assertEqual(role.actor_id, actor_id)

        new_movie.delete()
        new_actor.delete()

    def test_patch_role_by_invalid_age_interval(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_role = Role(movie_id = movie_id, **AppTestCase.test_role)
        new_role.insert()
        role_id = new_role.id

        change_data = {
            'min_age': 25,
            'max_age': 20,
        }

        res = self.client().patch(f'/roles/{role_id}', json = change_data, headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Min age can not be greater than max age')

        new_movie.delete()

    def test_delete_role(self):
        new_movie = Movie(**AppTestCase.test_movie)
        new_movie.insert()
        movie_id = new_movie.id

        new_role = Role(movie_id = movie_id, **AppTestCase.test_role)
        new_role.insert()
        role_id = new_role.id

        res = self.client().delete(f'/roles/{role_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], role_id)

        new_movie.delete()

    def test_delete_role_error_by_invalid_role_id(self):
        invalid_role_id = 0
        res = self.client().delete(f'/roles/{invalid_role_id}', headers=HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid role id') 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()