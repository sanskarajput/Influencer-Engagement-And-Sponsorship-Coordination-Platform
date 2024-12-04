<template>
  <div class="text-center">
    <div class="error mx-auto" data-text="401">401</div>
    <p class="lead text-gray-800 mb-5">User Login Required</p>
    <p class="text-gray-500 mb-0">You need to login to access this page...</p>
    <router-link to="/login">&larr; Back to Login</router-link>
  </div>

</template>

<script>
export default {
  name: 'Unauthorized-Error',
  mounted() {
    document.title = 'Unauthorized-Error';
  }
}
</script>

<style scoped></style>