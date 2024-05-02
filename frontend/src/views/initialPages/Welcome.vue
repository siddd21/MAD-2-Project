<template>
    <div class="container">
        <div class="row center-box">
            <div class="col-md-5 rounded bg-light">
                <div class="text-center p-4">
                    <h3>Welcome to Rhythmix</h3>
                    <br />
                    <br />
                    <div class="d-grid gap-2 col-6 mx-auto">
                        <h5>Log in to start listening</h5>
                        <a href="/login" class="btn btn-dark">Login</a>
                        <RouterLink :to="{ name: 'Login' }"></RouterLink>
                        <br />
                        Don't have an account?
                        <a href="/register" class="btn btn-dark">Register here </a>
                        <RouterLink :to="{ name: 'Register' }"></RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Welcome",
}
</script>