import routers from "./routers";

export default {
  methods: {
    $capitalize(role) {
      return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase();
    },
    $errorComesNow(error) {
      console.log(error)
      // console.log(error.response)
      // console.log(error.response.data)
      if (error.code === "ERR_NETWORK") {
        routers.push({ name: "network-error" });
      } else if (error.response.status == 401) {
        routers.push({ name: 'unauthorized' });
      } else if (error.response.status == 403) {
        routers.push({ name: 'forbidden' });
      } else if (error.response.status == 404) {
        routers.push({ name: 'pageNotFound' });
      }
    },
    $getDateTimeInUTC(dateString) {
      const dateObject = new Date(dateString);

      const date = `${dateObject.getUTCFullYear()}-${(dateObject.getUTCMonth() + 1).toString().padStart(2, '0')}-${dateObject.getUTCDate().toString().padStart(2, '0')}`;
      const time = `${dateObject.getUTCHours().toString().padStart(2, '0')}:${dateObject.getUTCMinutes().toString().padStart(2, '0')}:${dateObject.getUTCSeconds().toString().padStart(2, '0')} UTC`.slice(0, -7);

      return { date, time };
    },
    $forCreatedAtLong(startTime) {
      if (startTime) {
        const currentTime = new Date();
        const timeDifference = currentTime - new Date(startTime);

        // Calculate seconds, minutes, hours, days, weeks, months, and years
        const seconds = Math.floor(timeDifference / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        const weeks = Math.floor(days / 7);
        const months = Math.floor(days / 30);
        const years = Math.floor(days / 365);

        if (years > 0) {
          return `${years} ${years === 1 ? 'year' : 'years'} ago`;
        } else if (months > 0) {
          return `${months} ${months === 1 ? 'month' : 'months'} ago`;
        } else if (weeks > 0) {
          return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`;
        } else if (days > 0) {
          return `${days} ${days === 1 ? 'day' : 'days'} ago`;
        } else if (hours > 0) {
          return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
        } else if (minutes > 0) {
          return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;
        } else if (seconds > 10) {
          return `${seconds} ${seconds === 1 ? 'second' : 'seconds'} ago`;
        } else {
          return "just now";
        }
      }
      return "time not found";
    },
    $forCreatedAtShort(startTime) {
      if (startTime) {
        const currentTime = new Date();
        const timeDifference = currentTime - new Date(startTime);
    
        // Calculate seconds, minutes, hours, days, weeks, months, and years
        const seconds = Math.floor(timeDifference / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        const weeks = Math.floor(days / 7);
        const months = Math.floor(days / 30);
        const years = Math.floor(days / 365);
    
        if (years > 0) {
          return `${years}y ago`;
        } else if (months > 0) {
          return `${months}mo ago`;
        } else if (weeks > 0) {
          return `${weeks}w ago`;
        } else if (days > 0) {
          return `${days}d ago`;
        } else if (hours > 0) {
          return `${hours}h ago`;
        } else if (minutes > 0) {
          return `${minutes}m ago`;
        } else if (seconds > 10) {
          return `${seconds}s ago`;
        } else {
          return "just now";
        }
      }
      return "time not found";
    },
    $formatDateRange(start_date, end_date) {
      // const options = { year: 'numeric', month: 'short', day: 'numeric' };

      const start = new Date(start_date);
      const end = new Date(end_date);

      const startMonth = start.toLocaleString('default', { month: 'short' });
      const startDay = start.getDate();
      const startYear = start.getFullYear();
      const endMonth = end.toLocaleString('default', { month: 'short' });
      const endDay = end.getDate();
      const endYear = end.getFullYear();

      if (startYear === endYear) {
        return `${startMonth} ${startDay} - ${endMonth} ${endDay}, ${endYear}`;
      }
      return `${startMonth} ${startDay}, ${startYear} - ${endMonth} ${endDay}, ${endYear}`;

    },
    $forStatus(start_date, end_date) {
      if (!start_date || !end_date) {
        return 'draft';
      }
    
      const currentTime = new Date();
      const startTime = new Date(start_date);
      const endTime = new Date(end_date);
    
      if (currentTime < startTime) {
        return 'scheduled';
      } else if (currentTime >= startTime && currentTime <= endTime) {
        return 'active';
      } else if (currentTime > endTime) {
        return 'ended';
      }
    }
  },

}
