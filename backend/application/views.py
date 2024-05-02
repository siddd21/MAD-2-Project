from datetime import datetime, timedelta
import os
import uuid
import wave
from flask import current_app as app
from flask import jsonify, render_template, request
from flask_security import (
    login_user,
    current_user,
    auth_required,
    roles_required,
    logout_user,
    roles_accepted,
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import *
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import seaborn as sns
from .models import *
from .security import user_datastore
from .instances import cache

current_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(current_dir, "..", "frontend", "src")
# base_dir = "/home/sidd/STUDY/MAD-2/Project/frontend/src"
upload_folder_profile_pic = os.path.join(base_dir, "assets", "profile_pictures")
upload_folder_graphs = os.path.join(base_dir, "assets", "graphs")
sns.set_theme()


def audio_duration(file_path):
    with wave.open(file_path, "r") as audio_file:
        frame_rate = audio_file.getframerate()
        n_frames = audio_file.getnframes()
        duration = n_frames / float(frame_rate)
        return duration


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/user_login")
def login():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "email not provided"}), 404

    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if check_password_hash(user.password, data.get("password")):
        login_user(user)
        if user.login_count is None:
            user.login_count = 1
        else:
            user.login_count += 1
        if user.current_login_at is None:
            user.current_login_at = datetime.now()
            user.last_login_at = user.current_login_at
        else:
            user.last_login_at = user.current_login_at
            user.current_login_at = datetime.now()
        db.session.commit()
        return (
            jsonify(
                {
                    "token": user.get_auth_token(),
                    "email": user.email,
                    "role": user.roles[0].name,
                    "blacklisted": user.blacklisted,
                }
            ),
            200,
        )

    else:
        return jsonify({"message": "Wrong Password"}), 400


@app.post("/register")
def register():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    if not email:
        return jsonify({"message": "Email not provided"}), 404

    if not password:
        return jsonify({"message": "Password not provided"}), 404

    if user_datastore.find_user(email=email):
        return jsonify({"message": "User already exists!"}), 404

    if "profile_pic" in request.files:
        profile_pic = request.files["profile_pic"]
        profile_pic_name = f"{uuid.uuid4().hex}_{profile_pic.filename}"
        profile_pic_path = os.path.join(upload_folder_profile_pic, profile_pic_name)
        profile_pic.save(profile_pic_path)
        user_datastore.create_user(
            email=email,
            password=generate_password_hash(password),
            roles=["general_user"],
            username=name,
            profile_picture=profile_pic_name,
        )

    else:
        profile_pic_name = "profile-icon-design-free-vector.jpg"
        user_datastore.create_user(
            email=email,
            password=generate_password_hash(password),
            roles=["general_user"],
            username=name,
            profile_picture=profile_pic_name,
        )
    db.session.commit()
    return jsonify({"message": "Registered succesfully!"}), 200


@app.get("/get_song/<id>")
@auth_required
@roles_accepted("creator", "general_user")
def get_song(id):
    song = Song.query.filter_by(id=id).first()
    song.played += 1
    db.session.commit()
    if song in current_user.rated_songs:
        rating = (
            db.session.query(song_rating)
            .filter_by(song_id=id, user_id=current_user.id)
            .first()
            .rating
        )
    else:
        rating = 0
    if song in current_user.liked_songs:
        liked = True
    else:
        liked = False
    if song:
        return {
            "name": song.name,
            "lyrics": song.lyrics,
            "artist": song.artist,
            "genre": song.genre,
            "audio": song.audio,
            "poster": song.poster,
            "duration": song.duration,
            "liked": liked,
            "rating": rating,
        }, 200
    else:
        return jsonify({"message": "Song not found"}), 400


