<template>
  <adminNotifications v-if="$store.getters.role === 'admin'"></adminNotifications>
  <influencerNotifications v-else-if="$store.getters.role === 'influencer'"></influencerNotifications>
  <sponsorNotifications v-else-if="$store.getters.role === 'sponsor'"></sponsorNotifications>
</template>

<script>
import adminNotifications from '@/components/notifications/admin.vue'
import influencerNotifications from '@/components/notifications/influencer.vue'
import sponsorNotifications from '@/components/notifications/sponsor.vue'

export default {
  name: 'All-Notifications',
  components: {
    adminNotifications,
    influencerNotifications,
    sponsorNotifications,
  },
  computed: {
  },
  mounted() {
        document.title = 'Notifications';
    }

}
</script>

<style scoped></style>