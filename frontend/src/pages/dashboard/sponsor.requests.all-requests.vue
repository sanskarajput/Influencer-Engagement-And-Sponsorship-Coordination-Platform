  <template>
    <div class="d-sm-flex align-items-center justify-content-between mb-1 mx-4">
      <h1 class="mb-0 text-gray-800 fw-bold fs-2">
        Your All Requests
      </h1>
    </div>
    <Datatable v-if="isApproved" ref="dataT" :url="url" :columns="columns" :handleRemoveSelected="handleRemoveSelected">
    </Datatable>
    <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
      <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
      <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
      <span class="fs-5 fw-bold">Then You Can See All Your Requests.</span><br>
      <span class="fs-5 fw-bold">If You Have Any.</span><br>
      <span class="fs-1 fw-bold"> &#128591;</span>
    </div>
  </template>

<script>
import axios from 'axios';
import Datatable from '@/components/additional/datatable-server.vue';

export default {
  name: 'Sponsor-Requests-All-Requests',
  components: {
    Datatable
  },
  data() {
    return {
      isApproved: false,
      ApprovalDataFetched: false
    }
  },
  methods: {
    handleRemoveSelected(id) {
      const response = axios.delete(`${this.$store.state.basePath}/request/delete/${id}`, {
        headers: {
          'Content-Type': 'application/json',
          'Auth-Token': this.$store.getters.auth_token
        }
      }).then(res => {
        this.$toast.info(`${res.data.db_data.message}`,
          {
            position: 'bottom-right',
            duration: 5000,
            dismissible: true
          }
        );
      }).catch(error => {
        console.error("Data delete failed:", error);
      })

      return response;
    },
    async isSponsorApproved() {
      try {
        const response = await axios.get(
          `${this.$store.state.basePath}/sponsor/is-approved/${this.$store.getters.role_id}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );

        this.isApproved = response.data.db_data.isApproved;
        this.ApprovalDataFetched = true;
      } catch (error) {
        this.$errorComesNow(error);
      }
    }
  },
  beforeMount() {
    this.isSponsorApproved();
  },
  computed: {
    url() {
      return `${this.$store.state.basePath}/all-requests-of-a-sponsor`;
    },
    columns() {
      return [
        [{
          field: 'state',
          checkbox: true,
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          switchable: false,
        }, {
          title: 'S. No.',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          switchable: false,
          class: "serial-number",
          formatter: (value, row, index) => {
            return this.$refs.dataT.getCurrentOffset() + index + 1;
          },
          footerFormatter: () => {
            return 'Total';
          },
        }, {
          field: 'id',
          title: 'ID',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: false,
          switchable: false,
        }, {
          field: 'campaign_name',
          title: 'Campaign\'s Title',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          switchable: false,
          formatter: (value, row) => {
            return `<a class="goto" href="javascript:void(0)" title="See Campaign">${row.campaign_name}</a>`;
          },
          events: {
            'click .goto': (e, value, row) => {
              this.$router.push({ name: 'each-campaign-details', query: { show: row.campaign_id } });
            }
          }
        }, {
          field: 'influencer_username',
          title: 'Influencer',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: true,
          switchable: false,
          formatter: (value, row) => {
            return `<a class="goto" href="javascript:void(0)" title="Profile">${row.influencer_username}</a>`;
          },
          events: {
            'click .goto': (e, value, row) => {
              this.$router.push({ name: 'other-user-profile-view', params: { role: 'influencer' }, query: { user_id: row.influencer_s_user_id } });
            }
          }
        }, {
          field: 'message',
          title: 'Message',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: true,
          switchable: true,
        }, {
          field: 'requirements',
          title: 'Requirements',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: false,
          switchable: true,
        }, {
          field: 'payment',
          title: 'Payment',
          rowspan: 1,
          align: 'end',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: true,
          switchable: true,
          formatter: (value) => {
            return `<b>₹</b> ${new Intl.NumberFormat().format(value)}<b>.</b>00`;
          },
          footerFormatter: (data) => {
            let sum = 0;
            data.forEach(function (row) {
              sum += row.payment;
            });
            return `<b>₹</b> ${new Intl.NumberFormat().format(sum)}<b>.</b>00`;
          },
        }, {
          field: 'time',
          title: 'Requested . . .',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          visible: false,
          sortable: true,
          formatter: (value, row) => {
            return this.$forCreatedAtLong(row.time);
          },
        }, {
          field: 'status',
          title: 'Status',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          sortable: true,
          visible: true,
          switchable: true,
          formatter: (value) => {
            return this.$capitalize(value);
          }
        }, {
          title: 'Edit',
          rowspan: 1,
          align: 'center',
          valign: 'middle',
          colspan: 1,
          class: "edit",
          clickToSelect: false,
          visible: true,
          switchable: true,
          formatter: () => {
            return `<a class="edit" href="javascript:void(0)" title="Edit Request Details"><i class="fas fa-edit"></i></a>`;
          },
          events: {
            'click .edit': (e, value, row) => {
              this.$router.push({ name: 'each-request-details', query: { show: row.id } });
            }
          }
        }]
      ]
    }
  }
}

</script>

<style scoped></style>