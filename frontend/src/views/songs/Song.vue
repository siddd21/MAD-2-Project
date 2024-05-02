<template>
    <div v-if="loading">
        Loading...
    </div>
    <div v-else class="content container">
        <div class="row">
            <div class="col-md-6">
                <div class="song-poster">
                    <img v-if="poster" :src="require(`@/assets/posters/${poster}`)" alt="Song Poster" class="rounded" />
                    <h3>{{ name }}</h3>
                    <p>{{ artist }}</p>
                </div>
                <div class="flex-row d-flex justify-content-between">
                    <i :class="{
        'fa-solid': isLiked,
        'fa-regular': !isLiked
    }" class="fa-heart clickable" @click="like"></i>
                    <b-form-rating no-border inline v-model="rating" @change="rateSong"></b-form-rating>
                </div>
            </div>
            <div class="col-md-6">
                <div class="lyrics-container">
                    <div class="lyrics">
                        <div v-for="(lyric, index) in lyricsLines" :key="index">
                            {{ lyric }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="audio">
            <audio controls class="player">
                <source :src="require(`@/assets/audios/${audio}`)" type="audio/wav" />
            </audio>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    name: "Song",
    props: ['id'],
    data() {
        return {
            loading: true,
            name: null,
            audio: null,
            poster: null,
            lyrics: null,
            token: null,
            artist: null,
            rating: 0,
            isLiked: null,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (this.token) {
            // this.getAlbums()
        }
        else {
            this.$router.push('/login')
        }
    },
    mounted() {
        axios.get(`http://127.0.0.1:5000/get_song/${this.id}`, {
            headers: {
                'Authentication-Token': `${this.token}`
            }
        })
            .then(response => {
                console.log(response.data)
                this.name = response.data.name
                this.artist = response.data.artist
                this.audio = response.data.audio
                this.poster = response.data.poster
                this.lyrics = response.data.lyrics
                this.isLiked = response.data.liked
                this.rating = response.data.rating
                console.log(this.rating)
                this.loading = false
            })
            .catch(error => {
                this.loading = false
                console.log(error)
            })
    },
    computed: {
        lyricsLines() {
            if (this.lyrics) {
                return this.lyrics.split('\n')
            }
            return []
        }
    },
    methods: {
        like() {
            this.isLiked = !this.isLiked
            axios.get(`http://127.0.0.1:5000/like_song/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`
                }
            })
        },
        rateSong() {
            console.log("triggered")
            axios.post(`http://127.0.0.1:5000/rate_song/${this.id}`, {
                rating: this.rating
            }, {
                headers: {
                    'Authentication-Token': `${this.token}`
                }
            })
        }
    },
}
</script>
