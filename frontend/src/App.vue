<template>
  <div id="app">
    <AdminNavbar v-if="this.$route.name.startsWith('admin')" />
    <Navbar v-else />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import AdminNavbar from './components/AdminNavbar.vue';
export default {
  components: {
    Navbar,
    AdminNavbar
  }
}
</script>

