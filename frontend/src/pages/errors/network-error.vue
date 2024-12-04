<template>
  <div class="text-center">
    <div class="error mx-auto" data-text="500">500</div>
    <p class="lead text-gray-800 mb-5">Network Error</p>
    <p class="text-gray-500 mb-0">So, Sorry for the Inconvenience, we are working on it, and will be available soon...</p>
    <router-link to="/dashboard">&larr; Back to Dashboard</router-link>
  </div>

</template>

<script>
export default {
  name: 'Network-Error',
  mounted() {
    document.title = 'Network-Error';
  }
}
</script>

<style scoped></style>