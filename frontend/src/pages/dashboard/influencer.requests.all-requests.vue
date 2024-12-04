<template>
  <div class="d-sm-flex align-items-center justify-content-between mb-1 mx-4">
    <h1 class="mb-0 text-gray-800 fw-bold fs-2">
      Your All Requests
    </h1>
  </div>
  <Datatable ref="dataT" :url="url" :columns="columns"></Datatable>
</template>

<script>
import Datatable from '@/components/additional/datatable-server.vue';

export default {
name: 'Influencer-Requests-All-Requests',
components: {
  Datatable
},
data() {
  return {
  }
},
methods: {
},
computed: {
  url() {
    return `${this.$store.state.basePath}/all-requests-of-a-influencer`;
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
        visible:false
      },{
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
      },{
        field: 'id',
        title: 'ID',
        rowspan: 1,
        align: 'center',
        valign: 'middle',
        colspan: 1,
        sortable: true,
        visible: false,
        switchable: false,
      },{
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
      },{  
        field: 'sponsor_username',
        title: 'Sponsor',
        rowspan: 1,
        align: 'center',
        valign: 'middle',
        colspan: 1,
        sortable: true,
        visible: true,
        switchable: false,
        formatter: (value, row) => {
          return `<a class="goto" href="javascript:void(0)" title="Profile">${row.sponsor_username}</a>`;
        },
        events: {
          'click .goto': (e, value, row) => {
            this.$router.push({ name: 'other-user-profile-view', params:{ role:'sponsor' }, query: { user_id: row.sponsor_s_user_id } });
          }
        }
      },{
        field: 'message',
        title: 'Message',
        rowspan: 1,
        align: 'center',
        valign: 'middle',
        colspan: 1,
        sortable: true,
        visible: true,
        switchable: true,
      },{
        field: 'requirements',
        title: 'Requirements',
        rowspan: 1,
        align: 'center',
        valign: 'middle',
        colspan: 1,
        sortable: true,
        visible: false,
        switchable: true,
      },{
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
          return  `<b>₹</b> ${new Intl.NumberFormat().format(value)}<b>.</b>00`;
        },
        footerFormatter: (data) => {
          let sum = 0;
          data.forEach(function (row) {
            sum += row.payment;
          });
          return `<b>₹</b> ${new Intl.NumberFormat().format(sum)}<b>.</b>00`;
        },
      },{
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
      },{
        field: 'status',
        title: 'Status',
        rowspan: 1,
        align: 'center',
        valign: 'middle',
        colspan: 1,
        sortable: true,
        visible: true,
        switchable: true,
        formatter: (value, row) => {
          return this.$capitalize(row.status);
        }
      },{
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