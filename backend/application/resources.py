import os
import werkzeug
from flask import request
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_security import (
    auth_required,
    roles_required,
    current_user,
    roles_accepted,
)
from sqlalchemy import *
from pydub import AudioSegment
import wave
import uuid
from .models import *
from .instances import cache

current_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(current_dir, "..", "frontend", "src")
mp3_dir = os.path.join(current_dir, "..", "backend")
# base_dir = "/home/sidd/STUDY/MAD-2/Project/frontend/src"
# mp3_dir = "/home/sidd/STUDY/MAD-2/Project/backend/"
upload_folder_mp3 = os.path.join(mp3_dir, "static", "mp3_files")
upload_folder_audios = os.path.join(base_dir, "assets", "audios")
upload_folder_posters = os.path.join(base_dir, "assets", "posters")
upload_folder_album_posters = os.path.join(base_dir, "assets", "album_posters")


api = Api(prefix="/api")
parser = reqparse.RequestParser()

parser.add_argument(
    "name", type=str, help="Song name is required and should be a string", required=True
)
parser.add_argument(
    "lyrics", type=str, help="Lyrics is required and should be a string", required=True
)
parser.add_argument(
    "genre", type=str, help="Genre is required and should be a string", required=True
)
parser.add_argument(
    "audio",
    type=werkzeug.datastructures.FileStorage,
    location="files",
    help="Audio file is required",
    required=True,
    dest="audio",
)


song_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "artist": fields.String,
    "lyrics": fields.String,
    "poster": fields.String,
    "genre": fields.String,
    "audio": fields.String,
    "duration": fields.Integer,
    "rating": fields.Integer,
    "date_added": fields.DateTime,
    "song_album": fields.String,
}


def audio_duration(file_path):
    with wave.open(file_path, "r") as audio_file:
        frame_rate = audio_file.getframerate()
        n_frames = audio_file.getnframes()
        duration = n_frames / float(frame_rate)
        return duration


