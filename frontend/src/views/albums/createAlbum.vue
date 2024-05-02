<template>
    <div class="container content">
        <div class="row album-form">
            <div class="col-md-6 rounded bg-dark text-white">
                <div class="p-4">
                    <div class="text-center">
                        <h3>Create Album</h3>
                    </div>
                    <form @submit.prevent="createAlbum" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="name" class="form-label">Title</label>
                            <input type="text" class="form-control" id="name" name="name" v-model="name" required />
                        </div>
                        <label v-if="genres.length <= 1" for="genre" class="form-label mb-3">Genre</label>
                        <label v-else for="genre" class="form-label mb-3">Genres</label>
                        <div v-for="(key, index1) in genres" :key="index1">
                            <div class="mb-3">
                                <div class="input-group">
                                    <input type="text" name="genre" :id="'genre-' + index1"
                                        :list="'genre-list-' + index1" v-model="key.genre" class="form-control rounded"
                                        :aria-describedby="'genre-' + index1 + '-feedback'" required>
                                    <datalist :id="'genre-list-' + index1" size="5">
                                        <option v-for="genre in genreList" :value="genre">{{ genre }}</option>
                                    </datalist>
                                    <div class="input-group-append" v-if="index1 === genres.length - 1">
                                        <span class="p-1">
                                            <i class="fa-solid fa-circle-plus clickable" @click="addGenre"></i>
                                        </span>
                                    </div>
                                    <div class="input-group-append">
                                        <span class="p-1">
                                            <i class="fa-solid fa-circle-xmark clickable"
                                                @click="removeGenre(index1)"></i>
                                        </span>
                                    </div>
                                </div>
                                <div v-if="key.isRepeated">
                                    <p class="text-danger">{{ key.msgRepeated }}</p>
                                </div>
                                <div v-if="key.isInvalid">
                                    <p class="text-danger">{{ key.msgInvalid }}</p>
                                </div>
                            </div>
                        </div>
                        <p clas="text-danger" v-show="displayGenreMessage">{{ genreError }}</p>
                        <div class="mb-2">Songs:</div>
                        <div class="mb-3 form check">
                            <b-table-simple sticky-header="165px" dark borderless>
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
                        <div class="mb-3">
                            <label for="poster" class="form-label">Album Poster</label>
                            <input class="form-control form-control-md" id="poster" type="file" name="poster"
                                accept="image/png, image/jpeg" @change="fileChange($event)" required />
                        </div>
                        <br>
                        <div class="text-center">
                            <button type="submit" class="btn btn-light text-center">Create Album</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import genreData from '@/genres.json'

export default {
    name: 'createAlbum',
    data() {
        return {
            name: null,
            genres: [{
                genre: '',
                isInvalid: false,
                msgInvalid: '',
                isRepeated: false,
                msgRepeated: '',
            }],
            genreList: null,
            songList: [],
            poster: null,
            token: null,
            displayGenreMessage: false,
            genreError: "Album should have atleast one genre!",
            displaySongMessage: false,
            songError: "Album should have atleast one song!",
            message: null,
            creatorId: null,
            selectedSongs: []
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
    mounted() {
        this.genreList = genreData.genres
    },
    methods: {
        addGenre() {
            this.genres.push({
                genre: '',
                isInvalid: false,
                msgInvalid: '',
                isRepeated: false,
                msgRepeated: '',
            })
        },
        removeGenre(index) {
            if (this.genres.length > 1) {
                this.genres.splice(index, 1)
            }
            else {
                this.displayGenreMessage = true
                setTimeout(() => {
                    this.displayGenreMessage = false
                }, 2000);
            }
        },
        getSongs() {
            axios.get(`http://127.0.0.1:5000/current_creator_songs/albums`, {
                headers: {
                    'Authentication-Token': `${this.token}`,
                },
            })
                .then(response => {
                    console.log(response.data)
                    this.songList = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        fileChange(event) {
            const file = event.target.files[0]
            this.poster = file

        },
        createAlbum(event) {
            event.preventDefault()
            console.log("func was triggered")
            const formData = new FormData()
            let genresArray = []
            let songsArray = []
            let flag = false
            for (let i = 0; i < this.genres.length; i += 1) {
                let element = this.genres[i]
                if (genresArray.includes(element.genre)) {
                    element.isRepeated = true
                    element.msgRepeated = 'Cannot add a genre more than once!'
                    flag = true;
                } else {
                    element.isRepeated = false;
                    element.msgInvalid = '';
                }
                if (!this.genreList.includes(element.genre)) {
                    element.isInvalid = true;
                    element.msgInvalid = 'Genre needs to be from the datalist!';
                    flag = true;
                } else {
                    element.isInvalid = false;
                    element.msgInvalid = '';
                }
                genresArray.push(element.genre)
            }
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
            formData.append('poster', this.poster)
            console.log(this.formData)
            axios.post('http://127.0.0.1:5000/api/albums/post', formData, {
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
                            this.$router.push('/creator_albums')
                        })
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>