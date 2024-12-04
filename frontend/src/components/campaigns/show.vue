<template>
    <div class="row">
        <div class="px-1 mb-md-0" :class="!accordionVisible ? 'col' : 'col-md-8'">
            <div class="row">
                <p class="col-12 fs-1 text-center text-gray-800 fs-2 fw-bold">Campaign Details</p>
                <div class="col-12">
                    <card v-if="campaign.dataFetched && allAccordionData" :mainCampaign="campaign"
                        :request="allAccordionData[0]" :accordionVisible="accordionVisible">
                    </card>
                </div>
            </div>
        </div>
        <div v-if="accordionVisible" class="col-md-4 px-2 pt-5 pt-md-0 animation-right-to-left">
            <div class="row">
                <div class="col-12 fs-1 text-center text-black fw-bold mb-3">
                    <div class="row text-gray-800 fs-2 fw-bold">
                        <div class="col-10 pl-8">
                            {{ $store.getters.role === 'sponsor' ? 'All Influencers' : $store.getters.role === 'admin' ? 'Requests Status' : 'Request Status' }}
                        </div>
                        <div class="col-2">
                            <i class="fa-solid fa-xmark cross"
                                @click="$router.push({ name: 'each-campaign-details', query: { show: campaign_id } })"></i>
                        </div>
                    </div>
                </div>
                <template v-if="campaign.dataFetched && allAccordionData">
                    <div v-if="allAccordionData.length" class="accordion" id="accordionExample">
                        <accordion v-for="(each_Role_Details_With_Request, index) in allAccordionData" :key="index"
                            :each_Role_Details_With_Request="each_Role_Details_With_Request" :index="index"
                            :campaign_id="campaign_id"
                            @refresh-show-component-to-fetchAccordionData="$emit('refresh-show-component-to-fetchAccordionData')">
                        </accordion>
                    </div>
                    <div v-else class="text-center mt-5">
                        No 
                        <span v-if="$store.getters.role === 'sponsor'">Influencers found.</span>
                        <span v-if="$store.getters.role === 'admin'">Requests found with this Campaign.</span>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import card from "./detailed-card.vue";
import accordion from "./accordion.vue";

export default {
    name: 'Show-Campaign',
    components: {
        card,
        accordion
    },
    props: {
        campaign_id: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            campaign: {
                dataFetched: false,

                campaign_id: null,
                title: null,
                category: null,
                budget: null,
                visibility: null,
                description: null,
                goals: null,
                flagged: null,
                start_date: null,
                end_date: null,
                time: null,
                campaigner: null,
                campaigner_s_user_id: null,

                status: null,
                duration: null,
                imageUrl: null,
                stats: null,
                progress: null,
            },
            allAccordionData: null,
            accordionVisible: false
        }
    },
    methods: {
        async fetchAccordionData() {
            try {
                // Dynamically creating the URL based on the user's role
                let url = `${this.$store.state.basePath}`;
                if (this.$store.getters.role === 'sponsor') {
                    url += `/all-influencers-for-each-campaign-page/${this.campaign_id}`;
                } else if (this.$store.getters.role === 'influencer') {
                    url += `/request-with-this-campaign/${this.campaign_id}/${this.$store.getters.role_id}`;
                } else if (this.$store.getters.role === 'admin') {
                    url += `/all-requests-with-this-campaign/${this.campaign_id}`;
                }

                // Make the API request
                const response = await axios.get(url, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    }
                });

                this.allAccordionData = response.data.db_data;
                // console.log(this.allAccordionData);

                // Logic to display influencers in accordion
            } catch (error) {
                this.$errorComesNow(error);
            }
        },
        async fetchData() {
            try {
                const response = await axios.get(`${this.$store.state.basePath}/campaign/${this.campaign_id}`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );
                const data = response.data.db_data;

                this.campaign.campaign_id = data.id;
                this.campaign.title = data.name;
                this.campaign.description = data.description;
                this.campaign.category = data.category;
                this.campaign.start_date = data.start_date;
                this.campaign.end_date = data.end_date;
                this.campaign.budget = data.budget;
                this.campaign.visibility = data.visibility;
                this.campaign.goals = data.goals;
                this.campaign.flagged = data.flagged;
                this.campaign.time = data.time;
                this.campaign.campaigner = data.campaigner;
                this.campaign.campaigner_s_user_id = data.campaigner_s_user_id;

                this.campaign.status = this.$forStatus(data.start_date, data.end_date);
                this.campaign.duration = this.$formatDateRange(data.start_date, data.end_date);
                this.campaign.imageUrl = 'https://via.placeholder.com/150',
                    this.campaign.progress = 75,
                    this.campaign.stats = [
                        { label: 'Reach', value: '15.2k' },
                        { label: 'Clicks', value: '1.8k' },
                        { label: 'CTR', value: '11.8%' }
                    ]

                this.campaign.dataFetched = true;
            } catch (error) {
                this.$errorComesNow(error);
            }
        },
    },

    beforeMount() {
        this.fetchData().then(() => {
            this.fetchAccordionData();
        })
    },
    watch: {
        '$route.query': {
            immediate: true,
            handler(newQuery) {
                if (newQuery['show-request-details'] == 'true' || newQuery['show-all-influencers'] == 'true') {
                    this.accordionVisible = true;
                } else {
                    this.accordionVisible = false;
                }
            }
        },
        'accordionVisible': {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.fetchAccordionData();
                }
            }
        }
    }
}
</script>


<style scoped>
.animation-right-to-left{
    animation: slideRight 1s ease-in-out;
}

@keyframes slideRight {
    0% {
        transform: translateX(100%);
    }
    100% {
        transform: translateX(0);
    }
}

.main-shirnk {
    transition: all 1s ease-in-out;
}

.mx-8 {
    margin-right: 7%;
    margin-left: 7%;
}

.pl-8 {
    padding-left: 20%;
}

.cross {
    cursor: pointer;
    font-size: 20px;
}
</style>