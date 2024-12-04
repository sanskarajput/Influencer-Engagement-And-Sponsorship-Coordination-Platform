<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      All Sponsors
    </h1>
  </div>
  <div v-if="sponsors.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
    <card v-for="(user, index) in sponsors" :key="index" profileOf="sponsor" :user="user"></card>
  </div>
</template>

<script>
import axios from 'axios';
import card from '@/components/profile/small-card.vue';
export default {
  name: 'All-Sponsors',
  components: {
    card
  },
  data() {
    return {
      sponsors: []
    }
  },
  methods: {
    async fetchSponsorsProfile() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/all-sponsors-profiles`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.sponsors = response.data.db_data;
      } catch (error) {
        console.error('Error fetching Sponsors:', error);
        this.$errorComesNow(error);
      }
    }
  },
  beforeMount() {
    this.fetchSponsorsProfile();
  }
}

</script>

<style scoped></style>