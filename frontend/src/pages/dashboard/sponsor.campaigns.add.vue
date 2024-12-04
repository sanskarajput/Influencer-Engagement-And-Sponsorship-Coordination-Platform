<template>
  <addNewCampaign v-if="isApproved"></addNewCampaign>
  <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
    <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
    <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
    <span class="fs-5 fw-bold">Then You Can Add Campaign.</span><br>
    <span class="fs-1 fw-bold"> &#128591;</span>
  </div>
</template>

<script>
import axios from 'axios';
import addNewCampaign from '@/components/campaigns/add.vue'
export default {
  name: 'Sponsor-Campaigns-Add',
  components: {
    addNewCampaign,
  },
  data() {
    return {
      isApproved: false,
      ApprovalDataFetched: false,
    }
  },
  methods: {
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
    }
  },
  beforeMount() {
    this.isSponsorApproved();
  },
  mounted() {
    document.title = "Add Campaign";
  }

}
</script>

<style scoped></style>