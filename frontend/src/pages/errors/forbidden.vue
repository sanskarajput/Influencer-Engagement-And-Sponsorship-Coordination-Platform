<template>
  <div class="text-center">
    <div class="error mx-auto" data-text="403">403</div>
    <p class="lead text-gray-800 mb-5">Forbidden</p>
    <p class="text-gray-500 mb-0">You don't have permission to access this page...</p>
    <router-link to="/dashboard">&larr; Back to Dashboard</router-link>
  </div>

</template>

<script>
export default {
  name: 'Forbidden-Error',
  mounted() {
    document.title = 'Forbidden-Error';
  }

}
</script>

<style scoped></style>