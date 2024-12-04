<template>
  <adminDashboard v-if="$store.getters.role === 'admin'"></adminDashboard>
  <influencerDashboard v-else-if="$store.getters.role === 'influencer'"></influencerDashboard>
  <sponsorDashboard v-else-if="$store.getters.role === 'sponsor'"></sponsorDashboard>
</template>

<script>
import adminDashboard from '@/components/dashboard/admin.vue'
import influencerDashboard from '@/components/dashboard/influencer.vue'
import sponsorDashboard from '@/components/dashboard/sponsor.vue'

export default {
  name: 'User-Dashboard',
  components: {
    adminDashboard,
    influencerDashboard,
    sponsorDashboard,
  },
  props: {
  },
  data() {
    return {
    }
  },
  methods: {
  },
  computed: {
  },
  watch: {
  },
  beforeCreate() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    document.title = `${this.$capitalize(this.$store.getters.role)}'s Dashboard`;
  },
  beforeUpdate() {
  },
  updated() {
  },
  begoreUnmount() {
  },
  unmounted() {
  }
}
</script>

<style scoped></style>