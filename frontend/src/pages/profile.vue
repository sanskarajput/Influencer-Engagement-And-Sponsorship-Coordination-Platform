<template>
    <profile></profile>
</template>

<script>
import profile from '@/components/profile/main.vue';

export default {
    name: 'ProfileView',
    components:{
        profile
    },
    mounted() {
        document.title = 'User Profile';
    }

}
</script>

<style scoped></style>