<template>
    <div class="content container">
        <div v-if="artistsData.length==0" class="text-center">
            <h3>
                You are not following any artist!
            </h3>
            <router-link :to="{name:'allArtists'}">Click here to listen to new Artists and follow them!</router-link>
        </div>
        <b-table-simple v-else sticky-header="80vh">
            <b-thead>
                <b-tr>
                    <b-th>#</b-th>
                    <b-th>Name</b-th>
                    <b-th>Rating</b-th>
                </b-tr>
            </b-thead>
            <b-tbody>
                <b-tr v-for="(artist, index) in  artistsData  " :key="artist.id">
                    <b-td>{{ index + 1 }}</b-td>
                    <b-td>
                        <img :src="require(`@/assets/profile_pictures/${artist.profile_picture}`)" class="rounded table-image" />
                        <router-link :to="{ name: 'Artist', params: { id: artist.id } }"
                            class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                            {{ artist.name }}
                        </router-link>
                    </b-td>
                    <b-td>
                        {{ artist.rating }} <i class="fa-solid fa-star"></i>
                    </b-td>
                </b-tr>
            </b-tbody>
        </b-table-simple>
    </div>
</template>

<script>
import axios from 'axios'
export default{
    name:'followingArtists',
    data(){
        return {
            token:null,
            artistsData: [],
        }
    },
    created() {
        this.token = localStorage.getItem('auth-token')
        console.log(this.token)
        if (this.token) {
            this.getArtists()
        }
        else {
            this.$router.push('/login')
        }
    },
    methods:{
        getArtists(){
            axios.get(`http://127.0.0.1:5000/following_artists`,{
                headers:{
                    'Authentication-Token':this.token,
                }
            }).then(response=>{
                this.artistsData = response.data
            }).catch(error=>{
                console.log(error)
            })
        }
    }
}
</script>