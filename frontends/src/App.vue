<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

// Pinia 스토어 불러오기
const userStore = useUserStore()
const router = useRouter()

// 로그아웃 함수
const logout = async () => {
  try {
    await userStore.logout()
    // router.push('/login') // 로그아웃 후 로그인 페이지로 이동
  } catch (error) {
    console.error('로그아웃 실패:', error)
  }
}

// TailoredNews 페이지로 이동
const goToTailoredNews = () => {
  if (!userStore.isLoggedIn()) {
    alert('로그인이 필요합니다.')
    router.push('/login') // 로그인 페이지로 리디렉션
    return
  }
  router.push('/tailored-news') // TailoredNews 페이지로 이동
}
</script>

<template>
  <!-- 네비게이션 바 -->
  <nav>
    <!-- 플랫폼 이름 -->
    <div class="platform-name">無愚題: 어리석음이 없는 제목</div>

    <!-- 네비게이션 링크 -->
    <div class="nav-links">
      <RouterLink to="/">메인 페이지</RouterLink>
      <RouterLink to="/news-analysis">뉴스 분석 페이지</RouterLink>
      <button class="tailored-button" @click="goToTailoredNews">
        맞춤 늬-우스
      </button>

      <!-- 로그인 여부에 따라 사용자 이름과 로그아웃 버튼 표시 -->
      <template v-if="userStore.loginUsername">
        <span class="username">{{ userStore.loginUsername }}님</span>
        <button class="logout-button" @click="logout">로그아웃</button>
      </template>
      <template v-else>
        <RouterLink to="/login">로그인</RouterLink>
      </template>
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

/* Tailored News 버튼 스타일 */
.tailored-button {
  color: #fff;
  font-size: 1.1rem; /* 네비게이션 링크와 동일한 크기 */
  font-weight: bold; /* 동일한 굵기 */
  text-decoration: none; /* 링크 스타일 제거 */
  background: none; /* 배경 제거 */
  border: none; /* 테두리 제거 */
  cursor: pointer;
  transition: color 0.3s ease, text-shadow 0.3s ease, transform 0.2s ease;
}

/* Tailored News 버튼 호버 효과 */
.tailored-button:hover {
  color: #ffdd57; /* 호버 시 텍스트 색상 변경 */
  text-shadow: 0 2px 5px rgba(255, 221, 87, 0.8); /* 호버 시 텍스트 그림자 */
  transform: scale(1.1); /* 호버 시 크기 약간 확대 */
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

/* 로그아웃 버튼 스타일 */
.logout-button {
  background-color: #ff5a57;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #e04747;
}
</style>
