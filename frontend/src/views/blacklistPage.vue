<template>
    <div class=" d-flex flex-column justify-content-between align-items-center container text-center">
        <h3>
            You have been blcklisted by the administrator for violating the company
            policies.
        </h3>
        <p>For more information conatct the administrator.</p>
        <p>
            <a href="/terms&conditions">Click here to read the company policies.</a>
        </p>
    </div>
</template>

<script>
export default {
    name: 'blacklistPage',
    created(){
        localStorage.clear()
    }
}
</script>

<style scoped>
body {
    background-color: black;
}
</style>