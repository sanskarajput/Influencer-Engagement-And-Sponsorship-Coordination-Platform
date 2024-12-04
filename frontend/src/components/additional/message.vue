<template>
    <div class="messaging-wrapper" :class="isMinimized ? 'minimized' : 'expandad'">
        <div class="messaging-header">
            <div class="header-content">
                <div class="title">Chats</div>
                <button class="minimize-btn" @click="toggleMinimize">
                    <i v-if="isMinimized" class="fa-solid fa-angle-up"></i>
                    <i v-else class="fa-solid fa-angle-down"></i>
                </button>
            </div>
        </div>

        <div class="messages-area" v-show="!isMinimized" ref="messagesContainer">
            <div v-for="message in messages" :key="message.id" class="message"
                :class="{ 'sent': isSent(message.commenter_role) }">
                <div class="message-bubble" :class="{ 'message-bubble-sent': isSent(message.commenter_role) }">
                    <div class="message-content">{{ message.comment }}</div>
                    <div class="message-time">{{ $forCreatedAtShort(message.time) }}</div>
                </div>
            </div>
        </div>

        <div class="message-input-container" v-show="!isMinimized">
            <textarea v-model="newMessage" placeholder="Write a message..." @keydown="handleKeyDown" rows="1"
                ref="messageInput"></textarea>
            <button class="send-btn" @click="sendMessage" :disabled="!newMessage.trim()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: 'ModernMessaging',
    props: {
        request_id: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            isMinimized: false,
            newMessage: '',
            messages: null,
            interval: null,
        }
    },
    methods: {
        toggleMinimize() {
            this.isMinimized = !this.isMinimized
            if (!this.isMinimized) {
                this.$nextTick(() => {
                    this.scrollToBottom()
                })
            }
        },
        handleKeyDown(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                this.sendMessage()
            }
        },
        async sendMessage() {
            if (this.$store.getters.role === 'admin') {
                this.newMessage = ''
                this.$toast.success('Admins Are not Allowed to Chatting !',
                    {
                        position: 'bottom-right',
                        duration: 5000,
                        dismissible: true
                    }
                )
                return
            }
            if (!this.newMessage.trim()) return
            try {
                let response = await axios.post(`${this.$store.state.basePath}/requests/${this.request_id}/chat/create`,
                    {
                        comment: this.newMessage
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    const data = response.data.db_data;
                    this.messages.push(data);
                    this.newMessage = ''
                    this.$refs.messageInput.style.height = 'auto'
                    this.$nextTick(() => {
                        this.scrollToBottom()
                    })
                }
            } catch (error) {
                this.$errorComesNow(error);
            }
        },
        scrollToBottom() {
            const container = this.$refs.messagesContainer
            if (container) {
                container.scrollTop = container.scrollHeight
            }
        },
        async fetchData() {
            try {
                let response = await axios.get(`${this.$store.state.basePath}/requests/${this.request_id}/chat/fetch`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Auth-Token': this.$store.getters.auth_token
                        }
                    }
                );

                if (response.status === 200) {
                    this.messages = response.data.db_data;
                }
            } catch (error) {
                this.$errorComesNow(error);
            }
        },
        isSent(commenter) {
            return this.$store.getters.role === commenter.toLowerCase() ? true : false;
        }
    },
    mounted() {
        this.fetchData().then(() => {
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        });

        this.interval = setInterval(() => {
            this.fetchData();
        }, 1000);

        this.$refs.messageInput.addEventListener('input', (e) => {
            e.target.style.height = 'auto'
            e.target.style.height = e.target.scrollHeight + 'px'
        })
    },
    beforeUnmount() {
        clearInterval(this.interval);
    }
}
</script>

<style scoped>
.messaging-wrapper {
    position: fixed;
    bottom: 0;
    right: 20px;
    width: 342px;
    background: rgb(204, 204, 204);
    border-radius: 16px 16px 0 0;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}

.messaging-header {
    padding: 12px 16px;
    background: #398ee3;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    cursor: pointer;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.title {
    font-weight: 600;
    font-size: 15px;
    color: #ffffff;
}

.minimize-btn {
    background: none;
    border: none;
    padding: 6px;
    cursor: pointer;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s;
    font-size: 15px;
    border-radius: 50%;
}

.minimize-btn:hover {
    color: #1a1a1a;
    background: #dadada;
}

.messages-area {
    height: 340px;
    overflow-y: auto;
    padding: 16px;
    background: #fafafa;
    display: flex;
    flex-direction: column;
    scroll-behavior: smooth;
}

.message {
    margin-bottom: 8px;
    max-width: 85%;
    align-self: flex-start;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    animation: fadeIn .5s ease-out;
}

.message.sent {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    object-fit: cover;
}

.message-bubble {
    background: white;
    border-radius: 14px;
    padding: 8px 12px;
    box-shadow: 4px 4px 4px rgba(0, 0, 0, 0.05);
    position: relative;
}

.message.sent .message-bubble {
    box-shadow: 4px 4px 8px rgba(45, 126, 226, 0.479);
    background: #398ee3;
    color: white;
}

.message-content {
    font-size: 13px;
    line-height: 1.4;
    margin-bottom: 2px;
}

.message-time {
    font-size: 9px;
    color: #999;
    text-align: right;
}

.message.sent .message-time {
    color: rgba(255, 255, 255, 0.7);
}

.message-input-container {
    padding: 12px;
    background: white;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
    display: flex;
    gap: 8px;
    align-items: flex-end;
}

.message-input-container textarea {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #e0e0e0;
    border-radius: 20px;
    resize: none;
    font-size: 13px;
    font-family: inherit;
    max-height: 120px;
    transition: border-color 0.2s;
    line-height: 1.4;
}

.message-input-container textarea:focus {
    outline: none;
    border-color: #0a66c2;
}

.send-btn {
    padding: 8px;
    background: #0a66c2;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    height: 32px;
    width: 32px;
}

.send-btn:hover {
    background: #0855a1;
}

.send-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.minimized {
    height: auto;
}

/* Custom Scrollbar */
.messages-area::-webkit-scrollbar {
    width: 6px;
}

.messages-area::-webkit-scrollbar-track {
    background: transparent;
}

.messages-area::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 2px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.2);
}

textarea::-webkit-scrollbar {
    width: 0px;
}

textarea::-webkit-scrollbar-track {
    background: transparent;
}

textarea::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 2px;
}

textarea::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.2);
}

/* Animations */
@keyframes slideIn {
    from {
        transform: translateY(100%);
    }

    to {
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

.messaging-wrapper:not(.minimized) {
    animation: slideIn 1s cubic-bezier(0.4, 0, 0.2, 1);
}


/* @keyframes slideOut {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(100%);
    }
}

.messaging-wrapper:not(.expandad) {
    animation: slideOut 1s cubic-bezier(0.4, 0, 0.2, 1);
}
 */
</style>
