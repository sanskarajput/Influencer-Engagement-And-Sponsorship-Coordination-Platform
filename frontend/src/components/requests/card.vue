<template>
  <div class="card">
    <div class="header-section">
      <h1>
        <span>
          Request Details
        </span>
        <span class="fs-6">
          <span v-if="$store.getters.role === 'influencer'|| $store.getters.role === 'admin'">for Campaign : <router-link :to="{name: 'each-campaign-details', query: {show:campaign_id}}"> {{ campaign_name }} </router-link></span>
          <span v-if="$store.getters.role === 'sponsor'">for your Campaign : <router-link :to="{name: 'each-campaign-details', query: {show:campaign_id}}"> {{ campaign_name }} </router-link></span>
          <span v-if="$store.getters.role === 'sponsor' || $store.getters.role === 'admin'"> with Influencer : <router-link :to="{name: 'other-user-profile-view', params:{ role:'influencer' }, query: {user_id:influencer_s_user_id}}"> {{ influencer_name }} </router-link></span>
        </span>
      </h1>
      <div class="status-section">
        <div class="status-badge" :class="`status-${status.toLowerCase()}`">
          <i class="fas fa-clock"></i>
          {{ status }}
          <button class="edit-button" @click="editingStatus = true; showDeletePopover = false; editedStatus = status"
            v-if="$store.getters.role === 'influencer' && availableTransitions.length">
            <i class="fa-solid fa-pen"></i>
          </button>
        </div>
        <form v-if="editingStatus && availableTransitions.length" class="status-edit-form-popover">
          <div class="radio-group">
            <div class="radio-item">
              <input type="radio" :id="status.toLowerCase()" :value="editedStatus" v-model="editedStatus" name="status"
                @change="saveStatus">
              <label :for="status.toLowerCase()" class="status-badge" :class="`status-${status.toLowerCase()}`">
                <i class="fas fa-clock"></i>
                {{ editedStatus }}
              </label>
            </div>
            <div v-for="newStatus in availableTransitions" :key="newStatus" class="radio-item">
              <input type="radio" :id="newStatus.toLowerCase()" :value="newStatus" v-model="editedStatus" name="status"
                @change="saveStatus">
              <label :for="newStatus.toLowerCase()" class="status-badge" :class="`status-${newStatus.toLowerCase()}`">
                <i class="fas fa-clock"></i>
                {{ newStatus }}
              </label>
            </div>
            <button type="button" class="cancel-button"
              @click="editingStatus = false; editedStatus = ''">Cancel</button>
          </div>
        </form>
      </div>
      <div class="delete-button-section" v-if="$store.getters.role === 'sponsor'">
        <button class="delete-button" @click="showDeletePopover = true; editingStatus = false">
          <i class="fas fa-trash"></i>
        </button>
        <div v-if="showDeletePopover" class="popover">
          <p>Are you sure you want to delete?</p>
          <div class="popover-actions">
            <button @click="confirmDelete" class="confirm-button">Confirm</button>
            <button @click="showDeletePopover = false" class="cancel-button">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <div class="requirements-section">
        <div class="section-header">
          <div class="header-content">
            <i class="fas fa-clipboard-list me-2"></i>
            Requirements
          </div>
          <button v-if="$store.getters.role === 'sponsor' && !editingRequirements" class="edit-button"
            @click="editingRequirements = true; editedRequirements = requirements;">
            <i class="fa-solid fa-pen"></i>
          </button>
        </div>

        <div v-if="!editingRequirements" class="requirements-list">
          <div v-for="(req, index) in requirements" :key="index" class="requirement-item">
            <span class="requirement-number">{{ index + 1 }}</span>
            <div class="requirement-text">{{ req.text }}</div>
          </div>
        </div>

        <form v-else @submit.prevent="saveRequirements" class="requirements-edit-form">
          <div v-for="(req, index) in editedRequirements" :key="index" class="requirement-edit-item">
            <span class="requirement-number">{{ index + 1 }}</span>
            <textarea v-model="req.text" class="edit-input" placeholder="Enter requirement..."
              style="overflow: hidden; width: 100%;" rows="1"></textarea>
          </div>
          <button @click.prevent="addRequirement" class="add-button">
            <i class="fas fa-plus"></i> Add Requirement
          </button>
          <div class="button-group">
            <button type="submit" class="save-button">Save All Requirements</button>
            <button type="button" class="cancel-button"
              @click="editingRequirements = false; editedRequirements = []">Cancel</button>
          </div>

        </form>
      </div>

      <div class="side-section">
        <div class="payment-card">
          <div class="section-header">
            <div class="header-content">
              <i class="fas fa-credit-card me-2"></i>
              Payment Amount <i v-if="editingPayment"><b>in ₹</b></i>
            </div>
            <button v-if="$store.getters.role === 'sponsor' && !editingPayment" class="edit-button" @click="editingPayment = true; editedPayment = payment">
              <i class="fa-solid fa-pen"></i>
            </button>
          </div>
          <div v-if="!editingPayment" class="payment-value">₹ {{ payment }}.00</div>
          <form v-else @submit.prevent="savePayment" class="payment-edit-form">
            <input v-model="editedPayment" type="number" class="edit-input" />
            <div class="button-group">
              <button type="submit" class="save-button">Save Amount</button>
              <button type="button" class="cancel-button"
                @click="editingPayment = false; editedPayment = ''">Cancel</button>
            </div>
          </form>
        </div>

        <div class="message-section">
          <div class="section-header">
            <div class="header-content">
              <i class="fas fa-comment-alt me-2"></i>
              Message
            </div>
            <button v-if="$store.getters.role === 'sponsor' && !editingMessage" class="edit-button" @click="editingMessage = true; editedMessage = message">
              <i class="fa-solid fa-pen"></i>
            </button>
          </div>

          <div v-if="!editingMessage" class="message-content">
            {{ message }}
          </div>
          <form v-else @submit.prevent="saveMessage" class="message-edit-form">
            <textarea v-model="editedMessage" class="edit-input stretch-textarea" rows="" @input="adjustHeight"
              ref="autoResize"></textarea>
            <div class="button-group">
              <button type="submit" class="save-button">Save Message</button>
              <button type="button" class="cancel-button"
                @click="editingMessage = false; editedMessage = ''">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <message v-if="request_id" :request_id="request_id"></message>
