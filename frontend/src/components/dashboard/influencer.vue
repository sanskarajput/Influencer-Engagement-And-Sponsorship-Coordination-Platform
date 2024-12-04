<template>
  <!-- dashboard parent -->
  <div v-if="dashboardsDataFetched">

    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="mb-0 text-gray-800 fs-2 fw-bold">
        Dashboard
      </h1>
    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Earnings (Monthly) Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  Earnings (Monthly)</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  ₹ <counter :till="stats.current_month.earnings"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-calendar fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Earnings (Monthly) Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  Earnings (Annual)</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  ₹ <counter :till="stats.current_year.earnings"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-indian-rupee-sign fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Earnings (Monthly) Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  Total Requests
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_requests"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Requests Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  Pending Requests</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_pending_requests"></counter>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-comments fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Row -->

    <div class="row">

      <!-- Area Chart -->
      <div class="col-xl-8 col-lg-7">
        <div class="card shadow mb-4">
          <!-- Card Header - Dropdown -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area">
              <AreaChart
              :data="[0, 10500, 500, 1500, 1000, 2020, 1000, 2000, 1200, 3000, 2500, 4000]"
              chartTitle="Earnings"
              ></AreaChart>
            </div>
          </div>
        </div>
      </div>

      <!-- Pie Chart -->
      <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
          <!-- Card Header - Dropdown -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Campaign's Visibility</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-pie">
              <PieChart :data="[70,30]"></PieChart>
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
              <p>This is the Influencer Dashboard that provides a comprehensive view of active and past campaigns,
                incoming ad requests, payment updates, and performance analytics. Include features to accept or decline
                collaborations, communicate with sponsors, and update personal profiles effortlessly. The dashboard
                will also showcase earnings, campaign timelines, and engagement stats, helping influencers track their
                progress and optimize their collaborations.</p>
              <p class="mb-0">Ensure a user-friendly design that simplifies managing opportunities and interactions,
                empowering influencers to focus on delivering high-quality content.</p>
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
          `${this.$store.state.basePath}/influencer-dashboard-details`,
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
    },
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