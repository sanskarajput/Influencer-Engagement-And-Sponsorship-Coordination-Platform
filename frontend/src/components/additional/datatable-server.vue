<template>
    <div class="bootstrap-table-wrapper">
        <div id="toolbar" v-if="$store.getters.role === 'sponsor'">
            <button id="remove" class="btn btn-danger" :disabled="!hasSelections" @click="removeSelected">
                <i class="fa fa-trash"></i> Delete
            </button>
        </div>
        <!-- Bootstrap table element with all necessary data attributes -->
        <table 
        id="my-table" 
        ref="bootstrapTable" 
        data-toolbar="#toolbar" 
        data-search="true" 
        data-show-refresh="true"
        data-show-toggle="true" 
        data-show-fullscreen="true" 
        data-show-columns="true"
        data-show-columns-toggle-all="true" 
        data-detail-view="true" 
        data-show-export="true"
        data-click-to-select="false" 
        data-minimum-count-columns="2" 
        data-show-pagination-switch="true"
        data-pagination="true" 
        data-id-field="id" 
        data-page-list="[10, 25, 50, 100, all]" 
        data-show-footer="true"
        data-side-pagination="server">
        </table>
    </div>
</template>

<script>
// Import jQuery and make it globally available
import axios from 'axios';
import jQuery from 'jquery'
const $ = jQuery
window.jQuery = jQuery

