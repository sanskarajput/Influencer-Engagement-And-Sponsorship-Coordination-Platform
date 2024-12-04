<template>
  <!-- Page Wrapper -->
  <div id="wrapper">
    <!-- Sidebar -->
    <sidebar v-if="$store.getters.isAuthenticated"></sidebar>
    <!-- End of Sidebar -->

    <!-- Content Wrapper -->
    <div id="content-wrapper" class="d-flex flex-column">

      <!-- Main Content -->
      <div id="content">

        <!-- navbar/Topbar -->
        <navbar></navbar>
        <!-- End of navbar/Topbar -->

        <!-- Begin main Content -->
        <div class="container-fluid">
          <router-view></router-view>
        </div>
        <!-- End main Content -->

      </div>
      <!-- End of Main Content -->

      <!-- Footer -->
      <footre class="mt-5"></footre>
      <!-- End of Footer -->

    </div>
    <!-- End of Content Wrapper -->
  </div>
  <!-- End of Page Wrapper -->

  <scrollUpLogout></scrollUpLogout>


</template>

<script>
import sidebar from './components/sidebar.vue';
import scrollUpLogout from './components/scrollUp-logout.vue';
import navbar from './components/navbar.vue';
import footre from './components/footer.vue';


export default {
  name: 'App',
  components: {
    sidebar,
    scrollUpLogout,
    navbar,
    footre
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #000000;
}
</style>