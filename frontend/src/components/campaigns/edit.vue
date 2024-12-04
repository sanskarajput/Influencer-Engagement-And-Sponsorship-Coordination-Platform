<template>
    <Form ref="formRef" :formData="formData" :url="url" requestMethod="put">
        <template v-slot:title>
            <h1 class="form-title">Edit campaign details</h1>
        </template>
        <template v-slot:button>
            <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary mx-5">Save Changes</button>
                <button type="submit" class="btn btn-danger" @click="$refs.formRef.viewCampaign=true">Save Changes and View</button>
            </div>
        </template>
    </Form>
</template>

<script>
import axios from 'axios';
import Form from './form.vue';

export default {
    name: 'Edit-Campaign-Details',
    components: {
        Form
    },
    props: {
        campaign_id: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            formData: {
                name: null,
                description: null,
                category: null,
                start_date:null,
                start_time: null,
                end_date: null,
                end_time: null,
                budget: null,
                visibility: null,
                goals: null
            }
        }
    },
    computed: {
        url() {
            return `edit-all/${this.campaign_id}`;
        }
    },
    async beforeMount() {
        try {
            const response = await axios.get(`${this.$store.state.basePath}/campaign/${this.url}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    }
                }
            );
            const data = response.data.db_data;

                this.formData.name = data.name;
                this.formData.description = data.description;
                this.formData.category = data.category;
                this.formData.start_date = this.$getDateTimeInUTC(data.start_date).date;
                this.formData.start_time = this.$getDateTimeInUTC(data.start_date).time;
                this.formData.end_date = this.$getDateTimeInUTC(data.end_date).date;
                this.formData.end_time = this.$getDateTimeInUTC(data.end_date).time;
                this.formData.budget = data.budget;
                this.formData.visibility = data.visibility;
                this.formData.goals = data.goals;
                    
        } catch (error) {
            this.$errorComesNow(error);
        }

    }
}
</script>

<style scoped>

.form-title {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 25px;
    font-size: 24px;
    font-weight: 600;
  }</style>