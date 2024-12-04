<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      {{ $capitalize($route.params.role) }} Profile
    </h1>
  </div>
  <card v-if="user" :profileOf="$route.params.role" :user="user"></card>
</template>

<script>
import axios from 'axios';
import card from '@/components/profile/big-card.vue';

export default {
  name: 'Other-User-Profile-View',
  components: {
    card
  },
  data() {
    return {
      user: null
    }
  },
  methods: {
    async fetchOtherUserDetails() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/${this.$route.params.role}-details/${this.$route.query.user_id}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.user = response.data.db_data;
      } catch (error) {
        console.error('Error fetching User Details:', error);
        this.$errorComesNow();
      }
    }
  },
  beforeMount() {
    this.fetchOtherUserDetails();
  }

}
</script>

<style scoped></style>