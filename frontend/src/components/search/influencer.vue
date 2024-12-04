<template>
    <div class="mt-n3">
        <h2 class="text-gray-800 fs-2 fw-bold" v-if="AllPublicOngoingCampaign.length">Found These Campaigns...</h2>
        <h1 class="text-center mt-5 text-gray-800 fs-2 fw-bold" v-else>No Campaigns Found &#128533;</h1>
    </div>
    <div v-if="AllPublicOngoingCampaign.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
        <card v-for="(campaign, index) in AllPublicOngoingCampaign" :key="index" :campaign="campaign">
        </card>
    </div>
</template>

<script>
import axios from 'axios';
import card from '@/components/campaigns/card.vue';

export default {
    name: 'Influencer-Search-Result',
    components: {
        card
    },
    data() {
        return {
            AllPublicOngoingCampaign: []
        }
    },
    methods: {
        async fetchAllPublicOngoingCampaign() {
            try {
                const response = await axios.get(`${this.$store.state.basePath}/search-by-influencers`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    },
                    params: {
                        query: this.$route.query.query
                    }
                })

                this.AllPublicOngoingCampaign = response.data.db_data;
                // console.log(this.AllPublicOngoingCampaign);
                
            } catch (error) {
                this.$errorComesNow(error);
            }
        }
    },
    beforeMount() {
        // this.fetchAllPublicOngoingCampaign();
    },
    watch: {
        '$route.query.query': {
            handler: function () {
                this.fetchAllPublicOngoingCampaign();
            },
            immediate: true
        }
    }

}
</script>

<style scoped></style>