@app.get("/current_creator_songs/<string>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def current_creator_songs(string):
    creator = current_user
    all_songs = creator.songs
    if string != "albums":
        i = 1
        songs = {}
        this_song = {}
        for song in all_songs:
            this_song["id"] = song.id
            this_song["name"] = song.name
            this_song["genre"] = song.genre
            this_song["lyrics"] = song.lyrics
            this_song["poster"] = song.poster
            this_song["audio"] = song.audio
            this_song["duration"] = song.duration
            songs[i] = this_song
            i += 1
            this_song = {}
        return songs, 200
    else:
        no_album = []
        for song in all_songs:
            if song.album == None:
                no_album.append(song)
        i = 1
        no_album_songs = {}
        to_add = {}
        for song in no_album:
            to_add["id"] = song.id
            to_add["name"] = song.name
            to_add["genre"] = song.genre
            to_add["lyrics"] = song.lyrics
            to_add["poster"] = song.poster
            to_add["audio"] = song.audio
            to_add["duration"] = song.duration
            no_album_songs[i] = to_add
            i += 1
            to_add = {}
        return no_album_songs, 200


@app.get("/get_album/<id>")
@auth_required("token")
@roles_required("creator")
def get_album(id):
    album = Album.query.filter_by(id=id).first()
    songs = [
        {
            "id": song.id,
            "name": song.name,
            "artist": song.artist,
            "poster": song.poster,
            "genre": song.genre,
            "date_added": song.date_added,
            "duration": song.duration,
            "rating": song.rating,
        }
        for song in album.songs
    ]
    return {
        "id": album.id,
        "name": album.name,
        "artist": album.artist,
        "poster": album.poster,
        "songs": songs,
    }, 200


@app.get("/current_creator_albums")
@auth_required("token")
@roles_required("creator")
def current_creator_albums():
    all_albums = Album.query.filter_by(creator_id=current_user.id).all()
    albums = []
    for album in all_albums:
        albums.append(
            {
                "id": album.id,
                "name": album.name,
                "artist": album.artist,
                "genre": album.genre,
                "poster": album.poster,
                "rating": album.rating,
                "date_added": album.date_added.strftime("%d %b %Y"),
            }
        )
    return albums, 200


@app.get("/remove_album_song/<album_id>/<song_id>")
@auth_required("token")
@roles_required("creator")
def remove_album_song(album_id, song_id):
    album = Album.query.filter_by(id=album_id).first()
    song = Song.query.filter_by(id=song_id).first()
    if album:
        if song in album.songs:
            album.songs.remove(song)
            db.session.commit()
            return {"message": "Song removed succesfully!"}, 200


@app.get("/get_playlist/<id>")
@roles_accepted("creator", "general_user")
@auth_required("token")
def get_playlist(id):
    playlist = Playlist.query.filter_by(id=id).first()
    songs = [
        {
            "id": song.id,
            "name": song.name,
            "artist": song.artist,
            "poster": song.poster,
            "genre": song.genre,
        }
        for song in playlist.songs
    ]
    return {
        "id": playlist.id,
        "name": playlist.name,
        "songs": songs,
    }, 200


@app.get("/remove_playlist_song/<playlist_id>/<song_id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def remove_playlist_song(playlist_id, song_id):
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    song = Song.query.filter_by(id=song_id).first()
    if len(playlist.songs) > 1:
        playlist.songs.remove(song)
        db.session.commit()
        return {"message": "Song removed succesfully!"}, 200
    else:
        return {"message": "Playlist should have atleast one one song!"}, 400


@app.get("/add_playlist_songs/<id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def add_playlist_songs(id):
    subquery = (
        db.session.query(song_playlist.c.song_id).filter_by(playlist_id=id).subquery()
    )
    no_playlist = Song.query.filter(Song.id.notin_(subquery)).all()
    i = 1
    no_playlist_songs = {}
    to_add = {}
    for song in no_playlist:
        to_add["id"] = song.id
        to_add["name"] = song.name
        to_add["genre"] = song.genre
        to_add["lyrics"] = song.lyrics
        to_add["poster"] = song.poster
        to_add["audio"] = song.audio
        to_add["duration"] = song.duration
        no_playlist_songs[i] = to_add
        i += 1
        to_add = {}
    return no_playlist_songs, 200


@app.get("/like_song/<id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def like_song(id):
    song = Song.query.filter_by(id=id).first()
    if song in current_user.liked_songs:
        current_user.liked_songs.remove(song)
    else:
        current_user.liked_songs.append(song)
    db.session.commit()
    return {"message": "Operation succesfull!"}, 200


@app.post("/rate_song/<id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def rate_song(id):
    song = Song.query.filter_by(id=id).first()
    data = request.get_json()
    rating = data.get("rating")
    if song not in current_user.rated_songs:
        current_user.rated_songs.append(song)
        db.session.commit()
    db.session.query(song_rating).filter_by(song_id=id, user_id=current_user.id).update(
        {"rating": rating}
    )
    db.session.commit()
    ratings = db.session.query(song_rating).filter_by(song_id=id).all()
    creator_ratings = (
        db.session.query(song_rating).filter_by(user_id=current_user.id).all()
    )
    total_rating = 0
    rating_count = 0
    for element in ratings:
        total_rating += int(element[2])
        rating_count += 1
    song.rating = round((total_rating / rating_count), 2)
    db.session.commit()
    creator_total_rating = 0
    creator_rating_count = 0
    for element in creator_ratings:
        creator_total_rating += int(element[2])
        creator_rating_count += 1
    current_user.rating = round((creator_total_rating / creator_rating_count), 2)
    db.session.commit()
    album = song.song_album
    if album is not None:
        album_rating_list = []
        for s in album.songs:
            album_rating_list.append(s.rating)
        album.rating = round((sum(album_rating_list) / len(album_rating_list)), 2)
        db.session.commit()
    return {"message": "Operation completed succesfully!"}, 200


@app.get("/get_artists")
@auth_required("token")
@roles_accepted("creator", "general_user", "admin")
def get_artists():
    # @cache.cached(timeout=60)
    all_artists = (
        User.query.join(User.roles)
        .filter(Role.id == 2)
        .order_by(desc(User.rating))
        .all()
    )
    artists = []
    this_artist = {}
    for artist in all_artists:
        this_artist["id"] = artist.id
        this_artist["name"] = artist.username
        this_artist["rating"] = artist.rating
        this_artist["profile_picture"] = artist.profile_picture
        this_artist["blacklisted"] = artist.blacklisted
        artists.append(this_artist)
        this_artist = {}
    return artists, 200


@app.get("/get_artist_details/<id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def get_artist_details(id):
    artist = User.query.filter_by(id=id).first()
    artist_songs = Song.query.filter_by(creator_id=id).all()
    artist_albums = Album.query.filter_by(creator_id=id).all()
    songs = []
    this_song = {}
    for song in artist_songs:
        this_song["id"] = song.id
        this_song["name"] = song.name
        this_song["artist"] = song.artist
        this_song["artist_id"] = song.creator_id
        this_song["lyrics"] = song.lyrics
        this_song["poster"] = song.poster
        this_song["audio"] = song.audio
        this_song["duration"] = song.duration
        this_song["rating"] = song.rating
        this_song["duration"] = song.duration
        this_song["date_added"] = song.date_added.strftime("%d %b %Y")
        if song.song_album != None:
            this_song["album"] = song.song_album.name
            this_song["album_id"] = song.song_album.id
        else:
            this_song["album"] = None
            this_song["album_id"] = None
        songs.append(this_song)
        this_song = {}
    albums = []
    this_album = {}
    for album in artist_albums:
        this_album["id"] = album.id
        this_album["poster"] = album.poster
        this_album["name"] = album.name
        this_album["rating"] = album.rating
        this_album["date_added"] = album.date_added.strftime("%d %b %Y")
        albums.append(this_album)
        this_album = {}
    return {
        "songs": songs,
        "albums": albums,
        "name": artist.username,
        "profile_picture": artist.profile_picture,
        "followers": len(artist.followers.all()),
        "following": len(artist.following),
        "current_user_follower": current_user in artist.followers.all(),
        "current_user_is_artist": current_user == artist,
    }, 200


@app.get("/get_liked_songs")
@auth_required("token")
@roles_accepted("creator", "general_user")
def get_liked_songs():
    liked_songs_list = current_user.liked_songs
    songs = []
    this_song = {}
    for song in liked_songs_list:
        this_song["id"] = song.id
        this_song["name"] = song.name
        this_song["artist"] = song.artist
        this_song["artist_id"] = song.creator_id
        this_song["lyrics"] = song.lyrics
        this_song["poster"] = song.poster
        this_song["audio"] = song.audio
        this_song["duration"] = song.duration
        this_song["rating"] = song.rating
        this_song["duration"] = song.duration
        this_song["date_added"] = song.date_added.strftime("%d %b %Y")
        if song.song_album != None:
            this_song["album"] = song.song_album.name
            this_song["album_id"] = song.song_album.id
        else:
            this_song["album"] = None
            this_song["album_id"] = None
        songs.append(this_song)
        this_song = {}
    return songs, 200


@app.get("/current_creator_details")
@auth_required("token")
@roles_accepted("creator", "general_user")
def current_creator_details():
    albums = []
    songs = []
    all_songs = Song.query.filter_by(creator_id=current_user.id).all()
    all_albums = Album.query.filter_by(creator_id=current_user.id).all()
    for song in all_songs:
        if song.song_album == None:
            album_name = None
            album_id = None
        else:
            album_name = song.song_album.name
            album_id = song.song_album.id
        songs.append(
            {
                "id": song.id,
                "name": song.name,
                "poster": song.poster,
                "audio": song.audio,
                "duration": song.duration,
                "rating": song.rating,
                "date_added": song.date_added,
                "album": album_name,
                "album_id": album_id,
            }
        )
    for album in all_albums:
        albums.append(
            {
                "id": album.id,
                "name": album.name,
                "poster": album.poster,
                "date_added": album.date_added,
            }
        )
    return {
        "id": current_user.id,
        "name": current_user.username,
        "rating": current_user.rating,
        "songs": songs,
        "albums": albums,
        "followers": current_user.followers.all(),
    }, 200


@app.get("/update_role")
@auth_required("token")
@roles_required("general_user")
def update_role():
    creator_role = Role.query.filter_by(id=2).first()
    current_user.roles = [creator_role]
    db.session.commit()
    return {"message": "Role updated succesfully!"}, 200


@app.get("/new_releases")
@auth_required("token")
@roles_accepted("creator", "general_user")
def new_releases():
    fifteen_days_ago = datetime.now() - timedelta(days=15)
    recent_songs = Song.query.filter(Song.date_added >= fifteen_days_ago).all()
    songs = []
    this_song = {}
    for song in recent_songs:
        this_song["id"] = song.id
        this_song["name"] = song.name
        this_song["artist"] = song.artist
        this_song["artist_id"] = song.creator_id
        this_song["lyrics"] = song.lyrics
        this_song["poster"] = song.poster
        this_song["audio"] = song.audio
        this_song["duration"] = song.duration
        this_song["rating"] = song.rating
        this_song["duration"] = song.duration
        this_song["date_added"] = song.date_added.strftime("%d %b %Y")
        if song.song_album != None:
            this_song["album"] = song.song_album.name
            this_song["album_id"] = song.song_album.id
        else:
            this_song["album"] = None
            this_song["album_id"] = None
        songs.append(this_song)
        this_song = {}
    return songs, 200


@app.post("/search")
@auth_required("token")
@roles_accepted("creator", "general_user", "admin")
def search():
    data = request.get_json()
    string = data.get("query")
    query = "%" + str(string) + "%"
    song_result = Song.query.filter(
        or_(Song.name.ilike(query), Song.genre.ilike(query))
    ).all()
    artist_result = (
        User.query.join(User.roles)
        .filter(Role.id == 2)
        .filter(User.username.ilike(query))
        .order_by(desc(User.rating))
        .all()
    )
    album_result = Album.query.filter(
        or_(Album.name.ilike(query), Album.genre.ilike(query))
    ).all()
    songs = [
        {
            "id": song.id,
            "name": song.name,
            "artist": song.artist,
            "poster": song.poster,
            "genre": song.genre,
            "duration": song.duration,
            "date_added": song.date_added.strftime("%d %b %Y"),
        }
        for song in song_result
    ]
    albums = [
        {
            "id": album.id,
            "name": album.name,
            "artist": album.artist,
            "poster": album.poster,
            "genre": album.genre,
            "date_added": album.date_added.strftime("%d %b %Y"),
        }
        for album in album_result
    ]
    artists = [
        {
            "id": artist.id,
            "name": artist.username,
            "poster": artist.profile_picture,
            "rating": artist.rating,
            "blacklisted": artist.blacklisted,
        }
        for artist in artist_result
    ]
    return {"songs": songs, "albums": albums, "artists": artists}, 200


@app.get("/logout")
@auth_required("token")
def log_out():
    logout_user()
    return {"message": "Logged out successfully!"}, 200


def gen_ratings_graph(ratings_list):
    plt.clf()
    bins = [1, 2, 3, 4, 5]
    plt.hist(ratings_list, bins=bins, color="#304674", edgecolor="white")
    plt.xlabel("Rating")
    plt.ylabel("Songs")
    plt.title("Song Ratings")
    plt.tight_layout()
    plt.savefig(os.path.join(upload_folder_graphs, "ratings.png"))
    plt.show()
    return "ratings.png"


def gen_song_uploads_graph(dates, songs_list):
    plt.clf()
    plt.plot_date(dates, songs_list, linestyle="solid")
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(os.path.join(upload_folder_graphs, "songs_upload.png"))
    return "songs_upload.png"


@app.get("/admin_dashboard")
@auth_required("token")
@roles_required("admin")
def admin_dashboard():
    songs = Song.query.all()
    user_count = len(User.query.join(User.roles).filter(Role.id == 3).all())
    creator_count = len(User.query.join(User.roles).filter(Role.id == 2).all())
    song_count = len(Song.query.all())
    album_count = len(Album.query.all())
    total_streams = db.session.query(func.sum(Song.played)).scalar()
    most_played = Song.query.order_by(desc(Song.played)).first()
    most_played_song = most_played.name
    most_played_count = most_played.played
    ratings_list = [song.rating for song in songs]
    today = datetime.now().date()
    songs_upload_dict = {}
    for i in range(1, 16):
        past_day = today - timedelta(days=i)
        songs_upload_dict[past_day] = 0
    for song in songs:
        if song.date_added in songs_upload_dict.keys():
            songs_upload_dict[song.date_added] += 1
    songs_upload_graph = gen_song_uploads_graph(
        dates=songs_upload_dict.keys(), songs_list=songs_upload_dict.values()
    )
    ratings_graph = gen_ratings_graph(ratings_list)
    return {
        "user_count": user_count,
        "album_count": album_count,
        "creator_count": creator_count,
        "song_count": song_count,
        "total_streams": total_streams,
        "most_played_song": most_played_song,
        "most_played_count": most_played_count,
        "ratings_graph": ratings_graph,
        "songs_upload_graph": songs_upload_graph,
    }, 200


@app.post("/blacklist/<id>")
@auth_required("token")
@roles_required("admin")
def blacklist(id):
    creator = User.query.filter_by(id=id).first()
    creator.blacklisted = not creator.blacklisted
    db.session.commit()
    return {"message": "Operation succesfull!"}, 200


@app.post("/flag/<option>/<id>")
@auth_required("token")
@roles_accepted("creator", "general_user")
def flag(option, id):
    if option == "song":
        song = Song.query.filter_by(id=id).first()
        if song in current_user.flagged_songs:
            current_user.flagged_songs.remove(song)
            db.session.commit()
        elif song not in current_user.flagged_songs:
            current_user.flagged_songs.append(song)
            db.session.commit()
        if len(song.song_flagged_by) > 20:
            db.session.remove(song)
            db.session.commit()
    if option == "album":
        album = Album.query.filter_by(id=id).first()
        if album in current_user.flagged_albums:
            current_user.flagged_albums.remove(album)
            db.session.commit()
        else:
            current_user.flagged_albums.append(album)
            db.session.commit()
        if len(album.album_flagged_by) > 20:
            db.session.remove(album)
            db.session.commit()
    return {"message": "Operation succesful!"}, 200


@app.post("/follow/<id>")
@auth_required
@roles_accepted("creator", "general_user")
def follow(id):
    artist = User.query.filter_by(id=id).first()
    followers = artist.followers
    if current_user not in followers:
        followers.append(current_user)
        db.session.commit()
    else:
        followers.remove(current_user)
        db.session.commit()
    return {"message": "Operation succesful!"}, 200


@app.get("/following_artists")
@auth_required
@roles_accepted("creator", "general_user")
def following_artists():
    following = current_user.following
    artists = []
    this_artist = {}
    for artist in following:
        this_artist["id"] = artist.id
        this_artist["name"] = artist.username
        this_artist["rating"] = artist.rating
        this_artist["profile_picture"] = artist.profile_picture
        this_artist["blacklisted"] = artist.blacklisted
        artists.append(this_artist)
        this_artist = {}
    return artists, 200


@app.route("/profile", methods=["GET", "POST"])
@auth_required
@roles_accepted("creator", "general_user")
def profile():
    user = current_user
    if request.method == "GET":
        return {
            "name": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture,
        }, 200
    if request.method == "POST":
        if "name" in request.form:
            name = request.form.get("name")
            user.username = name
            db.session.commit()
            return {"message": "Changed"}, 200
        if "email" in request.form:
            email = request.form.get("email")
            emails = [user.email for user in User.query.all()]
            if email not in emails:
                user.email = email
                db.session.commit()
                return {"message": "Changed"}, 200
            else:
                return {"message": "Email already exists!"}, 404
        if "profile_picture" in request.files:
            profile_pic = request.files["profile_picture"]
            profile_pic_name = f"{uuid.uuid4().hex}_{profile_pic.filename}"
            profile_pic_path = os.path.join(upload_folder_profile_pic, profile_pic_name)
            profile_pic.save(profile_pic_path)
            user.profile_picture = profile_pic_name
            db.session.commit()
            return {"message": "Changed"}, 200
