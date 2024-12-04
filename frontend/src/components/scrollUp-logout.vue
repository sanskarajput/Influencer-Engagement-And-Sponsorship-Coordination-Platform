<template>
    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#app">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Logout Modal-->
    <div v-if="$store.getters.isAuthenticated" class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                    <button class="btn btn-primary" data-dismiss="modal" @click="logout">Logout</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Scroll-Logout-model',
    methods: {
        logout() {
            localStorage.removeItem('auth_token');
            this.$router.push({ name: 'logout' });
            setTimeout(()=> {
                localStorage.clear();

                this.$store.commit('updateAuthentication');
                this.$store.commit('updateAuthToken');
                this.$store.commit('updateUser_id');
                this.$store.commit('updateRole_id');
                this.$store.commit('updateRole');
                console.log("Logged out user.");
            },1000) 
        },
    }
}
</script>

<style scoped></style>
