<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">
        Sponsor's Approval Requests
      </h1>
    </div>
  <div v-if="sponsors.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
    <cardForSponsorRequest v-for="(user, index) in sponsors" :key="index" :user="user"></cardForSponsorRequest>
  </div>
  <div v-else>
    <p class="text-center">No sponsor's approval requests found.</p>
  </div>
</template>

<script>
import axios from 'axios';
import cardForSponsorRequest from '../profile/card-for-sponsor-request.vue';
export default {
  name: 'Admin-Notifications',
  components: {
    cardForSponsorRequest
  }, 
  data() {
    return {
      sponsors: []
    }
  },
  methods: {
    async fetchSponsorsProfileApprovalRequests() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/sponsor-approval-requests`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.sponsors = response.data.db_data;
        // console.log(this.sponsors);
        
      } catch (error) {
        console.error('Error fetching Sponsors:', error);
        this.$errorComesNow(error);
      }
    }
  },
  beforeMount() {
    this.fetchSponsorsProfileApprovalRequests();
  }
}

</script>

<style scoped></style>