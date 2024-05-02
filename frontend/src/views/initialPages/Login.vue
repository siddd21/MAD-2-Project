<template>
    <div class="container">
        <div class="row center-box text-white">
            <div class="col-md-4 rounded bg-dark">
                <div class="p-4">
                    <div class="text-center">
                        <h3>Login</h3>
                    </div>
                    <form @submit.prevent="login">
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="username" name="username" required
                                v-model="email" />
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" name="password" required
                                v-model="password" />
                        </div>
                        <div v-if="message" class="text-danger">
                            {{ message }}
                        </div>
                        <div class="text-center">
                            <button type="submit" class="btn btn-outline-light text-center">
                                Start Listening
                            </button>
                        </div>
                    </form>
                    <br />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Login",
    data() {
        return {
            email: null,
            passowrd: null,
            message: null,
        }
    },
    methods: {
        login() {
            axios.post('http://127.0.0.1:5000/user_login', {
                email: this.email,
                password: this.password,
            })
                .then(response => {
                    if (response.data.blacklisted) {
                        axios.get(`http://127.0.0.1:5000/logout`, {
                            headers: {
                                'Authentication-Token': response.data.token,
                            }
                        }).then(response => {
                            this.$router.push('/blacklist_page')
                        })
                    }
                    localStorage.setItem('auth-token', response.data.token)
                    localStorage.setItem('user-role', response.data.role)
                    if (!response.data.blacklisted){
                        localStorage.setItem('reload', 1)
                    }
                    if (response.data.role == 'admin') {
                        this.$router.push({ name: 'adminDashboard' })
                    } else {
                        this.$router.push({ name: 'Home' })
                    }
                })
                .catch(error => {
                    this.message = error.message
                    console.log(error)
                })

        }
    }
}
</script>