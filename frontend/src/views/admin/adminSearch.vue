<template>
    <div v-if="noResults == true" class="d-flex flex-column justify-content-center align-items-center text-center" style="height: 100vh">
        <h3>No results found</h3>
        <p>
          Please make sure your words are spelled correctly, or use fewer or
          different keywords.
        </p>
    </div>
    <div v-else class="content container">
        <b-tabs content-class="mt-3">
            <b-tab title="Songs">
                <b-table-simple v-if="songsData.length>0" sticky-header="77vh">
                    <b-thead>
                        <b-tr>
                            <b-th>#</b-th>
                            <b-th>Title</b-th>
                            <b-th>Artist</b-th>
                            <b-th>Genre</b-th>
                            <b-th>Date Added</b-th>
                            <b-th><i class="fa-solid fa-lg fa-clock"></i></b-th>
                            <b-th>Delete</b-th>
                        </b-tr>
                    </b-thead>
                    <b-tbody>
                        <b-tr v-for="(song, index) in  songsData  " :key="song.id">
                            <b-td>{{ index + 1 }}</b-td>
                            <b-td>
                                <img :src="require(`@/assets/posters/${song.poster}`)" class="rounded table-image" />
                                {{ song.name }}
                            </b-td>
                            <b-td>
                                {{ song.artist }}
                            </b-td>
                            <b-td>
                                {{ genres(song.genre) }}
                            </b-td>
                            <b-td>
                                {{ song.date_added }}
                            </b-td>
                            <b-td>
                                {{ secondsToMin(song.duration) }}
                            </b-td>
                            <b-td>
                                <button class="btn btn-danger" @click="deleteSong(song.id, song.name)">Delete</button>
                            </b-td>
                        </b-tr>
                    </b-tbody>
                </b-table-simple>
                <div v-else class="d-flex flex-column justify-content-center align-items-center text-center" style="height:77vh">
                    <h3>No Songs found</h3>
                    <p>
                        Please make sure your words are spelled correctly, or use fewer or
                        different keywords.
                    </p>
                </div>
            </b-tab>
            <b-tab title="Albums">
                <b-table-simple v-if="albumsData.length>0" sticky-header="77vh">
                    <b-thead>
                        <b-tr>
                            <b-th>#</b-th>
                            <b-th>Title</b-th>
                            <b-th>Artist</b-th>
                            <b-th>Genre</b-th>
                            <b-th>Date Added</b-th>
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
                                {{ album.artist }}
                            </b-td>
                            <b-td>
                                {{ genres(album.genre) }}
                            </b-td>
                            <b-td>
                                {{ album.date_added }}
                            </b-td>
                            <b-td>
                                <button class="btn btn-danger" @click="deleteAlbum(album.id, album.name)">Delete</button>
                            </b-td>
                        </b-tr>
                    </b-tbody>
                </b-table-simple>
                <div v-else class="d-flex flex-column justify-content-center align-items-center text-center" style="height:77vh">
                    <h3>No Albums found</h3>
                    <p>
                        Please make sure your words are spelled correctly, or use fewer or
                        different keywords.
                    </p>
                </div>
            </b-tab>
            <b-tab title="Artists">
                <b-table-simple v-if="artistsData.length>0" sticky-header="77vh">
                    <b-thead>
                        <b-tr>
                            <b-th>#</b-th>
                            <b-th>Artist</b-th>
                            <b-th>Rating</b-th>
                        </b-tr>
                    </b-thead>
                    <b-tbody>
                        <b-tr v-for="(artist, index) in  artistsData  " :key="artist.id">
                            <b-td>{{ index + 1 }}</b-td>
                            <b-td>
                                <img :src="require(`@/assets/profile_pictures/${artist.poster}`)"
                                    class="rounded table-image" />
                                {{ artist.name }}
                            </b-td>
                            <b-td>
                                {{ artist.rating }} <i class="fa-solid fa-star"></i>
                            </b-td>
                            <b-td>
                                <button v-if="artist.blacklisted" class="btn btn-light"
                                    @click="whitelist(artist.id)">Whitelist</button>
                                <button v-else class="btn btn-dark" @click="blacklist(artist.id)">Blacklist</button>
                            </b-td>
                        </b-tr>
                    </b-tbody>
                </b-table-simple>
                <div v-else class="d-flex flex-column justify-content-center align-items-center text-center" style="height:77vh">
                    <h3>No Artists found</h3>
                    <p>
                        Please make sure your words are spelled correctly, or use fewer or
                        different keywords.
                    </p>
                </div>
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'adminSearch',
    props: ['query'],
    data() {
        return {
            songsData: [],
            albumsData: [],
            artistsData: [],
            token: null,
            role: null,
            noResults: false,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (!this.token || this.role !== 'admin') {
            this.$router.push('/login')
        } else {
            this.getDetails()
        }
    },
    watch: {
        '$route.params.query': function (newQuery, oldQuery) {
            console.log('Route parameter changed:', newQuery);
            this.getDetails()
        }
    },
    methods: {
        getDetails() {
            axios.post(`http://127.0.0.1:5000/search`, {
                query: this.query
            }, {
                headers: {
                    'Authentication-Token': this.token
                }
            }).then(response => {
                console.log(response.data)
                this.songsData = response.data.songs
                this.albumsData = response.data.albums
                this.artistsData = response.data.artists
                if (this.songsData.length == 0 && this.albumsData.length == 0 && this.artistsData.length == 0){
                    this.noResults = true
                }else{
                    this.noResults = false
                }
            }).catch(error => {
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
        genres(string) {
            let list = string.split(',')
            let genre = ''
            for (let i = 0; i < list.length; i++) {
                let item = list[i]
                if (i != list.length - 1) {
                    genre += `${item.toString()} ,`
                } else {
                    genre += `${item.toString()}`
                }
            }
            return genre
        },
        deleteSong(songId, songName) {
            this.$bvModal.hide('delete-modal')
            this.$bvModal.msgBoxConfirm(`Are you sure you want to delete ${songName}?`, {
                title: 'Please Confirm',
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
                    axios.delete(`http://127.0.0.1:5000/api/songs/delete/${songId}`, {
                        headers: {
                            'Authentication-Token': `${this.token}`,
                        }
                    })
                        .then(response => {
                            this.$bvModal.msgBoxOk(`${response.data.message}`, {
                                title: 'Confirmation',
                                size: 'sm',
                                buttonSize: 'sm',
                                okVariant: 'success',
                                headerClass: 'p-2 border-bottom-0',
                                footerClass: 'p-2 border-top-0',
                                centered: true,
                                hideHeaderClose: true,
                            }).then(
                                window.location.reload()
                            )
                        })
                        .catch(error => {
                            console.log(error)
                        })
                }
            })
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
        blacklist(artistId) {
            this.$bvModal.msgBoxConfirm('Are you sure you want to blacklist this Creator?', {
                title: 'Blacklist Creator',
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
                    axios.post(`http://127.0.0.1:5000/blacklist/${artistId}`, {
                        headers: {
                            'Authentication-Token': this.token
                        }
                    }).then(response => {
                        window.location.reload()
                    }).catch(error => {
                        console.log(error)
                    })
                }
            })

        },
        whitelist(artistId) {
            this.$bvModal.msgBoxConfirm('Are you sure you want to whitelist this Creator?', {
                title: 'Whitelist Creator',
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
                    axios.post(`http://127.0.0.1:5000/blacklist/${artistId}`, {
                        headers: {
                            'Authentication-Token': this.token
                        }
                    }).then(response => {
                        window.location.reload()
                    }).catch(error => {
                        console.log(error)
                    })
                }
            })

        },

    }
}
</script>