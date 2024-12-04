<template>
    <div v-if="campaign.dataFetched" class="campaign-card">
        <div class="campaign-header">
            <div class="image-container">
                <img src="@/assets/campaign.jpg" alt="Campaign Image"
                    class="campaign-image" />
                <input type="file" ref="imageUpload" style="display:none" accept="image/*">
                <br>
            </div>

            <div class="header-content">
                <div class="campaign-title-section">
                    <h1>{{ campaign.title }}</h1>

                    <div class="campaign-meta-1">
                        <span class="campaign-category">
                            <i class="fas fa-tag"></i>
                            {{ campaign.category }}
                        </span>

                        <span class="campaign-visibility" :class="campaign.visibility.toLowerCase()">
                            <i class="fas"
                                :class="campaign.visibility.toLowerCase() === 'public' ? 'fa-lock-open' : 'fa-lock'">
                            </i>
                            {{ campaign.visibility.toLowerCase() }}
                        </span>

                        <span class="campaign-status" :class="campaign.status.toLowerCase()">
                            <i class="fas fa-circle"></i>
                            {{ campaign.status.toLowerCase() }}
                        </span>
                        
                        <span>
                          <i class="fas fa-flag fa-lg" :class="campaign.flagged ? 'text-danger' : 'text-warning'"></i>
                        </span>

                    </div>
                    <div v-if="$store.getters.role === 'sponsor' && !accordionVisible" class="campaign-meta-2 mt-2">
                        <router-link class="request-exist"
                            :to="{ name: 'each-campaign-details', query: { show: campaign.campaign_id, 'show-all-influencers': true } }">
                            Click Here
                        </router-link>
                        &nbsp;to view all Influencers and Requests
                    </div>
                    <div v-if="$store.getters.role === 'influencer' && request.requestExist && !accordionVisible"
                        class="campaign-meta-2 mt-2">
                        Requested {{ $forCreatedAtLong(request.time) }},&nbsp;
                        <router-link class="request-exist"
                            :to="{ name: 'each-campaign-details', query: { show: campaign.campaign_id, 'show-request-details': true } }">
                            Click Here
                        </router-link>
                        &nbsp;to view details
                    </div>
                    <div v-if="$store.getters.role === 'admin' && !accordionVisible"
                        class="campaign-meta-2 mt-2">
                        <router-link class="request-exist"
                            :to="{ name: 'each-campaign-details', query: { show: campaign.campaign_id, 'show-request-details': true } }">
                            Click Here
                        </router-link>
                        &nbsp;to view all existing requests
                    </div>
                </div>

                <div class="action-section">
                    <span class="campaign-duration">
                        <i class="fas fa-calendar-alt"></i>
                        {{ campaign.duration }}
                    </span>

                    <div v-if="$store.getters.role === 'sponsor'" class="action-icons">
                        <i class="fas fa-edit edit-icon"
                            @click="$router.push({ name: 'each-campaign-details', query: { edit: campaign.campaign_id } })">
                        </i>
                        <i class="fas fa-trash delete-icon" @click="deleteCampaign"></i>
                    </div>
                    <div v-if="$store.getters.role === 'admin' || $store.getters.role === 'influencer' && !accordionVisible" class="action-icons fw-bold">
                      <span class="text-danger me-n4">Sponsored by :</span>
                      <router-link class="profile-button" :to="{ name: 'other-user-profile-view', params:{ role:'sponsor' }, query: { user_id: campaign.campaigner_s_user_id } }">{{ campaign.campaigner }}</router-link>
                    </div>
                </div>
            </div>
        </div>

        <div class="campaign-body">
            <div class="campaign-details">
                <section class="description-section">
                    <h2>
                        <i class="fas fa-file-alt"></i>
                        Campaign Description
                    </h2>
                    <p class="description-text">
                        {{ campaign.description }}
                    </p>
                </section>

                <section class="goals-section">
                    <h2>
                        <i class="fas fa-bullseye"></i>
                        Campaign Goals
                    </h2>
                    <p class="goals-text">
                        {{ campaign.goals }}
                    </p>
                </section>
            </div>

            <div class="campaign-sidebar">
                <div class="budget-card">
                    <h2>
                        <i class="fa-solid fa-credit-card"></i>
                        Campaign Budget
                    </h2>
                    <div class="budget-container">
                        <div class="budget-label">
                            <span>
                                <i class="fa-solid fa-indian-rupee-sign me-2"></i>
                                <span>
                                    {{ campaign.budget.toLocaleString() }}
                                </span>
                            </span>
                        </div>
                    </div>
                </div>

                <div class="performance-card">
                    <h2>
                        <i class="fas fa-chart-line"></i>
                        Campaign Performance
                    </h2>

                    <div class="progress-container">
                        <div class="progress-label">
                            <span>Campaign Progress</span>
                            <span class="progress-percentage">{{ campaign.progress }}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" :style="{ width: `${campaign.progress}%` }"></div>
                        </div>
                    </div>

                    <div class="stats-grid">
                        <div v-for="stat in campaign.stats" :key="stat.label" class="stat-item">
                            <div class="stat-label">{{ stat.label }}</div>
                            <div class="stat-value">{{ stat.value }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "EditableCampaignCard",
    props: {
        mainCampaign: {
            type: Object,
            required: true
        },
        request: {
            type: Object,
            required: false,
            default:() => ({
              
            })
        },
        accordionVisible: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    data() {
        return {
            campaign: { ...this.mainCampaign },
        };
    },
    methods: {
        async deleteCampaign() {
            try {
                await axios.delete(`${this.$store.state.basePath}/campaign/delete/${this.campaign.campaign_id}`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );
                this.$router.push({ name: 'dashboard' });
                this.$toast.success(`Campaign Deleted Successfully !`, {position: 'bottom-right'})
            } catch (error) {
                this.$errorComesNow(error);
            }
        }
    }
};
</script>

<style scoped>
.campaign-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    max-width: auto;
    font-family: "Inter", sans-serif;
}

