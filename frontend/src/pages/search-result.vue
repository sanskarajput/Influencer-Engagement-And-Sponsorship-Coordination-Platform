<template>
    <AdminSearchResult v-if="$store.getters.role === 'admin'"></AdminSearchResult>
    <SponsorSearchResult v-else-if="$store.getters.role === 'sponsor'"></SponsorSearchResult>
    <InfluencerSearchResult v-else-if="$store.getters.role === 'influencer'"></InfluencerSearchResult>
</template>

<script>
import AdminSearchResult from '@/components/search/admin.vue';
import SponsorSearchResult from '@/components/search/sponsor.vue';
import InfluencerSearchResult from '@/components/search/influencer.vue';

export default {
    name: 'Search-Result',
    components: {
        AdminSearchResult,
        SponsorSearchResult,
        InfluencerSearchResult
    },
    mounted() {
        document.title = 'Search';
    }
}
</script>

<style scoped></style>