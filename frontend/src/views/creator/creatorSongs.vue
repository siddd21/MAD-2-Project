<template>
    <div class="container content">
        <div v-if="Object.keys(songsData).length !== 0">
            <b-table-simple responsive sticky-header="80vh">
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
                        <b-td>{{ index }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/posters/${song.poster}`)" class="rounded table-image" />
                            <router-link :to="{ name: 'Song', params: { id: song.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ song.name }}
                            </router-link>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-trash-can fa-lg clickable" @click="$bvModal.show('delete-modal')"></i>
                            <b-modal id="delete-modal" hide-header-close>
                                <template v-slot:modal-title>
                                    <div class="text-center">Delete Song</div>
                                </template>
                                <template>
                                    <div class="d-block text-center ">
                                        Are you sure you want to permanently the song <b>{{ song.name }}</b>?
                                    </div>
                                </template>
                                <template v-slot:modal-footer>
                                    <button class="btn btn-danger p-1 m-1" @click="deleteSong(song.id)">Delete</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide('delete-modal')">Cancel</button>
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
            <router-link :to="{ name: 'uploadSong' }" class="btn btn-dark pill m-1">Upload Song</router-link>
        </div>
        <div v-else class="d-flex flex-column justify-content-center align-items-center">
            {{ songsData.length }}
            <div class="text-center">
                <p class="fs-2 fw-bold">You haven't uploaded any songs yet!</p>
                <router-link :to="{ name: 'uploadSong' }" class="btn btn-dark pill"><i
                        class="fa-solid fa-plus fa-lg p-1"></i>Upload Song</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'creatorSongs',
    data() {
        return {
            songsData: [],
            token: null,
            message: null,
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
            axios.get('http://127.0.0.1:5000/current_creator_songs/songs', {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songsData = response.data
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        deleteSong(songId) {
            // if (confirm(`Are yous sure you want to delete ${songName}?`)) {

            // }
            axios.delete(`http://127.0.0.1:5000/api/songs/delete/${songId}`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                }
            })
                .then(response => {
                    this.message = response.data.message
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
                        hideHeaderClose: true,
                    })
                        .then(() => {
                            window.location.reload()
                        })
                })
                .catch(error => {
                    console.log(error.data);
                });
        }
    }
}
</script>

<style scoped>
.pill {
    border-radius: 23px;
}
</style>