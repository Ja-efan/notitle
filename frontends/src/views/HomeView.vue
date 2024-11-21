<script setup>
import { onMounted } from 'vue'
import { useNewsStore } from '@/stores/news'
import router from '@/router';

// Pinia 스토어 불러오기
const newsStore = useNewsStore()

// 초기 데이터 로드
onMounted(() => {
  newsStore.fetchNews()
  console.log(newsStore.news)
})

const goToDetail = (id) => {
  console.log('사용자 선택 뉴스 ID: ', id)
  router.push({
    // 동적 라우트로 이동
    name: 'NewsDetail',
    params: { id }
  })
}

</script>

<template>
  <div class="news-container">
    <h1 class="news-title">뉴스 기사</h1>

    <!-- 카테고리 버튼 -->
    <div class="category-buttons">
      <button
        v-for="category in newsStore.categories"
        :key="category"
        :class="{ active: category === newsStore.selectedCategory }"
        @click="newsStore.selectCategory(category)"
      >
        {{ category }}
      </button>
    </div>

    <!-- 뉴스 카드 -->
    <div class="news-grid">
      <div 
        class="news-card" 
        v-for="article in newsStore.news" 
        :key="article.article_id"
        @click="goToDetail(article.article_id)"> <!--클릭 이벤트 추가-->
        <h2 class="news-header">{{ article.title }}</h2>
        <p class="news-summary">{{ article.summary }}</p>
        <!-- <p class="news-content">{{ article.content }}</p> -->
        <div class="news-footer">
          <span class="news-category">카테고리: {{ article.category_name }}</span>
          <!-- <span class="news-writer">작성자: {{ article.writer }}</span> -->
          <span class="news-media-company">{{ article.media_company_name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 스타일 정의 (이전과 동일) */
.news-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

.news-title {
  text-align: center;
  color: #2575fc;
  font-size: 2rem;
  margin-bottom: 20px;
}

.category-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
  gap: 10px;
}

.category-buttons button {
  background: #ffffff;
  border: 2px solid #2575fc;
  color: #2575fc;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.category-buttons button.active {
  background-color: #2575fc;
  color: #ffffff;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.news-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.news-card:hover {
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 */
  transform: translateY(-5px); /* 살짝 위로 올라가는 효과 */
}

.news-header {
  font-size: 1.5rem;
  color: #2575fc;
  margin-bottom: 10px;
}

.news-content {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #888;
}
</style>
