import store from './vuex';

export function beforeEach_guard(to) {   
    if (to.meta && to.meta.title) {
        document.title = to.meta.title;
    }
    if (to.meta.requiresAuth) {
        if (store.getters.isAuthenticated) {        
            if (to.name === 'login' || to.name === 'signup') {
                return { name: 'dashboard'  , params: {role : store.getters.role , user_id : store.getters.user_id } };
            }
            if (to.meta.allowedRoles) {              
                if (!to.meta.allowedRoles.includes(store.getters.role)) {
                    return {name : 'forbidden'};
                }
            }
        } else {
            if (to.name === 'login' || to.name === 'signup' || to.name === 'index' ) {  // routes having authRequired as false , it is redundent for checking here.
                return true;                            //  || to.name === 'home'
            }
            return { name: 'unauthorized' }; // after tha redirect to login.
        }
    } 
}
