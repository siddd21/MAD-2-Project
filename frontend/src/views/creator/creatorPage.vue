<template>
    <div class="content" style="margin-top: 100px">
        <div v-if="role !== 'creator'" class="content">
            <h1 class="text-center">Wanna be a creator?</h1>
            <br />
            <div class="text-center">
                <button @click="updateRole" class="btn text-center bg-dark text-white btn-lg">
                    Click here
                </button>
            </div>
        </div>
        <div v-else class="mx-5">
            <div class="row d-flex justify-content-between">
                <div class="col-2 text-center rounded text-white bg-dark bg-gradient">
                    <router-link :to="{ name: 'creatorSongs' }"
                        class="link-light link-offset-2 link-underline link-underline-opacity-0">
                        <p style="font-size: 100px">{{ songsData.length }}</p>
                        <h5>Songs Uploaded</h5>
                    </router-link>
                </div>
                <div class="col-2 text-center text-white rounded bg-dark bg-gradient">
                    <p style="font-size: 100px">{{ rating }}</p>
                    <h5>Average Rating</h5>
                </div>
                <div class="col-2 text-center rounded bg-dark bg-gradient">
                    <router-link :to="{ name: 'creatorAlbums' }"
                        class="link-light link-offset-2 link-underline link-underline-opacity-0">
                        <p style="font-size: 100px">{{ albumsData.length }}</p>
                        <h5>Albums Uploaded</h5>
                    </router-link>
                </div>
                <div class="col-2 text-center text-white rounded bg-dark bg-gradient">
                    <p style="font-size: 100px">{{ followers.length }}</p>
                    <h5>Followers</h5>
                </div>
            </div>
            <hr />
            <div v-if="songsData.length !== 0">
                <h4 class="text-center">Your Songs</h4>
                <div class="songs-container">
                    <b-table-simple sticky-header="270px">
                        <b-tbody>
                            <b-tr v-for="song in songsData" :key="song.id">
                                <b-td></b-td>
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
                                <b-td>{{ song.rating }} <i class="fa-solid fa-star"></i></b-td>
                            </b-tr>
                        </b-tbody>
                    </b-table-simple>
                </div>
                <router-link :to="{ name: 'uploadSong' }" class="btn btn-dark pill m-1">Upload Song</router-link>
                <router-link :to="{ name: 'createAlbum' }" class="btn btn-dark pill m-1">Create Album</router-link>
            </div>
            <div v-else class="text-center">
                <h4 class="text-center">You haven't uploaded any songs yet!</h4>
                <router-link :to="{ name: 'uploadSong' }" class="btn btn-dark">Click here to Upload!</router-link>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'creatorPage',
    data() {
        return {
            role: null,
            token: null,
            songsData: [],
            albumsData: [],
            followers: [],
            rating: null,
            id: null,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (!this.token) {
            this.$router.push('/login')
        } else {
            this.getDetails()
        }
    },
    methods: {
        getDetails() {
            axios.get('http://127.0.0.1:5000/current_creator_details', {
                headers: {
                    'Authentication-Token': this.token
                }
            }).then(response => {
                this.songsData = response.data.songs
                this.albumsData = response.data.albums
                this.followers = response.data.followers
                this.rating = response.data.rating
                this.id = response.data.id
            }).catch(error => {
                console.log(error)
            })
        },
        updateRole() {
            axios.get(`http://127.0.0.1:5000/update_role`, {
                headers: {
                    'Authentication-Token': this.token
                },
            }).then(response => {
                console.log(response)
                localStorage.setItem('user-role', 'creator')
                this.$bvModal.msgBoxOk(`You are now a creator!`, {
                    size: 'sm',
                    buttonSize: 'sm',
                    okVariant: 'success',
                    headerClass: 'p-2 border-bottom-0',
                    footerClass: 'p-2 border-top-0',
                    centered: true,
                    noCloseOnBackdrop: true,
                    hideHeaderClose: true,
                })
                    .then(() => {
                        window.location.reload()
                    })
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>

<style scoped>
.pill {
    border-radius: 23px;
}
</style>