export default {
    name: 'BootstrapTable',

    props: {
        url: {
            type: String,
            required: true
        },
        columns: {
            type: Array,
            required: true
        },
        handleRemoveSelected: {
            type: Function,
            required: false,
            default: () => {
                console.log("handleRemoveSelected Not required.");
            }
        }
    },

    data() {
        return {
            selections: [], // Stores selected row IDs
            hasSelections: false, 
            table: null,
            dataFromBackend: {},
            dataFeched: false
        }
    },

    methods: {
        async loadExternalResources() {
            const resources = [
                { type: 'css', url: 'https://cdn.jsdelivr.net/npm/bootstrap-table@1.23.5/dist/bootstrap-table.min.css' },
                { type: 'css', url: 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.1/font/bootstrap-icons.min.css' },
                // { type: 'script', url: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js' },
                { type: 'script', url: 'https://cdn.jsdelivr.net/npm/bootstrap-table@1.23.5/dist/bootstrap-table.min.js' },
                // { type: 'script', url: 'https://cdn.jsdelivr.net/npm/tableexport.jquery.plugin@1.29.0/tableExport.min.js' },
                // { type: 'script', url: 'https://cdn.jsdelivr.net/npm/bootstrap-table@1.23.5/dist/extensions/export/bootstrap-table-export.min.js' },
            ]

            await Promise.all(resources.map(resource => {
                return new Promise((resolve, reject) => {
                    const element = resource.type === 'script'
                        ? document.createElement('script')
                        : document.createElement('link')

                    element.onload = resolve
                    element.onerror = reject

                    if (resource.type === 'script') {
                        element.src = resource.url
                    } else {
                        element.rel = 'stylesheet'
                        element.href = resource.url
                    }

                    document.head.appendChild(element)
                })
            }))
        },

        initTable() {
            const $table = $(this.$refs.bootstrapTable)

            if (this.table) {
                $table.bootstrapTable('destroy')
            }

            this.table = $table.bootstrapTable({
                processing: true,        // Enables the "processing" indicator
                serverSide: true,        // Tells DataTables that the data is served by the server
                // detailView: true, 


                ajax: (params) => {
                    // Construct the request payload
                    const requestData = {
                        limit: params.data.limit,
                        offset: params.data.offset,
                        sort: params.data.sort,
                        order: params.data.order,
                        search: params.data.search,
                        searchOn: $table.bootstrapTable('getVisibleColumns')
                            .filter(col => !['S. No.', 'Edit'].includes(col.title))
                            .map(col => col.field)
                            .join(',')
                    };

                    // Make the Axios request
                    axios.get(this.url, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        },
                        params: requestData // Send the request payload as query parameters
                    })
                        .then(response => {
                            this.dataFromBackend = response.data.db_data;
                            this.dataFeched = true;
                            
                            params.success(response.data.db_data); // Send fetched data to bootstrapTable
                        })
                        .catch(error => {
                            params.error(error);
                            console.error("Data fetch failed:", error);
                            this.$errorComesNow(error);
                        });
                },

                formatNoMatches: () => {
                    if (this.dataFeched) {
                        if (this.dataFromBackend.rows.length) {
                            return ''; // Data exists, no message needed
                        }

                        if (this.$route.fullPath === '/dashboard/my-all-campaigns') {
                            // Return raw HTML for a link
                            return `
                            <p class="fs-1 fw-bold mt-3 mb-n3">You do not have any Campaigns .....</p><br>
                            <a href="/dashboard/add-campaign" style="text-decoration:none" >
                                <span class="fs-2 fw-bold">Add Campaign</span>
                                <i class="fs-2 fw-bold fas fa-fw fa-bullhorn"></i>
                            </a>`;
                        }

                        if (this.$route.fullPath === '/dashboard/my-all-requests') {
                            return  '<p class="fs-1 fw-bold">No data available, Please make some request on any Campaign.. &#128591;</p>';
                        }

                        if (this.$route.fullPath === '/dashboard/my-requests') {
                            return  '<p class="fs-1 fw-bold">No data available, Let Sponsors make some request with you.. &#128591;</p>';
                        }

                        return 'No data available'; // Default message for no matches
                    } else {
                        return 'Not able to fetch data from server ...'; // Message when data is not fetched yet
                    }
                },

                detailFormatter: (index, row) => {
                    const html = Object.entries(row)
                        .filter(([key]) => key !== 'state')
                        .map(([key, value]) => `
                            <div class="detail-row">
                            <span class="detail-label">${key}:</span>
                            <span class="detail-value">${value}</span>
                            </div>
                        `).join('')
                    return `<div class="detail-view">${html}</div>`
                },

                columns: this.columns,

                // Process server response to maintain selections
                responseHandler: (res) => {
                    // console.log(res);
                    return ({
                        ...res,
                        rows: res.rows.map(row => ({
                            ...row,
                            state: this.selections.includes(row.id)
                        }))
                    })
                }
            })

            // Bind selection change events
            $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table',
                () => {
                    this.selections = $table.bootstrapTable('getSelections').map(row => row.id)
                    this.hasSelections = this.selections.length > 0
                }
            )
        },

        async removeSelected() {
            $(this.$refs.bootstrapTable).bootstrapTable('remove', {
                field: 'id',
                values: this.selections
            })
            const promises = this.selections.map(this.handleRemoveSelected);
            await Promise.allSettled(promises);

            this.$toast.success('All Deleted Successfully !!!!!!!',
                {
                    position: 'bottom-right',
                    duration: 5000,
                    dismissible: true
                }
            )

            this.hasSelections = false;
            $(this.$refs.bootstrapTable).bootstrapTable('refresh')
        },

        getCurrentOffset() {
            const pageSize = $(this.$refs.bootstrapTable).bootstrapTable('getOptions').pageSize;
            const currentPage = $(this.$refs.bootstrapTable).bootstrapTable('getOptions').pageNumber;
            return (currentPage - 1) * pageSize; // Calculating the current offset
        },
    },

    mounted() {
        this.loadExternalResources().then(() => {
            try {
                this.initTable();
            } catch (error) {
                console.error('Initialization failed:', error)
            }
        }).catch(error => {
            console.error('Resource loading failed:', error)
        })
    },

    beforeUnmount() {
        if (this.table) {
            $(this.$refs.bootstrapTable).bootstrapTable('destroy')
        }
        // location.reload();

    }
}
</script>

<style scoped></style>