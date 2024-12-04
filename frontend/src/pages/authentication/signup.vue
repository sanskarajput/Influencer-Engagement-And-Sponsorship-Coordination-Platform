<template>
    <!-- <div class="container"> -->

    <div class="row justify-content-center animation">

        <div class="col-xl-10 col-lg-12 col-md-9">

            <div class="row justify-content-center">
                <div class="col-xl-10 col-lg-12 col-md-9 card o-hidden border-0 shadow-lg my-5">
                    <div class="card-body p-0">
                        <!-- Nested Row within Card Body -->
                        <div class="row">
                            <div class="col-lg-4 d-none d-lg-block bg-login-image image"></div>
                            <div class="col-lg-8">
                                <div class="p-5">
                                    <div class="text-center">
                                        <h1 class="h4 text-gray-900 mb-4">Create an Account !</h1> 
                                    </div>
                                    <form class="user" @submit="signup" novalidate="true">
                                        <div class="form-group row my-n3">
                                            <div class="col-sm-5 mb-n3">
                                                <div class="float-label-input">
                                                    <input type="text" id="username" v-model="username" placeholder="">
                                                    <label for="username">Username</label>
                                                </div>
                                            </div>
                                            <div class="col-sm-7">
                                                <div class="float-label-input">
                                                    <input type="text" id="name" v-model="name" placeholder="">
                                                    <label for="name">Full Name</label>
                                                </div>
                                            </div>
                                        </div>

                                        <div class="form-group mb-n3">
                                            <div class="float-label-input">
                                                <input type="email" id="email" v-model="email" placeholder="">
                                                <label for="email">Email</label>
                                            </div>
                                        </div>

                                        <div class="form-group row">
                                            <div class="col-sm-6">
                                                <div class="float-label-input">
                                                    <input :type="pwd.PasswordIcon ? 'text' : 'password'" id="password"
                                                        v-model="password" placeholder="">
                                                    <label for="password">Password</label>
                                                </div>
                                                <i class="toggle-password"
                                                    :class="pwd.PasswordIcon ? 'fas fa-eye-slash' : 'fas fa-eye'"
                                                    @click="pwd.PasswordIcon = !pwd.PasswordIcon">
                                                </i>
                                            </div>
                                            <div class="col-sm-6">
                                                <div class="float-label-input">
                                                    <input :type="pwd.RepeatPasswordIcon ? 'text' : 'password'"
                                                        id="repeatPassword" v-model="repeatPassword" placeholder="">
                                                    <label for="repeatPassword">Repeat Password</label>
                                                </div>
                                                <i class="toggle-password"
                                                    :class="pwd.RepeatPasswordIcon ? 'fas fa-eye-slash' : 'fas fa-eye'"
                                                    @click="pwd.RepeatPasswordIcon = !pwd.RepeatPasswordIcon">
                                                </i>
                                            </div>
                                        </div>

                                        <div class="form-group row text-center mt-n3">
                                            <div class="col-sm-4 form-check mb-1">
                                                <input class="form-check-input" type="radio" name="role" id="role-1"
                                                    value="sponsor" v-model="role">
                                                <label class="form-check-label font-cursive"
                                                    for="role-1">Sponsor</label>
                                            </div>
                                            <div class="col-sm-4 form-check mb-1">
                                                <input class="form-check-input" type="radio" name="role" id="role-2"
                                                    value="influencer" v-model="role">
                                                <label class="form-check-label font-cursive"
                                                    for="role-2">Influencer</label>
                                            </div>
                                            <div class="col-sm-4 form-check mb-1">
                                                <input class="form-check-input" type="radio" name="role" id="role-3"
                                                    value="admin" v-model="role" disabled>
                                                <label class="form-check-label font-cursive" 
                                                    for="role-3">Admin</label>
                                            </div>
                                        </div>

                                        <button class="btn btn-primary btn-user btn-block font-cursive"
                                            type="submit">Signup</button>

                                        <hr>
                                        <!-- <div class="row justify-content-center font-cursive">
                                            <div class="col">
                                                <a href="index.html" class="btn btn-google btn-user btn-block">
                                                    Register with <i class="fab fa-google fa-fw"></i>
                                                </a>
                                            </div>
                                            <div class="col">
                                                <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                                    Register with <i class="fab fa-facebook-f fa-fw"></i>
                                                </a>
                                            </div>
                                        </div> -->
                                    </form>
                                    <hr>
                                    <div class="text-center">
                                        <router-link class="small" to="/login">Already have an account? Login !</router-link>
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
export default {
    name: 'SignupPage',
    data() {
        return {
            pwd: {
                PasswordIcon: false,
                RepeatPasswordIcon: false
            },
            email: "",
            username: null,
            name: null,
            role: "influencer",
            password: null,
            repeatPassword: null
        }
    },
    methods: {
        signup(e) {
            e.preventDefault();

            // add fetch api
            fetch(`${this.$store.state.basePath}/my-signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    username: this.username,
                    name: this.name,
                    role: this.role,
                    password: this.password
                })
            })
                .then(response => {
                    // console.log(response)
                    if (!response.ok) {
                        // First parse the error response before throwing
                        return response.json().then(errData => {
                            throw new Error(`HTTP error! status: ${response.status}, error: ${JSON.stringify(errData)}`);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                    this.$router.push({ name: 'login' })
                })
                .catch(error => console.error(error))


            // clear form fields
            // this.email = '';
            // this.username = '';
            // this.name = '';
            // this.role = '';
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
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(0);
    }
}

.image{
    background-image: url('@/assets/sign-up.jpg');
    background-size: cover;
    background-position: center;
    height: 100vh;
    position: relative;
}
</style>