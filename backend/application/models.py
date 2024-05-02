from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy.ext.mutable import MutableList
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()


liked_songs = db.Table(
    "liked_songs",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)
song_playlist = db.Table(
    "song_playlist",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
    db.Column(
        "playlist_id", db.Integer, db.ForeignKey("playlist.id"), primary_key=True
    ),
)

song_rating = db.Table(
    "song_rating",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("rating", db.Integer),
)
flagged_songs = db.Table(
    "flagged_songs",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)
flagged_albums = db.Table(
    "flagged_albums",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("album_id", db.Integer, db.ForeignKey("album.id"), primary_key=True),
)
user_relationships = db.Table(
    "user_relationships",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("following_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    # permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=True)
    blacklisted = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=0)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer())
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic")
    )
    songs = db.relationship("Song", backref="creator")
    albums = db.relationship("Album", backref="creator")
    playlists = db.relationship("Playlist", backref="user")
    liked_songs = db.relationship("Song", secondary=liked_songs, backref="liked_by")
    rated_songs = db.relationship("Song", backref="rated_by", secondary=song_rating)
    flagged_songs = db.relationship(
        "Song", backref="song_flagged_by", secondary=flagged_songs
    )
    flagged_albums = db.relationship(
        "Album", backref="album_flagged_by", secondary=flagged_albums
    )
    followers = db.relationship(
        "User",
        secondary=user_relationships,
        primaryjoin=(user_relationships.c.following_id == id),
        secondaryjoin=(user_relationships.c.follower_id == id),
        backref="following",
        lazy="dynamic",
    )


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.String(1000), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    audio = db.Column(db.String(100), nullable=False)
    poster = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, default=0)
    duration = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    played = db.Column(db.Integer, nullable=False, default=0)
    album = db.Column(db.Integer, db.ForeignKey("album.id"))
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    playlist = db.relationship("Playlist", backref="songs", secondary=song_playlist)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    poster = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False, default=0)
    artist = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    songs = db.relationship("Song", backref="song_album")


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    activity_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
