<template>
    <div class="container content">
        <div class="row album-form">
            <div class="col-md-6 rounded bg-dark text-white">
                <div class="p-4">
                    <div class="text-center">
                        <h3>Create Playlist</h3>
                    </div>
                    <form @submit.prevent="createplaylist" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" name="name" v-model="name" required />
                        </div>
                        <div class="mb-2">Songs:</div>
                        <div class="mb-3 form check">
                            <b-table-simple sticky-header="340px" dark borderless>
                                <b-tbody>
                                    <b-tr v-for="(song,index) in songList" :key="index">
                                        <b-td>
                                            <input type="checkbox" class="form-check-input" :id="'song' + song.id" name="songs"
                                                :value="song.id" v-model="selectedSongs" />
                                            <label class="form-check-label ms-1" :for="'song' + song.id">{{ song.name }}</label>
                                        </b-td>
                                    </b-tr>
                                </b-tbody>
                            </b-table-simple>
                        </div>
                        <p class="text-danger" v-show="displaySongMessage">{{ songError }}</p>
                        <br>
                        <div class="text-center">
                            <button type="submit" class="btn btn-light text-center">Create Playlist</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'createPlaylist',
    data() {
        return {
            name: null,
            selectedSongs: [],
            songList: [],
            token: null,
            displaySongMessage: false,
            songError: "Playlist should have atleast one song!",
            message: null,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.creatorId = localStorage.getItem('id')
        if (this.token) {
            this.getSongs()
        } else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSongs() {
            axios.get(`http://127.0.0.1:5000/api/songs/get`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songList = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        createplaylist(event) {
            event.preventDefault()
            console.log("func was triggered")
            const formData = new FormData()
            let flag = false
            if (this.selectedSongs.length == 0) {
                flag = true
                this.displaySongMessage = true
            }
            if (flag) {
                return null
            }
            for (let id of this.selectedSongs) {
                formData.append('songs', id)
            }
            formData.append('name', this.name)
            axios.post('http://127.0.0.1:5000/api/playlists/post', formData, {
                headers: {
                    'Authentication-Token': `${this.token}`
                }
            })
                .then(response => {
                    this.message = response.data.message
                    this.$bvModal.msgBoxOk(`${this.message}`, {
                        title: 'Confirmation',
                        size: 'sm',
                        buttonSize: 'sm',
                        okVariant: 'success',
                        headerClass: 'p-2 border-bottom-0',
                        footerClass: 'p-2 border-top-0',
                        centered: true,
                        noCloseOnBackdrop: true,
                        okTitle: 'Redirect',
                    })
                        .then(() => {
                            this.$router.push('/user_playlists')
                        })
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }

}
</script>