<template>
  <div class="profile-card animation-small-to-original">
    <!-- Cover Image -->
       <img :src="require(`@/assets/banner-for-${profileOf}s.jpg`)" :alt="user.name + ' cover'" class="cover-img w-100">

    <!-- type -->
    <p v-if="profileOf === 'sponsor'" class="user-type">
      <span v-if="user.type === 'Individual'" class="badge badge-primary">Individual</span>
      <span v-else-if="user.type === 'Company'" class="badge badge-success">Company</span>
    </p>

    <!-- Profile Content -->
    <div class="text-center">
      <router-link :to="{name: 'other-user-profile-view', params:{ role: profileOf }, query : { user_id : user[`${profileOf}_s_user_id`] }}" >
        <img :src="user.avatar ? `data:image/png;base64,${user.avatar}` : require('@/assets/profile-user.png')" :alt="user.name" class="profile-img">
      </router-link>

      <div class="pb-4 px-4 pt-1">
        <h6 class="mb-0 text-black ml-2">
          <router-link :to="{name: 'other-user-profile-view', params:{ role: profileOf }, query : { user_id : user[`${profileOf}_s_user_id`] }}" class="user-name" >
            <i class="fs-4 fw-bold">{{ user.name }}</i>
          </router-link>
          <i v-if="profileOf === 'influencer' && user.isActive" class="fas fa-circle-check verified-badge fs-6"></i>
          <i v-if="profileOf === 'sponsor' && user.isApproved === 'TRUE'" class="fas fa-check-circle verified-badge fs-5" ></i>
        </h6>

        <!-- Niche -->
        <p v-if="profileOf === 'influencer'" class="text-muted fs-7 mb-0">{{ user.niche || 'Niche : will update soon....'}}</p>

        <!-- category -->
        <p v-if="profileOf === 'influencer'" class="text-muted fs-8 mb-3">{{ user.category || 'Category : will update soon....'}}</p>

        <!-- industry -->
        <p v-if="profileOf === 'sponsor'" class="text-muted fs-7 mb-0">{{ user.industry || 'Industry : will update soon....'}}</p>

        <!-- budget -->
        <p v-if="profileOf === 'sponsor'" class="text-muted fs-8 mb-3">{{ user.budget ? `₹ ${user.budget}.00` : 'Budget : will update soon....' }}</p>
        
        <!-- Social Links -->
        <div v-if="profileOf === 'influencer'" class="social-links d-flex justify-content-center mb-3">
          <p v-if="!parsedLinks.length" class="text-muted fs-8 mb-3">{{ 'Links : will update soon....' }}</p>
          <a v-for="(link, index) in parsedLinks" :key="index" :href="link.url" :class="link.platform" target="_blank" v-show="!!link.url">
            <i class="fab fa-sm"
              :class="link.platform === 'facebook' ? `fa-${link.platform}-f` : `fa-${link.platform}`"></i>
          </a>
        </div>

        <!-- description -->
        <p class="extra-small mb-3">
          {{ user.description || 'description : will update soon....' }}
        </p>


        <!-- Stats -->
        <div class="stats row text-center g-0 text-black">
          <div v-for="(stat, label) in stats" :key="label" class="col">
            <h6 class="mb-0 ">{{ stat }}</h6>
            <small class="">{{ label }}</small>
          </div>
          <div v-if="profileOf === 'influencer'" class="col">
            <h6 class="mb-0 ">Reach</h6>
            <small class="">{{ user.reach || 'N/A' }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sponsor-Profile-All-Influencers',
  props: {
    user: {
      type: Object,
      required: true
      // default: () => {
      //   return {
      //     role_id : 2,
      //     role_s_user_id : 2,
      //     name: 'Sarah Johnson',
      //     username: 'John',

      //     niche: 'Digital Creator & Lifestyle Influencer',
      //     category: 'Digital Creator & Lifestyle',
      //     reach : 2322,

      //     type: "Individual",
      //     industry: 'industry',
      //     budget: "budget",

      //     description: 'Creating c that inspires. Travel enthusiast, foodie, antent that inspires. Travel enthusiast, foodie, antent that inspires. Travel enthusiast, foodie, antent that inspires. Travel enthusiast, foodie, antent that inspires. Travel enthusiast, foodie, antent that inspires. Travel enthusiast, foodie, a Love sharing my journey and connecting with amazing people! ✨',
      //     isActive: true,
      //     avatar: 'https://placeholder.com/120',
      //   }
      // }
    },
    profileOf: {
      type: String,
      required: true,
      validator: value => ['influencer', 'sponsor'].includes(value)
    },
    stats: {
      type: Object,
      default: () => {
        return {
          Followers: '1.2M',
          Posts: '4.5K'
        }
      }
    }
  },
  computed: {
    parsedLinks() {
      try {        
        return typeof this.user.link === 'string' ? JSON.parse(this.user.link) : [];
      }
      catch {
        return [];
      }
    },

  }
}
</script>

<style scoped>
.profile-card {
  position: relative;
  width: 250px;
  border: 1px solid #2d353a;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.4s;
  margin-bottom: 1.5rem;
  background: linear-gradient(
    45deg,
    hsl(240deg 47% 94%) 0%,
    hsl(311deg 80% 95%) 12%,
    hsl(347deg 100% 95%) 21%,
    hsl(29deg 100% 92%) 27%,
    hsl(50deg 100% 89%) 33%,
    hsl(48deg 100% 89%) 38%,
    hsl(37deg 100% 91%) 44%,
    hsl(24deg 100% 92%) 50%,
    hsl(9deg 100% 94%) 56%,
    hsl(6deg 81% 93%) 64%,
    hsl(21deg 100% 91%) 72%,
    hsl(37deg 81% 88%) 81%,
    hsl(64deg 51% 84%) 90%,
    hsl(109deg 61% 86%) 100%
  );
}

.profile-card:hover {
  transform: scale(1.08);
}

.cover-img {
  height: 100px;
  object-fit: cover;
}

.profile-img {
  background-color: #fff;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  margin-top: -40px;
}

.verified-badge {
  color: #24f21d;
  margin-left: 6px;
}

.fs-7 {
  font-size: 11.5px;
}

.fs-8 {
  font-size: 10.5px;
}

.user-type {
  position: absolute;
  top: 5px;
  right: 14px;
}

.user-name {
  text-decoration: none;
}

.social-links a {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.3s;
  margin: 0 5px;
}

.social-links a:hover {
  transform: scale(1.1);
}

.extra-small {
  font-size: 0.75rem;
  color: darkblue;
  min-height: 50px;
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}


.youtube {
  background: #FF0000;
  color: white;
  opacity: 0.95;
}

.youtube:hover {
  background: #cc0000;
  opacity: 1;
}

.facebook {
  background: #1877F2;
  color: white;
  opacity: 0.95;
}

.facebook:hover {
  background: #0d65d9;
  opacity: 1;
}

.instagram {
  background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
  color: white;
  opacity: 0.95;
}

.instagram:hover {
  opacity: 1;
}

.twitter {
  background: #1DA1F2;
  color: white;
  opacity: 0.95;
}

.twitter:hover {
  background: #0c85d0;
  opacity: 1;
}

.stats {
  border-top: 1px solid #9b9696;
  padding-top: 1rem;
  margin-bottom: -.5rem;
}
</style>