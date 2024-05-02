<template>
    <div class="container content">
        <div v-if="songsData.length === 0" class="d-flex flex-column justify-content-center align-items-center">
            <div class="text-center">
                <p class="fs-2 fw-bold">You haven't liked any songs yet!</p>
                <router-link :to="{ name: 'allSongs' }">Click to listen to songs!</router-link>
            </div>
        </div>
        <div v-else>
            <b-table-simple sticky-header="85vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Title</b-th>
                        <b-th>Artist</b-th>
                        <b-th>Album</b-th>
                        <b-th>Date Added</b-th>
                        <b-th>Unlike</b-th>
                        <b-th><i class="fa-solid fa-lg fa-clock"></i></b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="(song, index) in  songsData  " :key="song.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/posters/${song.poster}`)" class="rounded table-image" />
                            <router-link :to="{ name: 'Song', params: { id: song.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ song.name }}
                            </router-link>
                        </b-td>
                        <b-td>
                            <router-link :to="{ name: 'Artist', params: { id: song.artist_id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ song.artist }}
                            </router-link>
                        </b-td>
                        <b-td v-if="song.album != null">
                            <router-link :to="{ name: 'Album', params: { id: song.album_id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ song.album }}
                            </router-link>
                        </b-td>
                        <b-td v-else>-</b-td>
                        <b-td>
                            {{ song.date_added }}
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-lg fa-trash-can clickable" title="Remove from liked songs"
                                @click="removeSong(song.id)"></i>
                        </b-td>
                        <b-td>
                            {{ secondsToMin(song.duration) }}
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'likedSongs',
    data() {
        return {
            songsData: [],
            token: null,

        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (this.token) {
            this.getSongs()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSongs() {
            axios.get('http://127.0.0.1:5000/get_liked_songs', {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songsData = response.data
                    console.log(this.songsData)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        secondsToMin(seconds) {
            if (parseInt(seconds) < 60) {
                let second = seconds.toString().split('.')
                return `0:${second[0]}`
            } else {
                let x = (seconds / 60).toString().split('.')
                let minutes = x[0]
                let s = `0.${x[1]}`
                let second = Math.round(s * 60)
                if (second.toString().length == 1) {
                    let zero = `0${second}`
                    second = zero
                }
                return `${minutes}:${second}`

            }
        },
        removeSong(songId) {
            axios.get(`http://127.0.0.1:5000/like_song/${songId}`, {
                headers: {
                    'Authentication-Token': this.token
                }
            }).then(value => {
                if (value) {
                    window.location.reload()
                }
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>

<style scoped>

</style>