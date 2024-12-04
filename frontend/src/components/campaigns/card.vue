<template>
  <div class="campaign-card">
    <!-- Campaign Image -->
    <div class="campaign-image-container">
      <img src="@/assets/campaign.jpg" :alt="campaign.title" class="campaign-image">
    </div>

    <div class="campaign-content">
      <!-- Campaign Title -->
      <h3 class="campaign-title">
        <span>{{ campaign.title }}</span>
        <span>
          <i class="fas fa-flag fa-lg flagged" :class="campaign.flagged ? 'text-danger' : 'text-warning'"></i>
        </span>
      </h3>
      <div class="category-tag text-muted">
        {{ campaign.category }}
      </div>

      <!-- <hr class="sidebar-divider mb-2 mt-1"> -->

      <div class="extra-small mb-2">
        {{ campaign.description }} 
      </div> 

      <!-- Campaign Progress -->
      <div class="campaign-progress-section">
        <div class="progress-header">
          <span class="progress-label">Progress</span>
          <span class="progress-percentage" :style="{ color: getProgressColor(campaign.campaign_id * 10) }">
            {{ campaign.campaign_id * 10 }}%
          </span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{
            width: `${campaign.campaign_id * 10}%`,
            backgroundColor: getProgressColor(campaign.campaign_id * 10)
          }"></div>
        </div>
      </div>

      <!-- Campaign Stats -->
      <!-- <div v-if="stats?.length" class="campaign-stats-grid">
        <div 
          v-for="(stat, index) in stats" 
          :key="index" 
          class="stat-item"
        >
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div> -->

      <!-- Campaign Duration -->
      <div class="campaign-duration">
        <i class="fa fa-calendar duration-icon"></i>
        <span class="duration-text">
          {{ $formatDateRange(campaign.start_date, campaign.end_date) }}
        </span>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="view-details-btn" @click="$router.push({
          name: 'each-campaign-details',
          query: { show: campaign.campaign_id }
        })">
          View Details
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CampaignCard',
  props: {
    campaign: {
      type: Object,
      required: true,
    },
    stats: {
      type: Array,
      default: () => [
        { label: 'Reach', value: '15.2k' },
        { label: 'Clicks', value: '1.8k' },
        { label: 'CTR', value: '11.8%' }
      ]
    }
  },
  methods: {
    getProgressColor(percentage) {
      // Convert percentage to a color between red and green
      const red = Math.floor(255 * (1 - percentage / 100));
      const green = Math.floor(255 * (percentage / 100));
      return `rgba(${red}, ${green}, 01,.7)`;
    }
  },
  computed: {
    statusBadgeClass() {
      const statusClasses = {
        draft: 'bg-secondary',
        active: 'bg-success',
        ended: 'bg-secondary',
        scheduled: 'bg-info'
      }
      return statusClasses[this.campaign.status?.toLowerCase()] || 'bg-secondary'
    }
  }
}
</script>

<style scoped>
.campaign-card {
  width: 230px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 1s ease, box-shadow 0.3s ease;
  margin-bottom: 25px;
  border-radius: 12px;
}

.campaign-card:hover {
  border-radius: 12px;
  transform:translateY(-2%);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.campaign-image-container {
  position: relative;
}

.campaign-image {
  border-radius: 12px;
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.campaign-card:hover .campaign-imag-e {
  transform:translateY(5deg);
}

.campaign-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  margin: 0px;
  display: flex;
  justify-content: space-between;
  font-style: italic;
  text-transform: capitalize;
}

.flagged {
  font-size: 1.3rem;
  rotate:3deg;
}

.category-tag {
  color: white;
  text-transform: capitalize;
  border-radius: 20px;
  font-size: 0.85rem;
  margin-bottom: 2px;
  font-weight: 600;
}

.sidebar-divider{
  border-top: .01rem solid rgb(0, 0, 0)
}

.campaign-content {
  padding: 5px 5px;
}


.extra-small {
  font-size: 0.75rem;
  color: darkblue;
  min-height: 50px;
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.campaign-progress-section {
  margin-bottom: 15px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.progress-label {
  color: #666;
  font-size: 0.9rem;
}

.progress-percentage {
  font-weight: bold;
  transition: color 0.3s ease;
}

.progress-bar-container {
  background-color: #e9ecef;
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition: width 0.5s ease, background-color 0.3s ease;
}

.campaign-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.stat-item {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s ease;
}

.stat-item:hover {
  background-color: #e9ecef;
}

.stat-label {
  color: #6c757d;
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.stat-value {
  font-weight: bold;
  color: #333;
}

.campaign-duration {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  color: #6c757d;
}

.duration-icon {
  margin-right: 10px;
  color: #6c757d;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

.view-details-btn {
  color: white;
  border: none;
  padding: 5px;
  border-radius: 8px;
  width: 100px;
  transition: background-color 0.3s ease;
  border: 1px solid #007bff;
  color: #007bff;
  font-weight: bold;
}

.view-details-btn:hover {
  color: #ffffff;
  background-color: #007bff;
}
</style>