import json
import os
import re
import datetime as dt
from datetime import datetime
import validators

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column
from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy import ForeignKey, Enum, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy_utils import ChoiceType

db = SQLAlchemy()

ETHNICITY_TYPE = [
    'asian',
    'black',
    'latino',
    'middle eastern',
    'south asian',
    'southeast asian',
    'white',
]

ETHNICITY_TYPE_ENUM = Enum(*ETHNICITY_TYPE, name='ethnicity')

HAIR_COLOR_TYPE = [
    'black',
    'brown',
    'blond',
    'auburn',
    'chestnut',
    'red',
    'gray',
    'white',
    'bald',
]

HAIR_COLOR_TYPE_ENUM = Enum(*HAIR_COLOR_TYPE, name='hair_color')

EYE_COLOR_TYPE = [
    'amber',
    'blue',
    'brown',
    'gray',
    'green',
    'hazel',
    'red',
    'violet',
]

EYE_COLOR_TYPE_ENUM = Enum(*EYE_COLOR_TYPE, name='eye_color')

BODY_TYPE = [
    'average',
    'slim',
    'athletic',
    'muscular',
    'curvy',
    'heavyset',
    'plus-sized',
]

BODY_TYPE_ENUM = Enum(*BODY_TYPE, name='body_type')

GENDER_TYPE = [
    'male',
    'female',
]

GENDER_TYPE_ENUM = Enum(*GENDER_TYPE, name='gender')


