import { createWebHistory, createRouter } from "vue-router";

const routes = [
    {
        name: "index",
        path: "/",
        meta: { requiresAuth: false , title : "Index Page"},
        component : () => import("@/pages/home.vue")
    },
    {
        name: "login",
        path: "/login",
        meta: { requiresAuth: true , title : "Login"},
        component: () => import("@/pages/authentication/login.vue")
    },
    {
        name: "signup",
        path: "/signup",
        meta: { requiresAuth: true , title : "Sign up" },
        component: () => import("@/pages/authentication/signup.vue")
    },
    {
        name: "logout",
        path: "/logout",
        // meta: { requiresAuth: true }, // Note that Navigation Guards are not applied on the route that redirects, only on its target.
        redirect: { name: "index" }
    },
    {
        name: "pageNotFound",
        path: "/:NotFound(.*)*",
        component: () => import("@/pages/errors/pageNotFound.vue")
    },
    {
        name: "forbidden",
        path: "/forbidden",
        meta: { requiresAuth: true },
        component: () => import("@/pages/errors/forbidden.vue")
    },
    {
        name: "unauthorized",
        path: "/unauthorized",
        // redirect : {name : "login"},
        component: () => import("@/pages/errors/unauthorized.vue")
    },
    {
        name: "network-error",
        path: "/network-error",
        component: () => import("@/pages/errors/network-error.vue")
    },
    {
        name: "profile",
        path: "/your-profile",
        props: true,
        meta: { requiresAuth: true, allowedRoles: ["sponsor", "influencer", "admin"], title : "Your Profile" },
        component: () => import("@/pages/profile.vue")
    },
    {
        name: "settings",
        path: "/settings",
        props: true,
        meta: { requiresAuth: true, allowedRoles: ["sponsor", "influencer", "admin"] , title : "Settings"},
        component: () => import("@/pages/settings.vue")
    },
    {
        name: "notifications",
        path: "/dashboard/notifications",
        meta: { requiresAuth: true, allowedRoles: ["admin", "sponsor", "influencer"], title : "Notifications" },
        component: () => import("@/pages/notifications.vue"),
    },
    {
        name: "dashboard",
        path: "/dashboard",
        meta: { requiresAuth: true, allowedRoles: ["sponsor", "influencer", "admin"] , title : "Dashboard"},
        component: () => import("@/pages/dashboard.vue"),
    },
    {
        name: "search",
        path: "/search-result", // query
        meta: { requiresAuth: true, allowedRoles: ["sponsor", "influencer"] , title : "Search Results"},
        component: () => import("@/pages/search-result.vue"),
    },
    {
        name: "other-user-profile-view",
        path: "/dashboard/:role(sponsor|influencer)-profile",  // query will be user_id
        meta: { requiresAuth: true, allowedRoles: ["influencer","sponsor","admin"] , title : "Users Profile"},
        component: () => import("@/pages/dashboard/other-user-profile-view.vue"),
    },
    {
        name: "each-campaign-details",
        path: "/dashboard/campaign", // show
        meta: { requiresAuth: true, allowedRoles: ["influencer","sponsor","admin"] , title : "Campaign Details"},
        component: () => import("@/pages/dashboard/each-campaign-details.vue"),
        props: true,
    },
    {
        name: "each-request-details",
        path: "/dashboard/request", // show 
        meta: { requiresAuth: true, allowedRoles: ["influencer","sponsor","admin"], title : "Requests Details" },
        component: () => import("@/pages/dashboard/each-request-details.vue"),
        props: true,
    },
    {
        name: "all-influencers",
        path: "/dashboard/all-influencers",
        meta: { requiresAuth: true, allowedRoles: ["sponsor","admin"] , title : "All Influencers"},
        component: () => import("@/pages/dashboard/all-influencers.vue"),
        props: true,
    },
    {
        name: "all-sponsors",
        path: "/dashboard/all-sponsors",
        meta: { requiresAuth: true, allowedRoles: ["influencer","admin"] , title : "All Sponsors" },
        component: () => import("@/pages/dashboard/all-sponsors.vue"),
    },
    //////////////////////////////////// resources-for-sponsors
    {
        name: "add-campaign",
        path: "/dashboard/add-campaign",
        meta: { requiresAuth: true, allowedRoles: ["sponsor"], title : "Add Campaigns" },
        component: () => import("@/pages/dashboard/sponsor.campaigns.add.vue"),
    },
    {
        name: "all-campaigns-for-sponsors",// only his
        path: "/dashboard/my-all-campaigns",
        meta: { requiresAuth: true, allowedRoles: ["sponsor"] , title : "My All Campaigns"},
        component: () => import("@/pages/dashboard/sponsor.campaigns.all-campaigns.vue"),
    },
    {
        name: "all-requests-for-sponsors",
        path: "/dashboard/my-all-requests",
        meta: { requiresAuth: true, allowedRoles: ["sponsor"] , title : "My All Requests"},
        component: () => import("@/pages/dashboard/sponsor.requests.all-requests.vue"),
        props: true,
    },
    // each-influencer-profile-view-for-sponsors === other-user-profile-view

    //////////////////////////////////// resources-for-influencers
    {
        name: "all-public-campaigns-for-influencers",
        path: "/dashboard/all-campaigns",
        meta: { requiresAuth: true, allowedRoles: ["influencer"] , title : "All Campaigns"},
        component: () => import("@/pages/dashboard/influencer.campaigns.all-public-campaigns.vue"),
    },
    {
        name: "all-requests-for-influencers",
        path: "/dashboard/my-requests",
        meta: { requiresAuth: true, allowedRoles: ["influencer"] , title : "My All Requests"},
        component: () => import("@/pages/dashboard/influencer.requests.all-requests.vue"),
    },
    // each-sponsor-profile-view-for-influencers === other-user-profile-view

    ///////////////////////// resources-for-admin
    {
        name: "all-campaigns-for-a-admin",
        path: "/dashboard/all-available-campaigns",
        meta: { requiresAuth: true, allowedRoles: ["admin"], title : "All Available Campaigns" },
        component: () => import("@/pages/dashboard/admin.all-campaigns.vue"),
    }
]


const routers = createRouter({
    history: createWebHistory(),
    routes
})


import { beforeEach_guard } from './navigation-guards';
routers.beforeEach(beforeEach_guard);

export default routers;