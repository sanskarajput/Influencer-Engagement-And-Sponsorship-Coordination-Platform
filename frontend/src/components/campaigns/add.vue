<template>
    <Form ref="formRef" :formData="formData" url="add-new" requestMethod="post">
        <template v-slot:title>
            <h1 class="text-center fw-bold fs-1 text-black">Create campaign</h1>
        </template>
        <template v-slot:button>
            <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary mx-5">Publish</button>
                <button type="submit" class="btn btn-danger" @click="$refs.formRef.viewCampaign = true">Publish and
                    View</button>
            </div>
        </template>
    </Form>
</template>

<script>
import Form from './form.vue'

export default {
    name: 'Create-Campaign',
    components: {
        Form
    },
    data() {
        return {
            intervalId: null,
            formData: {
                name: null,
                description: null,
                category: null,
                start_date: this.getTodayDate(),
                start_time: this.getCurrentTime(),
                end_date: this.getDateAfterOnWeek(),
                end_time: this.getCurrentTime(),
                budget: null,
                visibility: null,
                goals: null
            }
        }
    },
    methods: {
        getTodayDate() {
            let today = new Date();
            let dd = String(today.getDate()).padStart(2, '0');
            let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            let yyyy = today.getFullYear();
            return yyyy + '-' + mm + '-' + dd;
        },
        getDateAfterOnWeek() {
            let today = new Date();
            let tomorrow = new Date(today);
            tomorrow.setDate(today.getDate() + 7);
            let dd = String(tomorrow.getDate()).padStart(2, '0');
            let mm = String(tomorrow.getMonth() + 1).padStart(2, '0');
            let yyyy = tomorrow.getFullYear();
            return yyyy + '-' + mm + '-' + dd;
        },
        getCurrentTime() {
            // 24 hour format
            let today = new Date();
            let hh = String(today.getHours()).padStart(2, '0');
            let mm = String(today.getMinutes()).padStart(2, '0');
            return hh + ':' + mm;
        },
    },
    mounted() {
        this.intervalId = setInterval(() => {
            this.formData.start_time = this.getCurrentTime();
            this.formData.end_time = this.getCurrentTime();
        }, 1000 * 60); // Update every minute
    },
    beforeUnmount() {
        clearInterval(this.intervalId);
    }
}
</script>

<style scoped></style>