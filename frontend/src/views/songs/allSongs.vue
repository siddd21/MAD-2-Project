<template>
    <div class="container content">
        <b-table-simple responsive sticky-header="85vh">
            <b-thead>
                <b-tr>
                    <b-th>#</b-th>
                    <b-th>Title</b-th>
                    <b-th>Artist</b-th>
                    <b-th>Album </b-th>
                    <b-th>Date Added </b-th>
                    <b-th><i class="fa-regular fa-clock fw-bold"></i></b-th>
                    <b-th>Rating</b-th>
                    <b-th>Flag</b-th>
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
                        {{ secondsToMin(song.duration) }}
                    </b-td>
                    <b-td>{{ song.rating }} <i class="fa-solid fa-star"></i></b-td>
                    <b-td>
                        <button v-if="song.flagged" @click="flagSong(song.id)" class="btn btn-outline-success"
                            :id="'flag_button' + song.id">un-Flag</button>
                        <button v-else @click="flagSong(song.id)" class="btn btn-outline-danger"
                            :id="'flag_button' + song.id">Flag</button>
                        <b-tooltip placement="leftbottom" :target="'flag_button' + song.id" noninteractive>More than 20
                            flags will delete the song!</b-tooltip>
                    </b-td>
                </b-tr>
            </b-tbody>
        </b-table-simple>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'allSongs',
    data() {
        return {
            songsData: null,
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
            axios.get('http://127.0.0.1:5000/api/songs/get', {
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
        flagSong(songId) {
            axios.post(`http://localhost:5000/flag/song/${songId}`, {}, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            }).then(response => {
                window.location.reload()
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>

<style scoped>
.table-wrapper {
    max-height: 400px;
    overflow-y: auto;
}

.table-fixed thead {
    position: sticky;
    top: 0;
    z-index: 1;
    background-color: #fff;
}
</style>