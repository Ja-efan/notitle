<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Pinia 스토어 불러오기
const userStore = useUserStore()
</script>

<template>
  <nav>
    <!-- RouterLink 에서 경로를 선택하고 -->
    <RouterLink to="/">메인 페이지</RouterLink> |
    <RouterLink to="/login">로그인</RouterLink>
    
    <!-- 로그인된 사용자 이름 표시 -->
    <span v-if="userStore.loginUsername" class="username">
      | {{ userStore.loginUsername }}님
    </span>
  </nav>

  <!-- RouterView 에 경로에 해당하는 컴포넌트가 출력된다. -->
  <RouterView />
</template>


<style scoped>
/* 네비게이션 바 스타일 */
nav {
  background-color: #2575fc;
  padding: 10px 20px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* 네비게이션 링크 스타일 */
nav a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  transition: color 0.3s ease, text-shadow 0.3s ease;
}

/* 로그인된 사용자 이름 스타일 */
.username {
  color: #ffdd57;
  font-size: 1rem;
  font-weight: bold;
  margin-left: 10px;
}
</style>
