<template>
    <div class="content container">
        <b-table-simple sticky-header="100vh">
            <b-thead>
                <b-tr>
                    <b-th>#</b-th>
                    <b-th>Name</b-th>
                    <b-th>Rating</b-th>
                    <b-th>Blacklist</b-th>
                </b-tr>
            </b-thead>
            <b-tbody>
                <b-tr v-for="(artist, index) in  artistsData  " :key="artist.id">
                    <b-td>{{ index + 1 }}</b-td>
                    <b-td>
                        <img :src="require(`@/assets/profile_pictures/${artist.profile_picture}`)"
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
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'adminCreators',
    data() {
        return {
            token: null,
            role: null,
            artistsData: [],
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (this.token && this.role === 'admin') {
            this.getArtists()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getArtists() {
            axios.get(`http://127.0.0.1:5000/get_artists`, {
                headers: {
                    'Authentication-Token': this.token,
                }
            }).then(response => {
                console.log(response.data)
                this.artistsData = response.data
                console.log(this.artistsData)
            }).catch(error => {
                console.log(error)
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