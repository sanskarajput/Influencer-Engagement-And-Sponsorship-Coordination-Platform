<template>
  <div class="profile-container animation-small-to-original">
    <div class="profile-card">
      <div class="profile-header">
        <div class="avatar-section">
          <img :src="user.avatar ? `data:image/png;base64,${user.avatar}` : require('@/assets/profile-user.png')"
            :alt="user.name" class="profile-avatar">
          <!-- <div v-if="user.isActive" class="active-badge"></div> -->
        </div>

        <div class="user-details">
          <h2 class="text-black">{{ user.name }}</h2>
          <p class="username">
            @{{ user.username }}
            <i v-if="profileOf === 'influencer' && user.isActive" class="fas fa-circle-check verified-badge fs-6"></i>
            <i v-if="profileOf === 'sponsor' && user.isApproved === 'TRUE'"
              class="fas fa-check-circle verified-badge fs-6"></i>
          </p>


          <div class="profile-badges" v-if="profileOf === 'sponsor'">
            <span v-if="user.type === 'Individual'" class="badge">Individual</span>
            <span v-else-if="user.type === 'Company'" class="badge">Company</span>
          </div>
        </div>
      </div>

      <div class="profile-content">

        <div class="profile-meta">
          <div v-if="profileOf === 'influencer'" class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Niche</span>
              <span :class="{ 'meta-value': user.niche }">{{ user.niche || 'Not specified' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Category</span>
              <span :class="{ 'meta-value': user.category }">{{ user.category || 'Not specified' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Email</span>
              <span :class="{ 'meta-value': user.email }">{{ user.email || 'Not specified' }}</span>
            </div>
          </div>

          <div v-if="profileOf === 'sponsor'" class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Industry</span>
              <span :class="{ 'meta-value': user.industry }">{{ user.industry || 'Not specified' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Budget</span>
              <span :class="{ 'meta-value': user.budget }">{{ user.budget ? `₹ ${user.budget}.00` : 'Not specified'
                }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Email</span>
              <span :class="{ 'meta-value': user.email }">{{ user.email || 'Not specified' }}</span>
            </div>
          </div>
        </div>

        <div class="description">
          <span class="meta-label">Description</span>
          <p>{{ user.description || 'No description available' }}</p>
        </div>

        <div v-if="profileOf === 'influencer'" class="social-links">
          <p v-if="!parsedLinks.length" class="text-muted fs-8 mb-3">{{ 'Links : will update soon....' }}</p>
          <a v-for="(link, index) in parsedLinks" :key="index" :href="link.url" :class="link.platform" target="_blank"
            v-show="!!link.url">
            <i class="fab fa-lg"
              :class="link.platform === 'facebook' ? `fa-${link.platform}-f` : `fa-${link.platform}`"></i>
          </a>
        </div>

        <div class="profile-stats">
          <div v-for="(stat, label) in stats" :key="label" class="stat-item">
            <span class="stat-value">{{ stat }}</span>
            <span class="stat-label">{{ label }}</span>
          </div>
          <div v-if="profileOf === 'influencer'" class="stat-item">
            <span class="stat-value">{{ user.reach || 'N/A' }}</span>
            <span class="stat-label">Reach</span>
          </div>
        </div>

        <div class="profile-actions" v-if="$store.getters.role === 'admin' && profileOf === 'sponsor'">
          <button class="btn btn-reject" @click="buttonClicked('FALSE')" :disabled="user.isApproved == 'FALSE'">
            Disapprove
          </button>
          <button class="btn btn-approve" @click="buttonClicked('TRUE')" :disabled="user.isApproved == 'TRUE'">
            Approve
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HorizontalProfileCard',
  props: {
    user: {
      type: Object,
      required: true,
      /*
      default: () => ({
        role_id : 2,
        role_s_user_id : 2,
        name: 'Alex Rodriguez',
        username: 'alex_pro_creator',

        niche: 'Digital Creator & Lifestyle Influencer',
        category: 'Digital Creator & Lifestyle',
        reach : 2322,
        link: "[{ platform: 'linkedin', url: 'https://linkedin.com' }, { platform: 'twitter', url: 'https://twitter.com' }]",
        
        type: "Individual",
        industry: 'industry',
        budget: "budget",
        description: 'Passionate technologist bridging innovation and storytelling.',

        email: 'alex@example.com',
        isActive: true,
      })
      */
    },
    profileOf: {
      type: String,
      required: true,
      validator: value => ['influencer', 'sponsor'].includes(value)
    },
    stats: {
      type: Object,
      default: () => ({
        Followers: '1.5M',
        Engagement: '8.5%'
      })
    }
  },
  methods: {
    async buttonClicked(value) {
      // validate value
      if (value !== 'TRUE' && value !== 'FALSE') {
        console.error('Invalid value provided for approval status');
        return;
      }

      try {
        const response = await axios.post(`${this.$store.state.basePath}/sponsor-approval/${this.user.sponsor_id}`,
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
        console.log('Approval status updated:', response.data);
        location.reload();
      } catch (error) {
        // console.error('Error updating approval status:', error);
        this.$errorComesNow(error);
      }
    }
  },
  computed: {
    parsedLinks() {
      try {
        return typeof this.user.link === 'string' ? JSON.parse(this.user.link) : [];
      } catch {
        return [];
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
}

.profile-card {
  display: flex;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 5px solid #3498db;
}

.profile-header {
  width: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 15px;
  color: white;
  background-color: #3498db;
}

.avatar-section {
  position: relative;
  margin-bottom: 15px;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
}

.active-badge {
  position: absolute;
  bottom: 95px;
  right: 10px;
  width: 20px;
  height: 20px;
  background: #2be779;
  border-radius: 50%;
  border: 3px solid white;
}

.user-details {
  text-align: center;
}

.user-details h2 {
  margin: 10px 0 5px;
  font-size: 1.5em;
}

.username {
  margin: 0 0 10px;
  opacity: 0.8;
}

.profile-badges .badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 1rem;
}

.profile-content {
  flex-grow: 1;
  padding: 20px;
}

.description {
  margin-top: 10px;
  margin-bottom: 20px;
  color: #555;
  background-color: #fcf2f2;
  padding: 10px;
  border-radius: 10px;
}

.profile-meta {
  margin-bottom: 20px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  background-color: #fcf2f2;
  padding: 10px;
  border-radius: 10px;
}

.meta-label {
  font-family: cursive;
  color: #888;
  font-size: 1rem;
  margin-bottom: 5px;
  font-weight: 600;
}

.meta-value {
  font-weight: 600;
  color: #333;
}

.social-links {
  display: flex;
  justify-content: start;
  gap: 15px;
  margin-bottom: 20px;
}

.social-links a {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: transform 0.2s;
  text-decoration: none;
}

.social-links a:hover {
  transform: scale(1.1);
}


.youtube {
  background: #FF0000;
  color: white;
  opacity: 0.95;
}

.youtube:hover {
  background: #cc0000;
  opacity: 1;
}

.facebook {
  background: #1877F2;
  color: white;
  opacity: 0.95;
}

.facebook:hover {
  background: #0d65d9;
  opacity: 1;
}

.instagram {
  background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
  color: white;
  opacity: 0.95;
}

.instagram:hover {
  opacity: 1;
}

.twitter {
  background: #1DA1F2;
  color: white;
  opacity: 0.95;
}

.twitter:hover {
  background: #0c85d0;
  opacity: 1;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-weight: bold;
  font-size: 1.2em;
}

.stat-label {
  color: #666;
  font-size: 0.9em;
  font-family: cursive;

}


.profile-actions {
  display: flex;
  gap: 8px;
  margin-top: 20px;
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
  opacity: 0.8;
}

.btn-reject {
  background-color: #ff0000;
  color: white;
}

.btn-approve {
  background-color: #01bb4e;
  color: white;
}

.btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  opacity: 1;
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
  }

  .profile-header {
    width: 100%;
  }
}
</style>