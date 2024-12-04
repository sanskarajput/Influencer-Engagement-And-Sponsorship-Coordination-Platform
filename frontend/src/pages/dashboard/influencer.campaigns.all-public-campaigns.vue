<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      All Public And Ongoing Campaigns
    </h1>
  </div>
  <div v-if="campaigns.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
    <card v-for="(campaign, index) in campaigns" :key="index" :campaign="campaign"></card>
  </div>
</template>

<script>
import axios from 'axios';
import card from '@/components/campaigns/card.vue';
export default {
  name: 'Influencer-Campaigns-All-Public-Campaigns',
  components: {
    card
  },
  data() {
    return {
      campaigns: []
    }
  },
  methods: {
    async fetchPublicCampaignData() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/all-public-campaigns`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.campaigns = response.data.db_data;
      } catch (error) {
        console.error('Error fetching campaigns:', error);
        this.$errorComesNow();
      }
    }
  },
  beforeMount() {
    this.fetchPublicCampaignData();
  }
}

</script>

<style scoped></style>