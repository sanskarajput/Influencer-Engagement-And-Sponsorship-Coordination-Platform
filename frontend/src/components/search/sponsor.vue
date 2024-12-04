<template>
    <div v-if="isApproved" class="mt-n3">
        <h2 class="text-gray-800 fs-2 fw-bold" v-if="AllInfluencersBasedOnSearch.length">Found These Influencers...</h2>
        <h1 class="text-center mt-5 text-gray-800 fs-2 fw-bold" v-else>No Influencers Found &#128533;</h1>
    </div>
    <div v-if="isApproved && AllInfluencersBasedOnSearch.length" class="d-flex flex-wrap gap-2 justify-content-evenly">
        <card v-for="(user, index) in AllInfluencersBasedOnSearch" :key="index" profileOf="influencer" :user="user">
        </card>
    </div>
    <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
        <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
        <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
        <span class="fs-5 fw-bold">Then You Can Search.</span><br>
        <span class="fs-1 fw-bold"> &#128591;</span>
    </div>
</template>

<script>
import axios from 'axios';
import card from '@/components/profile/small-card.vue';

export default {
    name: 'Sponsor-Search-Result',
    components: {
        card
    },
    data() {
        return {
            isApproved: false,
            ApprovalDataFetched: false,
            AllInfluencersBasedOnSearch: []
        }
    },
    methods: {
        async fetchAllInfluencersBasedOnSearch() {
            try {
                const response = await axios.get(`${this.$store.state.basePath}/search-by-sponsors`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    },
                    params: {
                        query: this.$route.query.query
                    }
                })

                this.AllInfluencersBasedOnSearch = response.data.db_data;
            } catch (error) {
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
    },
    beforeMount() {
        this.isSponsorApproved();
        // this.fetchAllInfluencersBasedOnSearch();
    },
    watch: {
        '$route.query.query': {
            handler: function () {
                this.fetchAllInfluencersBasedOnSearch();
            },
            immediate: true
        }
    }
}
</script>

<style scoped></style>