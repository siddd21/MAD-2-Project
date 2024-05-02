import Vue from "vue";
import VueRouter from "vue-router";
import Welcome from "../views/initialPages/Welcome.vue";
import Login from "../views/initialPages/Login.vue";
import Register from "../views/initialPages/Register.vue";
import Home from "../views/Home.vue";
import uploadSong from "../views/songs/uploadSong.vue";
import creatorSongs from "../views/creator/creatorSongs.vue";
import Song from "../views/songs/Song.vue";
import updateSong from "../views/songs/updateSong.vue";
import allSongs from "../views/songs/allSongs.vue";
import createAlbum from "../views/albums/createAlbum.vue";
import creatorAlbums from "../views/creator/creatorAlbums.vue";
import creatorAlbum from "../views/creator/creatorAlbum.vue";
import Album from "../views/albums/Album.vue";
import allAlbums from "../views/albums/allAlbums.vue";
import createPlaylist from "../views/playlists/createPlaylist.vue";
import userPlaylists from "../views/playlists/userPlaylists.vue";
import Playlist from "../views/playlists/Playlist.vue";
import allArtists from "../views/artist/allArtists.vue";
import Artist from "../views/artist/Artist.vue";
import followingArtists from "../views/artist/followingArtists.vue";
import creatorPage from "../views/creator/creatorPage.vue";
import newReleases from "../views/songs/newReleases.vue";
import likedSongs from "../views/songs/likedSongs.vue";
import Profile from "../views/Profile.vue";
import searchPage from "../views/searchPage.vue";
import adminDashboard from "../views/admin/adminDashboard.vue";
import adminSongs from "../views/admin/adminSongs.vue";
import adminAlbums from "../views/admin/adminAlbums.vue";
import adminCreators from "../views/admin/adminCreators.vue";
import adminSearch from "../views/admin/adminSearch.vue";
import blacklistPage from "../views/blacklistPage.vue";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
  {
    path: "/upload_song",
    name: "uploadSong",
    component: uploadSong,
  },
  {
    path: "/creator_songs",
    name: "creatorSongs",
    component: creatorSongs,
  },
  {
    path: "/song/:id",
    name: "Song",
    component: Song,
    props: true,
  },
  {
    path: "/update_song/:id",
    name: "updateSong",
    component: updateSong,
    props: true,
  },
  {
    path: "/all_songs/",
    name: "allSongs",
    component: allSongs,
  },
  {
    path: "/create_album",
    name: "createAlbum",
    component: createAlbum,
  },
  {
    path: "/creator_albums",
    name: "creatorAlbums",
    component: creatorAlbums,
  },
  {
    path: "/creator_album/:id",
    name: "creatorAlbum",
    component: creatorAlbum,
    props: true,
  },
  {
    path: "/album/:id",
    name: "Album",
    component: Album,
    props: true,
  },
  {
    path: "/all_albums",
    name: "allAlbums",
    component: allAlbums,
    props: true,
  },
  {
    path: "/create_playlist",
    name: "createPlaylist",
    component: createPlaylist,
  },
  {
    path: "/user_playlists",
    name: "userPlaylists",
    component: userPlaylists,
  },
  {
    path: "/playlist/:id",
    name: "Playlist",
    component: Playlist,
    props: true,
  },
  {
    path: "/artist/:id",
    name: "Artist",
    component: Artist,
    props: true,
  },
  {
    path: "/all_artists",
    name: "allArtists",
    component: allArtists,
  },
  {
    path: "/following_artists",
    name: "followingArtists",
    component: followingArtists,
  },
  {
    path: "/new_releases",
    name: "newReleases",
    component: newReleases,
  },
  {
    path: "/liked_songs",
    name: "likedSongs",
    component: likedSongs,
  },
  {
    path: "/creator_page",
    name: "creatorPage",
    component: creatorPage,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/search_page/:query",
    name: "searchPage",
    component: searchPage,
    props: true,
  },
  {
    path: "/admin_dashboard",
    name: "adminDashboard",
    component: adminDashboard,
  },
  {
    path: "/admin_songs",
    name: "adminSongs",
    component: adminSongs,
  },
  {
    path: "/admin_albums",
    name: "adminAlbums",
    component: adminAlbums,
  },
  {
    path: "/admin_creators",
    name: "adminCreators",
    component: adminCreators,
  },
  {
    path: "/admin_search/:query",
    name: "adminSearch",
    component: adminSearch,
    props: true,
  },
  {
    path: "/blacklist_page",
    name: "blacklistPage",
    component: blacklistPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
