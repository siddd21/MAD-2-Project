<template>
    <div class="container content">
        <div class="row d-flex justify-content-around">
            <div class="d-flex">
                <img :src="require(`@/assets/album_posters/${albumPoster}`)" :alt="name"
                    class="rounded-circle profile-pic" />
                <div>
                    <p class="fs-1 fw-bolder m-2">{{ albumName }}</p>
                    <p class="ms-2">By {{albumArtist}}</p>
                </div>
            </div>
        </div>
        <hr />
        <div>
            <b-table-simple sticky-header="50vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Title</b-th>
                        <b-th>Date Added </b-th>
                        <b-th><i class="fa-regular fa-clock fw-bold"></i></b-th>
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
                            {{ song.date_added.slice(4, 16) }}
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
    name: 'Album',
    props: ['id'],
    data() {
        return {
            songsData: null,
            token: null,
            albumName: null,
            albumPoster: null,
            albumArtist: null,

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
            axios.get(`http://127.0.0.1:5000/get_album/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songsData = response.data.songs
                    this.albumName = response.data.name
                    this.albumPoster = response.data.poster
                    this.albumArtist = response.data.artist
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
    }
}
</script>

<style scoped>
.table-wrapper {
    max-height: 400px;
    /* Set a maximum height to enable scrolling */
    overflow-y: auto;
    /* Enable vertical scrolling */
}

.table-fixed thead {
    position: sticky;
    top: 0;
    z-index: 1;
    /* Ensure the header is above other content */
    background-color: #fff;
    /* Optionally set background color */
}
</style>