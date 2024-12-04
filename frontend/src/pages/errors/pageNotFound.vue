<template>
  <div class="text-center">
    <div class="error mx-auto" data-text="404">404</div>
    <p class="lead text-gray-800 mb-5">Page Not Found</p>
    <p class="text-gray-500 mb-0">It looks like you are trying to found a page that doesn't exist...</p>
    <router-link to="/dashboard">&larr; Back to Dashboard</router-link>
  </div>

</template>

<script>
export default {
  name: 'Page-Not-Found-Error',
  mounted() {
    document.title = 'Page-Not-Found';
  }
}
</script>

<style scoped></style>