<template>
  <div class="flex-row">
    <nav
      v-show="this.$route.name !== 'Welcome' && this.$route.name !== 'Login' && this.$route.name !== 'Register' && this.$route.name !== 'blacklistPage'"
      class="navbar navbar-expand-lg fixed-top bg-dark navbar-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" :to="{ name: 'Home' }"><i class="bi bi-headphones me-2"
            style="font-size: 25px"></i>RHYTHMIX</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :class="{ 'active': this.$route.name == 'Home' }" class="nav-link"
                :to="{ name: 'Home' }">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link :class="{ 'active': this.$route.name == 'newReleases' }" class="nav-link"
                :to="{ name: 'newReleases' }">New Releases</router-link>
            </li>
            <li class="nav-item dropdown">
              <a :class="{ 'active': this.$route.name == 'userPlaylists' || this.$route.name == 'userPlaylists' }"
                class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Library
              </a>
              <ul class="dropdown-menu">
                <li><router-link class="dropdown-item" :to="{ name: 'userPlaylists' }">Playists</router-link></li>
                <li><router-link class="dropdown-item" :to="{ name: 'likedSongs' }">Liked Songs</router-link></li>
                <li><router-link class="dropdown-item" :to="{ name: 'followingArtists' }">Following Artists</router-link></li>
              </ul>
            </li>
          </ul>
          <form @submit.prevent="search" class="d-flex mx-auto my-2" role="search" name="search_form">
            <input v-model="query" class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
              name="query" id="query" />
            <button class="btn btn-outline-light" type="submit">
              <i class="fa-solid fa-magnifying-glass"></i>
            </button>
          </form>
          <ul class="navbar-nav ms-auto">
            <li v-show="role === 'creator'" class="nav-item dropdown">
              <a :class="{ 'active': this.$route.name == 'creatorAlbums' || this.$route.name == 'creatorSongs' || this.$route.name == 'creatorPage' }"
                class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Creator Account
              </a>
              <ul class="dropdown-menu">
                <li><router-link class="dropdown-item" :to="{ name: 'creatorPage' }">Dashboard</router-link></li>
                <li><router-link class="dropdown-item" :to="{ name: 'creatorSongs' }">Your Songs</router-link></li>
                <li><router-link class="dropdown-item" :to="{ name: 'creatorAlbums' }">Your Albums</router-link>
                </li>
              </ul>
            </li>
            <li v-show="role !== 'creator'" class="nav-item">
              <router-link :class="{ 'active': this.$route.name == 'creatorPage' }" class="nav-link"
                :to="{ name: 'creatorPage' }">Creator Account</router-link>
            </li>
            <li class="nav-item">
              <router-link :class="{ 'active': this.$route.name == 'Profile' }" class="nav-link"
                :to="{ name: 'Profile' }">Profile</router-link>
            </li>
            <li class="nav-item">
              <button @click="logout" class="nav-link">Logout<i class="fa-solid fa-right-from-bracket ms-1"></i></button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Navbar',
  data() {
    return {
      role: null,
      showNavbar: false,
      query: null,
      token: null,
      pageReload: false,
    }
  },
  created() {
    this.token = localStorage.getItem('auth-token')
    this.assignRole()
  },
  methods: {
    logout() {
      this.$bvModal.msgBoxConfirm(`It's sad to see you leave.\n Hope to see you soon!`, {
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'Logout',
        cancelTitle: 'Cancel',
        footerClass: 'p-2',
        centered: true,
        noCloseOnBackdrop: true,
        hideHeaderClose: true,
      }).then(value => {
        if (value) {
          this.role = ''
          localStorage.clear()
          axios.get(`http://127.0.0.1:5000/logout`, {
            headers: {
              'Authentication-Token': this.token
            }
          }).then(response => {
            console.log(response)
            this.$router.push('/login')
          }).catch(error => {
            console.log(error)
          })
        } else {
          return null
        }
      })
    },
    search() {
      if (this.token && this.query) {
        this.$router.push({ path: `/search_page/${this.query}` });
        this.query = null
      } else if (!this.query) {
        this.query = null
        return null
      } else {
        this.$router.push('/login')
      }
    },
    assignRole() {
      this.role = localStorage.getItem('user-role')
    }
  },
}
</script>