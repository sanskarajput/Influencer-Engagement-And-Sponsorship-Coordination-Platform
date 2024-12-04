<template>
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="mb-0 text-gray-800 fw-bold fs-2">
            Request Details
        </h1>
    </div>
    <Card></Card>
</template>

<script>
import Card from '@/components/requests/card.vue';

export default {
    name: 'Each-Request-Details',
    components: {
        Card
    }

}
</script>

<style scoped></style>