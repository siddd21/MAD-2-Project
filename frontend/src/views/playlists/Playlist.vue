<template>
    <div>
        <div v-if="loading" class="container">
            <div class="row">
                <div class="col-md-12 d-flex align-items-center justify-content-center">
                    <div class="mb-3">
                        <b-spinner label="Loading..."></b-spinner>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="container content">
            <b-table-simple sticky-header="85vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Name</b-th>
                        <b-th>Delete</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="(song, index) in  songsData  " :key="song.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/posters/${song.poster}`)" class="rounded table-image" />
                            <RouterLink :to="{ name: 'Song', params: { id: song.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ song.name }}
                            </RouterLink>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-trash-can fa-lg clickable" @click="$bvModal.show('delete-modal')"></i>
                            <b-modal id="delete-modal" hide-header-close>
                                <template v-slot:modal-title>
                                    <div class="text-center">Remove Song</div>
                                </template>
                                <template>
                                    <div class="d-block text-center ">
                                        Are you sure you want to remove <b>{{ song.name }}</b> from the playlist?
                                    </div>
                                </template>
                                <template v-slot:modal-footer>
                                    <button class="btn btn-danger p-1 m-1" @click="removeSong(song.id)">Remove</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide('delete-modal')">Cancel</button>
                                </template>
                            </b-modal>
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
            <button class="btn btn-dark pill" @click="$bvModal.show('add-songs-modal')"><i
                    class="fa-solid fa-plus fa-lg p-1"></i>Add songs</button>
            <b-modal id="add-songs-modal" hide-header-close scrollable>
                <template v-slot:modal-title>
                    <div class="text-center">Select Songs to add</div>
                </template>
                <template>
                    <div class="d-block">
                        <div class="form-check" v-for="key in  toAddSongs " :key="key.id">
                            <input :id="key.id" class="form-check-input" type="checkbox" v-model="selectedSongs"
                                :value="key.id">
                            <label class="form-check-label" :for="key.id">{{ key.name }}</label>
                        </div>
                    </div>
                </template>
                <template v-slot:modal-footer>
                    <button class="btn btn-dark p-1 m-1" @click="addSongs">Add</button>
                    <button class="btn btn-secondary m-1 p-1" @click="clearChecks">Cancel</button>
                </template>
            </b-modal>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Playlist',
    props: ['id'],
    data() {
        return {
            loading: true,
            songsData: null,
            toAddSongs: null,
            token: null,
            message: null,
            selectedSongs: [],
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
            axios.get(`http://127.0.0.1:5000/get_playlist/${this.id}`, {
                headers: {
                    'Authentication-token': `${this.token}`
                }
            })
                .then(response => {
                    this.songsData = response.data.songs
                    this.loading = false
                })
                .catch(error => {
                    console.log(error)
                })
            axios.get(`http://127.0.0.1:5000//add_playlist_songs/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            }).then(response => {
                this.toAddSongs = response.data
                console.log(response.data)
            }).catch(error => {
                console.log(error)
            })
        },
        removeSong(songId) {
            axios.get(`http://127.0.0.1:5000/remove_playlist_song/${this.id}/${songId}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then((response) => {
                    this.message = response.data.message
                    console.log(this.message)
                    this.$bvModal.hide('delete-modal')
                    this.$bvModal.msgBoxOk(`${this.message}`, {
                        title: 'Confirmation',
                        size: 'sm',
                        buttonSize: 'sm',
                        okVariant: 'success',
                        headerClass: 'p-2 border-bottom-0',
                        footerClass: 'p-2 border-top-0',
                        centered: true,
                        noCloseOnBackdrop: true,
                    })
                        .then(() => {
                            window.location.reload()
                        })

                })
                .catch((error) => {
                    this.$bvModal.hide('delete-modal')
                    this.$bvModal.msgBoxOk(`${error.response.data.message}`, {
                        title: 'Error',
                        size: 'sm',
                        buttonSize: 'sm',
                        okVariant: 'warning',
                        headerClass: 'p-2 border-bottom-0',
                        footerClass: 'p-2 border-top-0',
                        centered: true,
                        noCloseOnBackdrop: true,
                    })
                })
        },
        addSongs() {
            axios.put(`http://127.0.0.1:5000/api/playlists/put/${this.id}/songs`, {
                songs: this.selectedSongs
            }, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                }
            }).then(response => {
                this.message = response.data.message
                this.$bvModal.hide('add-songs-modal')
                this.$bvModal.msgBoxOk(`${this.message}`, {
                    title: 'Confirmation',
                    size: 'sm',
                    buttonSize: 'sm',
                    okVariant: 'success',
                    headerClass: 'p-2 border-bottom-0',
                    footerClass: 'p-2 border-top-0',
                    centered: true
                })
                    .then(() => {
                        window.location.reload()
                    })

            })
        },
        clearChecks() {
            this.$bvModal.hide('add-songs-modal')
            this.selectedSongs = []
        }
    }
}
</script>

<style scoped>
.pill {
    border-radius: 23px;
}
</style>