</template>

<script>
import axios from "axios";
import message from '@/components/additional/message.vue';

const RequestStatus = {
  PENDING: 'PENDING',
  ACCEPTED: 'ACCEPTED',
  DECLINED: 'DECLINED',
  COMPLETED: 'COMPLETED',
  REJECTED: 'REJECTED'
};

const TRANSITIONS = {
  [RequestStatus.PENDING]: [RequestStatus.ACCEPTED, RequestStatus.DECLINED, RequestStatus.REJECTED],
  [RequestStatus.ACCEPTED]: [RequestStatus.COMPLETED],
  [RequestStatus.DECLINED]: [RequestStatus.REJECTED, RequestStatus.ACCEPTED],
  [RequestStatus.COMPLETED]: [],
  [RequestStatus.REJECTED]: []
};

export default {
  name: 'RequestCard',
  components: {
    message
  },
  data() {
    return {
      request_id: '',
      campaign_id: '',
      influencer_id: '',
      influencer_s_user_id:'',
      campaign_name : '',
      influencer_name: '',
      time: '',

      status: '',
      editingStatus: false,
      editedStatus: '',


      requirements: [],
      editingRequirements: false,
      editedRequirements: [],

      payment: '0',
      editingPayment: false,
      editedPayment: '',

      message: '',
      editingMessage: false,
      editedMessage: '',

      showDeletePopover: false,
    }
  },
  computed: {
    availableTransitions() {
      return TRANSITIONS[this.status] || [];
    }
  },
  methods: {
    saveStatus() {
      if (this.editedStatus && TRANSITIONS[this.status].includes(this.editedStatus)) {
        this.updateData('edit-status', {status: this.editedStatus})
        // this.status = this.editedStatus;
      }
      this.editingStatus = false;
    },
    saveRequirements() {
      this.requirements = JSON.parse(JSON.stringify(this.editedRequirements))
      this.updateData('edit-requirements',{requirements : this.editedRequirements.map(item => item.text).filter(text => text).join("$@$")})
      this.editingRequirements = false
    },
    addRequirement() {
      this.editedRequirements.push({ text: '' });
    },
    savePayment() {
      this.updateData('edit-payment', {payment :this.editedPayment})
      // this.payment = this.editedPayment
      this.editingPayment = false
    },
    saveMessage() {
      this.updateData('edit-message', {message :this.editedMessage})
      // this.message = this.editedMessage
      this.editingMessage = false
    },
    async confirmDelete() {
      try {
        await axios.delete(
          `${this.$store.state.basePath}/request/delete/${this.$route.query.show}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        )
        this.$router.push({ name: 'each-campaign-details-for-sponsors', query: { 'show': this.campaign_id } });
        // console.log(response);
        this.$toast.success(`Request Revoked Successfully !`,
          {
            position: 'bottom-right',
            duration: 5000,
            dismissible: true
          }
        )

      } catch (error) {
        this.$errorComesNow(error);
      }
      this.showDeletePopover = false;
    },

    adjustHeight() {
      // Adjust the height of the textarea
      const textarea = this.$refs.autoResize;
      if (textarea) {
        textarea.style.height = 'auto'; // Reset height to shrink if needed
        textarea.style.height = `${textarea.scrollHeight}px`; // Set height based on scrollHeight
      }
    },

    async updateData(endPoint, data) {
      try {
        await axios.patch(
          `${this.$store.state.basePath}/request/${endPoint}/${this.$route.query.show}`,
          data,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        )
        this.$toast.success(`${this.$capitalize(endPoint.split('-')[1])} Updated Successfully !`,
          {
            position: 'bottom-right',
            duration: 5000,
            dismissible: true
          }
        )
        this.fetchData();

      } catch (error) {
        this.$errorComesNow(error);
      }
    },

    async fetchData() {
      try {
        const response = await axios.get(`${this.$store.state.basePath}/request/${this.$route.query.show}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        )        

        const data = response.data.db_data;
        this.request_id = data.id;
        this.campaign_id = data.campaign_id;
        this.influencer_s_user_id = data.influencer_s_user_id;
        this.influencer_id = data.influencer_id;
        this.status = data.status;
        this.requirements = data.requirements.split('$@$').filter(item => item).map(item => ({ text: item }));
        this.message = data.message;
        this.payment = data.payment;
        this.time = data.time;
        this.campaign_name = data.campaign_name;
        this.influencer_name = data.influencer_name;
        

      } catch (error) {
        this.$errorComesNow(error);
      }

    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>


<style scoped>
select {
    width: 100%;
    padding: 8px 4px 4px 14px;
    border: 1px solid #4199f8;
    border-radius: 50px;
    box-shadow: 0px 0px 4px 0px #4199f8;
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease-out;
}
/* Layout & Container Styles */
.card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px -1px rgb(0 0 0 / 0.1);
  width: 100%;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.side-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header Styles */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-right: auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #040506;
}

.stretch-textarea {
  width: 100%;
  height: auto;
  min-height: 40px;
  resize: none;
  box-sizing: border-box;
  overflow: hidden;
  padding: 5px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Status Section Styles */
.status-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  margin-right: 1rem;
}

.status-edit-form {
  /* min-width: 300px; */
  display: flex;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: z4px 4px 6px -1px rgb(0 0 0 / 0.1);
}

.radio-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  /* margin-bottom: 1rem; */
}

.radio-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.radio-item input[type="radio"] {
  display: none;
}

.radio-item input[type="radio"]+label {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.radio-item input[type="radio"]:checked+label {
  opacity: 1;
  border: 1px solid black;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Status Colors */
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

/* Requirements Section Styles */
.requirements-section {
  background: #f1f5f9;
  padding: 1.5rem;
  border-radius: 12px;
}

.requirements-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.requirement-item,
.requirement-edit-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  align-items: flex-start;
}

.requirement-number {
  flex-shrink: 0;
  min-width: 28px;
  width: 28px;
  height: 28px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.requirement-text {
  color: #475569;
  font-size: 0.95rem;
  width: 100%;
}

.requirements-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Message Section Styles */
.message-section {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #467dc4;
}

.message-content {
  color: #475569;
  line-height: 1.6;
}

.message-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Payment Section Styles */
.payment-card {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #467dc4;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-grow: 1;
  margin-right: 1rem;
}

.payment-label-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.payment-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #334155;
}

.payment-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Delete Button Section Styles */
.delete-button-section {
  display: flex;
  align-items: center;
  position: relative;
}

.delete-button {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.5rem;
}

/* Popover Styles */
.status-edit-form-popover {
  position: absolute;
  top: 100%;
  left: -10%;
  margin-top: 0.5rem;
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 0.05rem solid rgb(165, 163, 163);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  z-index: 10;
  width: 160px;
}

.popover {
  position: absolute;
  top: 100%;
  left: -790%;
  margin-top: 0.5rem;
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 0.05rem solid rgb(165, 163, 163);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  z-index: 10;
  width: 200px;
}

.popover-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

/* Button Styles */
.button-group {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.edit-button {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
}

.edit-button:hover {
  color: #1e293b;
}

.save-button {
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
}

.save-button:hover {
  background-color: #2563eb;
}

.cancel-button {
  background-color: #e2e8f0;
  color: #475569;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

.add-button {
  width: 100%;
  background-color: #f1f5f9;
  border: 1px dashed #94a3b8;
  color: #64748b;
  padding: 0.75rem;
  border-radius: 0.375rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.add-button:hover {
  background-color: #e2e8f0;
  color: #475569;
}

.confirm-button {
  background-color: #ef4444;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

/* Media Queries */
@media (max-width: 768px) {
  h1 {
    font-size: 1rem;
  }

  .main-content {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .status-edit-form {
    min-width: 250px;
  }

  .radio-group {
    flex-direction: column;
  }

  .status-badge {
    gap: 0.5rem;
    padding: 0.4rem .7rem;
    font-size: 0.6rem;
  }
}
</style>