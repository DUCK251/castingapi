# CASTING API Backend

## Motivation

The Casting API Backend project is the Capstone Project for the [Udacity Full Stack NanoDegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044). The project is to practice the skills learned during the Full Stack Web Developer Nanodegree Program. The syllabus of the Udacity FSND is [here](https://d20vrrgs8k4bvw.cloudfront.net/documents/en-US/Full+Stack+-+nd0044+-+syllabus.pdf). The skills used in the Casting API project are described below.

### Stack

- Flask
- PostgreSQL
- SQLAlchemy
- Flask-CORS(Cross-Origin Resource Sharing)
- Unittest
- [Auth0](https://auth0.com/) and RBAC(role-based access control)
- [Docker Compose](https://docs.docker.com/compose/)
- Heroku Deployment
- CI/CD by [CircleCI](https://circleci.com/)

The project URL is 
```
http://duckcastingapi.herokuapp.com/
```

The usage of the API is described in the Introduction part and the Endpoints part.

## Introduction

The casting agency app helps users find the actor for roles in the movie.
The app is used to store movies, actors, and roles associated with the movies. 
The details of database models and endpoints are described below.
Users can send a post request with the movie data including title, company, release date, and description in order to store movie data.
Users can send a post request with the actor data including name, age, gender, and location in order to store actor data.
Users can send a post request with the role data in order to store role data.
Users can also retrieve filtered actors by query string to find talents for hire.
Users can also retrieve filtered roles by query string to find proper roles for an actor.
Users can update movies and actor's details and also delete a movie and an actor by sending requests to the appropriate endpoints.
If an actor is determined for a role, the user can update role data associated with the actor.
The API also implements RBAC(role-based access control) by using [Auth 0](https://auth0.com/). 
Only produce executives can access all methods. 
Casting assistants and Casting directors are given limited access permissions. 
The details of permissions are described below.

## Getting Started

### Using Docker Compose

You are able to use [Docker Compose](https://docs.docker.com/compose/).
First you should install docker and docker compose. Instructions for installing docker for your platform can be found in the [docker docs](https://docs.docker.com/engine/install/) and the [docker compose docs](https://docs.docker.com/compose/install/). Then run in the project directory :


```
docker-compose build
docker-compose up -d
```

Check http://localhost:5000/ and then you will see 'hello world!'.
You can check the logs via `docker-compose logs -f`.

If you want to delete docker images and volumes, run

```
docker stop castingapi_web_1
docker stop castingapi_db_1
docker rm castingapi_web_1
docker rm castingapi_db_1
docker volume rm castingapi_postgres_data
```

### Installing Dependencies

#### Virtual Enviornment

We recommend working within a virtual environment. Instructions for setting up a virtual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

On macOS and Linux:

```bash
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```

On Windows:

```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

## Database Setup

From the folder in terminal run

On macOS and Linux:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///castingapi"
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

On Windows:

```bash
set APP_SETTINGS=config.DevelopmentConfig;
set DATABASE_URL=postgresql:///castingapi;
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server

From within the app directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source env/bin/activate
export APP_SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql:///castingapi'
export AUTH0_DOMAIN='dev-hrmvva9b.us.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='casting'
python3 app.py
```

or, execute:

```bash
source setup.sh
python3 app.py
```

Setting the `APP_SETTINGS` variable will detect file changes and restart the server automatically.

Setting the `DATABASE_URL` variable will set `SQLALCHEMY_DATABASE_URI` in config.py

## RBAC Description

- There are 3 roles and 12 permissions. They are described below. Test Tokens are in setup.sh.

### Assistant

- The assistant role is granted to casting assistants. It contains `get:actors`, `get:movies`, `get:roles` permissions.

### Director

- The director role is granted to casting directors. It contains all permissions assistants have and `patch:actors`, `patch:movies`, `patch:roles`, `post:actors`, `post:roles`, `delete:actors`, `delete:roles`.
- In short, Director has all permissions without `post:movies` and `delete:movies`.

### Producer

- The producer role is granted to executive producers. It contains all permissions directors have and `post:movies`, `delete:movies`.

## Endpoints

### Movie DataBase Description

|Column|Type|Description|
|-|-|-|
|id|int|primary key|
|title|string|not null|
|release_date|date|not null, input string format "%Y-%m-%d" ex)"2020-11-12"|
|company|string|not null|
|description|string||

### GET /movies

- General:
    - Fetches a dictionary of movies
    - Query parameters are `title`, `min_release_date`, `max_release_date`, `release_date`, `comapny`, `description`, `search_term`, `page`, `page_size`
    - `search_term` is for title search and it is case insensitive.
    - Returns : movies, total_movies, success, page
    - The return `movies` is paginated with pagesize and `total_movies` is the number of movies without pagination. (default page is 1 and default page_size is 10)
- Request
```
curl http://127.0.0.1:5000/movies?min_release_date=2022-01-01
```
- Response
```
{
  "movies": [
    {
      "company": "BBC Films", 
      "description": "Vincent's life is on hold until he finds his wife's killer. Alice, his neighbor, is convinced she can make him happy. She decides to invent a culprit, so that Vincent can find revenge and leave the past behind. But there is no ideal culprit and no perfect crime.", 
      "id": 1203, 
      "release_date": "2022-10-21", 
      "title": "A Crime"
    }, 
    {
      "company": "ABC Productions", 
      "description": "The wife and mistress of the sadistic dean of an exclusive prep school conspire to murder him.", 
      "id": 1204, 
      "release_date": "2022-05-05", 
      "title": "Diabolique"
    }, 
    {
      "company": "ABC Productions", 
      "description": "A story of slavery, set in the southern U.S. in the 1930s.", 
      "id": 1206, 
      "release_date": "2022-07-15", 
      "title": "Manderlay"
    }, 
    {
      "company": "Jadran Film", 
      "description": "The life of Jesus Christ, his journey through life as he faces the struggles all humans do, and his final temptation on the cross.", 
      "id": 1208, 
      "release_date": "2023-10-01", 
      "title": "The Last Temptation of Christ"
    }, 
    {
      "company": "Jadran Film", 
      "description": "Three young soldiers who participated in a military operation that went wrong, and where one of their comrades had been killed before their eyes, are placed in a luxury hotel to prevent a scandal. Despite the help of a young military psychiatrist, the young trio denies any trauma suffered, but they seem to hold a very different secret truth.", 
      "id": 1209, 
      "release_date": "2023-01-01", 
      "title": "Palace Beach Hotel"
    }, 
    {
      "company": "Met film", 
      "description": "When violent conflict breaks out between greedy railroaders and a tribe of Mescalero Apaches, only two men, destined to be blood brothers, can prevent all-out war: chief's son Winnetou and German engineer Old Shatterhand.", 
      "id": 1214, 
      "release_date": "2022-02-02", 
      "title": "Winnetou"
    }, 
    {
      "company": "Met film", 
      "description": "Daredevil mountain climbers on their attempt to break yet another speed climbing record.", 
      "id": 1215, 
      "release_date": "2023-09-09", 
      "title": "Am Limit"
    }, 
    {
      "company": "Netflix", 
      "description": "Anna life stroy", 
      "id": 1216, 
      "release_date": "2024-06-06", 
      "title": "Mein Gott, Anna!"
    }, 
    {
      "company": "Netflix", 
      "description": "In a trendy restaurant, public prosecutor Manuel Bacher and his colleagues toast his promotion. On the way home, he meets a quarrelling junkie couple in a park. Manuel wants to help the woman, who is beaten and strangled, and intervenes.", 
      "id": 1217, 
      "release_date": "2024-07-17", 
      "title": "Momentversagen"
    }, 
    {
      "company": "Matrix film", 
      "description": "Just Fake one", 
      "id": 1218, 
      "release_date": "2024-08-28", 
      "title": "Fake Movie"
    }
  ], 
  "success": true,
  "page": 1,
  "total_movies": 11
}
```

### GET /movies/{movie_id}/roles

- General:
    - Fetches a dictionary of roles of a movie
    - Returns : roles, movie_id, success
- Request
```
curl http://127.0.0.1:5000/movies/1/roles
```
- Response
```
{
  "movie_id": 1,
  "roles": [
    {
      "actor_id": null,
      "description": null,
      "gender": "male",
      "id": 1,
      "max_age": 30,
      "min_age": 25,
      "name": "kimmich"
    },
    {
      "actor_id": null,
      "description": null,
      "gender": "male",
      "id": 2,
      "max_age": 35,
      "min_age": 30,
      "name": "revan"
    }
  ],
  "success": true
}
```

### POST /movies
- We can create movie data by the api.
- Bearer Token having `post:movies` permission is needed.
- Create:
    - Create a movie by sending `title, release_date, company, description`. The argument `description` can be null.
    - Request Arguments : title, release_date, company, description
    - Returns : success, id
- Request
```
curl \
-X POST http://127.0.0.1:5000/movies \
-d '{"title": "Test movie", "release_date": "2020-11-12", "company": "Test company", "description" : "fun movie"}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {movie_id}
}
```

### PATCH /movies/{movie_id}
- We can modify movie data by the api.
- Bearer Token having `patch:movies` permission is needed.
- Modify:
    - Modify a movie by sending `title, release_date, company, description`.
    - Request Arguments : title, release_date, company, description
    - Returns : success, id
- Request
```
curl \
-X PATCH http://127.0.0.1:5000/movies/{movie_id} \
-d '{"title": "changed test movie"}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {movie_id}
}
```

### DELETE /movies/{movie_id}
- We can delete movie data by the api.
- Bearer Token having `delete:movies` permission is needed.
- Delete:
    - Request Arguments : None
    - Returns : success, id
    - If the given ID is not valid, returns 422 error.
- Request
```
curl \
-X DELETE http://127.0.0.1:5000/movies/{movie_id} \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {movie_id}
}
```

### Role DataBase Description

|Column|Type|Description|
|-|-|-|
|id|int|primary key|
|movie_id|int|not null, foreign key|
|actor_id|int|foreign key|
|name|string|not null|
|gender|enum|not null, one of ['male','female']|
|min_age|int|not null|
|max_age|int|not null|
|description|string||

### GET /roles

- General:
    - Fetches a dictionary of roles
    - Query parameters are `movie_id`, `actor_id`, `name`, `gender`, `min_age`, `max_age`, `description`, `page`, `page_size`
    - Returns : roles, total_roles, success, page
    - The return `roles` is paginated with pagesize and `total_roles` is the number of roles without pagination. (default page is 1 and default page_size is 10)
- Request
```
curl http://127.0.0.1:5000/roles?gender=male
```
- Response
```
{
  "roles": [
    {
      "description": null, 
      "gender": "male", 
      "id": 1, 
      "max_age": 30, 
      "min_age": 25, 
      "movie_id": 1, 
      "actor_id": null, 
      "name": "kimmich"
    }, 
    {
      "description": null, 
      "gender": "male", 
      "id": 2, 
      "max_age": 35, 
      "min_age": 30, 
      "movie_id": 1, 
      "actor_id": null, 
      "name": "revan"
    }, 
    {
      "description": null, 
      "gender": "male", 
      "id": 3, 
      "max_age": 25, 
      "min_age": 15, 
      "movie_id": 2, 
      "actor_id": null, 
      "name": "jack"
    }, 
    {
      "description": null, 
      "gender": "male", 
      "id": 7, 
      "max_age": 60, 
      "min_age": 50, 
      "movie_id": 4, 
      "actor_id": null, 
      "name": "park"
    }, 
    {
      "description": null, 
      "gender": "male", 
      "id": 8, 
      "max_age": 80, 
      "min_age": 70, 
      "movie_id": 4, 
      "actor_id": null, 
      "name": "park"
    }
  ],
  "page": 1,
  "success": true, 
  "total_roles": 5
}
```

### POST /roles
- We can create role data by the api.
- Bearer Token having `post:roles` permission is needed.
- Create:
    - Create a role by sending `movie_id, actor_id, name, gender, min_age, max_age, description`. The argument `actor_id, description` can be null.
    - Request Arguments : movie_id, actor_id, name, gender, min_age, max_age, description
    - Returns : success, id
- Request
```
curl \
-X POST http://127.0.0.1:5000/roles \
-d '{"movie_id": 1, "name": "jack", "gender": "male", "min_age": 30, "max_age": 35, "description": "jack is strong man"}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {role_id}
}
```

### PATCH /roles/{role_id}
- We can modify role data by the api.
- Bearer Token having `patch:roles` permission is needed.
- Modify:
    - Modify a role by sending `movie_id, actor_id, name, gender, min_age, max_age, description`.
    - Request Arguments : movie_id, actor_id, name, gender, min_age, max_age, description
    - Returns : success, id
- Request
```
curl \
-X PATCH http://127.0.0.1:5000/roles/{role_id} \
-d '{"actor_id": 1}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {role_id}
}
```

### DELETE /roles/{role_id}
- We can delete role data by the api.
- Bearer Token having `delete:roles` permission is needed.
- Delete:
    - Request Arguments : None
    - Returns : success, id
    - If the given ID is not valid, returns 422 error.
- Request
```
curl \
-X DELETE http://127.0.0.1:5000/roles/{role_id} \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {role_id}
}
```

### Actor DataBase Description

|Column|Type|Description|
|-|-|-|
|id|int|primary key|
|name|string|not null|
|age|int|not null|
|gender|enum|not null, one of GENDER_TYPE|
|location|string|not null|
|passport|boolean|default `false`|
|driver_license|boolean|default `false`|
|ethnicity|enum|one of ETHNICITY_TYPE|
|hair_color|enum|one of HAIR_COLOR_TYPE|
|eye_color|enum|one of EYE_COLOR_TYPE|
|body_type|enum|one of BODY_TYPE|
|height|int|Centimetre (cm)|
|description|string||
|image_link|string|URL|
|phone|string|ex)'+1-202-555-0169'|
|email|string|ex)'udacity@casitng.com'|

GENDER_TYPE = [
    'male',
    'female'
]

ETHNICITY_TYPE = [
    'asian',
    'black',
    'latino',
    'middle eastern',
    'south asian',
    'southeast asian',
    'white'
]

HAIR_COLOR_TYPE = [
    'black',
    'brown',
    'blond',
    'auburn',
    'chestnut',
    'red',
    'gray',
    'white',
    'bald'
]

EYE_COLOR_TYPE = [
    'amber',
    'blue',
    'brown',
    'gray',
    'green',
    'hazel',
    'red',
    'violet'
]

BODY_TYPE = [
    'average',
    'slim',
    'athletic',
    'muscular',
    'curvy',
    'heavyset',
    'plus-sized'
]

### GET /actors

- General:
    - Fetches a dictionary of actors
    - Query parameters are `name`, `age`, `min_age`, `max_age`, `gender`, `location`, `passport`, `driver_license`, `ethnicity`, `hair_color`, `eye_color`, `body_type`, `height`, `min_height`, `max_height`, `description`, `image_link`, `phone`, `email`, `search_term`, `page`, `page_size`.
    - By `search_term` query parameter, we are able to search name.
    - Returns : actors, success, page, total_actors
    - The return `actors` is paginated with pagesize and `total_actors` is the number of actors without pagination. (default page is 1 and default page_size is 10)
- Request
```
curl http://127.0.0.1:5000/actors?ethnicity=asian&gender=female
```
- Response
```
{
  "actors": [
    {
      "age": 40, 
      "body_type": "slim", 
      "description": null, 
      "driver_license": false, 
      "email": "effective@casting.com", 
      "ethnicity": "asian", 
      "eye_color": "gray", 
      "gender": "female", 
      "hair_color": "gray", 
      "height": 189, 
      "id": 9, 
      "image_link": null, 
      "location": "KA", 
      "name": "Meret Becker", 
      "passport": false, 
      "phone": "+1-202-555-0169"
    }
  ], 
  "success": true,
  "page": 1,
  "total_actors": 1
}
```

### GET /actors/{actor_id}/roles

- General:
    - Fetches a dictionary of roles of an actor
    - Returns : roles, actor_id, success
- Request
```
curl http://127.0.0.1:5000/actors/1/roles
```
- Response
```
{
  "actor_id": 1,
  "roles": [
    {
      "description": null,
      "gender": "male",
      "id": 1,
      "max_age": 30,
      "min_age": 25,
      "movie_id": 1,
      "name": "kimmich"
    },
    {
      "description": null,
      "gender": "male",
      "id": 2,
      "max_age": 35,
      "min_age": 30,
      "movie_id": 2,
      "name": "revan"
    }
  ],
  "success": true
}
```

### POST /actors
- We can create actor data by the api.
- Bearer Token having `post:actors` permission is needed.
- Create:
    - Create an actor by sending `name`, `age`, `gender`, `location`, `passport`, `driver_license`, `ethnicity`, `hair_color`, `eye_color`, `body_type`, `height`, `description`, `image_link`, `phone`, `email`. The arguments `name`, `age`, `gender`, `location` can not be null.
    - Request Arguments : name, age, gender, location, passport, driver_license, ethnicity, hair_color, eye_color, body_type, height, description, image_link, phone, email, description
    - Returns : success, id
- Request
```
curl \
-X POST http://127.0.0.1:5000/actors \
-d '{"name": "Sofia", "age": 40, "gender": "female", "location": "LA", "passport": true, "driver_license": true, "ethnicity": "white", "hair_color": "brown", "eye_color": "brown", "body_type": "slim", "height": 165, "description": "this is fake actor", "phone": "+1-202-555-0169", "email": "test@casting.com"}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {actor_id}
}
```

### PATCH /actors/{actor_id}
- We can modify actor data by the api.
- Bearer Token having `patch:actors` permission is needed.
- Modify:
    - Modify an actor by sending `name`, `age`, `gender`, `location`, `passport`, `driver_license`, `ethnicity`, `hair_color`, `eye_color`, `body_type`, `height`, `description`, `image_link`, `phone`, `email`.
    - Request Arguments : name, age, gender, location, passport, driver_license, ethnicity, hair_color, eye_color, body_type, height, description, image_link, phone, email, description
    - Returns : success, id
- Request
```
curl \
-X PATCH http://127.0.0.1:5000/actors/{actor_id} \
-d '{"passport": false}' \
-H "Content-Type:application/json" \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {role_id}
}
```

### DELETE /actors/{actor_id}
- We can delete actor data by the api.
- Bearer Token having `delete:actors` permission is needed.
- Delete:
    - Request Arguments : None
    - Returns : success, id
    - If the given ID is not valid, returns 422 error.
- Request
```
curl \
-X DELETE http://127.0.0.1:5000/actors/{actor_id} \
-H "Authorization: Bearer {TOKEN}"
```
- Response
```
{
  "success": true,
  "id": {role_id}
}
```

### Error Handling

- List of errors 

|Error Code|Message|
|-|-|
|400|Bad request|
|401|Unauthorized error|
|404|Not found|
|422|Unprocessable|
|500|Internal server error|

- Response

```
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```


## Testing
To run the tests, run
```
source setup.sh
export DATABASE_URL=postgresql:///castingapi_test
dropdb castingapi_test
createdb castingapi_test
python manage.py db upgrade
python3 test_case.py
python3 test_app_by_assistant_token.py
python3 test_app_by_director_token.py
python3 test_app_by_producer_token.py
```
You can find tokens in setup.sh.

## Heroku URL

- http://duckcastingapi.herokuapp.com/
- Test Tokens are in `setup.sh`