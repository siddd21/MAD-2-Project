<template>
  <div class="container content">
    <div class="row center-box">
      <div class="col-md-6 rounded bg-dark text-white">
        <div class="p-4">
          <div class="text-center">
            <h3>Upload Song</h3>
          </div>
          <form @submit.prevent="UploadSong" enctype="multipart/form-data">
            <div class="mb-3">
              <label for="title" class="form-label">Title</label>
              <input type="text" class="form-control" id="title" name="title" v-model="name" />
            </div>
            <label v-if="genres.length <= 1" for="genre" class="form-label mb-3">Genre</label>
            <label v-else for="genre" class="form-label mb-3">Genres</label>
            <div v-for="(key, index) in genres" :key="index">
              <div class="mb-3">
                <div class="input-group">
                  <input type="text" name="genre" id="genre" :list="'genre-list-' + index" v-model="key.genre"
                    class="form-control rounded">
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
              <textarea class="form-control" id="lyrics" name="lyrics" cols="30" rows="10" required
                v-model="lyrics"></textarea>
            </div>
            <br />
            <div>
              <label for="song" class="form-label">Upload song</label>
              <input class="form-control form-control-md" id="song" type="file" name="song" accept=".mp3"
                @change="fileChange('audio', $event)" required />
            </div>
            <br />
            <div>
              <label for="poster" class="form-label">Want to upload a poster for your song?</label>
              <input class="form-control form-control-md" id="poster" type="file" name="poster"
                accept="image/png, image/jpeg" @change="fileChange('poster', $event)" required />
            </div>
            <br />
            <div class="text-center">
              <button type="submit" class="btn btn-light text-center">
                Submit
              </button>
            </div>
            <!-- <p v-show="message" class="text-center">{{ message }}</p> -->
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
  name: 'uploadSong',
  data() {
    return {
      name: null,
      featuringArtists: null,
      lyrics: null,
      audio: null,
      poster: null,
      genres: [{
        genre: '',
        isInvalid: false,
        msgInvalid: '',
        isRepeated: false,
        msgRepeated: '',
      }],
      genreList: null,
      displayMessage: false,
      genreError: "Song should have atleast one genre!",
      token: null,
      message: false,
      featuringArtistsDispaly: false,
    }
  },
  created() {
    this.token = localStorage.getItem('auth-token')
    if (this.token) {
      console.log("verified")
    }
    else {
      this.$router.push('/login')
    }
  },
  mounted() {
    this.genreList = genreData.genres
  },
  methods: {
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
    fileChange(type, event) {
      const file = event.target.files[0]
      if (type === 'audio') {
        this.audio = file
        console.log(this.audio)
      }
      else {
        this.poster = file
      }
    },
    UploadSong(event) {
      event.preventDefault()
      console.log("func was triggered")
      let genresArray = []
      let flag = false
      // for (let gen of this.genres) {
      //   if (!this.genreList.includes(gen.genre)) {
      //     this.message = "Genre needs to be from the datalist!"
      //     setTimeout(() => {
      //       this.message = false
      //     }, 2000);
      //     return null
      //   }
      // }
      for (let i = 0; i < this.genres.length; i += 1) {
        console.log("for was triggered")
        let element = this.genres[i]
        if (genresArray.includes(element.genre)) {
          console.log("repeat was triggered")
          // element.isRepeated = true
          // element.msgRepeated = 'Cannot add a genre more than once!'
          this.$set(element, 'isRepeated', true);
          this.$set(element, 'msgRepeated', 'Cannot add a genre more than once!');
          flag = true;
        } else {
          // element.isRepeated = false;
          // element.msgInvalid = '';
          this.$set(element, 'isRepeated', false);
          this.$set(element, 'msgInvalid', '');
        }
        if (!this.genreList.includes(element.genre)) {
          console.log("invalid was triggered")
          // element.isInvalid = true;
          // element.msgInvalid = 'Genre needs to be from the datalist!';
          this.$set(element, 'isInvalid', true);
          this.$set(element, 'msgInvalid', 'Genre needs to be from the datalist!');
          flag = true;
        } else {
          // element.isInvalid = false;
          // element.msgInvalid = '';
          this.$set(element, 'isInvalid', false);
          this.$set(element, 'msgInvalid', '');
        }
        console.log(this.genres)
        genresArray.push(element.genre)
        console.log(genresArray)
      }
      if (flag) {
        console.log("flag was triggered")
        return null
      }
      const formData = new FormData()
      for (let gen of this.genres) {
        formData.append('genres', gen.genre)
      }
      formData.append('name', this.name)
      formData.append('lyrics', this.lyrics)
      formData.append('audio', this.audio)
      formData.append('poster', this.poster)
      axios.post('http://127.0.0.1:5000/api/songs/post', formData, {
        headers: {
          'Authentication-Token': `${this.token}`
        }
      })
        .then(response => {
          this.message = response.data.message
          // setTimeout(() => {
          //   this.$router.push('/creator_songs')
          // }, 2000);
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
              this.$router.push('/creator_songs')
            })

        })
        .catch(error => (console.log(error)))
    }
  }
}
</script>

<style scoped>
.flash-message {
  z-index: 100;
  background-color: white;
  color: black;
  /* padding: 2px; */
  transition: all 5s;
}

.fa-solid.fa-circle-xmark,
.fa-solid.fa-circle-plus {
  background-color: transparent !important;
  /* Remove white background */
}
</style>