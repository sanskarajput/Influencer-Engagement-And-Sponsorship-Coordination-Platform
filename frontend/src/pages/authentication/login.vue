<template>

    <!-- <div class="container"> -->

    <!-- Outer Row -->
    <div class="row justify-content-center animation">

        <div class="col-xl-10 col-lg-12 col-md-9">

            <div class="row justify-content-center">
                <div class="col-xl-10 col-lg-12 col-md-9 card o-hidden border-0 shadow-lg my-5">
                    <div class="card-body p-0">
                        <!-- Nested Row within Card Body -->
                        <div class="row">
                            <div class="col-lg-6 d-none d-lg-block bg-login-image image"></div>
                            <div class="col-lg-6">
                                <div class="p-5">
                                    <div class="text-center">
                                        <h1 class="h4 text-gray-900 mb-4">Welcome Back!</h1>
                                    </div>
                                    <form class="user" @submit="login" novalidate="true">
                                        <div class="float-label-input">
                                            <input type="text" id="name" v-model="emailORusername" placeholder="">
                                            <label for="name">Email</label>
                                        </div>
                                        <div class="float-label-input">
                                            <input :type="pwd.PasswordIcon ? 'text' : 'password'" id="password"
                                                v-model="password" placeholder="">
                                            <label for="password">Password</label>
                                            <i class="toggle-password login-pwd-eye-position me-2"
                                                :class="pwd.PasswordIcon ? 'fas fa-eye-slash' : 'fas fa-eye'"
                                                @click="pwd.PasswordIcon = !pwd.PasswordIcon">
                                            </i>
                                        </div>
                                        <button class="btn btn-primary btn-user btn-block font-cursive" type="submit">
                                            Login
                                        </button>
                                        <hr>
                                        <!-- <div class="row justify-content-center font-cursive">
                                            <div class="col">
                                                <a href="index.html" class="btn btn-google btn-user btn-block">
                                                    Login with <i class="fab fa-google fa-fw"></i>
                                                </a>
                                            </div>
                                            <div class="col">
                                                <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                                    Login with <i class="fab fa-facebook-f fa-fw"></i>
                                                </a>
                                            </div>
                                        </div> -->
                                    </form>
                                    <hr>
                                    <!-- <div class="text-center">
                                        <a class="small" href="forgot-password.html">Forgot Password?</a>
                                    </div> -->
                                    <div class="text-center">
                                        <router-link class="small" to="/signup">Create an Account!</router-link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <!-- </div> -->




</template>

<script>
import axios from 'axios';

export default {
    name: 'LoginPage',
    data() {
        return {
            pwd: {
                PasswordIcon: false,
            },
            emailORusername: null, // null will be None in python
            password: "" // "" will be "" in python  , but both are fine
        }
    },
    methods: {
        login(e) {
            e.preventDefault();

            axios.post(`${this.$store.state.basePath}/my-login`, {
                emailORusername: this.emailORusername,
                password: this.password
            })
                .then(response => {
                    // console.log(response)
                    // return response.data.db_data;
                    return response.data.db_data;
                })
                .then(data => {
                    // console.log(data)
                    localStorage.setItem('user_id', data.id);
                    localStorage.setItem('auth_token', data.auth_token);
                    localStorage.setItem('email', data.email);
                    localStorage.setItem('username', data.username);
                    localStorage.setItem('name', data.name);
                    localStorage.setItem('role', data.role);
                    localStorage.setItem('role_id', data.role_id);
                    
                    this.$store.commit('updateAuthentication');
                    this.$store.commit('updateAuthToken');
                    this.$store.commit('updateRole');
                    this.$store.commit('updateRole_id');
                    this.$store.commit('updateUser_id');


                    // console.log(`Login with emailORusername: ${this.emailORusername} and password: ${this.password}`)
                    // console.log(localStorage.getItem("auth_token"));

                    // redirect to dashboard
                })
                .then(() => {
                    this.$router.push({ name: 'dashboard' });
                })
                .catch(error => {
                    this.$errorComesNow(error);  // from mixins
                })

            // clear form fields
            // this.emailORusername = '';
            // this.password = '';


        }
    }

}
</script>

<style scoped>
h1 {
    font-weight: 700;
    margin-top: 10px;
}

.animation {
    animation: myAnim .8s ease 0s 1 normal forwards;
}

@keyframes myAnim {
    0% {
        transform: translateX(100%);
    }

    100% {
        transform: translateX(0);
    }
}

.image{
    background-image: url('@/assets/sign-in.jpg');
    background-size: cover;
    background-position: center;
    height: 70vh;
    position: relative;
}
</style>