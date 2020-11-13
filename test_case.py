import random
from random import randint

from app import app
from models import db, Actor, Movie, Role
from models import ETHNICITY_TYPE
from models import HAIR_COLOR_TYPE
from models import EYE_COLOR_TYPE
from models import BODY_TYPE
from models import GENDER_TYPE

PHONES = [
    '+1-202-555-0169',
    '+1-202-555-0125',
    '+1-202-555-0133',
    '+1-202-555-0143',
    '+1-202-555-0163',
    '+1-202-555-0159',
    '+1-202-555-0166',
    '+1-202-555-0169',
    '+1-202-555-0172',
    '+1-202-555-0102',
    '+1-202-555-0183',
    '+1-202-555-0137'
]

EMAILS = [
    'this@casting.com',
    'test@casting.com',
    'that@casting.com',
    'udacity@casitng.com',
    'python@casting.com',
    'java@casting.com',
    'javascript@casting.com',
    'effective@casting.com',
    'pythonic@casting.com',
    'nodejs@casting.com',
    'docker@casting.com',
    'kubenetic@casting.com'
]


def insert_movie(title, release_date, company, description):
    movie = Movie(
                title=title, 
                release_date=release_date,
                company=company,
                description=description)
    movie.insert()


def insert_actor(name, age, gender, location):
    actor = Actor(name=name, age=age, gender=gender, location=location)
    actor.passport = random.choice([True, False])
    actor.driver_license = random.choice([True, False])
    actor.ethnicity = random.choice(ETHNICITY_TYPE)
    actor.hair_color = random.choice(HAIR_COLOR_TYPE)
    actor.eye_color = random.choice(EYE_COLOR_TYPE)
    actor.body_type = random.choice(BODY_TYPE)
    actor.height = randint(160, 200)
    actor.phone = random.choice(PHONES)
    actor.email = random.choice(EMAILS)
    actor.insert()


def insert_role(movie_id, name, gender, min_age, max_age):
    role = Role(movie_id=movie_id, name=name, gender=gender, min_age=min_age, max_age=max_age)
    role.insert()


MOVIES = [
    ['Blancanieves', '2021-05-30', 'Nix Films', 'A twist on the Snow White fairy tale that is set in 1920s Seville and centered on a female bullfighter.'],
    ['Aufschneider', '2021-01-01', 'Nix Films', 'About a pathologist with a complicated life. His problems with himself, his colleagues and patients who come down to him, dead or alive.'],
    ['Edge of Darkness', '2020-12-30', 'BBC Films', 'As homicide detective Thomas Craven investigates the murder of his activist daughter, he uncovers a corporate cover-up and government conspiracy that attracts an agent tasked with cleaning up the evidence.'],
    ['A Crime', '2022-10-21', 'BBC Films', "Vincent's life is on hold until he finds his wife's killer. Alice, his neighbor, is convinced she can make him happy. She decides to invent a culprit, so that Vincent can find revenge and leave the past behind. But there is no ideal culprit and no perfect crime."],
    ['Diabolique', '2022-05-05', 'ABC Productions', "The wife and mistress of the sadistic dean of an exclusive prep school conspire to murder him."],
    ['Fish Tank', '2021-08-10', 'ABC Productions', "Everything changes for 15-year-old Mia when her mum brings home a new boyfriend."],
    ["Manderlay", "2022-07-15", "ABC Productions", "A story of slavery, set in the southern U.S. in the 1930s."],
    ["Precious", "2021-05-15", "ABC Productions", "In New York City's Harlem circa 1987, an overweight, abused, illiterate teen who is pregnant with her second child is invited to enroll in an alternative school in hopes that her life can head in a new direction."],
    ["The Last Temptation of Christ", "2023-10-01", "Jadran Film", "The life of Jesus Christ, his journey through life as he faces the struggles all humans do, and his final temptation on the cross."],
    ["Palace Beach Hotel", "2023-01-01", "Jadran Film", "Three young soldiers who participated in a military operation that went wrong, and where one of their comrades had been killed before their eyes, are placed in a luxury hotel to prevent a scandal. Despite the help of a young military psychiatrist, the young trio denies any trauma suffered, but they seem to hold a very different secret truth."],
    ["Nordwand", "2021-03-28", "Jadran Film", "Based on a true story, North Face is a survival drama film about a competition to climb the most dangerous rock face in the Alps. Set in 1936, as Nazi propaganda urges the nation's Alpinists to conquer the unclimbed north face of the Swiss massif - the Eiger - two reluctant German climbers begin their daring ascent."],
    ["Das Zeugenhaus", "2020-12-20", "Jadran Film", "Witnesses about to testify at the Nuremberg War Trials needed a safe place to wait. All under one roof, each with their own secrets. And the countess assigned to take care of them. What was her secret?"],
    ["Hannah Arendt", "2021-04-12", "Met film", "A look at the life of philosopher and political theorist Hannah Arendt, who reported for 'The New Yorker' on the trial of the Nazi leader Adolf Eichmann in Jerusalem."],
    ["Die Wand", "2021-04-13", "Met film", "A woman inexplicably finds herself cut off from all human contact when an invisible, unyielding wall suddenly surrounds the countryside. Accompanied by her loyal dog Lynx, she becomes immersed in a world untouched by civilization and ruled by the laws of nature."],
    ["Winnetou", "2022-02-02", "Met film", "When violent conflict breaks out between greedy railroaders and a tribe of Mescalero Apaches, only two men, destined to be blood brothers, can prevent all-out war: chief's son Winnetou and German engineer Old Shatterhand."],
    ["Am Limit", "2023-09-09", "Met film", "Daredevil mountain climbers on their attempt to break yet another speed climbing record."],
    ["Mein Gott, Anna!", "2024-06-06", "Netflix", "Anna life stroy"],
    ["Momentversagen", "2024-07-17", "Netflix", "In a trendy restaurant, public prosecutor Manuel Bacher and his colleagues toast his promotion. On the way home, he meets a quarrelling junkie couple in a park. Manuel wants to help the woman, who is beaten and strangled, and intervenes."],
    ["Fake Movie", "2024-08-28", "Matrix film", "Just Fake one"],
    ["Fun Movie", "2025-01-01", "Matrix film", "Just Fun one"]
]

ACTORS = [
    ['Inma Cuesta', 24, 'female', 'LA'],
    ['Ignacio Mateos', 62, 'male', 'CA'],
    ['Maribel Verdu', 33, 'female', 'LA'],
    ['Sofia Oria', 40, 'female', 'CA'],
    ['Pep Ferrer', 52, 'male', 'MA'],
    ['Josef Hader', 15, 'male', 'MA'],
    ['Ursula Strauss', 22, 'female', 'MA'],
    ['Georg Friedrich', 38, 'male', 'KA'],
    ['Meret Becker', 40, 'female', 'KA'],
    ['Simon Schwarz', 30, 'male', 'KA']
]

ROLES = [
    [1, 'kimmich', 'male', 25, 30],
    [1, 'revan', 'male', 30, 35],
    [2, 'jack', 'male', 15, 25],
    [2, 'mich', 'female', 10, 15],
    [3, 'kim', 'female', 20, 25],
    [3, 'lee', 'female', 20, 25],
    [4, 'park', 'male', 50, 60],
    [4, 'park', 'male', 70, 80],
]

for movie in MOVIES:
    insert_movie(movie[0], movie[1], movie[2], movie[3])

for actor in ACTORS:
    insert_actor(actor[0], actor[1], actor[2], actor[3])

for role in ROLES:
    insert_role(role[0], role[1], role[2], role[3], role[4])