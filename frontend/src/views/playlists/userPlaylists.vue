<template>
    <div class="container content">
        <div v-if="playlistsData.length !== 0">
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
                    <b-tr v-for="(playlist, index) in  playlistsData  " :key="playlist.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <RouterLink :to="{ name: 'Playlist', params: { id: playlist.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ playlist.name }}
                            </RouterLink>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-trash-can fa-lg clickable"
                                @click="$bvModal.show(`delete-modal-${playlist.id}`)"></i>
                            <b-modal :id="'delete-modal-' + playlist.id" hide-header-close>
                                <template v-slot:modal-title>
                                    <div class="text-center">Delete Playlist</div>
                                </template>

                                <template>
                                    <div class="d-block text-center ">
                                        Are you sure you want to permanently the playlist <b>{{ playlist.name }}</b>?
                                    </div>
                                </template>

                                <template v-slot:modal-footer>
                                    <button class="btn btn-danger p-1 m-1"
                                        @click="deletePlaylist(playlist.id)">Delete</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide(`delete-modal-${playlist.id}`)">Cancel</button>
                                </template>
                            </b-modal>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-pen fa-lg clickable"
                                @click="$bvModal.show(`update-modal-${playlist.id}`)"></i>
                            <b-modal :id="'update-modal-' + playlist.id" centered hide-header-close>

                                <template v-slot:modal-title>
                                    <div class="text-center">Update Playlist</div>
                                </template>

                                <template>
                                    <div class="d-block">
                                        <form id="updateForm" @submit.prevent="updatePlaylist">
                                            <div class="mb-3">
                                                <label id="name" for="name" class="form-label">Name</label>
                                                <input v-model="name" type="text" class="form-control" name="name"
                                                    id="name" autocomplete="off" required>
                                            </div>
                                        </form>
                                    </div>
                                </template>

                                <template v-slot:modal-footer>
                                    <button class="btn btn-primary p-1 m-1"
                                        @click="updatePlaylist($event, playlist.id)">Update</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide(`update-modal-${playlist.id}`)">Cancel</button>
                                </template>
                            </b-modal>
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
            <router-link :to="{ name: 'createPlaylist' }" class="btn btn-dark pill"><i
                    class="fa-solid fa-plus fa-lg p-1"></i>Create
                Playlist</router-link>
        </div>
        <div v-else class="d-flex flex-column justify-content-center align-items-center">
            <div class="text-center">
                <p class="fs-2 fw-bold">You don't have any playlists yet!</p>
                <router-link :to="{ name: 'createPlaylist' }" class="btn btn-dark pill"><i
                        class="fa-solid fa-plus fa-lg p-1"></i>Create Playlist</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'userPlaylists',
    data() {
        return {
            name: null,
            playlistsData: null,
            token: null,

        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.creatorId = localStorage.getItem('id')
        if (this.token) {
            this.getPlaylists()
        } else {
            this.$router.push('/login')
        }
    },
    methods: {
        getPlaylists() {
            console.log(this.token)
            axios.get('http://127.0.0.1:5000/api/playlists/get', {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            }).then(response => {
                this.playlistsData = response.data
            }).catch(error => {
                console.log(error)
            })
        },
        deletePlaylist(playlistId) {
            console.log(this.token)
            axios.delete(`http://127.0.0.1:5000/api/playlists/delete/${playlistId}`, {
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
                        noCloseOnBackdrop: true
                    })
                        .then(() => {
                            window.location.reload()
                        })
                })
                .catch(error => {
                    console.log(error.data);
                });
        },
        updatePlaylist(event, playlistId) {
            console.log(this.token)
            event.preventDefault()
            this.$bvModal.msgBoxConfirm(`Are you sure you want to update the playlist?`, {
                title: 'Please Confirm',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: 'YES',
                cancelTitle: 'NO',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true,
                noCloseOnBackdrop: true,
                hideHeaderClose: true,
            }).then(() => {
                console.log(this.token)
                axios.put(`http://127.0.0.1:5000/api/playlists/put/${playlistId}/data`, {
                    name: this.name
                }, {
                    headers: {
                        'Authentication-Token': `${this.token}`,
                    }
                }).then(response => {
                    this.message = response.data.message;
                    this.$bvModal.msgBoxOk(`${this.message}`, {
                        title: 'Confirmation',
                        size: 'sm',
                        buttonSize: 'sm',
                        okVariant: 'success',
                        headerClass: 'p-2 border-bottom-0',
                        footerClass: 'p-2 border-top-0',
                        centered: true,
                        noCloseOnBackdrop: true,
                        okTitle: 'OK',
                    }).then(() => {
                        window.location.reload()
                    })
                }).catch(error => {
                    console.log(error)
                })
            })

        },
    }
}
</script>

<style scoped>
.pill {
    border-radius: 23px;
}
</style>