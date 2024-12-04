<template>
    <div class="page-container">
        <!-- <header class="page-header" :style="{ backgroundImage: 'url(' + 'https://picsum.photos/2345' + ')', backgroundColor: lightcoral }" > -->
        <header class="page-header animation-small-to-original">
            <div class="user-info">
                <div class="avatar-wrapper">
                    <img :src="avatar || require('@/assets/profile-user.png')" :alt="name" class="avatar" />
                    <div v-if="canEdit" class="edit-avatar-overlay">
                        <button class="edit-avatar-btn" @click="showAvatarModal = true">
                            <i class="fas fa-camera"></i>
                        </button>
                    </div>
                </div>
                <div class="user-details">
                    <div class="user-details">
                        <div class="name-section">
                            <h1 class="user-name">{{ name ? name.split(" ").map(value => $capitalize(value)).join(" ") : name }}</h1>
                            <button v-if="canEdit" class="edit-btn" @click="openNameModal">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                        </div>
                        <div class="username-section">
                            <p class="username">@{{ username }}</p>
                            <button v-if="canEdit" class="edit-btn" @click="openUsernameModal">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <span v-if="isSpon && approved === 'TRUE'" class="approved">Approved</span>
            <span v-if="isSpon && approved === 'PENDING'" class="not-approved-pending">Not Approved, Status Pending...</span>
            <span v-if="isSpon && approved === 'FALSE'" class="rejected">Rejected</span>
            <!-- <div class="action-buttons" v-if="canDelete">
                <button class="delete-btn" @click="showDeleteModal = true">
                    <i class="fas fa-trash"></i>
                    Delete Profile
                </button>
            </div> -->
        </header>
        <div v-if="isAdmin" class="content-grid animation-small-to-original">
            <section class="main-info-card">
                <div class="card-header">
                    <h2>User Management</h2>
                </div>
                <p class="info-item">
                    <i class="">The Admin Dashboard allows the admin to oversee all users registered on the platform, categorized by roles such as Sponsors and Influencers. Each user is displayed with relevant details, including their username, registration date, and account status (active or flagged). Pending sponsor registration requests are highlighted, enabling the admin to review, approve, or reject them efficiently. Additionally, the admin has the authority to flag inappropriate users, ensuring compliance with the platform's policies and maintaining a safe environment.</i>
                </p>
                <div class="card-header">
                    <h2>Campaign Oversight</h2>
                </div>
                <p class="info-item">
                    <i class="">The dashboard provides a centralized view of all campaigns created by sponsors, categorized as public or private. Detailed information about each campaign, such as the campaign name, the sponsor who created it, and its current status (active, completed, or flagged), is available. Campaigns flagged for violating platform guidelines are prominently listed, allowing the admin to quickly identify and address potential issues. This capability ensures that all campaigns align with the platform’s standards.</i>
                </p>
            </section>
            <section class="main-info-card">
                <div class="card-header">
                    <h2>Insights and Monitoring</h2>
                </div>
                <p class="info-item">
                    <i class="">The admin can access a rich set of statistics and insights about the application’s usage. These include the total number of active users segmented by roles, flagged users and campaigns, and the performance of active campaigns. The dashboard also tracks the status of ad requests, providing a summary of pending, approved, and rejected requests. A recent activity log offers a chronological view of significant user actions and campaign updates, giving the admin real-time monitoring capabilities to oversee the platform effectively.</i>
                </p>
            </section>
        </div>

        <div v-else class="content-grid animation-small-to-original">
            <!-- Main Info Section -->
            <section class="main-info-card">
                <div class="card-header">
                    <h2>Profile Information</h2>
                    <button v-if="canEdit" class="edit-btn" @click="startEditing('profile')">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                </div>

                <div class="info-grid" v-if="isInflu">
                    <div class="info-item">
                        <label>Category</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !category }">{{ category ? $capitalize(category) : 'set not yet...' }}</p>
                        <select v-else v-model="editedData.category" class="edit-input" style="box-shadow:none;">
                            <option value="Lifestyle">Lifestyle</option>
                            <option value="Technology">Technology</option>
                            <option value="Fashion">Fashion</option>
                            <option value="Food">Food</option>
                            <option value="Travel">Travel</option>
                            <option value="Fitness">Fitness</option>
                            <option value="Beauty">Beauty</option>
                            <option value="Gaming">Gaming</option>
                            <option value="Music">Music</option>
                            <option value="Parenting">Parenting</option>
                        </select>
                    </div>

                    <div class="info-item">
                        <label>Niche</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !niche }">{{ niche ? $capitalize(niche) : 'set not yet...' }}</p>
                        <input v-else v-model="editedData.niche" type="text" class="edit-input" />
                    </div>
                    
                    <div class="info-item">
                        <label>Reach</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !reach }">{{ reach ? formatReach(reach) : 'set not yet...' }}</p>
                        <input v-else v-model.number="editedData.reach" type="number" class="edit-input" />
                    </div>
                </div>

                <div class="info-grid" v-if="isSpon">
                    <div class="info-item">
                        <label>Type</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !type }">{{ type ? $capitalize(type) : "set not yet..." }}</p>
                        <select v-else v-model="editedData.type" class="edit-input" style="box-shadow:none;">
                            <option value="Individual">Individual</option>
                            <option value="Company">Company</option>
                        </select>
                    </div>
                    <div class="info-item">
                        <label>Industry</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !industry }">{{ industry ? $capitalize(industry) : "set not yet..." }}</p>
                        <input v-else v-model="editedData.industry" type="text" class="edit-input" />
                    </div>
                    <div class="info-item">
                        <label>Budget</label>
                        <p v-if="!editing.profile" :class="{ 'text-secondary': !budget }">{{ budget ? formatNumber(budget) : 'set not yet...' }}</p>
                        <input v-else v-model.number="editedData.budget" type="number" class="edit-input" />
                    </div>
                </div>

                <div class="description-section">
                    <label>Description</label>
                    <p v-if="!editing.profile" :class="{ 'text-secondary': !description }">{{ description || 'set not yet...' }}</p>
                    <textarea v-else v-model="editedData.description" style="box-shadow:none"
                        class="edit-input description-input stretch-textarea" rows="" @input="adjustHeight"
                        ref="autoResize"></textarea>
                </div>

                <div v-if="editing.profile" class="edit-actions">
                    <button class="save-btn" @click="saveChanges('profile')">Save Changes</button>
                    <button class="cancel-btn" @click="cancelEditing('profile')">Cancel</button>
                </div>
            </section>

            <!-- Stats Card -->
            <section v-if="isInflu" class="stats-card">
                <div class="stat-item">
                    <i class="fa-solid fa-hill-avalanche"></i>
                    <div class="stat-content">
                        <h3>Niche</h3>
                        <p :class="{ 'text-secondary': !niche }">{{ niche ? $capitalize(niche) : 'set not yet...' }}</p>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fa-solid fa-icons"></i>
                    <div class="stat-content">
                        <h3>Category</h3>
                        <p :class="{ 'text-secondary': !category }">{{ category ? $capitalize(category) : 'set not yet...' }}</p>
                    </div>
                </div>
                <div class="stat-item">
                    <!-- <i class="fas fa-users"></i> -->
                    <i class="fa-solid fa-chart-line"></i>
                    <div class="stat-content">
                        <h3>Total Reach</h3>
                        <p :class="{ 'text-secondary': !reach }">{{ reach ? formatReach(reach) : 'set not yet...' }}</p>
                    </div>
                </div>
            </section>

            <section v-if="isSpon" class="stats-card">
                <div class="stat-item">
                    <i v-if="type && type === 'Company'" class="fa-solid fa-building"></i>
                    <i v-if="type && type === 'Individual'" class="fa-solid fa-street-view"></i>
                    <i v-if="!type" class="fa-solid fa-circle-exclamation"></i>
                    <div class="stat-content">
                        <h3>Type</h3>
                        <p :class="{ 'text-secondary': !type }">{{ type ? $capitalize(type) : "set not yet..." }}</p>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fa-solid fa-industry"></i>
                    <div class="stat-content">
                        <h3>Industry</h3>
                        <p :class="{ 'text-secondary': !industry }">{{ industry ? $capitalize(industry) : "set not yet..." }}</p>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fa-solid fa-piggy-bank"></i>
                    <div class="stat-content">
                        <h3>Budget</h3>
                        <p :class="{ 'text-secondary': !budget }">{{ budget ? formatNumber(budget) : 'set not yet...' }}</p>
                    </div>
                </div>
            </section>


            <!-- Social Links -->
            <section v-if="isInflu" class="links-card">
                <div class="card-header">
                    <h2>Social Links</h2>
                    <button v-if="canEdit" class="edit-btn" @click="startEditing('links')">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                </div>

                <div class="links-list">
                    <div v-if="!editing.links">
                        <div class="link-item" v-for="(link, index) in parsedLinks" :key="index">
                            <i :class="getLinkIcon(link.platform)"></i>
                            <a :href="link.url" target="_blank">{{ link.platform }}</a>
                        </div>
                    </div>

                    <div v-else class="edit-links">
                        <div v-for="(link, index) in editedData.links" :key="index" class="edit-link-item">
                            <select v-model="link.platform" class="edit-input">
                                <option value="instagram">Instagram</option>
                                <option value="youtube">YouTube</option>
                                <option value="facebook">Facebook</option>
                                <option value="twitter">Twitter</option>
                            </select>
                            <input v-model="link.url" type="url" class="edit-input" placeholder="Enter URL" />
                            <button class="remove-btn" @click="removeLink(index)">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <button v-if="editedData.links.length < 4" class="add-link-btn" @click="addNewLink">
                            <i class="fas fa-plus"></i> Add New Link
                        </button>
                    </div>

                    <div v-if="editing.links" class="edit-actions">
                        <button class="save-btn" @click="saveChanges('links')">Save Links</button>
                        <button class="cancel-btn" @click="cancelEditing('links')">Cancel</button>
                    </div>
                </div>
            </section>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <!-- <div v-if="showDeleteModal" class="modal-overlay">
        <div class="modal-content">
            <h2 class="text-center">Delete Profile</h2>
            <p>Are you sure you want to delete this influencer profile? This action cannot be undone.</p>
            <div class="modal-actions">
                <button class="delete-confirm-btn" @click="confirmDelete">Delete</button>
                <button class="cancel-btn" @click="showDeleteModal = false">Cancel</button>
            </div>
        </div>
    </div> -->

    <!-- Avatar Edit Modal -->
    <div v-if="showAvatarModal" class="modal-overlay">
        <div class="modal-content">
            <h2 class="text-center">Edit Avatar</h2>
            <div class="avatar-edit-content">
                <div class="preview-container">
                    <img :src="previewAvatar || avatar || require('@/assets/profile-user.png')" alt="Preview"
                        class="avatar-preview" />
                </div>
                <input type="file" accept="image/jpeg,image/png,image/jpg" @change="handleFileSelect" class="file-input" id="avatar-input" />
                <label for="avatar-input" class="file-input-label">
                    <i class="fas fa-upload"></i>
                    Choose Image
                </label>
            </div>
            <div class="modal-actions" style="justify-content: space-between;">
                <button v-if="avatar" class="delete-confirm-btn" @click="deleteAvatar">
                    <i class="fas fa-trash"></i> Delete
                </button>
                <button class="save-btn" @click="saveAvatar" :disabled="!selectedFile">Save</button>
                <button class="cancel-btn" @click="closeAvatarModal">Cancel</button>
            </div>
        </div>
    </div>

    <!-- Name Edit Modal -->
    <div v-if="showNameModal" class="modal-overlay">
        <div class="modal-content">
            <h2 class="text-center mb-n2">Edit Name</h2>
            <div class="edit-form">
                <div class="float-label-input">
                    <input type="text" id="name" v-model="editedData.name" placeholder="Enter name" class="edit-input">
                    <label for="name">Name</label>
                </div>
            </div>
            <div class="modal-actions">
                <button class="save-btn" @click="saveNameChanges">Save</button>
                <button class="cancel-btn" @click="showNameModal = false">Cancel</button>
            </div>
        </div>
    </div>

    <!-- Username Edit Modal -->
    <div v-if="showUsernameModal" class="modal-overlay">
        <div class="modal-content">
            <h2 class="text-center mb-n2">Edit Username</h2>
            <div class="edit-form">
                <div class="float-label-input">
                    <input type="text" id="username" v-model="editedData.username" placeholder="Enter username"
                        class="edit-input">
                    <label for="username">Username</label>
                </div>
            </div>
            <div class="modal-actions">
                <button class="save-btn" @click="saveUsernameChanges">Save</button>
                <button class="cancel-btn" @click="showUsernameModal = false">Cancel</button>
            </div>
        </div>
    </div>



