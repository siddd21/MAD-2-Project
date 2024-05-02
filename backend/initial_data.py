from application.security import user_datastore
from application.models import *
from werkzeug.security import generate_password_hash
from main import app

with app.app_context():
    db.drop_all()
    db.create_all()
    user_datastore.find_or_create_role(name="admin", description="This is Admin")
    user_datastore.find_or_create_role(name="creator", description="This is Creator")
    user_datastore.find_or_create_role(
        name="general_user", description="This is General user"
    )
    db.session.commit()
    if not user_datastore.find_user(email="admin@email.com"):
        user_datastore.create_user(
            email="admin@email.com",
            username="admin",
            password=generate_password_hash("admin"),
            roles=["admin"],
            profile_picture="profile-icon-design-free-vector.jpg",
        )
    if not user_datastore.find_user(email="arijit@email.com"):
        user_datastore.create_user(
            email="arijit@email.com",
            username="Arijit",
            password=generate_password_hash("arijit"),
            roles=["creator"],
            profile_picture="arijit.jpg",
        )
    if not user_datastore.find_user(email="ed@email.com"):
        user_datastore.create_user(
            email="ed@email.com",
            username="Ed Sheeran",
            password=generate_password_hash("ed"),
            roles=["creator"],
            profile_picture="ed.jpg",
        )
    if not user_datastore.find_user(email="mohit@email.com"):
        user_datastore.create_user(
            email="mohit@email.com",
            username="Mohit",
            password=generate_password_hash("mohit"),
            roles=["creator"],
            profile_picture="mohit.jpg",
        )
    if not user_datastore.find_user(email="taylor@email.com"):
        user_datastore.create_user(
            email="taylor@email.com",
            username="Taylor",
            password=generate_password_hash("taylor"),
            roles=["creator"],
            profile_picture="taylor.jpg",
        )
    if not user_datastore.find_user(email="louis@email.com"):
        user_datastore.create_user(
            email="louis@email.com",
            username="Louis",
            password=generate_password_hash("louis"),
            roles=["creator"],
            profile_picture="louis.jpg",
        )
    if not user_datastore.find_user(email="kk@email.com"):
        user_datastore.create_user(
            email="kk@email.com",
            username="KK",
            password=generate_password_hash("kk"),
            roles=["creator"],
            profile_picture="kk.jpg",
        )
    if not user_datastore.find_user(email="sunidhi@email.com"):
        user_datastore.create_user(
            email="sunidhi@email.com",
            username="Sunidhi",
            password=generate_password_hash("sunidhi"),
            roles=["creator"],
            profile_picture="default.jpg",
        )
    if not user_datastore.find_user(email="user1@email.com"):
        user_datastore.create_user(
            email="user1@email.com",
            username="user1",
            password=generate_password_hash("user1"),
            roles=["general_user"],
            profile_picture="default.jpg",
        )
    if not user_datastore.find_user(email="user2@email.com"):
        user_datastore.create_user(
            email="user2@email.com",
            username="user2",
            password=generate_password_hash("user2"),
            roles=["general_user"],
            profile_picture="default.jpg",
        )
    if not user_datastore.find_user(email="user3@email.com"):
        user_datastore.create_user(
            email="user3@email.com",
            username="user3",
            password=generate_password_hash("user3"),
            roles=["general_user"],
            profile_picture="default.jpg",
        )
    if not user_datastore.find_user(email="user4@email.com"):
        user_datastore.create_user(
            email="user4@email.com",
            username="user4",
            password=generate_password_hash("user4"),
            roles=["general_user"],
            profile_picture="default.jpg",
        )
    if not user_datastore.find_user(email="user5@email.com"):
        user_datastore.create_user(
            email="user5@email.com",
            username="user5",
            password=generate_password_hash("user5"),
            roles=["general_user"],
            profile_picture="default.jpg",
        )

    lyrics = """Lorem ipsum dolor sit amet consectetur, adipisicing elit. Fugiat dolorem dicta
    saepe quaerat facilis iure officiis nihil adipisci! Maxime ab enim eligendi
    rerum reiciendis animi unde recusandae ut deleniti assumenda. Lorem ipsum dolor
    sit amet consectetur adipisicing elit. Illum tenetur ab iste voluptatum totam
    inventore ex. Fuga mollitia aspernatur velit esse iste, alias aperiam neque
    libero, fugiat voluptatem, dolores minus. Lorem ipsum dolor sit amet
    consectetur, adipisicing elit. Fugiat dolorem dicta saepe quaerat facilis iure
    officiis nihil adipisci! Maxime ab enim eligendi rerum reiciendis animi unde
    recusandae ut deleniti assumenda. Lorem ipsum dolor sit amet consectetur
    adipisicing elit. Illum tenetur ab iste voluptatum totam inventore ex. Fuga
    mollitia aspernatur velit esse iste, alias aperiam neque libero, fugiat
    voluptatem, dolores minus. Lorem ipsum dolor sit amet consectetur, adipisicing
    elit. Fugiat dolorem dicta saepe quaerat facilis iure officiis nihil adipisci!
    Maxime ab enim eligendi rerum reiciendis animi unde recusandae ut deleniti
    assumenda. Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum
    tenetur ab iste voluptatum totam inventore ex. Fuga mollitia aspernatur velit
    esse iste, alias aperiam neque libero, fugiat voluptatem, dolores minus. Lorem
    ipsum dolor sit amet consectetur, adipisicing elit. Fugiat dolorem dicta saepe
    quaerat facilis iure officiis nihil adipisci! Maxime ab enim eligendi rerum
    reiciendis animi unde recusandae ut deleniti assumenda. Lorem ipsum dolor sit
    amet consectetur adipisicing elit. Illum tenetur ab iste voluptatum totam
    inventore ex. Fuga mollitia aspernatur velit esse iste, alias aperiam neque
    libero, fugiat voluptatem, dolores minus."""
    db.session.commit()
    song_1 = Song(
        name="Song-1",
        lyrics=lyrics,
        artist="Arijit",
        audio="audio-1.wav",
        poster="song-1.jpg",
        duration=100,
        creator_id=2,
        genre="Pop",
    )
    song_2 = Song(
        name="Song-2",
        lyrics=lyrics,
        artist="Arijit",
        audio="audio-2.wav",
        poster="song-2.png",
        duration=100,
        creator_id=2,
        genre="Pop",
    )
    song_3 = Song(
        name="Song-3",
        lyrics=lyrics,
        artist="Ed Sheeran",
        audio="audio-1.wav",
        poster="song-3.jpg",
        duration=100,
        creator_id=3,
        genre="Rock",
    )
    song_4 = Song(
        name="Song-4",
        lyrics=lyrics,
        artist="Ed Sheeran",
        audio="audio-2.wav",
        poster="song-4.jpg",
        duration=100,
        creator_id=3,
        genre="Rock",
    )
    song_5 = Song(
        name="Song-5",
        lyrics=lyrics,
        artist="Mohit",
        audio="audio-1.wav",
        poster="song-5.jpg",
        duration=100,
        creator_id=4,
        genre="Funk",
    )
    song_6 = Song(
        name="Song-6",
        lyrics=lyrics,
        artist="Mohit",
        audio="audio-2.wav",
        poster="song-6.jpg",
        duration=100,
        creator_id=4,
        genre="Funk",
    )
    song_7 = Song(
        name="Song-7",
        lyrics=lyrics,
        artist="Taylor",
        audio="audio-1.wav",
        poster="song-7.jpg",
        duration=100,
        creator_id=5,
        genre="Folk",
    )
    song_8 = Song(
        name="Song-8",
        lyrics=lyrics,
        artist="Taylor",
        audio="audio-2.wav",
        poster="song-8.jpg",
        duration=100,
        creator_id=5,
        genre="Folk",
    )
    song_9 = Song(
        name="Song-9",
        lyrics=lyrics,
        artist="Louis",
        audio="audio-2.wav",
        poster="song-9.jpg",
        duration=100,
        creator_id=6,
        genre="Country",
    )
    song_10 = Song(
        name="Song-10",
        lyrics=lyrics,
        artist="Louis",
        audio="audio-2.wav",
        poster="song-10.jpg",
        duration=100,
        creator_id=6,
        genre="Country",
    )
    song_11 = Song(
        name="Song-11",
        lyrics=lyrics,
        artist="KK",
        audio="audio-2.wav",
        poster="song-11.jpg",
        duration=100,
        creator_id=7,
        genre="Techno",
    )
    song_12 = Song(
        name="Song-12",
        lyrics=lyrics,
        artist="KK",
        audio="audio-1.wav",
        poster="song-12.jpg",
        duration=100,
        creator_id=7,
        genre="Techno",
    )
    song_13 = Song(
        name="Song-13",
        lyrics=lyrics,
        artist="Sunidhi",
        audio="audio-2.wav",
        poster="song-13.jpg",
        duration=100,
        creator_id=8,
        genre="Dubstep",
    )
    song_14 = Song(
        name="Song-14",
        lyrics=lyrics,
        artist="Sunidhi",
        audio="audio-1.wav",
        poster="song-14.jpg",
        duration=100,
        creator_id=8,
        genre="Dubstep",
    )
    song_15 = Song(
        name="Song-15",
        lyrics=lyrics,
        artist="Arijit",
        audio="audio-2.wav",
        poster="song-15.jpg",
        duration=100,
        creator_id=2,
        genre="Bounce",
    )
    song_16 = Song(
        name="Song-16",
        lyrics=lyrics,
        artist="Ed Sheeran",
        audio="audio-1.wav",
        poster="song-16.jpg",
        duration=100,
        creator_id=3,
        genre="Bounce",
    )
    song_17 = Song(
        name="Song-17",
        lyrics=lyrics,
        artist="Mohit",
        audio="audio-2.wav",
        poster="song-17.jpg",
        duration=100,
        creator_id=4,
        genre="Rhythm and Blues",
    )
    song_18 = Song(
        name="Song-18",
        lyrics=lyrics,
        artist="Taylor",
        audio="audio-1.wav",
        poster="song-18.jpg",
        duration=100,
        creator_id=5,
        genre="Rhythm and Blues",
    )
    song_19 = Song(
        name="Song-19",
        lyrics=lyrics,
        artist="Louis",
        audio="audio-2.wav",
        poster="song-19.jpg",
        duration=100,
        creator_id=6,
        genre="Jazz",
    )
    song_20 = Song(
        name="Song-20",
        lyrics=lyrics,
        artist="KK",
        audio="audio-2.wav",
        poster="song-20.jpg",
        duration=100,
        creator_id=7,
        genre="Jazz",
    )
    db.session.add_all(
        [
            song_1,
            song_2,
            song_3,
            song_4,
            song_5,
            song_6,
            song_7,
            song_8,
            song_9,
            song_10,
            song_11,
            song_12,
            song_13,
            song_14,
            song_15,
            song_16,
            song_17,
            song_18,
            song_19,
            song_20,
        ]
    )
    db.session.commit()
    album_1 = Album(
        name="Album-1",
        poster="album-1.jpg",
        artist="Arijit",
        genre="Pop",
        creator_id=2,
    )
    album_2 = Album(
        name="Album-2",
        poster="album-2.jpg",
        artist="Ed Sheeran",
        genre="Rock",
        creator_id=3,
    )
    album_3 = Album(
        name="Album-3",
        poster="album-3.jpg",
        artist="Mohit",
        genre="Folk",
        creator_id=4,
    )
    album_4 = Album(
        name="Album-4",
        poster="album-4.jpg",
        artist="Taylor",
        genre="Country",
        creator_id=5,
    )
    album_5 = Album(
        name="Album-5",
        poster="album-5.jpg",
        artist="Louis",
        genre="Techno",
        creator_id=6,
    )
    album_6 = Album(
        name="Album-6",
        poster="album-6.jpg",
        artist="KK",
        genre="Dubstep",
        creator_id=7,
    )
    album_7 = Album(
        name="Album-7",
        poster="album-7.jpg",
        artist="Sunidhi",
        genre="Funk",
        creator_id=8,
    )
    db.session.add_all([album_1, album_2, album_3, album_4, album_5, album_6, album_7])
    db.session.commit()
    album_1.songs.extend([song_1, song_2])
    album_2.songs.extend([song_3, song_4])
    album_3.songs.extend([song_5, song_6])
    album_4.songs.extend([song_7, song_8])
    album_5.songs.extend([song_9, song_10])
    album_6.songs.extend([song_11, song_12])
    album_7.songs.extend([song_13, song_14])
    db.session.commit()
