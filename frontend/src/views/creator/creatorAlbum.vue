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
        <div class="container content">
            <div class="row d-flex justify-content-around">
                <div class="d-flex">
                    <img :src="require(`@/assets/album_posters/${albumPoster}`)" :alt="name"
                        class="rounded-circle profile-pic" />
                    <div>
                        <p class="fs-1 fw-bolder m-2">{{ albumName }}</p>
                    </div>
                </div>
            </div>
            <hr />
            <b-table-simple sticky-header="85vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Name</b-th>
                        <b-th>Delete</b-th>
                        <b-th>Update</b-th>
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
                            <i class="fa-solid fa-trash-can fa-lg clickable"
                                @click="$bvModal.show(`delete-modal-${song.id}`)"></i>
                            <b-modal :id="'delete-modal-' + song.id" hide-header-close>
                                <template v-slot:modal-title>
                                    <div class="text-center">Remove Song</div>
                                </template>
                                <template>
                                    <div class="d-block text-center ">
                                        Are you sure you want to remove <b>{{ song.name }}</b> from the album?
                                    </div>
                                </template>
                                <template v-slot:modal-footer>
                                    <button class="btn btn-danger p-1 m-1" @click="removeSong(song.id)">Remove</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide(`delete-modal-${song.id}`)">Cancel</button>
                                </template>
                            </b-modal>
                        </b-td>
                        <b-td>
                            <router-link :to="{ name: 'updateSong', params: { id: song.id } }" class="link-dark">
                                <i class="fa-solid fa-pen fa-lg"></i>
                            </router-link>
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
                        <div class="form-check" v-for="(key, index1) in  toAddSongs " :key="key.id">
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
    name: 'Album',
    props: ['id'],
    data() {
        return {
            loading: true,
            songsData: null,
            toAddSongs: null,
            token: null,
            albumId: null,
            albumName: null,
            albumPoster: null,
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
            console.log("getSongs was triggered")
            axios.get(`http://127.0.0.1:5000/get_album/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    console.log("data received")
                    console.log(response.data)
                    this.songsData = response.data.songs
                    this.albumId = response.data.id
                    this.albumName = response.data.name
                    this.albumPoster = response.data.poster
                    this.loading = false
                })
                .catch(error => {
                    console.log(error)
                })
            axios.get(`http://127.0.0.1:5000/current_creator_songs/albums`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            }).then(response => {
                this.toAddSongs = response.data
            }).catch(error => {
                console.log(error)
            })
        },
        removeSong(songId) {
            if (this.songsData.length != 1) {
                axios.get(`http://127.0.0.1:5000/remove_album_song/${this.albumId}/${songId}`, {
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
                        console.log(error)
                    })
            }
            else {
                this.$bvModal.msgBoxConfirm('Deleting this song will delete the album. Do you want to continue?', {
                    title: 'Please Confirm',
                    size: 'sm',
                    buttonSize: 'sm',
                    okVariant: 'danger',
                    okTitle: 'YES',
                    cancelTitle: 'NO',
                    footerClass: 'p-2',
                    hideHeaderClose: true,
                    centered: true
                })
                    .then(value => {
                        if (value) {
                            this.$router.push({ name: 'creatorAlbums' })
                            axios.get(`http://127.0.0.1:5000/remove_album_song/${this.albumId}/${songId}`, {
                                headers: {
                                    'Authentication-Token': `${this.token}`,
                                },
                            })
                            axios.delete(`http://127.0.0.1:5000/api/albums/delete/${this.albumId}`, {
                                headers: {
                                    'Authentication-Token': `${this.token}`,
                                },
                            }).then(response => {
                                window.location.reload()
                            })
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        addSongs() {
            axios.put(`http://127.0.0.1:5000/api/albums/put/${this.albumId}/songs`, {
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
                    hideHeaderClose: true,
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