class Songs(Resource):
    @auth_required("token")
    # @cache.cached(timeout=60)
    @roles_accepted("creator", "general_user", "admin")
    def get(self):
        all_songs = Song.query.order_by(desc(Song.rating)).all()
        songs = []
        this_song = {}
        for song in all_songs:
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
            if song in current_user.flagged_songs:
                this_song["flagged"] = True
            else:
                this_song["flagged"] = False
            if song.song_album != None:
                this_song["album"] = song.song_album.name
                this_song["album_id"] = song.song_album.id
            else:
                this_song["album"] = None
                this_song["album_id"] = None
            songs.append(this_song)
            this_song = {}
        return songs, 200

    @auth_required("token")
    @roles_required("creator")
    def post(self):
        audio = request.files["audio"]
        poster = request.files["poster"]
        genres = list(set(request.form.getlist("genres")))
        destination = ""
        audio_name = "nothing found"
        if audio.filename.split(".")[-1] == "mp3":
            mp3_file_path = os.path.join(upload_folder_mp3, audio.filename)
            audio.save(mp3_file_path)
            source = mp3_file_path
            # audio_name = secure_filename(f"{audio.filename[0:-4]}.wav")
            audio_name = f"{uuid.uuid4().hex}_{audio.filename[0:-4]}.wav"
            destination = f"/home/sidd/STUDY/MAD-2/Project/frontend/src/assets/audios/{audio_name}"
            sound = AudioSegment.from_mp3(source)
            sound.export(destination, format="wav")
            os.remove(mp3_file_path)
        elif audio.filename.split(".")[-1] == "wav":
            audio_name = f"{uuid.uuid4().hex}{audio.filename}"
            audio_file_path = os.path.join(upload_folder_audios, audio_name)
            audio.save(audio_file_path)
        poster_name = f"{uuid.uuid4().hex}_{poster.filename}"
        poster_file_path = os.path.join(upload_folder_posters, poster_name)
        poster.save(poster_file_path)
        dur = audio_duration(destination)
        duration = f"{dur:.2f}"
        genre = ""
        for i in range(len(genres)):
            if i != len(genres) - 1:
                genre += f"{genres[i]},"
            else:
                genre += f"{genres[i]}"
        song = Song(
            name=request.form.get("name"),
            lyrics=request.form.get("lyrics"),
            artist=current_user.username,
            audio=audio_name,
            genre=genre,
            poster=poster_name,
            duration=duration,
            creator_id=current_user.id,
        )
        db.session.add(song)
        activity = UserActivity(user_id=current_user.id, activity_type="Song upload")
        db.session.add(activity)
        db.session.commit()
        return {
            "message": "Song created succesfully",
            "current_user": current_user.id,
        }, 200

    @auth_required("token")
    @roles_required("creator")
    def put(self, id):
        song = Song.query.filter_by(id=id).first()
        name = request.form.get("name")
        lyrics = request.form.get("lyrics")
        genres = list(set(request.form.getlist("genres")))
        genre = ""
        for i in range(len(genres)):
            if i != len(genres) - 1:
                genre += f"{genres[i]},"
            else:
                genre += f"{genres[i]}"
        if name != song.name:
            song.name = name
        if lyrics != song.lyrics:
            song.lyrics = lyrics

        if genre != song.genre:
            song.genre = genre

        if "audio" in request.files:
            audio = request.files["audio"]
            audio_name = ""
            if audio.filename.split(".")[-1] == "mp3":
                mp3_file_path = os.path.join(upload_folder_mp3, audio.filename)
                audio.save(mp3_file_path)
                source = mp3_file_path
                audio_name = f"{uuid.uuid4().hex}_{audio.filename[0:-4]}.wav"
                destination = f"/home/sidd/STUDY/MAD-2/Project/frontend/src/assets/audios/{audio_name}"
                sound = AudioSegment.from_mp3(source)
                sound.export(destination, format="wav")
                os.remove(mp3_file_path)
            elif audio.filename.split(".")[-1] == "wav":
                audio_name = f"{uuid.uuid4().hex}_{audio.filename}"
                destination = os.path.join(upload_folder_audios, audio_name)
                audio.save(destination)
            prev_audio = song.audio
            prev_audio_path = f"/home/sidd/STUDY/MAD-2/Project/frontend/src/assets/audios/{prev_audio}"
            if os.path.exists(prev_audio_path):
                os.remove(prev_audio_path)
            else:
                print("Previous audio file could not be found")
            dur = audio_duration(destination)
            duration = f"{dur:.2f}"
            song.audio = audio_name
            song.duration = duration
        if "poster" in request.files:

            poster = request.files["poster"]
            prev_poster = song.poster
            prev_poster_path = f"/home/sidd/STUDY/MAD-2/Project/frontend/src/assets/posters/{prev_poster}"
            if os.path.exists(prev_poster_path):
                os.remove(prev_poster_path)
            else:
                print("Previous poster could not be found")
            poster_name = f"{uuid.uuid4().hex}_{poster.filename}"
            poster_file_path = os.path.join(upload_folder_posters, poster_name)
            poster.save(poster_file_path)

            song.poster = poster_name
        activity = UserActivity(user_id=current_user.id, activity_type="Song update")
        db.session.add(activity)
        db.session.commit()

        return {
            "message": "Song updated successfully!",
        }, 200

    @auth_required("token")
    @roles_accepted("creator", "admin")
    def delete(self, id):
        song = Song.query.filter_by(id=id).first()

        if song:
            db.session.delete(song)
            activity = UserActivity(
                user_id=current_user.id, activity_type="Song delete"
            )
            db.session.add(activity)
            db.session.commit()

            return {
                "message": "Song deleted successfully!",
                "current_user": current_user.id,
            }, 200
        return {"message": "Song does not exist!"}, 200


api.add_resource(
    Songs, "/songs/get", "/songs/post", "/songs/put/<id>", "/songs/delete/<id>"
)


