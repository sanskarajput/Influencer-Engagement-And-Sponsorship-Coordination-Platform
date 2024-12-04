import Vuex from 'vuex'

const store = new Vuex.Store({
    state: {
        basePath: 'http://127.0.0.1:5000',
        user : {
            isAuthenticated : !!localStorage.getItem("auth_token"), // Initialize based on auth_token presence
            auth_token : localStorage.getItem("auth_token") ? localStorage.getItem("auth_token") : null,
            user_id : localStorage.getItem("user_id") ? Number(localStorage.getItem("user_id")) : null,
            role : localStorage.getItem("role") ? localStorage.getItem("role").toLowerCase() : null,
            role_id : localStorage.getItem("role_id") ? Number(localStorage.getItem("role_id")) : null,
        }
    },
    getters: {
        isAuthenticated: state => state.user.isAuthenticated, // Getter will now use state
        auth_token: state => state.user.auth_token,  // Getter will now use state
        user_id: state => state.user.user_id,
        role: state => state.user.role,
        role_id: state => state.user.role_id,
    },
    mutations: {
        updateAuthentication(state) {
            state.user.isAuthenticated = !!localStorage.getItem("auth_token");
        },
        updateAuthToken(state) {
            state.user.auth_token = localStorage.getItem("auth_token") ? localStorage.getItem("auth_token") : null;
        },
        updateUser_id(state) {
            state.user.user_id = localStorage.getItem("user_id") ? Number(localStorage.getItem("user_id")) : null;
        },
        updateRole(state) {
            state.user.role = localStorage.getItem("role") ? localStorage.getItem("role").toLowerCase() : null;
        },
        updateRole_id(state) {
            state.user.role_id = localStorage.getItem("role_id") ? Number(localStorage.getItem("role_id")) : null;
        }
    },
    actions: {
        //////////////////////////////////// create actions like this
        // updateAuthentication({ commit }) {
        //     const auth_tokenExists = !!localStorage.getItem("auth_token");
        //     commit('updateAuthenticated', auth_tokenExists);
        // }
    }
});



export default store;