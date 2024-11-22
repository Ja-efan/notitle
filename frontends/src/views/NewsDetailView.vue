<template>
  <div class="detail-container">
    <h3 class="detail-header">뉴스 상세보기</h3>
    <div v-if="article" class="detail-card">
      <p>
        <strong>카테고리</strong> | 
        <span class="detail-category">{{ article.category_name }}</span>
      </p>
      <p>
          <span class="detail-title">{{ article.title }}</span>
      </p>
      <p class="detail-meta">
        <span>{{ article.published_date }}</span>
        <br>
        <span>{{ article.writer }} ({{ article.media_company_name }})</span>
      </p>

      <p class="detail-content">{{ article.content }}</p>
    </div>
    <div v-else class="loading-message">
      <p>뉴스 데이터를 불러오는 중...</p>
    </div>
  </div>

   <!-- 챗봇 영역 -->
   <div class="chatbot-container">
      <h3 class="chatbot-title">이 기사에 대해 궁금한 점을 물어보세요!</h3>
      <div class="chatbot-messages">
        <div v-for="(message, index) in chatMessages" :key="index" class="chatbot-message">
          <p><strong>{{ message.sender }}:</strong> {{ message.text }}</p>
        </div>
      </div>
      <div class="chatbot-input">
        <input
          type="text"
          v-model="userInput"
          placeholder="여기에 질문을 입력하세요..."
          @keydown.enter="sendMessage"
        />
        <button @click="sendMessage">전송</button>
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
    const response = await axios.get(`${API_URL}/api/v1/news/${route.params.id}/`) // ID로 API 호출
    article.value = response.data
  } catch (error) {
    console.error('Failed to fetch news detail:', error)
  }
}

// 기본 메시지 
const chatMessages = ref([
  { sender: 'chabot', text: '안녕하세요! 이 기사에 대해 궁금한 점이 있으면 물어보세요.'}, 
])

const userInput = ref("")

//  메시지 전송 함수 
const sendMessage = () => {
  if (userInput.value.trim()) {
    // 사용자 메시지 추가 
    chatMessages.value.push({ sender: 'user', text: userInput.value })

    // 챗봇 응답 추가 ( 예제: 간단한 자동 응답)
    setTimeout(() => {
      chatMessages.value.push({
        sender: "chatbot",
        text: "죄송합니다. 아직 이 질문에 대한 답변을 준비 중입니다.",
      })
    }, 1000)

    // 사용자 입력 필드 초기화 
    userInput.value = ''
  }
}
onMounted(() => {
  fetchNewsDetail()
})
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.detail-container {
  max-width: 800px; /* 중앙에 적당한 크기의 컨테이너 */
  margin: 20px auto; /* 수직 및 수평 중앙 정렬 */
  padding: 20px;
  font-family: 'Arial', sans-serif; /* 읽기 쉬운 폰트 설정 */
  background-color: #f9f9f9; /* 연한 배경색 */
  border-radius: 8px; /* 둥근 모서리 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  color: #333;
}

/* 제목 스타일 */
.detail-header {
  text-align: center; /* 중앙 정렬 */
  color: #2575fc; /* 브랜드 컬러 */
  font-size: 2rem; /* 적당히 큰 제목 크기 */
  margin-bottom: 20px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); /* 약간의 텍스트 그림자 */
}

/* 기사 날짜 스타일 */
.detail-date {
  font-size: 0.85rem; /* 글자 크기를 작게 */
  color: #999; /* 연한 색상 */
  margin-bottom: 10px; /* 아래쪽 여백 추가 */
  display: block; /* 날짜를 블록 형태로 */
  text-align: right; /* 날짜를 오른쪽 정렬 */
}

/* 상세 카드 스타일 */
.detail-card {
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  font-size: 1rem;
  line-height: 1.6; /* 텍스트 줄 간격 */
  color: #555; /* 중간 밝기의 텍스트 색상 */
}

/* 카테고리 텍스트 스타일 */
.detail-category {
  font-weight: bold;
  color: #2575fc; /* 카테고리 강조 색상 */
}

/* 제목 텍스트 스타일 */
.detail-title {
  font-size: 1.5rem; /* 큰 텍스트 크기 */
  color: #333; /* 제목은 기본 텍스트 색상 */
  margin-bottom: 10px;
  display: block; /* 블록 형태로 보여줌 */
}

/* 작성자 텍스트 스타일 */
.detail-writer {
  font-style: italic; /* 이탤릭체로 스타일링 */
  color: #888; /* 중간 밝기의 회색 */
  text-align: right;
}

/* 기사 메타 정보 (날짜 + 작성자) 스타일 */
.detail-meta {
  font-size: 0.85rem; /* 작은 글씨 크기 */
  color: #999; /* 연한 색상 */
  margin-bottom: 10px; /* 아래쪽 여백 */
  display: block; /* 블록 형태 */
  text-align: right; /* 오른쪽 정렬 */
}
/* 본문 텍스트 스타일 */
.detail-content {
  margin-top: 15px;
  font-size: 1rem;
  color: #444; /* 약간 어두운 본문 색상 */
  text-align: justify; /* 텍스트 양쪽 정렬 */
}

/* 로딩 메시지 스타일 */
.loading-message {
  text-align: center;
  color: #999;
  font-size: 1.2rem;
  font-style: italic;
}

/* 챗봇 컨테이너 스타일 */
.chatbot-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 챗봇 제목 스타일 */
.chatbot-title {
  font-size: 1.5rem;
  color: #2575fc;
  margin-bottom: 20px;
  text-align: center;
}

/* 챗봇 메시지 영역 스타일 */
.chatbot-messages {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chatbot-message {
  margin-bottom: 10px;
}

/* 챗봇 입력 영역 스타일 */
.chatbot-input {
  display: flex;
  gap: 10px;
}

.chatbot-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
}

.chatbot-input input:focus {
  border-color: #2575fc;
}

.chatbot-input button {
  padding: 10px 20px;
  background-color: #2575fc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chatbot-input button:hover {
  background-color: #1b5ab6;
}
</style>
