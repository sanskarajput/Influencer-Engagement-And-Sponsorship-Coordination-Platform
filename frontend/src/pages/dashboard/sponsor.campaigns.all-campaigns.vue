<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-1 mx-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      Your All Campaigns
    </h1>
  </div>
  <Datatable v-if="isApproved" ref="dataT" :url="url" :columns="columns" :handleRemoveSelected="handleRemoveSelected">
  </Datatable>
  <div v-if="ApprovalDataFetched && !isApproved" class="text-center mt-5 pt-5">
    <span class="fs-1 fw-bold">You Are Not <span class="text-primary">Approved</span> Yet.</span><br>
    <span class="fs-4 fw-bold">Let Admin Approve Your Credentials.</span><br>
    <span class="fs-5 fw-bold">Then You Can See All Your Campaign.</span><br>
    <span class="fs-5 fw-bold">If You Have Any.</span><br>
    <span class="fs-1 fw-bold"> &#128591;</span>
  </div>
</template>

<script>
import axios from 'axios';
import Datatable from '@/components/additional/datatable-server.vue';

export default {
  name: 'Sponsor-Campaigns-All-Campaigns',
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
      const response = axios.delete(`${this.$store.state.basePath}/campaign/delete/${id}`, {
        headers: {
          'Content-Type': 'application/json',
          'Auth-Token': this.$store.getters.auth_token
        }
      }).then(res => {
        console.log(res);
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
      return `${this.$store.state.basePath}/all-campaigns-of-a-sponsor`;
    },
    columns() {
      return [
        [{
          field: 'state',
          checkbox: true,
          // title: 'Name',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          visible: true,
          switchable: false,
          // sortable: true,
          // sorter: () => { },
          // formatter: (value, row, index) => { },
          // footerFormatter: (data) => { },
        }, {
          title: 'S. No.',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          visible: true,
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
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: false,
          switchable: false,
        }, {
          field: 'name',
          title: 'Campaign\'s Tilte',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: true,
          switchable: false,
          formatter: (value, row) => {
            return `<a class="goto" href="javascript:void(0)" title="See Campaign">${row.name}</a>`;
          },
          events: {
            'click .goto': (e, value, row) => {
              // console.log("e",e);
              // console.log("value",value); // will be value of that cell
              // console.log("row",row);  // will be the whole row's data
              // console.log("index",index); // will be the index of the row starting from 0
              this.$router.push({ name: 'each-campaign-details', query: { show: row.id } });
            }
          }
        }, {
          field: 'description',
          title: 'Description',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: false,
          switchable: true,
        }, {
          field: 'category',
          title: 'Category',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: true,
          switchable: true,
        }, {
          // field: 'name',
          title: 'Time',
          rowspan: 1,
          colspan: 2,
          align: 'center',
          valign: 'middle',
          // sortable: true,
          // visible: false,
          // switchable: false,
          // sorter: () => { },
          // formatter: (value, row, index) => { },
          // footerFormatter: (data) => { },
        }, {
          field: 'budget',
          title: 'Budget',
          rowspan: 2,
          colspan: 1,
          align: 'end',
          valign: 'middle',
          sortable: true,
          visible: true,
          switchable: true,
          // sorter: () => { },
          formatter: (value) => {
            return `<b>₹</b> ${new Intl.NumberFormat().format(value)}<b>.</b>00`;
          },
          footerFormatter: (data) => {
            let sum = 0;
            data.forEach(function (row) {
              sum += row.budget;
            });
            return `<b>₹</b> ${new Intl.NumberFormat().format(sum)}<b>.</b>00`;
          },
        }, {
          field: 'visibility',
          title: 'Visibility',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: true,
          switchable: true,
          // sorter: () => { },
          // formatter: (value, row, index) => { },
          formatter: (value) => {
            return this.$capitalize(value);
          }
        }, {
          field: 'goals',
          title: 'Goals',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: false,
          switchable: true,
        }, {
          field: 'time',
          title: 'Created At . . .',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          formatter: (value, row) => {
            return this.$forCreatedAtLong(row.time);
          },
        }, {
          field: 'flagged',
          title: 'Flag',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          class: "flag",
          sortable: true,
          visible: true,
          switchable: true,
          formatter: (value) => {
            if (value) {
              return `<span class="flag" title="Flag Campaign"><i class="fas fa-flag text-danger"></i></span>`;
            }
            return `<span class="flag" title="Flag Campaign"><i class="fas fa-flag text-success"></i></span>`;
          }
        }, {
          // field: 'status',
          title: 'Edit',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          class: "edit",
          clickToSelect: false,
          visible: true,
          switchable: true,
          formatter: () => {
            return `<a class="edit" href="javascript:void(0)" title="Edit Campaign"><i class="fas fa-edit"></i></a>`;
          },
          events: {
            'click .edit': (e, value, row) => {
              this.$router.push({ name: 'each-campaign-details', query: { edit: row.id } });
            }
          }
          // footerFormatter: (data) => { },
        }],
        [{
          field: 'start_date',
          title: 'Start Time',
          rowspan: 1,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: false,
          switchable: true,
          // sorter: () => { },
          formatter: (value) => {
            return value.substr(0, 22);
          },
        }, {
          field: 'end_date',
          title: 'End Time',
          rowspan: 1,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: false,
          switchable: true,
          // sorter: () => { },
          formatter: (value) => {
            return value.substr(0, 22);
          },
        }]
      ]
    }
  }
}

</script>

<style scoped></style>