class Albums(Resource):
    # @cache.cached(timeout=60)
    @auth_required("token")
    @roles_accepted("creator", "general_user", "admin")
    def get(self):
        all_albums = Album.query.order_by(desc(Album.rating)).all()
        albums = []
        for album in all_albums:
            if album in current_user.flagged_albums:
                flag = True
            else:
                flag = False
            albums.append(
                {
                    "id": album.id,
                    "name": album.name,
                    "artist": album.artist,
                    "artist_id": album.creator_id,
                    "genre": album.genre,
                    "poster": album.poster,
                    "rating": album.rating,
                    "date_added": album.date_added.strftime("%d %b %Y"),
                    "flagged": flag,
                }
            )
        return albums, 200

    @auth_required("token")
    @roles_required("creator")
    def post(self):
        poster = request.files["poster"]
        poster_name = f"{uuid.uuid4().hex}_{poster.filename}"
        poster_file_path = os.path.join(upload_folder_album_posters, poster_name)
        poster.save(poster_file_path)
        genres = list(set(request.form.getlist("genres")))
        genre = ""
        for i in range(len(genres)):
            if i != len(genres) - 1:
                genre += f"{genres[i]},"
            else:
                genre += f"{genres[i]}"
        album = Album(
            name=request.form.get("name"),
            poster=poster_name,
            genre=genre,
            artist=current_user.username,
            creator_id=current_user.id,
        )
        db.session.add(album)
        db.session.commit()
        songs = request.form.getlist("songs")
        song_ratings = []
        for song_id in songs:
            song_obj = Song.query.filter_by(id=song_id).first()
            album.songs.append(song_obj)
            song_ratings.append(int(song_obj.rating))
        rating = round(sum(song_ratings) / len(song_ratings), 2)
        album.rating = rating
        db.session.commit()
        return {"message": "Album created!"}, 200

    @auth_required("token")
    @roles_required("creator")
    def put(self, id, string):

        album = Album.query.filter_by(id=id).first()
        if string == "data":
            genres = list(set(request.form.getlist("genres")))
            genre_list = album.genre.split(",")
            genre = album.genre
            for i in range(len(genres)):
                if genres[i] not in genre_list:
                    if i != len(genres) - 1:
                        genre += f"{genres[i]},"
                    else:
                        genre += f"{genres[i]}"
            album.genre = genre
            album.name = request.form.get("name")
            db.session.commit()
            return {"message": "Album updated succesfully!"}, 200
        elif string == "songs":
            data = request.get_json()
            songs = data.get("songs")
            for song_id in songs:
                song = Song.query.filter_by(id=song_id).first()
                album.songs.append(song)
            db.session.commit()
            return {"message": "Songs added succesfully!"}, 200

    @auth_required("token")
    @roles_accepted("creator", "admin")
    def delete(self, id):
        album = Album.query.filter_by(id=id).first()
        db.session.delete(album)
        db.session.commit()
        return {"message": "Album deleted succesfully!"}, 200


api.add_resource(
    Albums,
    "/albums/get",
    "/albums/post",
    "/albums/put/<id>/<string>",
    "/albums/delete/<id>",
)


class Playlists(Resource):
    @auth_required("token")
    @roles_accepted("creator", "general_user")
    def get(self):
        all_playlists = Playlist.query.all()
        playlists = []
        for playlist in all_playlists:
            playlists.append(
                {
                    "id": playlist.id,
                    "name": playlist.name,
                    "user_id": playlist.user_id,
                }
            )

        return playlists, 200

    @auth_required("token")
    @roles_accepted("creator", "general_user")
    def post(self):

        playlist = Playlist(name=request.form.get("name"), user_id=current_user.id)
        db.session.add(playlist)
        db.session.commit()
        songs = request.form.getlist("songs")

        for song_id in songs:
            song = Song.query.filter_by(id=song_id).first()
            playlist.songs.append(song)
        db.session.commit()
        return {"message": "Playlist created succesfully!"}

    @auth_required("token")
    @roles_accepted("creator", "general_user")
    def put(self, id, string):

        playlist = Playlist.query.filter_by(id=id).first()

        if string == "data":
            data = request.get_json()

            playlist.name = data.get("name")
            db.session.commit()
            return {"message": "Playlist updated succesfully!"}
        elif string == "songs":
            data = request.get_json()
            songs = data.get("songs")
            for song_id in songs:
                song = Song.query.filter_by(id=song_id).first()
                playlist.songs.append(song)
            db.session.commit()
            return {"message": "Songs added succesfully!"}, 200

    @auth_required("token")
    @roles_accepted("creator", "general_user")
    def delete(self, id):
        playlist = Playlist.query.filter_by(id=id).first()
        db.session.delete(playlist)
        db.session.commit()
        return {"message": "Playlist deleted succesfully!"}


api.add_resource(
    Playlists,
    "/playlists/get",
    "/playlists/post",
    "/playlists/put/<id>/<string>",
    "/playlists/delete/<id>",
)