</template>

<script>
import axios from 'axios';

export default {
    name: 'InfluencerDetailsPage',

    data() {
        return {
            // for all
            user_role_id: '',
            username: '',
            name: '',
            avatar: '',
            time: '',

            // for inlfu and spon
            description: '',

            // only for influencer
            category: '',
            niche: '',
            reach: 0,
            link: [],

            // only for sponsor
            type: '',
            industry: '',
            budget: 0,
            approved:'',

            // UI State
            editing: {
                profile: false,
                links: false
            },
            // showDeleteModal: false,
            showAvatarModal: false,
            showNameModal: false,
            showUsernameModal: false,
            selectedFile: null,
            previewAvatar: null,

            // Edited Data
            editedData: {
                name: '',
                username: '',
                category: '',
                niche: '',
                reach: 0,
                description: '',
                links: [],
                type: '',
                industry: '',
                budget: 0
            }
        };
    },

    computed: {
        canEdit() {
            return true;
        },

        canDelete() {
            // return this.$store.getters.role === 'admin';
            return true;
        },

        parsedLinks() {
            try {
              return typeof this.link === 'string' ? JSON.parse(this.link) : [];
            } 
            catch {
              return [];
            }
        },
        availablePlatformForLinks() {
            let availablePlatforms = ['instagram', 'youtube', 'facebook', 'twitter'];
            let parsedLinks = this.editedData.links;

            for (let link of parsedLinks) {
                if (availablePlatforms.includes(link.platform)) {
                    availablePlatforms = availablePlatforms.filter(platform => platform!== link.platform);
                }
            }
            return availablePlatforms;
        },
        isInflu() {
            return this.$store.getters.role == 'influencer';
        },
        isAdmin() {
            return this.$store.getters.role == 'admin';
        },
        isSpon() {
            return this.$store.getters.role == 'sponsor';
        },

    },

    methods: {
        formatNumber(num) {
            return new Intl.NumberFormat().format(num);
        },

        formatReach(reach) {
            if (reach < 1000) {
                return reach; 
            }

            const suffixes = ["", "K", "M", "B", "T"];
            let suffixIndex = 0;
            let formattedReach = reach;

            while (formattedReach >= 1000) {
                formattedReach /= 1000;
                suffixIndex++;
            }

            // Round to one decimal place and append the appropriate suffix
            return `${formattedReach.toFixed(1)}${suffixes[suffixIndex]}`;
        },

        getLinkIcon(platform) {
            const icons = {
                instagram: 'fab fa-instagram',
                youtube: 'fab fa-youtube',
                facebook: 'fab fa-facebook',
                twitter: 'fab fa-twitter'
            };
            return icons[platform.toLowerCase()] || 'fas fa-link';
        },

        startEditing(section) {
            this.editing[section] = true;

            this.editedData.description = this.description;

            this.editedData.category = this.category;
            this.editedData.niche = this.niche;
            this.editedData.reach = this.reach;
            this.editedData.links = [...this.parsedLinks];

            this.editedData.type = this.type;
            this.editedData.industry = this.industry;
            this.editedData.budget = this.budget;
        },

        cancelEditing(section) {
            this.editing[section] = false;
        },

        addNewLink() {
            this.editedData.links.push({ platform: this.availablePlatformForLinks[0], url: '' });
        },

        removeLink(index) {
            this.editedData.links.splice(index, 1);
        },

        async saveChanges(section) {
            try {
                let promises;
                if (section === 'profile') {
                    let editedData = { ...this.editedData };
                    delete editedData['links'];
                    promises = Object.entries(editedData).map(param => param[1] ? param : null).filter(param => param).map(param => this.saveChangesRequest(param));
                } else if (section === 'links') {
                    let param = ['link', JSON.stringify(this.editedData.links)];
                    promises = [await this.saveChangesRequest(param)];                    
                }
                await Promise.allSettled(promises);
                this.editing[section] = false;
                this.fetchData();
                this.$toast.success(`${this.$capitalize(section)} updated successfully !`, {
                        position: 'bottom-right',
                        duration: 5000,
                        dismissible: true
                    });
            } catch (error) {                
                this.$errorComesNow(error);
            }
        },

        async saveChangesRequest(param) {
            try {
                let endpoint = `${this.$store.state.basePath}/edit-${this.$store.getters.role}-${param[0]}/${this.user_role_id}`;
                let data = {
                    [param[0]]: param[1]
                };

                const response = axios.patch(endpoint,
                    data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Auth-Token': this.$store.getters.auth_token
                    }
                });
                
                return response;
            } catch (error) {
                this.$errorComesNow(error);
            }
        },

        // async confirmDelete() {
        //     try {
        //         const response = await axios.delete(
        //             `${this.$store.state.basePath}/influencer/delete/${this.influencer_id}`,
        //             {
        //                 headers: {
        //                     'Content-Type': 'application/json',
        //                     'Auth-Token': this.$store.getters.auth_token
        //                 }
        //             }
        //         );

                
        //         if (response.data.success) {
        //             this.$toast.success('Influencer profile deleted successfully!', {
        //                 position: 'bottom-right',
        //                 duration: 5000,
        //                 dismissible: true
        //             });
        //             this.$router.push({ name: 'influencer-list' });
        //         }
        //     } catch (error) {
        //         this.$errorComesNow(error);
        //     }
        //     this.showDeleteModal = false;
        // },

        openNameModal() {
            this.editedData.name = this.name;
            this.showNameModal = true;
        },

        async saveNameChanges() {
            try {
                const response = await axios.patch(
                    `${this.$store.state.basePath}/edit-${this.$store.getters.role}-name/${this.$route.query.user_id}`,
                    {
                        name: this.editedData.name,
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    this.name = this.editedData.name;
                    this.$toast.success('Your Name updated successfully!');
                }
                this.showNameModal = false;
            } catch (error) {
                this.$errorComesNow(error);
            }
        },

        openUsernameModal() {
            this.editedData.username = this.username;
            this.showUsernameModal = true;
        },

        async saveUsernameChanges() {
            try {
                const response = await axios.patch(
                    `${this.$store.state.basePath}/edit-${this.$store.getters.role}-username/${this.$route.query.user_id}`,
                    {
                        username: this.editedData.username,
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    this.username = this.editedData.username;
                    this.$toast.success('Your Username updated successfully!');
                }
                this.showUsernameModal = false;
            } catch (error) {
                this.$errorComesNow(error);
            }
        },

        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                this.selectedFile = file;
                this.previewAvatar = URL.createObjectURL(file);
            }
        },

        async deleteAvatar() {
            try {
                const response = await axios.delete(
                    `${this.$store.state.basePath}/delete-${this.$store.getters.role}-avatar/${this.$route.query.user_id}`,
                    {
                        headers: {
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    this.avatar = null;
                    this.$toast.success('Avatar deleted successfully!');
                }
                this.showAvatarModal = false;
                location.reload();
            } catch (error) {
                this.$errorComesNow(error);
            }
        },

        async saveAvatar() {
            if (!this.selectedFile) return;

            const formData = new FormData();
            formData.append('avatar', this.selectedFile);

            try {
                const response = await axios.patch(
                    `${this.$store.state.basePath}/edit-${this.$store.getters.role}-avatar/${this.$route.query.user_id}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    this.avatar =  URL.createObjectURL(this.selectedFile);
                    this.$toast.success('Avatar updated successfully!');
                }
                this.showAvatarModal = false;
                location.reload();
            } catch (error) {
                this.$errorComesNow(error);
            }
        },

        closeAvatarModal() {
            this.showAvatarModal = false;
            this.selectedFile = null;
            this.previewAvatar = null;
        },

        adjustHeight() {
            // Adjust the height of the textarea
            const textarea = this.$refs.autoResize;
            if (textarea) {
                textarea.style.height = 'auto'; // Reset height to shrink if needed
                textarea.style.height = `${textarea.scrollHeight}px`; // Set height based on scrollHeight
            }
        },

        async fetchData() {
            try {
                const response = await axios.get(
                    `${this.$store.state.basePath}/${this.$store.getters.role}-details/${this.$route.query.user_id}`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                const data = response.data.db_data;
                // console.log(data);
                
                this.user_role_id = data[this.$store.getters.role + "_id"];
                this.username = data.username;
                this.name = data.name;
                this.avatar = data.avatar ? `data:image/png;base64,${data.avatar}` : null;
                this.time = data.time;

                this.description = this.isInflu || this.isSpon ? data.description : null;

                this.category = this.isInflu ? data.category : null;
                this.niche = this.isInflu ? data.niche : null;
                this.reach = this.isInflu ? data.reach : null;
                this.link = this.isInflu ? data.link : null;

                this.type = this.isSpon ? data.type : null;
                this.industry = this.isSpon ? data.industry : null;
                this.budget = this.isSpon ? data.budget : null;
                this.approved = this.isSpon ? data.approved : null;


            } catch (error) {
                this.$errorComesNow(error);
            }
        }
    },

    mounted() {
        this.fetchData();
    }
};
</script>

<style scoped>
.page-container {
    max-width: auto;
    margin: 0 auto;
    padding: 2rem;
    color: #1a1a1a;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #aad8fd;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.avatar-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
}

.avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.edit-avatar-overlay {
    position: absolute;
    bottom: 0;
    right: 0;
    background: #fff;
    border-radius: 50%;
    /* padding: 0.2rem; */
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.1);
    font-size: large
}

.edit-avatar-btn {
    background: #fff;
    border-radius: 50%;
    cursor: pointer;
    height: 2.5rem;
    width: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-details {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.name-section,
.username-section {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.edit-btn {
    padding: 0.25rem;
    font-size: 0.875rem;
}

.approved{
    padding: 2px 10px;
    font-family: cursive;
    background-color:rgb(0, 255, 0);    
    border-radius:20px;
    color:rgb(0, 0, 0);
    font-weight:bold;
}

.not-approved-pending{
    padding: 2px 10px;
    font-family: cursive;
    background-color:rgb(254, 103, 103);
    border-radius:20px;
    color:white;
    font-weight:bold;
}

.rejected{
    padding: 2px 10px;
    font-family: cursive;
    background-color:rgb(252, 0, 0);
    border-radius:20px;
    color:white;
    font-weight:bold;
}

.user-name {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0;
}

.username {
    font-size: 1.1rem;
    color: #666;
    margin: 0;
}

.name-section .edit-btn {
    opacity: 0;
}

.username-section .edit-btn {
    opacity: 0;
}

.name-section:hover .edit-btn {
    opacity: 1;
}

.username-section:hover .edit-btn {
    opacity: 1;
}

.content-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
}

.main-info-card {
    grid-row: span 2;
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    background-color: #aad8fd;
}

.card-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 0.95rem;
    background-color: #f7f9fa;
    border-radius: 0.5rem;
}

.info-item label {
    font-weight: 600;
    color: #666;
}

.description-section {
    background-color: #f7f9fa;
    padding: 0.95rem;
    border-radius: 0.5rem;
    margin-top: 2rem;
}

.stats-card {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Continuing from previous styles */

.stat-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-bottom: 1px solid #eee;
}

.stat-item:last-child {
    border-bottom: none;
}

.stat-item i {
    font-size: 1.5rem;
    color: #4299e1;
    background: #ebf8ff;
    padding: 1rem;
    border-radius: 0.75rem;
}

.stat-content {
    flex: 1;
}

.stat-content h3 {
    font-size: 0.9rem;
    color: #666;
    margin: 0 0 0.25rem 0;
}

.stat-content p {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0;
}

.links-card {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.links-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.link-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0rem;
    background: #f0f6fb;
    padding: 0.75rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.link-item:hover {
    background: #deedfd;
}

.link-item i {
    font-size: 1.25rem;
    color: #4299e1;
}

.link-item a {
    color: #1a1a1a;
    text-decoration: none;
    font-weight: 500;
}

.link-item a:hover {
    color: #4299e1;
}

/* Edit Mode Styles */
.edit-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    font-size: 1rem;
    color: #1a1a1a;
    background: #f8fafc;
    transition: all 0.2s ease;
}

.description-input {
    min-height: 120px;
    resize: vertical;
}

.edit-link-item {
    display: grid;
    grid-template-columns: 1fr 2fr auto;
    gap: 1rem;
    align-items: center;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 0.5rem;
    margin:15px 0px;
}

.edit-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e2e8f0;
}

/* Buttons */
.edit-btn {
    background: none;
    border: none;
    color: #64748b;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.edit-btn:hover {
    background: #f1f5f9;
    color: #1a1a1a;
}

.save-btn {
    background: #4299e1;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.save-btn:hover {
    background: #3182ce;
}

.cancel-btn {
    background: #f1f5f9;
    color: #64748b;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.cancel-btn:hover {
    background: #e2e8f0;
    color: #1a1a1a;
}

.delete-btn {
    background: #fee2e2;
    color: #dc2626;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.delete-btn:hover {
    background: #fecaca;
}

.add-link-btn {
    width: 100%;
    background: #f8fafc;
    border: 2px dashed #e2e8f0;
    color: #64748b;
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
}

.add-link-btn:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
    color: #1a1a1a;
}

.remove-btn {
    background: none;
    border: none;
    color: #ef4444;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.remove-btn:hover {
    background: #fee2e2;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 50;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.modal-content h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #dc2626;
}

.modal-content p {
    color: #4b5563;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
}

.delete-confirm-btn {
    background: #dc2626;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.delete-confirm-btn:hover {
    background: #b91c1c;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .content-grid {
        grid-template-columns: 1fr;
    }

    .main-info-card {
        grid-row: auto;
    }
}

@media (max-width: 768px) {
    .page-container {
        padding: 1rem;
    }

    .page-header {
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }

    .user-info {
        flex-direction: column;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .edit-link-item {
        grid-template-columns: 1fr;
    }

    .modal-content {
        width: 95%;
        padding: 1.5rem;
    }
}

@media (max-width: 480px) {
    .user-name {
        font-size: 1.5rem;
    }

    .edit-actions {
        flex-direction: column;
    }

    .modal-actions {
        flex-direction: column;
    }
}

/* Utility Classes */
.text-truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.avatar-edit-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    margin: 1.5rem 0;
}

.preview-container {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid #e2e8f0;
}

.avatar-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.file-input {
    display: none;
}

.file-input-label {
    background: #4299e1;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
}

.file-input-label:hover {
    background: #3182ce;
}

.edit-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 1.5rem 0;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    font-weight: 600;
    color: #4b5563;
}
</style>
