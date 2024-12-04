<template>
    <div v-if="localUser.approved != 'TRUE'" class="compact-profile">
        <div class="profile-header">
            <div class="avatar-container">
                <router-link
                    :to="{ name: 'other-user-profile-view', params: { role: 'sponsor' }, query: { user_id: localUser.sponsor_s_user_id } }">
                    <img :src="localUser.avatar ? `data:image/png;base64,${localUser.avatar}` : require('@/assets/profile-user.png')"
                        :alt="localUser.name" class="avatar" />
                </router-link>
                <div class="type-badge"
                    :class="{ 'company': localUser.type == 'Company', 'individual': localUser.type == 'Individual' }">
                    {{ localUser.type }}
                </div>
            </div>

            <div class="profile-summary">
                <h3 class="name">{{ localUser.name }}</h3>
                <p class="username">@{{ localUser.username }}</p>
            </div>
        </div>

        <div class="profile-details">
            <div class="detail">
                <span class="detail-icon">📧</span>
                <span class="detail-text">{{ localUser.email }}</span>
            </div>
            <div class="detail">
                <span class="detail-icon">💼</span>
                <span class="detail-text">{{ localUser.industry }}</span>
            </div>
            <div class="detail">
                <span class="detail-icon">💰</span>
                <span class="detail-text">{{ localUser.budget }}</span>
            </div>
        </div>
        <div class="description-details">
            <div class="detail">
                <span class="detail-icon">📧</span>
                <span class="description-text">{{ localUser.description }}</span>
            </div>
        </div>

        <div class="profile-actions">
            <button class="btn btn-reject" @click="buttonClicked('FALSE')" :disabled="localUser.approved == 'TRUE'">
                Reject
            </button>
            <button class="btn btn-approve" @click="buttonClicked('TRUE')" :disabled="localUser.approved == 'TRUE'">
                Approve
            </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'CompactProfileCard',
    props: {
        user: {
            type: Object,
            required: true,
        }
    },
    data() {
        return {
            localUser: {...this.user}
        }
    },
    methods: {
        async buttonClicked(value) {
            // validate value
            if (value!== 'TRUE' && value!== 'FALSE') {
                console.error('Invalid value provided for approval status');
                return;
            }

            try {
                const response = await axios.post(`${this.$store.state.basePath}/sponsor-approval/${this.localUser.sponsor_id}`,
                    {
                        status: value
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );
                console.log('Approval status updated:', response.data)
                this.localUser.approved = value; 
            } catch (error) {
                console.error('Error updating approval status:', error);
                this.$errorComesNow(error);
            }
        }
    }
}
</script>

<style scoped>
.compact-profile {
    --primary-color: #000000;
    --secondary-color: #718096;
    --border-color: #e2e8f0;

    width: 250px;
    border: 1.5px solid var(--border-color);
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    padding: 16px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    transition: all 0.2s ease-in-out;
    background: linear-gradient(45deg,
            hsl(240deg 47% 94%) 0%,
            hsl(311deg 80% 95%) 12%,
            hsl(347deg 100% 95%) 21%,
            hsl(29deg 100% 92%) 27%,
            hsl(50deg 100% 89%) 33%,
            hsl(48deg 100% 89%) 38%,
            hsl(37deg 100% 91%) 44%,
            hsl(24deg 100% 92%) 50%,
            hsl(9deg 100% 94%) 56%,
            hsl(6deg 81% 93%) 64%,
            hsl(21deg 100% 91%) 72%,
            hsl(37deg 81% 88%) 81%,
            hsl(64deg 51% 84%) 90%,
            hsl(109deg 61% 86%) 100%);
}

.compact-profile:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.avatar-container {
    position: relative;
    margin-right: 12px;
}

.avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid var(--primary-color);
}

.type-badge {
    position: absolute;
    bottom: -18px;
    border-radius: 5px;
    padding: 0 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: bold;
}

.type-badge.individual {
    background-color: #fbbf24;
    color: white;
}

.type-badge.company {
    background-color: #48bb78;
    color: white;
}

.profile-summary {
    flex-grow: 1;
}

.name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: 4px;
    line-height: 1.2;
}

.username {
    font-size: 0.8rem;
    color: var(--secondary-color);
    margin: 0;
}

.profile-details {
    background-color: #ecf5fb;
    border-radius: 8px;
    padding: 12px;
    margin: 24px auto 8px auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.description-details {
    background-color: #ecf5fb;
    border-radius: 8px;
    padding: 12px;
    margin: 8px auto 14px auto;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.detail {
    display: flex;
    align-items: center;
    margin-bottom: 3px;
    font-size: 0.8rem;
}

.detail:last-child {
    margin-bottom: 0;
}

.detail-icon {
    margin-right: 8px;
    opacity: 1;
    font-size: 1rem;
}

.detail-text {
    color: var(--primary-color);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.description-text {
    color: var(--primary-color);
    line-height: 1.6;
    font-size: 0.8rem;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

.profile-actions {
    display: flex;
    gap: 8px;
}

.btn {
    flex-grow: 1;
    padding: 8px;
    border: none;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-reject {
    background-color: #f94141;
    color: white;
}

.btn-approve {
    background-color: #06d75d;
    color: white;
}

.btn:disabled {
    background-color: #cbd5e0;
    cursor: not-allowed;
}

.btn:hover:not(:disabled) {
    opacity: 0.9;
    transform: translateY(-2px);
}

@media (max-width: 320px) {
    .compact-profile {
        width: 100%;
        max-width: 280px;
    }

    .profile-header {
        flex-direction: column;
        text-align: center;
    }

    .avatar-container {
        margin-right: 0;
        margin-bottom: 12px;
    }

    .profile-actions {
        flex-direction: column;
    }
}
</style>
