<template>
  <!-- dashboard parent -->
  <div v-if="dashboardsDataFetched">

    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="mb-0 text-gray-800 fs-2 fw-bold">
        Dashboard
      </h1>
    </div>

    <div class="row">

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  Influencers</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_influencers"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fab fa-confluence fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  Sponsors</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_sponsors"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fab fa-confluence fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  Campaigns
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_campaigns"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-bullhorn fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  Active Campaigns</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_active_campaigns"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-fire fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-secondary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-secondary text-uppercase mb-1">
                  Campaigns Budget</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  ₹ <counter :till="stats.campaigns_total_budget"></counter>.00
                </div>
              </div>
              <div class="col-auto">
                <i class="fa-solid fa-indian-rupee-sign fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  Requests</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_requests"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-clock-rotate-left fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-danger shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">
                  Pending Requests</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_pending_requests"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fa-solid fa-hourglass-half fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4 animation-small-to-original">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  Completed Requests</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_completed_requests"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fa-solid fa-hourglass-end fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Content Row -->

    <div class="row">

      <!-- Area Chart -->
      <div class="col-xl-8 col-lg-7 animation-small-to-original">
        <div class="card shadow mb-4">
          <!-- Card Header - Dropdown -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area">
              <AreaChart :data="[0, 1000, 1500, 100, 11000, 200, 1040, 2050, 1260, 3070, 2510, 4030]"
                chartTitle="Earnings"></AreaChart>
            </div>
          </div>
        </div>
      </div>

      <!-- Pie Chart -->
      <div class="col-xl-4 col-lg-5 animation-small-to-original">
        <div class="card shadow mb-4">
          <!-- Card Header - Dropdown -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Campaign's Visibility</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-pie">
              <PieChart :data="[170, 130]"></PieChart>
            </div>
            <div class="mt-4 text-center small">
              <span class="mr-2">
                <i class="fas fa-circle text-primary"></i> Public
              </span>
              <span class="mr-2">
                <i class="fas fa-circle text-success"></i> Private
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Content Column -->
      <div class="col-lg-6 mb-4">

        <!-- Project Card Example -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Status of Requests</h6>
          </div>
          <div class="card-body">
            <h4 class="small font-weight-bold">Pending <span class="float-right">20%</span></h4>
            <div class="progress mb-4">
              <div class="progress-bar status-pending" role="progressbar" style="width: 20%" aria-valuenow="20"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <h4 class="small font-weight-bold">Accepted <span class="float-right">40%</span></h4>
            <div class="progress mb-4">
              <div class="progress-bar status-accepted" role="progressbar" style="width: 40%" aria-valuenow="40"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <h4 class="small font-weight-bold">Declined <span class="float-right">60%</span></h4>
            <div class="progress mb-4">
              <div class="progress-bar status-declined" role="progressbar" style="width: 60%" aria-valuenow="80"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <h4 class="small font-weight-bold">Completed <span class="float-right">80%</span></h4>
            <div class="progress  mb-4">
              <div class="progress-bar status-completed" role="progressbar" style="width: 80%" aria-valuenow="100"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <h4 class="small font-weight-bold">Rejected <span class="float-right">100%</span></h4>
            <div class="progress mb-4">
              <div class="progress-bar status-rejected" role="progressbar" style="width: 100%" aria-valuenow="60"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
        </div>

      </div>

      <div class="col-lg-6 mb-4">

        <!-- Illustrations -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Illustrations</h6>
          </div>
          <div class="card-body">
            <div class="text-center">
              <img class="img-fluid px-3 px-sm-4 mt-3 mb-4" style="width: 25rem;" src="img/undraw_posting_photo.svg"
                alt="...">
            </div>
            <div class="card-body">
              <p>This is Admin Dashboard for overseeing the entire platform. Include tools to manage user accounts
                (sponsors and influencers), review and approve campaigns, monitor ad requests, and track platform
                activity. Provide insights through detailed analytics, such as user engagement, campaign performance,
                and system health. Add features for resolving disputes, managing payments, and handling role-based
                permissions.</p>
              <p class="mb-0">The interface should ensure smooth platform operations with real-time updates, efficient
                moderation tools, and comprehensive reporting</p>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
  <!-- dashboard parent end -->
</template>

<script>
import axios from 'axios';
import counter from '@/components/additional/counter.vue'
import AreaChart from '@/components/additional/area-chart.vue'
import PieChart from '@/components/additional/pie-chart.vue'

export default {
  name: 'Influencer-Dashboard',
  components: {
    counter,
    AreaChart,
    PieChart
  },
  props: {
  },
  data() {
    return {
      stats: null,
      charts: null,
      dashboardsDataFetched: false,
    }
  },
  methods: {
    async getDashboardData() {
      try {
        const response = await axios.get(
          `${this.$store.state.basePath}/admin-dashboard-details`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );

        const data = response.data.db_data;

        this.stats = data.stats;
        this.charts = data.charts;
        this.dashboardsDataFetched = true;
      } catch (error) {
        this.$errorComesNow(error);
      }
    }
  },
  computed: {
  },
  watch: {
  },
  beforeCreate() {
  },
  created() {
  },
  beforeMount() {
    this.getDashboardData();
  },
  mounted() {    
  },
  beforeUpdate() {
  },
  updated() {
  },
  begoreUnmount() {
  },
  unmounted() {
  }
}
</script>

<style scoped>

.status-pending {
  background-color: #fc863d;
}

.status-accepted {
  background-color: #05fab9;
}

.status-declined {
  background-color: #fb8585;
}

.status-completed {
  background-color: #04ff00;
}

.status-rejected {
  background-color: #ff0e0e;
}
</style>