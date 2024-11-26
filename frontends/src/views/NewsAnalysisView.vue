<script setup>
import { onMounted } from 'vue'
import { useAnalysisStore } from '@/stores/analysis'
import { Chart, registerables } from 'chart.js'

// Pinia 스토어 불러오기
const analysisStore = useAnalysisStore()

// Chart.js 등록
Chart.register(...registerables)

// 차트 생성 함수
const createCategoryChart = (data) => {
  const ctx = document.getElementById('categoryChart').getContext('2d')
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map((item) => item.category__category_name),
      datasets: [
        {
          label: '기사 수',
          data: data.map((item) => item.count),
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
  })
}

const createTopAuthorsChart = (data) => {
  const ctx = document.getElementById('authorsChart').getContext('2d')
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map((item) => item.writer),
      datasets: [
        {
          label: '기사 수',
          data: data.map((item) => item.count),
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255, 99, 132, 1)',
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
  })
}

const createSentimentChart = (sentimentData) => {
  const ctx = document.getElementById('sentimentChart').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['긍정', '중립', '부정'], // 카테고리 라벨
      datasets: [
        {
          data: [sentimentData.positive, sentimentData.neutral, sentimentData.negative], // 데이터 값
          backgroundColor: [
            'rgba(75, 192, 192, 0.6)', // 긍정: 초록색
            'rgba(255, 206, 86, 0.6)', // 중립: 노란색
            'rgba(255, 99, 132, 0.6)', // 부정: 빨간색
          ],
          borderColor: [
            'rgba(75, 192, 192, 1)', // 긍정 경계
            'rgba(255, 206, 86, 1)', // 중립 경계
            'rgba(255, 99, 132, 1)', // 부정 경계
          ],
          borderWidth: 1, // 경계 두께
        },
      ],
    },
    options: {
      responsive: true, // 반응형 설정
      plugins: {
        legend: { position: 'bottom' }, // 범례 위치
        tooltip: { enabled: true }, // 툴팁 활성화
      },
    },
  });
};

onMounted(() => {
  analysisStore.fetchAnalysisData().then(() => {
    const { category_distribution, sentiment_distribution, top_authors, wordcloud } = analysisStore.analysisData
    createCategoryChart(category_distribution)
    createSentimentChart(sentiment_distribution)
    createTopAuthorsChart(top_authors)
    // console.log(wordcloud)
  })
})
</script>

<template>
  <div class="analysis-container">
    <h1>뉴스 데이터 분석</h1>

    <!-- 로딩 표시 -->
    <div v-if="analysisStore.loading">데이터를 로드 중입니다...</div>

    <!-- 오류 표시 -->
    <div v-if="analysisStore.error" class="error">{{ analysisStore.error }}</div>

    <!-- 분석 데이터 -->
    <div v-if="analysisStore.analysisData" class="analysis-data">
      <h2>총 뉴스 기사 수: {{ analysisStore.analysisData.total_articles }}</h2>

      <!-- 감성 점수 차트 -->
      <div>
        <h3>감성 점수 분포</h3>
        <canvas id="sentimentChart"></canvas>
      </div>

      <!-- 카테고리 분포 차트 -->
      <div>
        <h3>카테고리별 기사 분포</h3>
        <canvas id="categoryChart"></canvas>
      </div>

    
      <!-- 워드 클라우드 -->
      <div>
        <h3>상위 키워드 워드 클라우드</h3>
        <div class="wordcloud">
          <img
            v-if="analysisStore.analysisData.wordcloud"
            :src="'data:image/png;base64,' + analysisStore.analysisData.wordcloud"
            alt="워드 클라우드"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analysis-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

h1, h2, h3 {
  color: #2575fc;
}

.error {
  color: red;
}

canvas {
  max-width: 100%;
  margin: 20px 0;
}

.wordcloud {
  text-align: center;
  margin-top: 20px;
}

.wordcloud img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>
