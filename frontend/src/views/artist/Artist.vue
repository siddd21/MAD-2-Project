<template>
    <div class="container content">
        <div class="row d-flex justify-content-around">
            <div class="d-flex">
                <img :src="require(`@/assets/profile_pictures/${profilePicture}`)" :alt="name"
                    class="rounded-circle profile-pic" />
                <div>
                    <p class="fs-1 fw-bolder m-2">{{ name }}</p>
                    <p>&nbsp; {{ followers }} Followers | {{ following }} Following</p>
                    <div v-show="!currentUserIsArtist">
                        <button v-if="currentUserFollower" id="following" @click="follow" type="button"
                            class="btn btn-primary" style="width:170px"><i class="fa-solid fa-check"></i>
                            Following</button>
                        <button v-else @click="follow" type="button" class="btn btn-primary"
                            style="width:170px">Follow</button>
                        <b-tooltip target="following" noninteractive>Unfollow</b-tooltip>
                    </div>
                </div>
            </div>
        </div>
        <hr />
        <b-tabs content-class="mt-3">
            <b-tab title="Songs" active>
                <div>
                    <b-table-simple responsive sticky-header="50vh">
                        <b-thead>
                            <b-tr>
                                <b-th>#</b-th>
                                <b-th>Title</b-th>
                                <b-th>Album</b-th>
                                <b-th>Rating</b-th>
                                <b-th>Date Added</b-th>
                                <b-th><i class="fa-solid fa-lg fa-clock"></i></b-th>
                            </b-tr>
                        </b-thead>
                        <b-tbody>
                            <b-tr v-for="( song, index ) in   songsData   " :key="song.id">
                                <b-td>{{ index + 1 }}</b-td>
                                <b-td>
                                    <img :src="require(`@/assets/posters/${song.poster}`)"
                                        class="rounded table-image" />
                                    <router-link :to="{ name: 'Song', params: { id: song.id } }"
                                        class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                        {{ song.name }}
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
                                    {{ song.rating }} <i class="fa-solid fa-star"></i>
                                </b-td>
                                <b-td>
                                    {{ song.date_added }}
                                </b-td>
                                <b-td>
                                    {{ secondsToMin(song.duration) }}
                                </b-td>
                            </b-tr>
                        </b-tbody>
                    </b-table-simple>
                </div>

            </b-tab>
            <b-tab title="Albums">
                <div>
                    <b-table-simple responsive sticky-header="50vh">
                        <b-thead>
                            <b-tr>
                                <b-th>#</b-th>
                                <b-th>Title</b-th>
                                <b-th>Rating</b-th>
                                <b-th>Date Added</b-th>
                            </b-tr>
                        </b-thead>
                        <b-tbody>
                            <b-tr v-for="( album, index ) in   albumsData   " :key="album.id">
                                <b-td>{{ index + 1 }}</b-td>
                                <b-td>
                                    <img :src="require(`@/assets/album_posters/${album.poster}`)"
                                        class="rounded table-image" />
                                    <router-link :to="{ name: 'Album', params: { id: album.id } }"
                                        class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                        {{ album.name }}
                                    </router-link>
                                </b-td>
                                <b-td>
                                    {{ album.rating }} <i class="fa-solid fa-star"></i>
                                </b-td>
                                <b-td>
                                    {{ album.date_added }}
                                </b-td>
                            </b-tr>
                        </b-tbody>
                    </b-table-simple>
                </div>
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Artist',
    props: ['id'],
    data() {
        return {
            songsData: [],
            albumsData: [],
            token: null,
            name: null,
            profilePicture: null,
            followers: null,
            following: null,
            currentUserFollower: false,
            currentUserIsArtist: true,

        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (this.token) {
            this.getArtistDetails()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getArtistDetails() {
            axios.get(`http://127.0.0.1:5000/get_artist_details/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songsData = response.data.songs
                    this.albumsData = response.data.albums
                    this.name = response.data.name
                    this.followers = response.data.followers
                    this.following = response.data.following
                    this.currentUserFollower = response.data.current_user_follower
                    this.currentUserIsArtist = response.data.current_user_is_artist
                    this.profilePicture = response.data.profile_picture
                    console.log(response.data)
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
        follow() {
            axios.post(`http://127.0.0.1:5000/follow/${this.id}`, {}, {
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