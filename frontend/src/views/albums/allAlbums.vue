<template>
    <div class="container content">
        <div class="table-wrapper">
            <b-table-simple sticky-header="85vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Title</b-th>
                        <b-th>Artist</b-th>
                        <b-th>Date Added </b-th>
                        <b-th>Flag</b-th>
                    </b-tr>
                </b-thead>
                <b-tbody>
                    <b-tr v-for="(album, index) in  albumsData  " :key="album.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/album_posters/${album.poster}`)" class="rounded table-image" />
                            <router-link :to="{ name: 'Album', params: { id: album.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ album.name }}
                            </router-link>
                        </b-td>
                        <b-td>
                            <router-link :to="{ name: 'Artist', params: { id: album.artist_id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ album.artist }}
                            </router-link>
                        </b-td>
                        <b-td>
                            {{ album.date_added }}
                        </b-td>
                        <b-td>
                            <button v-if="album.flagged" @click="flagAlbum(album.id)" class="btn btn-outline-success"
                                :id="'flag_button' + album.id">un-Flag</button>
                            <button v-else @click="flagAlbum(album.id)" class="btn btn-outline-danger"
                                :id="'flag_button' + album.id">Flag</button>
                            <b-tooltip placement="leftbottom" :target="'flag_button' + album.id" noninteractive>More
                                than
                                20 flags will delete the album!</b-tooltip>
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
    name: 'allAlbums',
    data() {
        return {
            albumsData: null,
            token: null,

        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (this.token) {
            this.getAlbums()
        }
        else {
            this.$router.push('/login')
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
                    console.log(response.data)
                    this.albumsData = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        flagAlbum(albumId) {
            axios.post(`http://localhost:5000/flag/album/${albumId}`, {}, {
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

<style scoped></style>