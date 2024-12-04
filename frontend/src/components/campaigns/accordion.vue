<template>
    <div class="accordion-item border-0 bg-transparent mb-1">
        <h2 class="accordion-header gradient">
            <div class="container">
                <div class="profile-container">
                    <router-link
                        :to="{ name: 'other-user-profile-view', params:{ role: for_profile_view.params.role }, query: { user_id: entry[for_profile_view.query.user_id] } }">
                        <img class="profile-avatar" :src="entry.avatar ? `data:image/png;base64,${entry.avatar}` : require('@/assets/profile-user.png')" :alt="entry[$store.getters.role === 'influencer' ? 'sponsor_username' : 'influencer_username']">
                    </router-link>
                    <div class="profile-info">
                        <div class="username fw-bold">
                            <router-link class="username-text"
                                :to="{ name: 'other-user-profile-view', params:{ role: for_profile_view.params.role }, query: { user_id: entry[for_profile_view.query.user_id] } }">
                                <span class="text-danger">
                                    {{ 
                                        $store.getters.role === 'influencer' ? 'Sponsor : ' : ''
                                    }}
                                </span>
                                <b>@</b>{{
                                    entry[$store.getters.role === 'sponsor' ? 'influencer_username' : 'sponsor_username']
                                }}
                            </router-link>
                        </div>
                        <div v-if="$store.getters.role === 'sponsor'" class="category">{{ entry.influencer_category }}
                        </div>
                    </div>
                    <div class="action-container">
                        <button class="request-btn btn fw-bold"
                            :class="[entry.requestExist ? 'border-0 disabled' : 'btn-outline-success border-2 text-black me-3']"
                            :disabled="entry.requestExist"
                            @click="!entry.requestExist && handleRequest(campaign_id, entry.influencer_s_user_id)">
                            {{ entry.requestExist ? `Requested ${$forCreatedAtShort(entry.time)}` : `Request` }}
                        </button>
                    </div>
                </div>
                <button v-if="entry.requestExist" class="accordion-button collapsed" type="button"
                    data-bs-toggle="collapse" :data-bs-target="`#collapse${index}`" aria-expanded="false"
                    :aria-controls="`collapse${index}`">
                </button>
            </div>
        </h2>
        <div v-if="entry.requestExist" :id="`collapse${index}`" class="accordion-collapse collapse"
            data-bs-parent="#accordionExample">
            <div class="accordion-body" style="padding: 5px;">
                <requestBody :request="entry"
                    @refresh-show-component-to-fetchAccordionData="$emit('refresh-show-component-to-fetchAccordionData')">
                </requestBody>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import requestBody from '@/components/requests/card-small.vue'


export default {
    name: 'Influ-Accordion',
    components: {
        requestBody,
    },
    props: {
        each_Role_Details_With_Request: {
            type: Object,
            required: true
        },
        index: {
            type: Number,
            required: true
        },
        campaign_id: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            entry: { ...this.each_Role_Details_With_Request }
        };
    },
    methods: {
        async handleRequest(campaign_id, influencer_s_user_id) {
            try {
                const response = await axios.post(`${this.$store.state.basePath}/request/create`,
                    {
                        campaign_id: campaign_id,
                        influencer_s_user_id: influencer_s_user_id
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );
                const data = response.data.db_data;
                // console.log(data);
                this.entry = data;

            } catch (error) {
                this.$errorComesNow(error);
            }
        }
    },
    computed:{
        for_profile_view() {
            if (this.$store.getters.role === 'sponsor') {
                return {
                    params: { role: 'influencer' },
                    query: { user_id: 'influencer_s_user_id' }
                }
            } else if (this.$store.getters.role === 'influencer') {
                return {
                    params: { role: 'sponsor' },
                    query: { user_id: 'sponsor_s_user_id' }
                }
            } else if (this.$store.getters.role === 'admin') {
                return {
                    params: { role: 'influencer' },
                    query: { user_id: 'influencer_s_user_id' }
                }
            }
            return {}
        }
    },
    mounted() {
        
    }
}
</script>

<style scoped>
.accordion-header {
    position: relative;
    background: #fff;
    border-radius: 16px 16px 0 0;
}

.profile-container {
    padding: .8rem 0rem;
    margin: 0rem -1rem 0rem -.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: nowrap;
}

.profile-avatar {
    width: 40px;
    height: 40px;
    background-color: #e9ecef;
    border-radius: 50%;
    min-width: 40px;
    border: 0.12rem solid black;
}

.profile-info {
    flex-grow: 1;
    min-width: 0;
}

.username {
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.username-text {
    color: black;
    text-decoration: none;
}

.category {
    font-size: clamp(0.75rem, 1.5vw, 0.875rem);
    color: #6c757d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #575757;
}

.action-container {
    text-align: right;
    min-width: fit-content;
    margin-right: 1.5rem;
}

.request-btn {
    font-size: clamp(0.75rem, 0vw, 0.875rem);
    padding: clamp(0.25rem, .3vw, 0.5rem) clamp(0.5rem, 1vw, 1rem);
    white-space: nowrap;
    border-radius: 5px;
    margin-bottom: 5px;
}

.btn-outline-success {
    border-color: yellowgreen;
    transition: all 0.3s ease-in-out;
}

.btn-outline-success:hover {
    /* border-color: #50c878; */
    transform: scale(1.1);
    border-color: black;
    background-color: yellowgreen;
}

.timestamp {
    font-size: clamp(0.65rem, 1.2vw, 0.75rem);
    color: #6c757d;
    margin-top: 0.25rem;
    text-align: center;
    white-space: nowrap;
}

.accordion-button {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 3rem;
    padding: 0;
    justify-content: center;
    border: none;
    background: transparent;
}

.accordion-button::after {
    margin: 0;
}

.accordion-button:not(.collapsed)::after {
    transform: rotate(-180deg);
}

@media (max-width: 576px) {
    .profile-container {
        padding: 0.75rem;
        gap: 0.75rem;
    }

    .profile-avatar {
        width: 40px;
        height: 40px;
        min-width: 40px;
    }
}

@media (max-width: 400px) {
    .profile-container {
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .request-btn {
        padding: 0.25rem 0.5rem;
    }
}

.disabled {
    cursor: not-allowed;
}

.gradient {
    background: linear-gradient(135deg,
            #c850c8 0%,
            #4a90e2 100%),
        linear-gradient(180deg,
            #000000 0%,
            #f3ebeb 100%);
    background-blend-mode: screen;
    ;
}
</style>