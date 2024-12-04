  <template>
    <div class="image">
    </div>
    <div class="text-center fw-bold mt-1">Welcome To !</div>
    <div class="text-center fw-bold mt-1">Influencer-Engagement-And-Sponsorship-Coordination-Platform</div>
  </template>

<script>
export default {
  name: 'HomePage',
  mounted() {
    document.title = 'Home';
  }

}
</script>

<style scoped>
.image {
  background-image: url('@/assets/welcome.jpg');
  background-size: contain;
  background-position: center;
  height: 40vh;
  position: relative;
  margin: 0%;
  border-radius: 10px;
}

.text-center {
  color: rgb(0, 0, 0);
  font-size: 55px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 1px;
}
</style>