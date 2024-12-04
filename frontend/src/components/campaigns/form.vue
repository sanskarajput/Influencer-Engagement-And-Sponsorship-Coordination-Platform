<template>
    <div class="campaign-form-container">
        <div class="form-wrapper">
            <slot name="title"></slot>
            <form @submit.prevent="submitForm" novalidate="true">
                <div class="form-group row">
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="text" id="name" v-model="localFormData.name" placeholder="">
                            <label for="name">Title</label>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="text" id="category" v-model="localFormData.category" placeholder="">
                            <label for="category">Category</label>
                        </div>
                    </div>
                </div>

                <div class="form-group row">
                    <div class="col">
                        <div class="float-label-input">
                            <textarea class="stretch-textarea" type="text" id="description"
                                v-model="localFormData.description" rows="" @input="adjustHeight"
                                ref="autoResizeDescription" placeholder=""></textarea>
                            <label for="description">Description</label>
                        </div>
                    </div>
                </div>

                <div class="group-form row">
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="date" id="start_date" v-model="localFormData.start_date" placeholder="">
                            <label for="start_date">Start Date</label>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="time" id="start_time" v-model="localFormData.start_time" placeholder="">
                            <label for="start_time">Start Time</label>
                        </div>
                    </div>
                </div>

                <div class="group-form row">
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="date" id="end_date" v-model="localFormData.end_date" placeholder="">
                            <label for="end_date">End Date</label>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="time" id="end_time" v-model="localFormData.end_time" placeholder="" required>
                            <label for="end_time">End Time</label>
                        </div>
                    </div>
                </div>

                <div class="group-form row mt-4">
                    <div class="col-sm-6">
                        <div class="float-label-input">
                            <input type="number" id="budget" v-model.number="localFormData.budget" placeholder="">
                            <label for="budget">Budget</label>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="float-label-input my-custom-select">
                            <select id="visibility" v-model="localFormData.visibility" required>
                                <option disabled value="">None</option>
                                <option value="PUBLIC">Public</option>
                                <option value="PRIVATE">Private</option>
                            </select>
                            <label for="visibility" class="form-label">Select Visibility</label>
                        </div>
                    </div>
                </div>

                <div class="group-form row mt-4">
                    <div class="col">
                        <div class="float-label-input">
                            <textarea class="stretch-textarea" type="text" id="goals" v-model="localFormData.goals"
                                rows="" @input="adjustHeight" ref="autoResizeGoals" placeholder=""></textarea>
                            <label for="goals">Goals</label>
                        </div>
                    </div>
                </div>
                <slot name="button"></slot>
            </form>
        </div>
    </div>  
</template>

<script>
import axios from 'axios';

export default {
    name: 'Add-Campaigns',
    props: {
        formData: {
            type: Object,
            required: true,
        },
        url: {
            type: String,
            required: true,
        },
        requestMethod: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            viewCampaign: false,
            localFormData: { ...this.formData } // Creating a local copy of formData
        }
    },
    methods: {
        async submitForm() {
            try {
                const response = await axios[this.requestMethod](
                    `${this.$store.state.basePath}/campaign/${this.url}`,
                    this.localFormData, // Useing local copy of formData for submission
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                // Redirect to show the newly created campaign OR edited campaign
                if (this.requestMethod === 'post') {
                    // this.localFormData = { ...this.formData }  // Reseting localFormData
                    if (this.viewCampaign) {
                        this.viewCampaign = false;  // reseting viewCampaign

                        this.$router.push({ name: 'each-campaign-details', query: { show: response.data.db_data.id } })
                        this.$toast.success('Campaign Created Successfully - redirected to detailed view of Campaign !', {position: 'top'});
                    } else {
                        this.$toast.success('Campaign Created Successfully !', {position: 'top'});
                    }
                } else if (this.requestMethod === 'put') {
                    if (this.viewCampaign) {
                        this.viewCampaign = false;  // reseting viewCampaign
                        this.localFormData = { ...this.formData }  // Resetinging localFormData

                        this.$router.push({ name: 'each-campaign-details', query: { show: response.data.db_data.id } })
                        this.$toast.success('Campaign updated Successfully - redirected to detailed view of Campaign !', {position: 'top'});
                    } else {
                        this.$toast.success('Campaign updated Successfully !', {position: 'top'});
                    }
                }
            } catch (error) {
                this.viewCampaign = false;
                this.$errorComesNow(error);
            }
        },
        adjustHeight() {
            // Adjust the height of the textarea
            const des_textarea = this.$refs.autoResizeDescription;
            const golas_textarea = this.$refs.autoResizeGoals;
            if (des_textarea) {
                des_textarea.style.height = 'auto'; // Reseting height to shrink if needed
                des_textarea.style.height = `${des_textarea.scrollHeight}px`; // Set height based on scrollHeight
                des_textarea.addEventListener('blur', function () {
                    des_textarea.style.height = 'auto';
                });
            }
            if (golas_textarea) {
                golas_textarea.style.height = 'auto';   
                golas_textarea.style.height = `${golas_textarea.scrollHeight}px`;   
                golas_textarea.addEventListener('blur', function () {
                    golas_textarea.style.height = 'auto';
                });
            }
        },
    },
    watch: {
        formData: {
            deep: true,  // Watch for nested properties changes
            immediate: true,
            handler(newValue) {
                this.localFormData = { ...newValue }; // Update local copy when prop changes
            }
        }
    },
    unmounted() {
        this.localFormData = { ...this.formData }
    }
}
</script>

<style scoped>
.campaign-form-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9fafb;
}

.form-wrapper {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 30px;
}

.form-title {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 25px;
    font-size: 24px;
    font-weight: 600;
}


select {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    margin-right: 300px;
    background: url('../../assets/down-arrow-image.svg') no-repeat;
    background-position: right 15px center;
    background-size: 14px;
    cursor: pointer;
}


.stretch-textarea {
    width: 100%;
    /* Full width of the cell */
    height: auto;
    /* Initial height is auto */
    min-height: 40px;
    /* Set a minimum height for the textarea */
    resize: none;
    /* Disable manual resizing */
    box-sizing: border-box;
    /* Include padding and border in the element's total width and height */
    overflow: hidden;
}

input[type="date"]::-webkit-calendar-picker-indicator {
    position: absolute;
    right: 15px;
    bottom: 8px;
}

input[type="time"]::-webkit-calendar-picker-indicator {
    position: absolute;
    right: 15px;
    bottom: 6px;
    font-size: 1.2rem;

}
</style>
