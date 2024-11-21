<template>
  <div>
    <h1>뉴스 상세보기</h1>
    <div v-if="article">
      <p><strong>제목:</strong> {{ article.news_title }}</p>
      <p><strong>카테고리:</strong> {{ article.category_name }}</p>
      <p><strong>작성자:</strong> {{ article.writer }}</p>
      <p><strong>내용:</strong></p>
      <p>{{ article.content }}</p>
    </div>
    <div v-else>
      <p>뉴스 데이터를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const article = ref(null)

// API URL
const API_URL = import.meta.env.VITE_DJANGO_API_URL

// 뉴스 데이터 가져오기
const fetchNewsDetail = async () => {
  try {
    const response = await axios.get(`${API_URL}/news/${route.params.id}/`) // ID로 API 호출
    article.value = response.data
  } catch (error) {
    console.error('Failed to fetch news detail:', error)
  }
}

onMounted(() => {
  fetchNewsDetail()
})
</script>

<style scoped>
/* 상세보기 스타일 */
</style>