.campaign-header {
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #4a90e2 0%, #50c878 100%);
    color: white;
    padding: 2rem;
    gap: 1rem;
}

.image-container {
    flex-shrink: 0;
}

.campaign-image {
    width: 150px;
    height: 100px;
    border-radius: 8px;
    object-fit: cover;
    border: 2px solid white;
}

.header-content {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.campaign-title-section h1 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.campaign-meta-1 {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.campaign-meta-2 {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #ccd2db;
    font-weight: bolder;
}

.request-exist {
    text-decoration: none;
    font-size: inherit;
    font-weight: inherit;
    color: inherit;
}

.request-exist:hover {
    color: blue;
}

.campaign-category,
.campaign-status,
.campaign-visibility {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    border: 1px solid;
}

.action-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
}

.action-icons {
    display: flex;
    gap: 1rem;
}

.profile-button {
    margin-bottom: 0.25rem;
    text-decoration: none;
    cursor: pointer;
    font-size: clamp(0.875rem, 2vw, 1rem);
    color: rgb(0, 0, 0);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-left: -8px;
}

.edit-icon:hover {
    color: #ffd700;
    transform: scale(1.2);
    cursor: pointer;
}

.delete-icon:hover {
    color: #ff4c4c;
    transform: scale(1.2);
    cursor: pointer;
}

.campaign-duration {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
}

.campaign-body {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    padding: 2rem;
}

.campaign-details {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.description-section,
.goals-section {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 1.5rem;
    border-radius: 12px;
}

.description-section h2,
.goals-section h2 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.25rem;
}

.description-text,
.goals-text {
    color: #4a5568;
    line-height: 1.7;
}

.campaign-sidebar {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.budget-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 1.5rem;
    border-radius: 12px;
}

.budget-card h2 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-size: 1.25rem;
}

.budget-label {
    display: flex;
    justify-content: space-between;
    margin-left: 2.2rem;
    color: #4a5568;
    font-size: 1.5rem;

}

.performance-card {
    background: #f1f5f9;
    padding: 1.5rem;
    border-radius: 12px;
}

.performance-card h2 {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #2c3e50;
    margin-bottom: 1.5rem;
    font-size: 1.25rem;
}

.progress-container {
    margin-bottom: 1.5rem;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    color: #4a5568;
}

