<script setup>
import { ref, onMounted } from 'vue'
import { useNewsStore } from '@/stores/news'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

// Pinia 스토어 불러오기
const newsStore = useNewsStore()
const userStore = useUserStore()
const router = useRouter()

// 로딩 상태
const isLoading = ref(true)

// 초기 데이터 로드
onMounted(async () => {
  isLoading.value = true // 로딩 시작
  await newsStore.fetchNews()
  isLoading.value = false // 로딩 완료
  console.log(newsStore.news)
})

const goToDetail = (id) => {
  if (!userStore.isLoggedIn()) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }
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

    <!-- 로딩 메시지 -->
    <div v-if="isLoading" class="loading-message">
      뉴스 카드를 로딩 중입니다...
    </div>

    <!-- 데이터 로드 완료 -->
    <div v-else>
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
          @click="goToDetail(article.article_id)"
        >
          <h2 class="news-header">{{ article.title }}</h2>
          <p class="news-summary">{{ article.summary }}</p>
          <p class="news-keyword">{{ article.keyword }}</p>
          <p class="news-date">📅 {{ article.published_date.substring(0,10) }}</p>
          <!-- 날짜를 출력하는 부분 추가 -->

          <div class="news-footer">
            <span class="news-category">카테고리: {{ article.category_name }}</span>
            <span class="news-media-company">{{ article.media_company_name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 뉴스 컨테이너 스타일 */
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

.loading-message {
  text-align: center;
  font-size: 1.5rem;
  color: #555;
  margin-top: 20px;
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
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.news-header {
  font-size: 1.5rem;
  color: #2575fc;
  margin-bottom: 10px;
}

.news-summary {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
  line-height: 1.5;
  text-overflow: ellipsis;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.news-keyword {
  font-size: 0.9rem;
  color: #2575fc;
  font-weight: bold;
  margin-bottom: 15px;
  display: inline-block;
  background: #e8f3ff;
  padding: 5px 10px;
  border-radius: 8px;
  text-transform: uppercase;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #888;
}
</style>
