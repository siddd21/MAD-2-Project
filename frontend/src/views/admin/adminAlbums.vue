<template>
    <div class="container content">
        <div>
            <b-table-simple sticky-header="100vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Name</b-th>
                        <b-th>Delete</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="(album, index) in  albumsData  " :key="album.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/album_posters/${album.poster}`)" class="rounded table-image" />
                            {{ album.name }}
                        </b-td>
                        <b-td>
                            <button class="btn btn-danger" @click="deleteAlbum(album.id, album.name)">Delete</button>
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
    name: 'adminAlbums',
    data() {
        return {
            name: null,
            albumsData: null,
            token: null,
            role: null,
            message: null,
            displayGenreMessage: false,
        };
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (this.token && this.role === 'admin') {
            this.getAlbums();
        }
        else {
            this.$router.push('/login');
        }
    },
    methods: {
        getAlbums() {
            axios.get('http://127.0.0.1:5000/api/albums/get', {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.albumsData = response.data;
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteAlbum(albumId, albumName) {
            this.$bvModal.msgBoxConfirm(`Are you sure you want to delete ${albumName}?`, {
                title: 'Delete Album',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: 'YES',
                cancelTitle: 'NO',
                footerClass: 'p-2',
                hideHeaderClose: true,
                centered: true
            }).then(value => {
                if (value) {
                    axios.delete(`http://127.0.0.1:5000/api/albums/delete/${albumId}`, {
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
                }
            })
        },
    },
    components: { RouterLink }
}

</script>