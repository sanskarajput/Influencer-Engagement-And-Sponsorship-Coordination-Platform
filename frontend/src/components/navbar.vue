<template>
    <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow"
        :style="$store.getters.isAuthenticated ? '' : 'height: 60px;'">

        <!-- website logo -->
        <router-link v-if="!$store.getters.isAuthenticated" class="navbar-brand d-flex align-items-center justify-content-center ml-3 fs-2 fw-bold text-primary" :to="{ name: 'login' }">
            <div class="navbar-brand-icon">
                <i class="fa-solid fa-users-line"></i>
            </div>
            <div class="navbar-brand-text mx-3 fs-5">IESCP <sup><i class="fa-solid fa-thumbs-up"></i></sup></div>
        </router-link>

        <!-- Sidebar Toggle (Topbar) -->
        <button v-if="$store.getters.isAuthenticated" id="sidebarToggleTop"
            class="btn btn-link d-md-none rounded-circle mr-3" @click="toggleSidebar">
            <i class="fa fa-bars"></i>
        </button>

        <!-- Topbar Search -->
        <form v-if="$store.getters.isAuthenticated && $store.getters.role !== 'admin'"
            class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
            <div class="input-group">
                <input 
                    type="text"
                    v-model="query" 
                    v-on:keypress.enter.prevent="searched"
                    class="form-control bg-light border-0 small" 
                    :placeholder="placeholder"
                    aria-label="Search" 
                    aria-describedby="basic-addon2" 
                    :disabled="!$store.getters.isAuthenticated">
                <div class="input-group-append">
                    <button @click="searched" class="btn btn-primary" type="button" :disabled="!$store.getters.isAuthenticated">
                        <i class="fas fa-search fa-sm"></i>
                    </button>
                </div>
            </div>
        </form>

        <!-- Topbar Navbar -->
        <ul class="navbar-nav ml-auto">

            <!-- Nav Item - Search Dropdown (Visible Only XS) -->
            <li v-if="$store.getters.isAuthenticated  && $store.getters.role !== 'admin'" class="nav-item dropdown no-arrow d-sm-none">
                <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button" data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-search fa-fw"></i>
                </a>
                <!-- Dropdown - Messages -->
                <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in"
                    aria-labelledby="searchDropdown">
                    <form class="form-inline mr-auto w-100 navbar-search">
                        <div class="input-group">
                            <input 
                                type="text"
                                v-model="query" 
                                v-on:keypress.enter.prevent="searched"
                                class="form-control bg-light border-0 small"
                                :placeholder="placeholder" 
                                aria-label="Search"
                                aria-describedby="basic-addon2" 
                                :disabled="!$store.getters.isAuthenticated">
                            <div class="input-group-append">
                                <button @click="searched" class="btn btn-primary" type="button"
                                    :disabled="!$store.getters.isAuthenticated">
                                    <i class="fas fa-search fa-sm"></i>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </li>


            <div v-if="$store.getters.isAuthenticated" class="d-inline-flex">

                <!-- Nav Item - Alerts -->
                <li class="nav-item dropdown no-arrow mx-1">
                    <a class="nav-link dropdown-toggle" href="#" id="alertsDropdown" role="button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="fas fa-bell fa-fw"></i>
                        <!-- Counter - Alerts -->
                        <span class="badge badge-danger badge-counter">3+</span>
                    </a>
                    <!-- Dropdown - Alerts -->
                    <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                        aria-labelledby="alertsDropdown">
                        <h6 class="dropdown-header">
                            Alerts Center
                        </h6>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="mr-3">
                                <div class="icon-circle bg-primary">
                                    <i class="fas fa-file-alt text-white"></i>
                                </div>
                            </div>
                            <div>
                                <div class="small text-gray-500">December 12, 2019</div>
                                <span class="font-weight-bold">A new monthly report is ready to download!</span>
                            </div>
                        </a>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="mr-3">
                                <div class="icon-circle bg-success">
                                    <i class="fas fa-donate text-white"></i>
                                </div>
                            </div>
                            <div>
                                <div class="small text-gray-500">December 7, 2019</div>
                                $290.29 has been deposited into your account!
                            </div>
                        </a>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="mr-3">
                                <div class="icon-circle bg-warning">
                                    <i class="fas fa-exclamation-triangle text-white"></i>
                                </div>
                            </div>
                            <div>
                                <div class="small text-gray-500">December 2, 2019</div>
                                Spending Alert: We've noticed unusually high spending for your account.
                            </div>
                        </a>
                        <router-link class="dropdown-item text-center small text-gray-500"
                            :to="{ name: 'notifications' }">Show All Alerts</router-link>
                    </div>
                </li>

                <!-- Nav Item - Messages -->
                <li class="nav-item dropdown no-arrow mx-1">
                    <a class="nav-link dropdown-toggle" href="#" id="messagesDropdown" role="button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="fas fa-envelope fa-fw"></i>
                        <!-- Counter - Messages -->
                        <span class="badge badge-danger badge-counter">7</span>
                    </a>
                    <!-- Dropdown - Messages -->
                    <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                        aria-labelledby="messagesDropdown">
                        <h6 class="dropdown-header">
                            Message Center
                        </h6>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="dropdown-list-image mr-3">
                                <img class="rounded-circle" src="img/undraw_profile_1.svg" alt="...">
                                <div class="status-indicator bg-success"></div>
                            </div>
                            <div class="font-weight-bold">
                                <div class="text-truncate">Hi there! I am wondering if you can help me with a
                                    problem I've been having.</div>
                                <div class="small text-gray-500">Emily Fowler · 58m</div>
                            </div>
                        </a>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="dropdown-list-image mr-3">
                                <img class="rounded-circle" src="img/undraw_profile_2.svg" alt="...">
                                <div class="status-indicator"></div>
                            </div>
                            <div>
                                <div class="text-truncate">I have the photos that you ordered last month, how
                                    would you like them sent to you?</div>
                                <div class="small text-gray-500">Jae Chun · 1d</div>
                            </div>
                        </a>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="dropdown-list-image mr-3">
                                <img class="rounded-circle" src="img/undraw_profile_3.svg" alt="...">
                                <div class="status-indicator bg-warning"></div>
                            </div>
                            <div>
                                <div class="text-truncate">Last month's report looks great, I am very happy with
                                    the progress so far, keep up the good work!</div>
                                <div class="small text-gray-500">Morgan Alvarez · 2d</div>
                            </div>
                        </a>
                        <a class="dropdown-item d-flex align-items-center" href="#">
                            <div class="dropdown-list-image mr-3">
                                <img class="rounded-circle" src="https://source.unsplash.com/Mv9hjnEUHR4/60x60"
                                    alt="...">
                                <div class="status-indicator bg-success"></div>
                            </div>
                            <div>
                                <div class="text-truncate">Am I a good boy? The reason I ask is because someone
                                    told me that people say this to all dogs, even if they aren't good...</div>
                                <div class="small text-gray-500">Chicken the Dog · 2w</div>
                            </div>
                        </a>
                        <a class="dropdown-item text-center small text-gray-500" href="#">Read More Messages</a>
                    </div>
                </li>

                <div class="topbar-divider d-none d-sm-block"></div>

                <!-- Nav Item - User Information -->
                <li class="nav-item dropdown no-arrow">
                    <span class="nav-link dropdown-toggle" id="userDropdown" role="button" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false" v-if="user">
                        <span class="mr-2 d-none d-lg-inline text-gray-600 fw-bold">{{ user.name }}</span>
                        <img class="img-profile" :src="user.avatar ? `data:image/png;base64,${user.avatar}` : require('@/assets/profile-user.png')" :alt="user.name">
                    </span>
                    <!-- Dropdown - User Information -->
                    <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                        aria-labelledby="userDropdown">
                        <router-link class="dropdown-item"
                            :to="{ name: 'profile', query: { user_id: $store.getters.user_id } }">
                            <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                            Profile
                        </router-link>
                        <router-link class="dropdown-item" :to="{ name: 'settings' }">
                            <i class="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                            Settings
                        </router-link>
                        <!-- <router-link class="dropdown-item" :to="{name : 'activity'}">
                            <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                            Activity Log
                        </router-link> -->
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">
                            <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                            Logout
                        </a>
                    </div>
                </li>

            </div>
            <div v-else class="my-container">
                <div class="slider" :class="$route.fullPath === '/login' && 'moveslider'"></div>
                <div class="my-btnnn">
                    <router-link class="nav-link login text-black" @click="loginToggle" :to="{ name: 'login' }">
                        Signin
                    </router-link>
                    <router-link class="nav-link signup text-black" @click="signupToggle" :to="{ name: 'signup' }">
                        Signup
                    </router-link>
                </div>


            </div>
        </ul>

    </nav>
