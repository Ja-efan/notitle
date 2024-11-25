<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Pinia 스토어 불러오기
const userStore = useUserStore()
</script>

<template>
  <!-- 네비게이션 바 -->
  <nav>
    <!-- 플랫폼 이름 -->
    <div class="platform-name">無愚題: 무우제</div>

    <!-- 네비게이션 링크 -->
    <div class="nav-links">
      <RouterLink to="/">메인 페이지</RouterLink> |
      <RouterLink to="/login">로그인</RouterLink> |
      
      <!-- 로그인된 사용자 이름 표시 -->
      <span v-if="userStore.loginUsername" class="username">
        {{ userStore.loginUsername }}님
      </span>
      
    </div>
  </nav>
  
  <RouterView />
</template>

<style scoped>
/* 네비게이션 바 스타일 */
nav {
  background-color: #2575fc;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between; /* 양쪽 정렬 */
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  color: #fff;
}

/* 플랫폼 이름 스타일 */
.platform-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
}

/* 네비게이션 링크 컨테이너 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 15px; /* 링크 간 간격 */
}

/* 네비게이션 링크 스타일 */
nav a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  transition: color 0.3s ease, text-shadow 0.3s ease, transform 0.2s ease;
}

/* 호버 효과: 색상 변경 및 텍스트 그림자 추가 */
nav a:hover {
  color: #ffdd57;
  text-shadow: 0 2px 5px rgba(255, 221, 87, 0.8);
  transform: scale(1.1);
}

/* 로그인된 사용자 이름 스타일 */
.username {
  color: #ffdd57;
  font-size: 1rem;
  font-weight: bold;
  margin-left: 10px;
}
</style>
