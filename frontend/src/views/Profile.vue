<template>
    <div class="container content">
        <div class="row d-flex justify-content-around">
            <div class="d-flex">
                <img :src="require(`@/assets/profile_pictures/${profilePicture}`)" :alt="name"
                    class="rounded-circle profile-pic" />
                <div>
                    <p class="fs-1 fw-bolder m-2">{{ name }}</p>
                </div>
            </div>
        </div>
        <hr />
        <div class="row">
            <div class="col-12">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <div class="d-flex align-items-center">
                        <input v-model="username" type="text" class="form-control" id="name" style="width:500px">
                        <button class="btn btn-dark ms-2" type="button" @click="updateName">Update</button>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="name" class="form-label">Email</label>
                    <div class="d-flex align-items-center">
                        <input v-model="email" type="email" class="form-control" id="email" style="width:500px">
                        <button class="btn btn-dark ms-2" type="button" @click="updateEmail">Update</button>
                    </div>
                    <p v-if="emailError" class="text-danger">{{emailError}}</p>
                </div>
                <div class="mb-3">
                    <label for="profile_picture" class="form-label">Profile picture</label>
                    <form @submit.prevent="updateProfilePic" enctype="multipart/form-data" class="d-flex align-items-center">
                        <input class="form-control" type="file" id="profile_picture"
                        accept="image/png, image/jpeg,image/jpg, image/webp" @change="fileChange" style="width:500px">
                        <button class="btn btn-dark ms-2" type="submit">Update</button>
                    </form>
                </div>
            </div>
        </div>
        <hr>
        <a href="/terms&conditions" target="_blank">Company Policy</a>
    </div>
</template>

<script>
import axios from 'axios'
export default{
    data(){
        return{
            token:null,
            username: null,
            name: null,
            profilePicture: null,
            ogEmail: null,
            email: null,
            emailError: null,
        }
    },
    created(){
        this.token = localStorage.getItem('auth-token')
        if (this.token){
            this.getDetails()
        }
        else{
            this.$router.push('/login')
        }
    },
    methods:{
        getDetails(){
            axios.get(`http://127.0.0.1:5000/profile`,{
                headers:{
                    'Authentication-Token': this.token,
                }
            }).then(response=>{
                let details = response.data
                this.name = details.name
                this.username = details.name
                this.email = details.email
                this.ogEmail = details.email
                this.profilePicture = details.profile_picture
            }).catch(error=>{
                console.log(error)
            })
        },
        updateName(){
            const formData = new FormData
            formData.append('name', this.username)
            axios.post(`http://127.0.0.1:5000/profile`,formData,{
                headers:{
                    'Authentication-Token': this.token,
                }
            }).then(response=>{
                window.location.reload()
            }).catch(error=>{
                console.log(error)
            })
        },
        updateEmail(){
            const formData = new FormData
            formData.append('email', this.email)
            axios.post(`http://127.0.0.1:5000/profile`,formData,{
                headers:{
                    'Authentication-Token': this.token,
                }
            }).then(response=>{
                this.emailError= null
                window.location.reload()
            }).catch(error=>{
                this.emailError = error.response.data.message
                this.email = this.ogEmail
                console.log(error)
            })
        },
        fileChange(event) {
            const file = event.target.files[0]
            this.profilePicture = file
        },
        updateProfilePic(){
            const formData = new FormData
            formData.append('profile_picture', this.profilePicture)
            axios.post(`http://127.0.0.1:5000/profile`,formData,{
                headers:{
                    'Authentication-Token': this.token,
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response=>{
                window.location.reload()
            }).catch(error=>{
                console.log(error)
            })
        },
    }
}
</script>