</template>


<script>
import axios from 'axios';
export default {
    name: 'NavBar',
    data() {
        return {
            user: null,
            query: null
        }
    },
    methods: {
        toggleSidebar() {
            document.getElementById('accordionSidebar').classList.toggle('toggled');
            document.getElementById('app').classList.toggle('sidebar-toggled');
            // document.getElementById('page-top').classList.toggle('sidebar-toggled');
        },
        loginToggle() {
            let slider = document.querySelector(".slider");
            slider.classList.add("moveslider");
        },
        signupToggle() {
            let slider = document.querySelector(".slider");
            slider.classList.remove("moveslider");
        },
        fetchLoggedInUserAvatar() {
            axios.get(
                `${this.$store.state.basePath}/${this.$store.getters.role}-details/${this.$store.getters.user_id}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    }
                }
            ).then((response) => {
                this.user = response.data.db_data;
            })
                .catch((error) => {
                    console.error(error);
                });
        },
        searched () {            
            this.$router.push({ name: 'search', query: { query: this.query } });
            this.query = null;
        }
    },
    computed: {
        localStorage() {
            return localStorage;
        },
        placeholder() {
            if (this.$store.getters.role === 'sponsor') {
                return 'Search for Influencers.....';
                // return 'Search for Influencers by their name, username, niche, category, reach and description';
            } else if ( this.$store.getters.role === 'influencer' ) {
                return 'Search for Campaigns.....';
                // return 'Search for Campaigns by their name, category, budget, goals and description';
            } else {
                return 'Search for...'
            }
        }
    },
    beforeMount() {
        if (this.$store.getters.isAuthenticated) {
            this.fetchLoggedInUserAvatar();
        }
    }
}
</script>

<style scoped>


.img-profile {
    border: 1.5px solid black;
    border-radius: 50%;
}


#sidebarToggleTop{
    height:2.5rem;
    width:2.5rem;
}

.my-btnnn {
    height: 52px;
    width: 300px;
    box-shadow: 0px 0px 30px rgb(251, 184, 137);
    border-radius: 50px;
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.login,
.signup {
    font-family: cursive;
    font-weight: bolder;
    font-size: 25px;
    border: none;
    outline: none;
    background-color: transparent;
    /* color: white !important; */
    position: relative;
    cursor: pointer;
}

.slider {
    height: 52px;
    width: 150px;
    border-radius: 50px;
    background-image: linear-gradient(to right,
            rgb(255, 195, 110),
            rgb(255, 146, 91));
    position: absolute;
    top: 4px;
    right: 12px;
    transition: all 0.5s ease-in-out;
}

.moveslider {
    right: 162px;
}


/* For Responsiveness of the page */

@media screen and (max-width: 850px) {
    .my-btnnn {
        height: 52px;
        width: 250px;
    }

    .login,
    .signup {
        font-size: 22px;
    }

    .slider {
        height: 52px;
        width: 125px;
        right: 12px;
    }

    .moveslider {
        right: 137px;
    }
}

@media screen and (max-width: 650px) {
    .my-btnnn {
        height: 52px;
        width: 200px;
    }

    .login,
    .signup {
        font-size: 20px;
    }

    .slider {
        height: 52px;
        width: 106px;
        right: 12px;
    }

    .moveslider {
        right: 106px;
    }
}

@media screen and (max-width: 450px) {
    .my-btnnn {
        height: 52px;
        width: 130px;
    }

    .login,
    .signup {
        font-size: 14px;
    }

    .slider {
        height: 52px;
        width: 68px;
        right: 12px;
    }

    .moveslider {
        right: 74px;
    }
}
</style>