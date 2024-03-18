from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.profile import Profile
from models.content import Content
from models.watchlist import WatchList

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            name = "User 1",
            email = "user1@email.com",
            password = bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name = "User 2",
            email = "user2@email.com",
            password = bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name = "User 3",
            email = "user3@email.com",
            password = bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    profiles = [
        Profile(
            name = "Profile 1"
        ),
        Profile(
            name = "Profile 2"
        ),
        Profile(
            name = "Profile 3"
        )
    ]

    db.session.add_all(profiles)

    contents = [
        Content(
            name = "Movie 1",
            genre = "Horror",
            description = "Desc",
            duration = "1:23:45"
        ),
        Content(
            name = "Movie 2",
            genre = "Comdey",
            description = "Desc",
            duration = "1:10:23"
        ),
        Content(
            name = "Show 1",
            genre = "Fantasy",
            description = "Desc",
            duration = "1:08:04"
        ),
        Content(
            name = "Show 2",
            genre = "Action",
            description = "Decs",
            duration = "0:43:21"
        )
    ]

    db.session.add_all(contents)

    watchlists = [
        WatchList(
            title = "Watchlist 1",
            content_id = "1",
            profile_id = "1"
        ),
        WatchList(
            title = "Watchlist 2",
            content_id = "3",
            profile_id = "1"
        ),
        WatchList(
            title = "Watchlist 3",
            content_id = "2",
            profile_id = "2"
        ),
        WatchList(
            title = "Watchlist 4",
            content_id = "4",
            profile_id = "2"
        )
    ]

    db.session.add_all(watchlists)

    db.session.commit()

    print("Tables Seeded")

