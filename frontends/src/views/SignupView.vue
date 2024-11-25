<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'


const userStore = useUserStore()

const username = ref(null)
const email = ref(null) // 이메일 필드 추가
const password1 = ref(null)
const password2 = ref(null)


const signUp = function() {
  const payload = {
    username: username.value,
    email: email.value, // 이메일 포함
    password1: password1.value,
    password2: password2.value
  }
  userStore.regist(payload)
}
</script>

<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1 class="signup-title">회원가입</h1>
      <form @submit.prevent="signUp">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Enter your username" />
        </div>

        <div class="form-group">
          <label for="email">Email</label> <!-- 이메일 입력 필드 -->
          <input type="email" id="email" v-model="email" placeholder="Enter your email" />
        </div>

        <div class="form-group">
          <label for="password1">Password</label>
          <input type="password" id="password1" v-model="password1" placeholder="Enter your password" />
        </div>

        <div class="form-group">
          <label for="password2">Confirm Password</label>
          <input type="password" id="password2" v-model="password2" placeholder="Confirm your password" />
        </div>

        <button type="submit" class="signup-button">Sign Up</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* 기존 스타일 그대로 유지 */
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  font-family: 'Arial', sans-serif;
  color: #333;
}

.signup-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.signup-title {
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #2575fc;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
}

.form-group input:focus {
  border-color: #2575fc;
}

.signup-button {
  display: block;
  width: 100%;
  padding: 10px 15px;
  background-color: #2575fc;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.signup-button:hover {
  background-color: #1b5ab6;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .signup-card {
    padding: 15px 20px;
  }

  .signup-title {
    font-size: 1.5rem;
  }

  .form-group input {
    font-size: 0.9rem;
  }

  .signup-button {
    font-size: 1rem;
  }
}
</style>