def setup_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    company = Column(String, nullable=False)
    description = Column(String)
    roles = relationship("Role", back_populates="movie", cascade="all, delete")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def update_by_dict(self, **kwags):
        '''
        The function does not commit.
        Use update() method to comiit
        '''
        columns = [c.key for c in Movie.__table__.columns]
        for key, value in kwags.items():
            if key in columns and value is not None:
                setattr(self, key, value)

    def format(self):
        release_date_format = '%Y-%m-%d'
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime(release_date_format),
            'company': self.company,
            'description': self.description
        }

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise AssertionError('No title provided')
        return title

    @validates('release_date')
    def validate_release_date(self, key, release_date):
        '''
        Args:
            key:
            release_date: datetime.date string format "%Y-%m-%d" ex) "2020-03-03"
        '''
        date_format = '%Y-%m-%d'
        if release_date is None:
            raise AssertionError('No release date provided')
        try:
            tranformed_date = datetime.strptime(release_date, date_format)
            return tranformed_date
        except:
            raise AssertionError(f'Provided release_date does not match format {date_format}')

    @validates('company')
    def validate_company(self, key, company):
        if not company:
            raise AssertionError('No company provided')
        return company


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(GENDER_TYPE_ENUM, nullable=False)
    location = Column(String, nullable=False)
    passport = Column(Boolean, default=False)
    driver_license = Column(Boolean, default=False)
    ethnicity = Column(ETHNICITY_TYPE_ENUM)
    hair_color = Column(HAIR_COLOR_TYPE_ENUM)
    eye_color = Column(EYE_COLOR_TYPE_ENUM)
    body_type = Column(BODY_TYPE_ENUM)
    height = Column(Integer)
    description = Column(String)
    image_link = Column(String)
    phone = Column(String)
    email = Column(String)
    roles = relationship("Role", back_populates="actor")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def update_by_dict(self, **kwags):
        '''
        The function does not commit.
        Use update() method to comiit
        '''
        columns = [c.key for c in Actor.__table__.columns]
        for key, value in kwags.items():
            if key in columns and value is not None:
                setattr(self, key, value)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'passport': self.passport,
            'driver_license': self.driver_license,
            'ethnicity': self.ethnicity,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color,
            'body_type': self.body_type,
            'height': self.height,
            'description': self.description,
            'image_link': self.image_link,
            'phone': self.phone,
            'email': self.email
        }

    @validates('name')
    def validate_name(self, key, name):
        if name is None:
            raise AssertionError('No name provided')
        return name

    @validates('age')
    def validate_age(self, key, age):
        if age is None:
            raise AssertionError('No age provided')
        try:
            age = int(age)
        except:
            raise AssertionError('age is not integer')
        return age

    @validates('gender')
    def validate_gender(self, key, gender):
        if gender is None:
            raise AssertionError('No gender provided')
        if gender not in GENDER_TYPE:
            raise AssertionError('Invalid gender type')
        return gender

    @validates('location')
    def validate_location(self, key, location):
        if location is None:
            raise AssertionError('No location provided')
        return location

    @validates('passport')
    def validate_passport(self, key, passport):
        return passport

    @validates('driver_license')
    def validate_driver_license(self, key, driver_license):
        return driver_license

    @validates('ethnicity')
    def validate_ethnicity(self, key, ethnicity):
        if ethnicity and ethnicity not in ETHNICITY_TYPE:
            raise AssertionError('Invalid ethnicity type')
        return ethnicity

    @validates('hair_color')
    def validate_hair_color(self, key, hair_color):
        if hair_color and hair_color not in HAIR_COLOR_TYPE:
            raise AssertionError('Invalid hair color type')
        return hair_color

    @validates('eye_color')
    def validate_eye_color(self, key, eye_color):
        if eye_color and eye_color not in EYE_COLOR_TYPE:
            raise AssertionError('Invalid eye color type')
        return eye_color

    @validates('body_type')
    def validate_body_type(self, key, body_type):
        if body_type and body_type not in BODY_TYPE:
            raise AssertionError('Invalid body type')
        return body_type

    @validates('height')
    def validate_height(self, key, height):
        if height is None:
            return height

        try:
            height = int(height)
        except:
            raise AssertionError('height is not integer')
        if height < 0:
            raise AssertionError('height can not be negative')
        return height

    @validates('description')
    def validate_description(self, key, description):
        return description

    @validates('image_link')
    def validate_image_link(self, key, image_link):
        if image_link and not validators.url(image_link):
            raise AssertionError('Invalid image_link url')
        return image_link

    # TO-DO: Implement validate_phone method
    @validates('phone')
    def validate_phone(self, key, phone):
        return phone

    @validates('email')
    def validate_email(self, key, email):
        if email and not validators.email(email):
            raise AssertionError('Invalid e-mail')
        return email


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    movie_id = Column(
                    Integer,
                    ForeignKey('movies.id', ondelete="CASCADE"),
                    nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id'))
    name = Column(String, nullable=False)
    gender = Column(GENDER_TYPE_ENUM, nullable=False)
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    description = Column(String)
    movie = relationship("Movie", back_populates="roles")
    actor = relationship("Actor", back_populates="roles")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def update_by_dict(self, **kwags):
        '''
        The function does not commit.
        Use update() method to comiit
        '''
        columns = [c.key for c in Role.__table__.columns]
        for key, value in kwags.items():
            if key in columns and value is not None:
                setattr(self, key, value)

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'name': self.name,
            'gender': self.gender,
            'min_age': self.min_age,
            'max_age': self.max_age,
            'description': self.description,
        }

    @validates('movie_id')
    def validate_movie_id(self, key, movie_id):
        if movie_id is None:
            raise AssertionError('No movie id provided')
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            raise AssertionError('Invalid movie id')
        return movie_id

    @validates('actor_id')
    def validate_actor_id(self, key, actor_id):
        if actor_id is None:
            return actor_id
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            raise AssertionError('Invalid actor id')
        return actor_id

    @validates('name')
    def validate_name(self, key, name):
        if name is None:
            raise AssertionError('No name provided')
        return name

    @validates('gender')
    def validate_gender(self, key, gender):
        if gender is None:
            raise AssertionError('No gender provided')
        if gender not in GENDER_TYPE:
            raise AssertionError('Invalid gender type')
        return gender

    @validates('min_age', 'max_age')
    def validate_ages(self, key, field):
        if field < 0:
            raise AssertionError('Age can not be negative')
        if key == 'max_age' and self.min_age > field:
            raise AssertionError('Min age can not be greater than max age')
        return field
