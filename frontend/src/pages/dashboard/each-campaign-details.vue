<template>
    <Show 
        v-if="$route.query.show" 
        :campaign_id="$route.query.show"
        @refresh-show-component-to-fetchAccordionData="uniqueKey++" 
        :key="uniqueKey">
    </Show>
    <Edit
        v-else-if="$store.getters.role === 'sponsor' && $route.query.edit" 
        :campaign_id="$route.query.edit">
    </Edit>
</template>

<script>
import Edit from '@/components/campaigns/edit.vue';
import Show from '@/components/campaigns/show.vue';

export default {
    name: 'Each-Campaign-Details-With--Edit(for sponsor)',
    components: {
        Show,
        Edit
    },
    data() {
        return {
            uniqueKey: 0
        }
    }
}
</script>

<style scoped>
Show {
    background-color: blue;
}
</style>