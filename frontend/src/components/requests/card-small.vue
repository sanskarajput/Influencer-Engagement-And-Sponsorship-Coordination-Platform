<template>
    <div class="card">
        <div class="header-section">
            <h6>Request Details</h6>
            <div class="status-section">
                <div class="status-badge" :class="`status-${request.status.toLowerCase()}`">
                    <i class="fas fa-clock"></i>
                    <span>{{ request.status }}</span>
                </div>
                <div class="header-actions">
                    <div class="action-dropdown">
                        <button onclick="this.nextElementSibling.classList.toggle('show')">
                            <i class="fas fa-ellipsis-h"></i>
                            <!-- <i class="fa-solid fa-ellipsis-vertical"></i> -->
                            <!-- <i class="fa-solid fa-bars"></i> -->
                        </button>
                        <div class="action-popover">
                            <button class="action-item"
                                @click="$router.push({ name: 'each-request-details', query: { 'show': request.adRequest_id } })">
                                <i class="fas fa-eye"></i>
                                <span>Details</span>
                            </button>
                            <button class="action-item text-danger"  v-if="$store.getters.role === 'sponsor'"
                            @click="deleteAdRequest">
                                <i class="fa-solid fa-trash-arrow-up"></i>
                                <span>Remove</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-content">
            <div class="message-section">
                <div class="message-header">
                    <i class="fas fa-comment-alt me-2"></i>
                    Message
                </div>
                <div class="message-text-wrapper">
                    <div class="message-content">
                        {{ request.message }}
                    </div>
                    <div class="message-tooltip">
                        {{ request.message }}
                    </div>
                </div>
            </div>

            <div class="payment-card">
                <div class="payment-info">
                    <span class="payment-label">                    
                        <i class="fas fa-credit-card me-2"></i>
                        Payment Amount
                    </span>
                    <span class="payment-value">₹ {{ request.payment }}</span>
                </div>
                <div class="payment-icon">
                    <i class="fas fa-credit-card"></i>
                </div>
            </div>


            <div class="requirements-section">
                <div class="requirements-header">
                    <i class="fas fa-clipboard-list me-2"></i>
                    Requirements
                </div>
                <div class="requirements-list">
                    <div class="requirement-item" v-for="(requirement,index) in request.requirements.split('$@$')" :key="index">
                        <span class="requirement-number">{{ index+1 }}</span>
                        <div class="requirement-text-wrapper">
                            <div class="requirement-text">{{ requirement }}</div>
                            <div class="requirement-tooltip">{{ requirement }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'card-small',
    emits: ['refresh-show-component-to-fetchAccordionData'],
    props: {
        request: {
            type: Object,
            required: true
        }
    },
    methods: {
        async deleteAdRequest() {
            try {
                const response = await axios.delete(`${this.$store.state.basePath}/request/delete/${this.request.adRequest_id}`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );
                const data = response.data.db_data;
                console.log(data);
                this.$emit('refresh-show-component-to-fetchAccordionData');
                this.$toast.success('Request removed successfully !',
                {
                    position: 'bottom-right',
                    duration: 5000,
                        dismissible: true
                    }
                )

            } catch (error) {
                this.$errorComesNow(error);
            }
        }
    },
    mounted() {
        document.addEventListener('click', function (event) {
            const dropdowns = document.querySelectorAll('.action-popover');
            dropdowns.forEach(dropdown => {
                if (!dropdown.closest('.action-dropdown').contains(event.target)) {
                    dropdown.classList.remove('show');
                }
            });
        });
    }
}
</script>

<style scoped>
.card {
    background: white;
    border-radius: 9.6px;
    padding: 1.2rem;
    box-shadow: 0 2.4px 12px -0.6px rgb(0 0 0 / 0.1);
    width: 100%;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1.2px solid #e5e7eb;
}

h6 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1e293b;
}

.status-section {
    display: flex;
    gap: 0.6rem;
    align-items: center;
    position: relative;
    bottom: 3px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.3rem 0.6rem 0.2rem;
    border-radius: 9999px;
    font-weight: bolder;
}

.status-pending {
    background-color: #fde68a;
    color: #92400e;
}

.status-accepted {
    background-color: #a7f3d0;
    color: #064e3b;
}

