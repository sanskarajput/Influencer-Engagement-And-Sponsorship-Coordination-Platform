<template>
    <span ref="counter">{{ displayValue }}</span>
</template>

<script>
export default {
    name: 'CounterNumber',
    props: {
        till: {
            type: Number,
            default: 0,
            validator: (value) => value >= 0
        }
    },
    data() {
        return {
            count: 0,
            duration: 1500,
            startTime: null,
            interval: null,
            displayValue: 0
        }
    },
    methods: {
        incrementCounter() {
            // If no valid till value or already completed, return
            if (this.till <= 0 || this.count >= this.till) {
                this.stopCounter();
                return;
            }

            const currentTime = Date.now();
            const elapsedTime = currentTime - this.startTime;
            const progress = Math.min(elapsedTime / this.duration, 1);

            this.count = Math.floor(this.till * progress);
            this.displayValue = this.count;

            if (progress >= 1) {
                this.stopCounter();
            }
        },
        stopCounter() {
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
                this.displayValue = this.till;
            }
        }
    },
    mounted() {
        // Only start if till is a positive number
        if (this.till > 0) {
            this.startTime = Date.now();
            this.interval = setInterval(this.incrementCounter, 10);
        } else {
            this.displayValue = 0;
        }
    },
    beforeUnmount() {
        this.stopCounter();
    }
}
</script>