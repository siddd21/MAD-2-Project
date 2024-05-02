<template>
    <div class="container content">
        <div>
            <b-table-simple sticky-header="85vh">
                <b-thead>
                    <b-tr>
                        <b-th>#</b-th>
                        <b-th>Title</b-th>
                        <b-th>Artist</b-th>
                        <b-th>Album </b-th>
                        <b-th>Date Added </b-th>
                        <b-th><i class="fa-regular fa-clock fw-bold"></i></b-th>
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
                        <b-td v-if="song.album != null">
                            {{ song.album }}
                        </b-td>
                        <b-td v-else>-</b-td>
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
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'adminSongs',
    data() {
        return {
            songsData: null,
            token: null,
            role: null,

        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (this.token && this.role === 'admin') {
            this.getSongs()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods: {
        getSongs() {
            axios.get('http://127.0.0.1:5000/api/songs/get', {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    this.songsData = response.data
                })
                .catch(error => {
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
        }
    }
}
</script>
