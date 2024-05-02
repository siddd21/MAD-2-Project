<template>
    <div class="container">
        <div class="row center-box">
            <div class="col-md-4 rounded bg-light">
                <div class="p-4">
                    <div class="text-center">
                        <h3>Register</h3>
                    </div>
                    <form @submit.prevent="register" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="name" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required v-model="email" />
                        </div>
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" name="name" v-model="name" />
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" name="password" v-model="password" />
                        </div>
                        <div class="mb-3">
                            <label for="profile_pic" class="form-label">Want to upload your profile picture?</label>
                            <input class="form-control" type="file" id="profile_pic" name="profile_pic"
                                accept="image/png, image/jpeg, image/webp" @change="fileChange" />
                        </div>
                        <div class="text-danger text-center" v-if="message">
                            {{ message }}
                        </div>
                        <div class="text-center">
                            <button type="submit" class="btn btn-dark">Register</button>
                        </div>
                    </form>
                    <br />
                    <!-- <div class="text-center">
                        <a href="/login" class="link-opacity-50-hover">Already a user? Login here!</a>
                    </div> -->
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'Register',
    data() {
        return {
            email: null,
            name: null,
            password: null,
            profile_pic: null,
            message: null,
        }
    },
    methods: {
        fileChange(event) {
            const file = event.target.files[0]
            this.profile_pic = file
        },
        register(event) {
            event.preventDefault()
            const formData = new FormData
            formData.append('email', this.email)
            formData.append('name', this.name)
            formData.append('password', this.password)
            formData.append('profile_pic', this.profile_pic)
            axios.post('http://127.0.0.1:5000/register', formData)
                .then(response => {
                    this.message = response.data.message
                    console.log(response.data)
                    this.$router.push({ name: 'Login' })
                })
                .catch(error => {
                    this.message = error.response.data.message
                    console.log(error.response)
                })

        }
    }
}

</script>