.status-declined {
    background-color: #fecaca;
    color: #991b1b;
}

.status-completed {
    background-color: #bfdbfe;
    color: #1e40af;
}

.status-rejected {
    background-color: #e5e7eb;
    color: #374151;
}


.status-badge i {
    font-size: 0.7rem;
    position: relative;
    bottom: 0.5px;
}

.status-badge span {
    font-size: .7rem;
}

.action-dropdown {
    position: relative;
}

.action-dropdown>i {
    font-size: 2rem;
}

.action-dropdown>button {
    background: none;
    border: none;
    cursor: pointer;
    height: 2rem;
    width: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgb(177, 217, 252);
    border-radius: 50%;
}

.action-dropdown>button i {
    font-size: 1rem;
    color: #000000;
}

.action-popover {
    display: none;
    position: absolute;
    top: 120%;
    right: 0;
    background: rgb(177, 217, 252);
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 10;
    width: 100px;
    padding: 0.3rem;
}

.action-popover.show {
    display: block;
}

.action-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    width: 100%;
    background: none;
    border: none;
    padding: 0.3rem 0.6rem;
    font-size: 0.9rem;
    color: #010101;
    cursor: pointer;
    text-align: left;
    border-radius: 4px;
}

.action-item:hover {
    background-color: #f1f5f9;
}

.action-item:nth-child(3) span {
    font-weight: 700;
}

.main-content {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.message-section {
    background: #f1f5f9;
    padding: 0.5rem 0.9rem;
    border-radius: 7.2px;
    border: 0.6px solid #e2e8f0;
}

.message-header {
    font-size: 0.76rem;
    font-weight: 600;
    color: #000000;
    margin-bottom: 0.3rem;
}

.message-header span {
    font-size: 0.86rem;
}

.message-text-wrapper {
    position: relative;
}

.message-content {
    color: #475569;
    line-height: 1.6;
    font-size: 0.7rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}

.message-text-wrapper:hover .message-tooltip {
    display: block;
}

.message-tooltip {
    display: none;
    position: absolute;
    background: #333;
    color: white;
    padding: 0.3rem;
    border-radius: 2.4px;
    font-size: 1rem;
    width: 100%;
    z-index: 1000;
    top: 100%;
    left: 0;
    margin-top: 3px;
    box-shadow: 0 1.2px 2.4px rgba(0, 0, 0, 0.2);
}

.payment-card {
    background: #f1f5f9;
    padding: 0.5rem 0.9rem;
    border-radius: 7.2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 0.6px solid #e2e8f0;
}

.payment-info {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.payment-label {
    font-size: 0.76rem;
    font-weight: 700;
    color: #000000;
}

.payment-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #334155;
}

.payment-icon {
    min-width: 28.8px;
    width: 28.8px;
    height: 28.8px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    font-size: 0.75rem;
}

.requirements-section {
    background: #f1f5f9;
    padding: 0.5rem 0.9rem;
    border-radius: 7.2px;
    border: 0.6px solid #e2e8f0;
}

.requirements-header {
    font-size: 0.76rem;
    font-weight: 600;
    color: #000000;
    margin-bottom: 0.6rem;
}

.requirements-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.requirement-item {
    display: flex;
    gap: 0.6rem;
    padding: 0.6rem;
    background: white;
    border-radius: 4.8px;
    border: 0.6px solid #e2e8f0;
}

.requirement-number {
    flex-shrink: 0;
    min-width: 16.8px;
    width: 16.8px;
    height: 16.8px;
    background: #e2e8f0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.525rem;
    font-weight: 600;
    color: #475569;
}

.requirement-text-wrapper {
    position: relative;
    width: 100%;
}

.requirement-text {
    color: #475569;
    line-height: 1.6;
    font-size: 0.7rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}


.requirement-text-wrapper:hover .requirement-tooltip {
    display: block;
}

.requirement-tooltip {
    display: none;
    position: absolute;
    background: #333;
    color: white;
    padding: 0.3rem;
    border-radius: 2.4px;
    font-size: 1rem;
    width: 100%;
    z-index: 1000;
    top: 100%;
    left: 0;
    margin-top: 3px;
    box-shadow: 0 1.2px 2.4px rgba(0, 0, 0, 0.2);
}
</style>