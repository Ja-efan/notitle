<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user';


// Chart.js 등록
Chart.register(...registerables);

const userStore = useUserStore

// State variables
const recommendedNews = ref([]);
const likedNewsAnalysis = ref(null);
const isLoading = ref(false);
const errorMessage = ref('');
const router = useRouter()

const NEWS_RECO_API_URL = import.meta.env.VITE_NEWS_RECO_API_URL;

// 차트 생성 함수
const createCategoryChart = (categoriesDistribution) => {
  const ctx = document.getElementById('categoryChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: categoriesDistribution.map((item) => item.category__category_name),
      datasets: [
        {
          label: '좋아요 개수',
          data: categoriesDistribution.map((item) => item.count),
          backgroundColor: 'rgba(37, 117, 252, 0.6)',
          borderColor: 'rgba(37, 117, 252, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
    },
  });
};

const createSentimentChart = (sentimentDistribution) => {
  const ctx = document.getElementById('sentimentChart').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['긍정', '중립', '부정'],
      datasets: [
        {
          data: [
            sentimentDistribution.positive,
            sentimentDistribution.neutral,
            sentimentDistribution.negative,
          ],
          backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(255, 99, 132, 0.6)'],
          borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(255, 99, 132, 1)'],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
      },
    },
  });
};

// API 호출
const fetchRecommendedNews = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(NEWS_RECO_API_URL, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });

    recommendedNews.value = response.data.recommended_news;
    likedNewsAnalysis.value = response.data.liked_news_analysis;

    // 차트 생성
    if (likedNewsAnalysis.value) {
      // nextTick을 사용해 DOM이 렌더링된 후 차트를 생성
      nextTick(() => {
        createCategoryChart(likedNewsAnalysis.value.categories_distribution);
        createSentimentChart(likedNewsAnalysis.value.sentiment_distribution);
      });
    }
  } catch (error) {
    errorMessage.value =
      error.response?.data?.detail || '추천 뉴스를 불러오는 데 실패했습니다.';
    console.error('Error fetching recommended news:', error);
  } finally {
    isLoading.value = false;
  }
};

const goToScrap = () => {
  router.push('/scrap'); // 좋아요 기사 페이지 이동
};

// 컴포넌트 마운트 시 API 호출
onMounted(() => {
  fetchRecommendedNews();
});
</script>

<template>
  <div class="tailored-news-container">
    <h1>맞춤 늬-우스</h1>
    <button @click="goToScrap" class="scrap-button">좋아요한 뉴스 보기</button>
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading">
      데이터를 불러오는 중입니다...
    </div>

    <!-- 에러 메시지 -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>

    <!-- 좋아요 분석 정보 -->
    <div v-if="likedNewsAnalysis" class="liked-analysis">
      <h2>좋아요 누른 뉴스 분석</h2>
      <p>총 좋아요 개수: {{ likedNewsAnalysis.total_liked }}</p>

      <div>
        <h3>카테고리별 좋아요 분포</h3>
        <canvas id="categoryChart"></canvas>
      </div>

      <div>
        <h3>감성 분포</h3>
        <canvas id="sentimentChart"></canvas>
      </div>
    </div>

    <!-- 추천 뉴스 리스트 -->
    <div v-if="recommendedNews.length > 0" class="news-list">
      <h2>추천 뉴스</h2>
      <div class="news-item" v-for="news in recommendedNews" :key="news.id">
        <h2 class="news-title">{{ news.title }}</h2>
        <p class="news-summary">{{ news.summary }}</p>
        <p class="news-category">
          카테고리: {{ news.category_name || '알 수 없음' }}
        </p>
        <a :href="news.url" target="_blank" class="news-link">
          기사 읽기
        </a>
      </div>
    </div>

    <!-- 추천 뉴스 없음 -->
    <div v-else-if="!isLoading" class="no-news">
      추천 뉴스가 없습니다.
    </div>
  </div>
</template>

<style scoped>
.tailored-news-container {
  max-width: 800px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.loading,
.error,
.no-news {
  text-align: center;
  font-size: 1.2rem;
  margin: 20px 0;
  color: #666;
}

.scrap-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}
.scrap-button:hover {
  background-color: #388e3c;
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

.news-title {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #2575fc;
}

.news-summary {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #333;
}

.news-category {
  font-size: 0.9rem;
  margin-bottom: 10px;
  color: #666;
}

.news-link {
  text-decoration: none;
  font-weight: bold;
  color: #4caf50;
}

.news-link:hover {
  text-decoration: underline;
  color: #388e3c;
}

.liked-analysis h2,
.news-list h2 {
  color: #2575fc;
}
</style>
