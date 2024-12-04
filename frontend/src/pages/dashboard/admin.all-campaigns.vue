<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-1 px-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      All Campaigns
    </h1>

    <div @click="downloadCSV" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i
        class="fas fa-download fa-sm text-white-50"></i> Downloads Data</div>
  </div>
  <Datatable :key="key" ref="dataT" :url="url" :columns="columns">
  </Datatable>
</template>

<script>
import Datatable from '@/components/additional/datatable-server.vue';
import axios from 'axios';
export default {
  name: 'All-Campaigns-For-Admin',
  components: {
    Datatable
  },
  data() {
    return {
      key: 0,
    }
  },
  methods: {
    async toggleFlagged(campaign_id) {
      try {
        await axios.post(
          `${this.$store.state.basePath}/toggle-campaign-flagged/${campaign_id}`,
          {},
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );
        this.key++;

      } catch (error) {
        this.$errorComesNow(error);
      }
    },
    async downloadCSV(){
      try {
        const response = await axios.get(
          `${this.$store.state.basePath}/csv-export`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Auth-Token': this.$store.getters.auth_token
            }
          }
        );

        const data = response.data;

        const blob = new Blob([data], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'Campaign_data.csv';
        link.click();
      } catch (error) {
        this.$errorComesNow(error);
      }
    }
  },
  computed: {
    url() {
      return `${this.$store.state.basePath}/all-campaigns-for-a-Admin`;
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
              this.$router.push({ name: 'each-campaign-details', query: { show: row.id } });
            }
          }
        }, {
          field: 'sponsor_username',
          title: 'Sponsor',
          rowspan: 2,
          colspan: 1,
          align: 'center',
          valign: 'middle',
          sortable: true,
          visible: true,
          switchable: false,
          formatter: (value, row) => {
            return `<a class="goto" href="javascript:void(0)" title="Profile">${row.sponsor_username}</a>`;
          },
          events: {
            'click .goto': (e, value, row) => {
              this.$router.push({ name: 'other-user-profile-view', params: { role: 'sponsor' }, query: { user_id: row.sponsor_s_user_id } });
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
          clickToSelect: false,
          visible: true,
          sortable: true,
          switchable: true,
          formatter: (value) => {
            if (value) {
              return `<a class="flag" href="javascript:void(0)" title="Flag Campaign"><i class="fas fa-flag text-danger fa-lg"></i></a>`;
            }
            return `<a class="flag" href="javascript:void(0)" title="Flag Campaign"><i class="fas fa-flag text-success fa-lg"></i></a>`;
          },
          events: {
            'click .flag': (e, value, row) => {
              this.toggleFlagged(row.id);
            }
          }
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