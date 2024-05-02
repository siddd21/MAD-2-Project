<template>
    <div v-if="loading1 || loading2 || loading3"
        class="d-flex flex-column align-items-center justify-content-center mb-3" style="height:90vh">
        <b-spinner label="Loading..."></b-spinner>
    </div>
    <div v-else class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="d-flex flex-row justify-content-between ms-2 pt-2">
                        <h3 class="fw-bolder">Top Songs</h3>
                        <router-link :to="{ name: 'allSongs' }" style="margin-right: 15px; padding-top: 5px"
                            class="link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover link-secondary fw-bolder">
                            Show more
                        </router-link>
                    </div>

                    <div class="d-flex flex-row" style="gap: 30px; margin-left: 15px; margin-right: 15px">
                        <div v-for="song in songsData" class="d-flex-flex-column">
                            <router-link :to="{ name: 'Song', params: { id: song.id } }">
                                <img :src="require(`@/assets/posters/${song.poster}`)" alt=""
                                    class="rounded song-image" />
                            </router-link>
                            <h5 class="text-center">{{ song.name }}</h5>
                            <div class="d-flex justify-content-between">
                                {{ song.artist }}
                                <span>{{ song.rating }} <i class="fa-solid fa-star"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="d-flex flex-row justify-content-between ms-2 pt-2">
                        <h3 class="fw-bolder">Top Albums</h3>
                        <router-link :to="{ name: 'allAlbums' }" style="margin-right: 15px; padding-top: 5px"
                            class="link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover link-secondary fw-bolder">
                            Show more
                        </router-link>
                    </div>

                    <div class="d-flex flex-row" style="gap: 30px; margin-left: 15px; margin-right: 15px">
                        <div v-for="album in albumsData" class="d-flex-flex-column">
                            <router-link :to="{ name: 'Album', params: { id: album.id } }">
                                <img :src="require(`@/assets/album_posters/${album.poster}`)" :alt="album.name"
                                    class="rounded song-image" />
                            </router-link>
                            <h5 class="text-center">{{ album.name }}</h5>
                            <div class="d-flex justify-content-between">
                                {{ album.artist }}
                                <span>{{ album.rating }} <i class="fa-solid fa-star"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <div class="d-flex flex-row justify-content-between ms-2 pt-2">
                        <h3 class="fw-bolder">Top Artists</h3>
                        <router-link :to="{ name: 'allArtists' }" style="margin-right: 15px; padding-top: 5px"
                            class="link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover link-secondary fw-bolder">
                            Show more
                        </router-link>
                    </div>

                    <div class="d-flex flex-row" style="gap: 30px; margin-left: 15px; margin-right: 15px">
                        <div v-for="artist in artistsData" class="d-flex-flex-column">
                            <router-link :to="{ name: 'Artist', params: { id: artist.id } }">
                                <img :src="require(`@/assets/profile_pictures/${artist.profile_picture}`)"
                                    :alt="artist.name" class="rounded-circle artist-image" />
                            </router-link>
                            <h5 class="text-center">{{ artist.name }}</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Home',
    data() {
        return {
            modal: false,
            token: null,
            songsData: [],
            albumsData: [],
            artistsData: [],
            loading1: true,
            loading2: true,
            loading3: true,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        const reload = localStorage.getItem('reload')
        if (reload == 1) {
            localStorage.setItem('reload', 0)
            window.location.reload()
        }
        if (this.token && reload == 0) {
            this.getSongs()
            this.getAlbums()
            this.getArtists()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSongs() {
            axios.get('http://127.0.0.1:5000/api/songs/get', {
                headers: {
                    'Authentication-token': `${this.token}`
                }
            }).then(response => {
                console.log(response.data)
                if (response.data.length < 7) {
                    this.songsData = response.data
                } else {
                    this.songsData = response.data.slice(0, 7)
                }
                this.loading1 = false
            })
                .catch(error => {
                    console.log(error)
                })
        },
        getAlbums() {
            axios.get('http://127.0.0.1:5000/api/albums/get', {
                headers: {
                    'Authentication-token': `${this.token}`
                }
            }).then(response => {
                console.log(response.data)
                if (response.data.length < 7) {
                    this.albumsData = response.data
                } else {
                    this.albumsData = response.data.slice(0, 7)
                }
                this.loading2 = false
            })
                .catch(error => {
                    console.log(error)
                })
        },
        getArtists() {
            axios.get('http://127.0.0.1:5000/get_artists', {
                headers: {
                    'Authentication-token': `${this.token}`
                }
            }).then(response => {
                console.log(response.data)
                if (response.data.length < 7) {
                    this.artistsData = response.data
                } else {
                    this.artistsData = response.data.slice(0, 7)
                }
                this.loading3 = false
            })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}

</script>
