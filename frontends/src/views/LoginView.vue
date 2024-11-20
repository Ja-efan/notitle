<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const logIn = function () {
  console.log('Logging in with', username.value, password.value)
  // 로그인 요청 처리 로직
}

const goSignUp = function () {
  router.push('/signup') // 회원가입 페이지로 이동
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">로그인</h1>
      <form @submit.prevent="logIn">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Enter your username">
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Enter your password">
        </div>

        <button type="submit" class="login-button">Login</button>
        <button type="button" class="signup-button" @click="goSignUp">Sign Up</button>
      </form>
    </div>
  </div>
</template>



<style scoped>
/* 전체 컨테이너 스타일 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  font-family: 'Arial', sans-serif;
  color: #fff;
}

/* 로그인 카드 스타일 */
.login-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px 30px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #333;
}

/* 제목 스타일 */
.login-title {
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
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

/* 로그인 버튼 스타일 */
.login-button {
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
  transition: background-color 0.3s ease;
  margin-bottom: 10px;
}

.login-button:hover {
  background-color: #1b5ab6;
}

/* 회원가입 버튼 스타일 */
.signup-button {
  display: block;
  width: 100%;
  padding: 10px 15px;
  background-color: #fff;
  border: 2px solid #2575fc;
  border-radius: 4px;
  color: #2575fc;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.signup-button:hover {
  background-color: #2575fc;
  color: #fff;
}
</style>