.progress-bar {
    height: 10px;
    background: #e2e8f0;
    border-radius: 5px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(to right, #4a90e2, #50c878);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.stat-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.stat-label {
    color: #64748b;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2c3e50;
}

@media (max-width: 768px) {
    .campaign-body {
        grid-template-columns: 1fr;
    }

    .campaign-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .action-section {
        align-items: flex-start;
    }
}
</style>















<!-- <template>
    <div class="campaign-container">
      <div class="campaign-hero">
        <div class="hero-overlay">
          <div class="hero-content">
            <div class="hero-image-container">
              <img 
                :src="campaign.image || defaultImage" 
                :alt="campaign.title" 
                class="hero-image"
              />
              <div class="hero-badge" :class="statusClass">
                {{ campaign.status }}
              </div>
            </div>
            
            <div class="hero-details">
              <h1 class="hero-title">{{ campaign.title }}</h1>
              <p class="hero-description">{{ campaign.description }}</p>
              
              <div class="hero-meta">
                <div class="meta-item">
                  <IconCalendar class="meta-icon" />
                  <span>{{ campaign.duration }}</span>
                </div>
                <div class="meta-item">
                  <IconUsers class="meta-icon" />
                  <span>{{ campaign.campaigner }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div class="campaign-details-grid">
        <div class="details-section progress-section">
          <div class="section-header">
            <IconTrendingUp class="section-icon" />
            <h3>Campaign Progress</h3>
          </div>
          
          <div class="progress-container">
            <div class="progress-header">
              <span>Overall Progress</span>
              <span class="progress-percentage">{{ campaign.progress }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-bar-fill" 
                :style="{ width: `${campaign.progress}%` }"
              ></div>
            </div>
          </div>
  
          <div class="milestones" v-if="campaign.milestones && campaign.milestones.length">
            <div class="milestone" v-for="(milestone, index) in campaign.milestones" :key="index">
              <div class="milestone-icon" :class="{ 'milestone-completed': milestone.completed }">
                {{ milestone.completed ? '✓' : '○' }}
              </div>
              <div class="milestone-details">
                <span class="milestone-title">{{ milestone.title }}</span>
                <span class="milestone-date">{{ milestone.date }}</span>
              </div>
            </div>
          </div>
        </div>
  
        <div class="details-section metrics-section">
          <div class="section-header">
            <IconChart class="section-icon" />
            <h3>Campaign Metrics</h3>
          </div>
          
          <div class="metrics-grid">
            <div 
              v-for="(metric, index) in campaign.metrics" 
              :key="index" 
              class="metric-card"
            >
              <div class="metric-icon">
                <component :is="metric.icon" />
              </div>
              <div class="metric-content">
                <span class="metric-label">{{ metric.label }}</span>
                <span class="metric-value">{{ metric.value }}</span>
              </div>
            </div>
          </div>
        </div>
  
        <div class="details-section financial-section">
          <div class="section-header">
            <IconDollarSign class="section-icon" />
            <h3>Financial Overview</h3>
          </div>
          
          <div class="financial-breakdown">
            <div class="financial-item">
              <span>Total Budget</span>
              <span class="financial-value">{{ campaign.budget }}</span>
            </div>
            <div class="financial-item">
              <span>Funds Raised</span>
              <span class="financial-value">{{ campaign.fundsRaised }}</span>
            </div>
            <div class="financial-progress">
              <div 
                class="financial-progress-bar" 
                :style="{ width: `${fundingPercentage}%` }"
              ></div>
            </div>
            <div class="financial-percentage">
              {{ fundingPercentage }}% Funded
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { 
    Calendar as IconCalendar, 
    Users as IconUsers, 
    TrendingUp as IconTrendingUp,
    DollarSign as IconDollarSign,
    BarChart2 as IconChart 
  } from 'lucide-vue-next'
  
    var campaign = {
        title: 'Unnamed Campaign',
        description: 'No description provided',
        image: 'https://placeholder.com/120',
        status: 'Draft',
        duration: 'Not Set',
        campaigner: 'Anonymous',
        progress: 0,
        budget: '$0',
        fundsRaised: '$0',
        milestones: [],
        metrics: [],
      }
  
  const defaultImage = '/api/placeholder/800/400'
  
  const statusClass = computed(() => {
    const statusMap = {
      'Active': 'badge-success',
      'Draft': 'badge-warning',
      'Completed': 'badge-complete',
      'Paused': 'badge-paused'
    }
    return statusMap[campaign.status] || 'badge-default'
  })
  
  const fundingPercentage = computed(() => {
    const budget = parseFloat(campaign.budget.replace(/[^0-9.-]+/g,""))
    const raised = parseFloat(campaign.fundsRaised.replace(/[^0-9.-]+/g,""))
    return Math.min(Math.round((raised / budget) * 100), 100)
  })
  </script>
  
  <style scoped>
  .campaign-container {
    max-width: 1200px;
    margin: 0 auto;
    font-family: 'Inter', sans-serif;
    background: #f4f6f9;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }
  
  .campaign-hero {
    position: relative;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
  }
  
  .hero-overlay {
    padding: 2rem;
    background: rgba(0, 0, 0, 0.1);
  }
  
  .hero-content {
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  .hero-image-container {
    position: relative;
    width: 250px;
    height: 250px;
  }
  
  .hero-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 12px;
  }
  
  .hero-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
  }
  
  .badge-success { background-color: #2ecc71; }
  .badge-warning { background-color: #f39c12; }
  .badge-complete { background-color: #3498db; }
  .badge-paused { background-color: #e74c3c; }
  .badge-default { background-color: #95a5a6; }
  
  .hero-details {
    flex-grow: 1;
  }
  
  .hero-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .hero-description {
    opacity: 0.8;
    margin-bottom: 1.5rem;
  }
  
  .hero-meta {
    display: flex;
    gap: 2rem;
  }
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .meta-icon {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .campaign-details-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    padding: 2rem;
    background: white;
  }
  
  .details-section {
    background: #f9fafb;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  }
  
  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 1rem;
  }
  
  .section-icon {
    color: #6a11cb;
  }
  
  .progress-container {
    margin-bottom: 1.5rem;
  }
  
  .progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .progress-bar {
    height: 10px;
    background: #e9ecef;
    border-radius: 5px;
  }
  
  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(to right, #6a11cb, #2575fc);
    border-radius: 5px;
  }
  
  .milestones {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .milestone {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .milestone-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #6a11cb;
  }
  
  .milestone-completed {
    background: #6a11cb;
    color: white;
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .metric-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .financial-breakdown {
    background: white;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .financial-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .financial-progress {
    height: 10px;
    background: #e9ecef;
    border-radius: 5px;
    margin: 1rem 0;
  }
  
  .financial-progress-bar {
    height: 100%;
    background: linear-gradient(to right, #6a11cb, #2575fc);
    border-radius: 5px;
  }
  
  @media (max-width: 1024px) {
    .campaign-details-grid {
      grid-template-columns: 1fr;
    }
  }
  </style> -->