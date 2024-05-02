<template>
    <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" style="font-size: 25px">
                <i class="bi bi-headphones me-2"></i>RHYTHMIX</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link :to="{ name: 'adminDashboard' }"
                            :class="{ 'active': this.$route.name == 'adminDashboard' }" class="nav-link"
                            aria-current="page">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'adminSongs' }"
                            :class="{ 'active': this.$route.name == 'adminSongs' }" class="nav-link">Songs</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'adminAlbums' }"
                            :class="{ 'active': this.$route.name == 'adminAlbums' }"
                            class="nav-link">Albums</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'adminCreators' }"
                            :class="{ 'active': this.$route.name == 'adminCreators' }"
                            class="nav-link">Creators</router-link>
                    </li>
                </ul>
                <form @submit.prevent="search" class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="query"
                        v-model="query" />
                    <button @click="search" class="btn btn-outline-light">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </button>
                </form>
                <li class="nav-item navbar-nav">
                    <a href="/" class="nav-link">Logout <i class="fa-solid fa-right-from-bracket"></i></a>
                </li>
            </div>
        </div>
    </nav>
</template>

<script>

export default {
    name: 'AdminNavbar',
    data() {
        return {
            query: null,
            token: null,
            role: null
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        this.role = localStorage.getItem('user-role')
        if (!this.token || this.role !== 'admin') {
            this.$router.push('/welcome')
        }
    },
    methods: {
        search() {
            if (this.token && this.query) {
                this.$router.push({ path: `/admin_search/${this.query}` });
                this.query = null
            } else if (!this.query) {
                this.query = null
                return null
            } else {
                this.$router.push('/login')
            }
        },
    },
}

</script>