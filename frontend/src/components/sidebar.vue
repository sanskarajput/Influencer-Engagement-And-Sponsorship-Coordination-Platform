<template>
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

        <!-- Sidebar - Brand -->
        <router-link class="sidebar-brand d-flex align-items-center justify-content-center" :to="{ name: 'index' }">
            <div class="sidebar-brand-icon">
                <i class="fa-solid fa-users-line fa-s"></i>
            </div>
            <div class="sidebar-brand-text mx-3">IESCP <sup><i class="fa-solid fa-thumbs-up"></i></sup></div>
        </router-link>

        <!-- Divider -->
        <hr class="sidebar-divider my-0">

        <!-- Nav Item - Dashboard -->
        <li class="nav-item">
            <router-link class="nav-link" :to="{ name : 'dashboard' }">
                <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>Dashboard</span>
            </router-link>
        </li>

        <!-- Divider -->
        <hr class="sidebar-divider">


        <div v-if="$store.getters.isAuthenticated" class="mb-n3"> <!--class="my-col"-->
            <!-- Heading -->
            <div class="sidebar-heading">
                Interface
            </div>


            <div v-if="$store.getters.role == 'sponsor'">
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'add-campaign' }">
                        <i class="fas fa-fw fa-bullhorn"></i>
                        <span>Add Campaign</span>
                    </router-link>
                </li>
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-campaigns-for-sponsors' }">
                        <i class="fas fa-fw fa-scroll"></i>
                        <span>My Campaigns</span>
                    </router-link>
                </li>
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-requests-for-sponsors' }">
                        <i class="fas fa-fw fa-concierge-bell"></i>
                        <span>My Requests</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" :to="{ name: 'all-influencers' }">
                        <i class="fab fa-fw fa-confluence"></i>
                        <span>All Influencers</span>
                    </router-link>
                </li>
            </div>

            <div v-if="$store.getters.role == 'influencer'">
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-public-campaigns-for-influencers' }">
                        <i class="fas fa-fw fa-bullhorn"></i>
                        <span>All Campaign</span>
                    </router-link>
                </li>
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-requests-for-influencers' }">
                        <i class="fas fa-fw fa-concierge-bell"></i>
                        <span>My All Requests</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" :to="{ name: 'all-sponsors' }">
                        <i class="fab fa-fw fa-confluence"></i>
                        <span>All Sponsors</span>
                    </router-link>
                </li>
            </div>

            <div v-if="$store.getters.role == 'admin'">
                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-campaigns-for-a-admin' }">
                        <i class="fas fa-fw fa-bullhorn"></i>
                        <span>All Campaign</span>
                    </router-link>
                </li>

                <li class="nav-item mb-n3">
                    <router-link class="nav-link" :to="{ name: 'all-sponsors' }">
                        <i class="fab fa-fw fa-confluence"></i>
                        <span>All Sponsors</span>
                    </router-link>
                </li>

                <li class="nav-item">
                    <router-link class="nav-link" :to="{ name: 'all-influencers' }">
                        <i class="fab fa-fw fa-confluence"></i>
                        <span>All Influencers</span>
                    </router-link>
                </li>
            </div>
            <!-- Divider -->
        </div>

        <hr class="sidebar-divider">

         <!-- Heading -->
         <div class="sidebar-heading">
            Addons
        </div>

        <!-- Nav Item - Pages Collapse Menu -->
        <li class="nav-item mb-n3">
            <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapsePages" aria-expanded="false"
                aria-controls="collapsePages">
                <i class="fas fa-fw fa-folder"></i>
                <span>Pages</span>
            </a>
            <div id="collapsePages" class="collapse" aria-labelledby="headingPages"
                data-parent="#accordionSidebar">
                <div class="bg-white py-2 collapse-inner rounded">
                    <h6 class="collapse-header">Login Screens:</h6>
                    <a class="collapse-item" href="login.html">Login</a>
                    <a class="collapse-item" href="register.html">Register</a>
                    <a class="collapse-item" href="forgot-password.html">Forgot Password</a>
                    <div class="collapse-divider"></div>
                    <h6 class="collapse-header">Other Pages:</h6>
                    <a class="collapse-item" href="404.html">404 Page</a>
                    <a class="collapse-item" href="blank.html">Blank Page</a>
                </div>
            </div>
        </li>

        <!-- Nav Item - Charts -->
        <li class="nav-item mb-n3">
            <a class="nav-link" href="charts.html">
                <i class="fas fa-fw fa-chart-area"></i>
                <span>Charts</span></a>
        </li>

        <!-- Nav Item - Tables -->
        <li class="nav-item">
            <a class="nav-link" href="tables.html">
                <i class="fas fa-fw fa-table"></i>
                <span>Tables</span></a>
        </li>

        <!-- Divider -->
        <hr class="sidebar-divider d-none d-md-block">

        <!-- Sidebar Toggler (Sidebar) -->
        <div class="text-center d-none d-md-inline">
            <button class="rounded-circle border-0" id="sidebarToggle" @click="toggleSidebar"></button>
        </div>

        <div class="sidebar-card d-none d-lg-flex">
            <img class="#sidebar-card-illustration mb-2 rounded-circle img-fluid" src="@/assets/IESCP-2.jpg"
                alt="...">
            <p class="text-center mb-2"><strong>Influencer Engagement & Sponsorship Coordination Platform</strong> to
                connect Sponsors and Influencers so that sponsors can get their product / service advertised and
                influencers can get monetary benefits !</p>
            <a href="https://github.com/sanskarajput/Influencer-Engagement-And-Sponsorship-Coordination-Platform" target="_blank">
                <i class="fab fa-github fa-3x text-black"></i>
            </a>
        </div>

    </ul>
</template>

<script>

export default {
    name: 'SideBar',
    data() {
        return {

        }
    },
    methods: {
        toggleSidebar() {
            document.getElementById('accordionSidebar').classList.toggle('toggled');
            document.getElementById('app').classList.toggle('sidebar-toggled');
            // document.getElementById('page-top').classList.toggle('sidebar-toggled');
        }
    }
}
</script>

<style></style>
