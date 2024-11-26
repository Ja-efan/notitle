<script setup>
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios';


const userStore = useUserStore()

const username = ref(null)
const email = ref(null) // 이메일 필드 추가
const password1 = ref(null)
const password2 = ref(null)

const dislikedCategories = ref([])  // 사용자 입력값 저장 (비선호 카테고리 )
const categories = ref([])  // 카테고리 목록

const GET_CATEGORIES_API_URL = import.meta.env.VITE_GET_CATEGORIES_API_URL

// Fetch categories (FE에서 선택할 카테고리 불러오기)
const fetchCategories = async () => {
  console.log(GET_CATEGORIES_API_URL)
  try {
    const response = await axios.get(
      GET_CATEGORIES_API_URL
    );

    console.log(response.data)
    categories.value = response.data;
    console.log(categories.value)
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};
fetchCategories()

// Watch dislikedCategories for changes
watch(dislikedCategories, (newValue) => {
  console.log('Disliked categories updated:', newValue);
});

// handle user registration

const signUp = function() {
  const payload = {
    username: username.value,
    email: email.value, // 이메일 포함
    password1: password1.value,
    password2: password2.value,
    disliked_categories: dislikedCategories.value,
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

        <!-- 비선호 카테고리 선택 -->
        <div>
          <h3>비선호 카테고리를 선택하세요.</h3>
          <div v-if="categories.length" class="category-container">
            <div v-for="category in categories" :key="category.id">
              <input 
                type="checkbox" 
                :id="'category-' + category.id" 
                :value="category.id" 
                v-model="dislikedCategories" 
              />
              <label :for="'category-' + category.id">{{ category.category_name }}</label>
            </div>
          </div>
          <div v-else class="loading-message">
            카테고리를 로드 중입니다...
          </div>
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
}
/* 비선호 카테고리 선택 섹션 스타일 */
h3 {
  margin: 20px 0 10px;
  font-size: 1.2rem;
  color: #333;
  text-align: left;
}

/* 카테고리 선택 컨테이너 */
.category-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

/* 개별 카테고리 스타일 */
.category-container label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background-color: #f9f9f9;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  color: #333;
  min-width: 80px; /* 버튼의 최소 너비 설정 */
  text-align: center; /* 텍스트 정렬 */
}

/* 카테고리 호버 스타일 */
.category-container label:hover {
  background-color: #eef3fc;
  border-color: #2575fc;
}

/* 체크박스 숨기기 */
.category-container input[type="checkbox"] {
  display: none;
}

/* 체크박스 선택 시 스타일 */
.category-container input[type="checkbox"]:checked + label {
  background-color: #2575fc;
  color: white;
  border-color: #1b5ab6;
}

</style>
