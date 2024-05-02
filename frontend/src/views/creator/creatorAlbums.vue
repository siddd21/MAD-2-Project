<template>
    <div class="container content">
        <div v-if="albumsData.length !== 0">
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
                    <b-tr v-for="(album, index) in  albumsData  " :key="album.id">
                        <b-td>{{ index + 1 }}</b-td>
                        <b-td>
                            <img :src="require(`@/assets/album_posters/${album.poster}`)" class="rounded table-image" />
                            <RouterLink :to="{ name: 'creatorAlbum', params: { id: album.id } }"
                                class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                {{ album.name }}
                            </RouterLink>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-trash-can fa-lg clickable"
                                @click="deleteAlbum(album.id, album.name)"></i>
                        </b-td>
                        <b-td>
                            <i class="fa-solid fa-pen fa-lg clickable"
                                @click="$bvModal.show(`update-modal-${album.id}`)"></i>
                            <b-modal :id="'update-modal-' + album.id" centered hide-header-close>

                                <template v-slot:modal-title>
                                    <div class="text-center">Update Album </div>
                                </template>

                                <template>
                                    <div class="d-block">
                                        <form id="updateForm" @submit.prevent="updateAlbum">
                                            <div class="mb-3">
                                                <label id="name" for="name" class="form-label">Name</label>
                                                <input v-model="name" type="text" class="form-control" name="name"
                                                    id="name" autocomplete="off">
                                            </div>
                                            <label v-if="genres.length <= 1" for="genre"
                                                class="form-label mb-3">Genre</label>
                                            <label v-else for="genre" class="form-label mb-3">Genres</label>
                                            <div v-for="(key, index) in genres" :key="index">
                                                <div class="mb-3">
                                                    <div class="input-group">
                                                        <input type="text" name="genre" :id="'genre-' + index"
                                                            :list="'genre-list-' + index" v-model="key.genre"
                                                            class="form-control rounded"
                                                            :aria-describedby="'genre-' + index + '-feedback'"
                                                            autocomplete="off" required>
                                                        <datalist :id="'genre-list-' + index" size="5">
                                                            <option v-for="genre in genreList" :value="genre">{{ genre
                                                                }}
                                                            </option>
                                                        </datalist>
                                                        <div class="input-group-append"
                                                            v-if="index === genres.length - 1">
                                                            <span class="p-1">
                                                                <i class="fa-solid fa-circle-plus clickable"
                                                                    @click="addGenre"></i>
                                                            </span>
                                                        </div>
                                                        <div class="input-group-append">
                                                            <span class="p-1">
                                                                <i class="fa-solid fa-circle-xmark clickable"
                                                                    @click="removeGenre(index)"></i>
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div v-if="key.isRepeated">
                                                        <p class="text-danger">{{ key.msgRepeated }}</p>
                                                    </div>
                                                    <div v-if="key.isInvalid">
                                                        <p class="text-danger">{{ key.msgInvalid }}</p>
                                                    </div>
                                                    <p class="text-danger" v-show="displayGenreMessage">{{ genreError }}
                                                    </p>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </template>
                                <template v-slot:modal-footer>
                                    <button class="btn btn-primary p-1 m-1"
                                        @click="updateAlbum($event, album.id)">Update</button>
                                    <button class="btn btn-secondary m-1 p-1"
                                        @click="$bvModal.hide(`update-modal-${album.id}`)">Cancel</button>
                                </template>
                            </b-modal>
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
            <router-link :to="{ name: 'createAlbum' }" class="btn btn-dark pill m-1">Create Album</router-link>
        </div>
        
        <div v-else class="d-flex flex-column justify-content-center align-items-center">
            <div class="text-center">
                <p class="fs-2 fw-bold">You don't have any albums yet!</p>
                <router-link :to="{ name: 'createAlbum' }" class="btn btn-dark pill"><i
                        class="fa-solid fa-plus fa-lg p-1"></i>Create Album</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import genreData from '@/genres.json'

export default {
    name: 'creatorAlbums',
    data() {
        return {
            name: null,
            albumsData: null,
            token: null,
            message: null,
            genres: [{
                genre: '',
                isInvalid: false,
                msgInvalid: '',
                isRepeated: false,
                msgRepeated: '',
            }],
            genreList: null,
            displayGenreMessage: false,
            genreError: "Album should have atleast one genre!",
        };
    },
    created() {
        this.token = localStorage.getItem('auth-token');
        if (this.token) {
            this.getAlbums();
        }
        else {
            this.$router.push('/login');
        }
    },
    mounted() {
        this.genreList = genreData.genres
    },
    methods: {
        // submitForm() {
        //     // const from = this.$ref.updateForm
        //     // if (form){
        //     //     form.submit()
        //     // }
        //     document.getElementById("updateForm").submit();
        // },
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
        getAlbums() {
            axios.get('http://127.0.0.1:5000/current_creator_albums', {
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
        updateAlbum(event, albumId) {
            event.preventDefault()
            let genresArray = []
            let flag = false
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
                if (element.genre != '') {
                    if (!this.genreList.includes(element.genre)) {
                        console.log("invalid was triggered");
                        this.$set(element, 'isInvalid', true);
                        this.$set(element, 'msgInvalid', 'Genre needs to be from the datalist!');
                        flag = true;
                    } else {
                        this.$set(element, 'isInvalid', false);
                        this.$set(element, 'msgInvalid', '');
                    }
                }
                genresArray.push(element.genre);
            }
            console.log(this.genres)
            if (flag) {
                return null
            }
            this.$bvModal.msgBoxConfirm(`Are you sure you want to update the album?\nChanges cannot be reversed!`, {
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
                const formData = new FormData()
                for (let gen of this.genres) {
                    formData.append('genres', gen.genre);
                }
                formData.append('name', this.name);
                axios.put(`http://127.0.0.1:5000/api/albums/put/${albumId}/data`, formData, {
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
                            okTitle: 'OK',
                        }).then(() => {
                            window.location.reload()
                        })
                    }).catch(error => {
                        console.log(error)
                    })
            })
        }
    },
    components: { RouterLink }
}

</script>
<style scoped>
.pill {
    border-radius: 23px;
}
</style>