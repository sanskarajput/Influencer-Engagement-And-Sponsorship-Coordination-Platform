<template>
  <div v-if="isApproved" class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      All Influencers
    </h1>
  </div>
  <div v-if="isApproved && influencers.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
    <card v-for="(user, index) in influencers" :key="index" profileOf="influencer" :user="user"></card>
  </div>
  <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
    <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
    <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
    <span class="fs-5 fw-bold">Then You Can See All Influencers.</span><br>
    <span class="fs-1 fw-bold"> &#128591;</span>
  </div>
</template>

<script>
import axios from 'axios';
import card from '@/components/profile/small-card.vue';
export default {
  name: 'All-Influencers',

  components: {
    card
  },
  data() {
    return {
      isApproved: false,
      ApprovalDataFetched: false,
      influencers: []
    }
  },
  methods: {
    async fetchInfluencersProfile() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/all-influencers-profiles`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.influencers = response.data.db_data;
      } catch (error) {
        console.error('Error fetching Influencers:', error);
        this.$errorComesNow(error);
      }
    },
    async isSponsorApproved() {
      try {
        const response = await axios.get(
          `${this.$store.state.basePath}/sponsor/is-approved/${this.$store.getters.role_id}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );

        this.isApproved = response.data.db_data.isApproved;
        this.ApprovalDataFetched = true;
      } catch (error) {
        this.$errorComesNow(error);
      }
    },
    async callBoth() {
      if (this.$store.getters.role === 'sponsor') {
        await this.isSponsorApproved();
      } else {
        this.isApproved = true;
        this.ApprovalDataFetched = true;
      }
      if (this.isApproved) {
        await this.fetchInfluencersProfile();
      }
    }
  },
  beforeMount() {
    this.callBoth();
  }


}

</script>

<style scoped></style>