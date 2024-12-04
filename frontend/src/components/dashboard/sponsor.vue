<template>
  <!-- dashboard parent -->
  <div v-if="isApproved && dashboardsDataFetched">

    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="mb-0 text-gray-800 fs-2 fw-bold">
        Dashboard
      </h1>
    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Investment (Monthly) Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  Investment (Monthly)</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  ₹ <counter :till="stats.current_month.investment"></counter>.00
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-calendar fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Investment (Monthly) Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  Investment (Annual)</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  ₹ <counter :till="stats.current_year.investment"></counter>.00
                </div>
              </div>
              <div class="col-auto">
                <i class="fa-solid fa-indian-rupee-sign fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Total Campaign Card Example -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  Total Campaigns
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  <counter :till="stats.total_campaigns"></counter>
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
            <h6 class="m-0 font-weight-bold text-primary">Investment Overview</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area">
              <AreaChart></AreaChart>
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
              <PieChart></PieChart>
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
              <p>This is user-friendly Sponsor Dashboard for an Influencer Engagement & Sponsorship
                Coordination Platform. The dashboard will allow sponsors to view and manage their campaigns, track ad
                requests, view influencer profiles, and evaluate performance metrics. Include features like an overview
                of
                active and completed campaigns, real-time notifications for updates on influencer collaborations, and a
                messaging system for seamless communication.</p>
              <p class="mb-0">The interface will display key statistics such as campaign reach, engagement rates, and
                payment details. Ensure an intuitive navigation experience, empowering sponsors to make data-driven
                decisions effectively.</p>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
  <!-- dashboard parent end -->
  <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
    <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
    <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
    <span class="fs-5 fw-bold">Then You Can See Your Dashboard.</span><br>
    <span class="fs-1 fw-bold"> &#128591;</span>
  </div>
</template>

<script>
import axios from 'axios';
import counter from '@/components/additional/counter.vue'
import AreaChart from '@/components/additional/area-chart.vue'
import PieChart from '@/components/additional/pie-chart.vue'

export default {
  name: 'Sponsor-Dashboard',
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
      isApproved: false,
      ApprovalDataFetched: false
    }
  },
  methods: {
    async getDashboardData() {
      try {
        const response = await axios.get(
          `${this.$store.state.basePath}/sponsors-dashboard-details`,
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
    async callBoth() {
      await this.isSponsorApproved();
      if (this.isApproved) {
        await this.getDashboardData();
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
    this.callBoth();
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