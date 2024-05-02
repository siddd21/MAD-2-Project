<template>
    <div v-if="loading">
        Loading...
    </div>
    <div class="container content" v-else>
        <div class="row center-box">
            <div class="col-md-6 rounded bg-dark text-white">
                <div class="p-4">
                    <div class="text-center">
                        <h3>Update Song</h3>
                    </div>
                    <form enctype="multipart/form-data" @submit.prevent="UpdateSong">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" name="name" v-model="name" required />
                        </div>
                        <label for="genre" class="form-label" v-if="genres.length <= 1"
                            style="margin-bottom: 8px">Genre</label>
                        <label for="genre" class="form-label" v-else style="margin-bottom: 8px">Genres</label>
                        <div v-for="(key, index) in genres" :key="index">
                            <div class="mb-3">
                                <div class="input-group">
                                    <input type="text" name="genre" id="genre" :list="'genre-list-' + index"
                                        v-model="key.genre" class="form-control rounded">
                                    <datalist :id="'genre-list-' + index" size="5">
                                        <option v-for="genre in genreList" :value="genre">{{ genre }}</option>
                                    </datalist>
                                    <div class="input-group-append" v-if="index === genres.length - 1">
                                        <span class="p-1">
                                            <i class="fa-solid fa-circle-plus clickable" @click="add"></i>
                                        </span>
                                    </div>
                                    <div class="input-group-append">
                                        <span class="p-1">
                                            <i class="fa-solid fa-circle-xmark clickable" @click="remove(index)"></i>
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
                        <p class="text-danger" v-show="displayMessage">{{ genreError }}</p>
                        <div>
                            <label for="lyrics" class="form-label">Lyrics</label>
                            <textarea class="form-control" id="lyrics" name="lyrics" cols="30" rows="10"
                                v-model="lyrics" required>
                            </textarea>
                        </div>
                        <br />
                        <div>
                            <label for="song" class="form-label">Upload song</label>
                            <input class="form-control form-control-md" id="song" type="file" name="song" accept=".mp3"
                                @change="fileChange('audio', $event)" />
                        </div>
                        <br />
                        <div>
                            <label for="poster" class="form-label">Want to upload a poster for your song?</label>
                            <input class="form-control form-control-md" id="poster" type="file" name="poster"
                                accept="image/png, image/jpeg" @change="fileChange('poster', $event)" />
                        </div>
                        <br />
                        <div class="text-center">
                            <button type="submit" class="btn btn-light text-center">
                                Update
                            </button>
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
    name: 'updateSong',
    props: ['id'],
    data() {
        return {
            name: null,
            lyrics: null,
            lyricsList: null,
            genre: null,
            genres: [],
            token: null,
            loading: true,
            genreList: null,
            displayMessage: false,
            genreError: "Song should have atleast one genre!",
            message: null,
            featuringArtistsDispaly: false,
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        if (this.token) {
            this.getSong()
        }
        else {
            this.$router.push('/login')
        }
    },
    mounted() {
        this.genreList = genreData.genres
    },
    methods: {
        hoverIn() {
            this.featuringArtistsDispaly = true
        },
        hoverOut() {
            this.featuringArtistsDispaly = false
        },
        add() {
            this.genres.push({ genres: '' })
        },
        remove(index) {
            if (this.genres.length > 1) {
                this.genres.splice(index, 1)
            }
            else {
                this.displayMessage = true
                setTimeout(() => {
                    this.displayMessage = false
                }, 2000);
            }
        },
        getSong() {
            axios.get(`http://127.0.0.1:5000/get_song/${this.id}`, {
                headers: {
                    'Authentication-Token': `${this.token}`
                }
            })
                .then(response => {
                    this.name = response.data.name
                    this.lyrics = response.data.lyrics
                    this.lyricsList = response.data.lyrics.split('\n')
                    console.log("this.lyricsList is")
                    console.log(this.lyricsList)
                    this.genre = response.data.genre.split(',')
                    this.loading = false
                    for (const gen of this.genre) {
                        this.genres.push({
                            genre: gen,
                            isInvalid: false,
                            msgInvalid: '',
                            isRepeated: false,
                            msgRepeated: '',
                        })
                    }
                })
                .catch(error => {
                    this.loading = false
                    console.log(error)
                })
        },
        fileChange(type, event) {
            const file = event.target.files[0]
            if (type === 'audio') {
                this.audio = file
            }
            else {
                this.poster = file
            }
        },
        UpdateSong(event) {
            event.preventDefault();
            this.$bvModal.msgBoxConfirm(`Are you sure you want to update the song?\nChanges cannot be reversed!`, {
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
            }).then((value) => {
                if (value) {
                    const formData = new FormData();
                    let genresArray = [];
                    let flag = false;

                    for (let i = 0; i < this.genres.length; i += 1) {
                        console.log("for was triggered");
                        let element = this.genres[i];
                        if (genresArray.includes(element.genre)) {
                            console.log("repeat was triggered");
                            this.$set(element, 'isRepeated', true);
                            this.$set(element, 'msgRepeated', 'Cannot add a genre more than once!');
                            flag = true;
                        } else {
                            this.$set(element, 'isRepeated', false);
                            this.$set(element, 'msgInvalid', '');
                        }
                        if (!this.genreList.includes(element.genre)) {
                            console.log("invalid was triggered");
                            this.$set(element, 'isInvalid', true);
                            this.$set(element, 'msgInvalid', 'Genre needs to be from the datalist!');
                            flag = true;
                        } else {
                            this.$set(element, 'isInvalid', false);
                            this.$set(element, 'msgInvalid', '');
                        }
                        genresArray.push(element.genre);
                        if (flag) {
                            console.log("flag was triggered");
                            return null;
                        }
                    }
                    for (let gen of this.genres) {
                        formData.append('genres', gen.genre);
                    }
                    formData.append('name', this.name);
                    formData.append('lyrics', this.lyrics);
                    if (this.audio === undefined) {
                        this.audio = null;
                        formData.append('audio', this.audio);
                    } else {
                        formData.append('audio', this.audio);
                    }
                    if (this.poster === undefined) {
                        this.poster = null;
                        formData.append('poster', this.poster);
                    } else {
                        formData.append('poster', this.poster);
                    }
                    console.log('poster is', this.poster)
                    console.log(this.formData)
                    axios.put(`http://127.0.0.1:5000/api/songs/put/${this.id}`, formData, {
                        headers: {
                            'Authentication-Token': `${this.token}`
                        }
                    })
                        .then(response => {
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
                                okTitle: 'Redirect',
                            })
                                .then(() => {
                                    this.$router.push('/creator_songs');
                                });
                        })
                        .catch(error => {
                            console.log("Error is", error);
                            this.message = error.data.message;
                        })
                }
            })
        }

    }
}
</script>

<style scoped>
.flash-message {
    transition: all ease-in-out 2s;
}
</style>