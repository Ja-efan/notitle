<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const likedNews = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');

const LIKED_NEWS_API_URL = import.meta.env.VITE_BACKEND_API_URL

const fetchLikedNews = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(
      LIKED_NEWS_API_URL, 
    {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`, // 인증 토큰
      },
    });
    likedNews.value = response.data;
  } catch (error) {
    errorMessage.value = '좋아요한 뉴스를 불러오는 데 실패했습니다.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchLikedNews();
});
</script>

<template>
  <div class="scrap-container">
    <h1>좋아요한 뉴스</h1>
    <!-- 로딩 상태 -->
    <div v-if="isLoading">데이터를 불러오는 중...</div>
    <!-- 에러 메시지 -->
    <div v-if="errorMessage">{{ errorMessage }}</div>
    <!-- 좋아요한 뉴스 리스트 -->
    <div v-if="likedNews.length > 0" class="news-list">
      <div class="news-item" v-for="news in likedNews" :key="news.id">
        <h2>{{ news.title }}</h2>
        <p>{{ news.summary }}</p>
        <p>카테고리: {{ news.category_name || '알 수 없음' }}</p>
        <a :href="news.url" target="_blank">기사 읽기</a>
      </div>
    </div>
    <!-- 좋아요한 뉴스가 없을 경우 -->
    <div v-else-if="!isLoading">좋아요한 뉴스가 없습니다.</div>
  </div>
</template>

<style scoped>
.scrap-container {
  max-width: 800px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}
.news-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.news-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.news-item h2 {
  color: #2575fc;
}
</style>
