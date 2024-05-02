<template>
    <div class="content">
        <div v-if="!loaded" class="d-flex flex-column align-items-center justify-content-center mb-3" style="height:90vh">
            <b-spinner label="Loading..."></b-spinner>
        </div>
        <div v-else class="mx-3 my-2">
            <div class="row">
                <div class="col-3 d-flex flex-column justify-content-between">
                    <div class="text-center bg-secondary bg-gradient rounded text-dark mb-3">
                        <p style="font-size: 100px">{{ userCount + creatorCount }}</p>
                        <h5>Total Users</h5>
                    </div>
                    <div class="text-center bg-secondary bg-gradient rounded mb-3">
                        <router-link :to="{ name: 'adminCreators' }"
                            class="link-dark link-offset-2 link-underline link-underline-opacity-0">
                            <p style="font-size: 100px">{{ creatorCount }}</p>
                            <div class="d-flex flex-row justify-content-between">
                                <h5></h5>
                                <h5>Creators</h5>
                                <b-icon class="pe-2" icon="arrow-right" font-scale="2"></b-icon>
                            </div>
                        </router-link>
                    </div>
                    <div class="text-center bg-secondary bg-gradient rounded text-dark">
                        <p style="font-size: 100px">{{ userCount }}</p>
                        <h5>General Users</h5>
                    </div>
                </div>
                <div class="col-9">
                    <div class="d-flex justify-content-around">
                        <div class="text-center bg-secondary bg-gradient rounded text-dark"
                            style="height: 200px; width: 300px">
                            <router-link :to="{ name: 'adminSongs' }"
                                class="link-dark link-offset-2 link-underline link-underline-opacity-0">
                                <p style="font-size: 100px">{{ songCount }}</p>
                                <div class="d-flex flex-row justify-content-between">
                                    <h6></h6>
                                    <h6 class="mb-auto">Total Songs</h6>
                                    <b-icon class="pe-2" icon="arrow-right" font-scale="2"></b-icon>
                                </div>
                            </router-link>
                        </div>
                        <div class="text-center bg-secondary bg-gradient rounded text-dark"
                            style="height: 200px; width: 300px">
                            <router-link :to="{ name: 'adminAlbums' }"
                                class="link-dark link-offset-2 link-underline link-underline-opacity-0">
                                <p style="font-size: 100px">{{ albumCount }}</p>
                                <div class="d-flex flex-row justify-content-between">
                                    <h6></h6>
                                    <h6 class="mb-auto">Total Albums</h6>
                                    <b-icon class="pe-2" icon="arrow-right" font-scale="2"></b-icon>
                                </div>
                            </router-link>
                        </div>
                        <div class="d-flex flex-column justify-content-between" style="height: 200px; width: 300px">
                            <div class="d-flex bg-secondary bg-gradient rounded text-dark justify-content-around"
                                style="height: 90px; width: 300px">
                                <p style="font-size: 50px" class="ms-2">{{ totalStreams }}</p>
                                <p style="font-size: 30px" class="mt-3 me-3">Total Streams</p>
                            </div>
                            <div class="bg-secondary bg-gradient rounded text-dark justify-content-around text-center"
                                style="height: 90px; width: 300px">
                                MOST PLAYED SONG
                                <p class="text-center text-uppercase" style="font-size: 40px">
                                    {{ mostPlayedSong }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-around mt-3">
                        <div class="">
                            <img :src="require(`@/assets/graphs/${ratingsGraph}`)" alt="Ratings garph"
                                style="height: 375px; width: 500px; border: 2px solid black" class="rounded" />
                        </div>
                        <div class="">
                            <img :src="require(`@/assets/graphs/${songsUploadGraph}`)" alt="Genre graph"
                                style="height: 375px; width: 500px; border: 2px solid black" class="rounded" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
export default {
    name: 'adminDashboard',
    data() {
        return {
            loaded: false,
            hover: true,
            token: null,
            userCount: null,
            creatorCount: null,
            songCount: null,
            albumCount: null,
            totalStreams: null,
            mostPlayedSong: null,
            mostPlayedCount: null,
            ratingsGraph: null,
            songsUploadGraph: null,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (!this.token) {
            this.$router.push('/token')
        } else {
            this.getDetails()
        }
    },
    methods: {
        getDetails() {
            axios.get(`http://127.0.0.1:5000/admin_dashboard`, {
                headers: {
                    'Authentication-Token': this.token,
                }
            }).then(response => {
                let data = response.data
                console.log(data.ratings_chart)
                this.userCount = data.user_count
                this.creatorCount = data.creator_count
                this.songCount = data.song_count
                this.albumCount = data.album_count
                this.totalStreams = data.total_streams
                this.mostPlayedCount = data.most_played_count
                this.mostPlayedSong = data.most_played_song
                this.ratingsGraph = data.ratings_graph
                this.songsUploadGraph = data.songs_upload_graph
                this.loaded = true
                console.log(this.ratingsGraph)
                console.log(this.songsUploadGraph)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>