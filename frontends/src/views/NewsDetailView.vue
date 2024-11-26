<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user';


const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const article = ref(null)
const chatMessages = ref([
  { sender: 'chatbot', text: '안녕하세요! 이 기사에 대해 궁금한 점이 있으면 물어보세요.' },
])
const userInput = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null) // 메시지 컨테이너에 대한 참조
const likes = ref(0) // 좋아요 수 상태 관리

// API URL
const BASE_API_URL = import.meta.env.VITE_DJANGO_API_URL
const CHATBOT_API_URL = import.meta.env.VITE_CHATBOT_API_URL
const NEWS_LIKE_API_URL = import.meta.env.VITE_NEWSLIKE_API_URL

// 뉴스 데이터 가져오기
const fetchNewsDetail = async () => {
  try {
    const response = await axios.get(
      `${NEWS_LIKE_API_URL}${route.params.id}/`,
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
        },
      }
    )
    article.value = response.data
    // likes.value = response.data.likes || 0 // 초기 좋아요 수
  } catch (error) {
    console.error('Failed to fetch news detail:', error)
  }

  // 좋아요 개수 가져오기 
  try {
    const response_likes= await axios.get(
      `${NEWS_LIKE_API_URL}${route.params.id}/accounts/likes/`,
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
        },
      }
    )
    likes.value = response_likes.data.like_count
  } catch (error) {
      console.error('Failed to fetch like count:', error)
  }
}

// 자동 스크롤 함수
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 메시지 전송 함수
const sendMessage = async () => {
  if (userInput.value.trim()) {
    // 사용자 입력값 초기화 먼저 실행
    const message = userInput.value; // 입력값을 미리 저장
    userInput.value = ''; // 입력창 초기화

    // 사용자 메시지 추가
    chatMessages.value.push({ sender: 'user', text: message });
    scrollToBottom(); // 사용자 메시지 추가 후 스크롤 업데이트
    isLoading.value = true;

    // 백엔드로 질문 전송
    try {
      const response = await axios.post(
        CHATBOT_API_URL,
        {
          question: message,
          article_id: route.params.id,
        },
        {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
          },
        }
      );

      // 챗봇 응답 추가
      chatMessages.value.push({ sender: 'chatbot', text: response.data.answer });
    } catch (error) {
      chatMessages.value.push({
        sender: 'chatbot',
        text: '죄송합니다. 현재 답변을 제공할 수 없습니다.',
      });
    } finally {
      isLoading.value = false;
      scrollToBottom(); // 메시지 추가 후 스크롤 업데이트
    }
  }
};


const likeArticle = async () => {

  // 추가 구현 (로그인 상태 확인)
  if (!userStore.isLoggedIn()) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }
  try {
    const response = await axios.post(
      `${NEWS_LIKE_API_URL}${route.params.id}/accounts/like/`,
      {
        news_id: route.params.id,
      }, 
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
        },
      }
    )
    likes.value += 1
    alert(response.data.message)
  } catch (error) {
    if (error.response?.status === 400) {
      alert('이미 좋아요를 누르셨습니다.')
    } else if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      console.error('좋아요 처리 중 오류 발생:', error)
    }
  }
}

// 추가 구현 (좋아요 버튼 상태 변경)
const alreadyLiked = ref(false)

const checkIfLiked = async () => {
  try {
    const response = await axios.get(`${BASE_API_URL}/api/v1/news/${route.params.id}/accounts/is_liked/`, {
      headers: {
          Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
        },
    })
    alreadyLiked.value = response.data.is_liked
  } catch (error) {
    console.error('좋아요 상태 확인 중 오류:', error)
  }
}

onMounted(() => {
  fetchNewsDetail()  // 뉴스 상세 정보 로드
  checkIfLiked()  // 좋아요 버튼 상태
  // fetchLikeCount()  // 좋아요 개수 가져오기 

})

</script>

<template>
  <div class="page-container">
    <!-- 뉴스 기사 영역 -->
    <div class="news-container">
      <h3 class="news-header">뉴스 기사 상세보기</h3>
      
      <div v-if="article" class="news-card">
        <p><strong>카테고리</strong> | <span class="news-category">{{ article.category_name }}</span></p>
        <p><span class="news-title">{{ article.title }}</span></p>
        <p class="news-meta">
          <span>{{ article.published_date }}</span><br />
          <span>{{ article.writer }} ({{ article.media_company_name }})</span>
        </p>
        <p class="news-content">{{ article.content }}</p>
        <p class="news-keyword">{{ article.keyword }}</p>
        <!-- 좋아요 버튼 -->
        <div class="like-button-container">
          <button
            :disabled="alreadyLiked"
            @click="likeArticle"
            class="like-button"
          >
            👍 좋아요 {{ likes }}
          </button>
        </div>
      </div>

      <div v-else class="loading-message">
        <p>뉴스 데이터를 불러오는 중...</p>
      </div>
    </div>

    <!-- 챗봇 영역 -->
    <div class="chatbot-container">
      <h3 class="chatbot-title">이 기사에 대해 궁금한 점을 물어보세요!</h3>
      <div class="chatbot-messages" ref="messagesContainer">
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
  </div>
</template>

<style scoped>
/* 전체 페이지 레이아웃 */
.page-container {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
  font-family: 'Arial', sans-serif;
}

/* 뉴스 기사 영역 스타일 */
.news-container {
  flex: 2;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: auto; /* 자동 높이 */
}

/* 챗봇 영역 스타일 */
.chatbot-container {
  flex: 1;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column; /* 아래쪽 입력 영역을 고정하고 메시지 영역을 확장 */
  height: auto; /* 자동 높이 */
}

/* 공통 스타일 */
h3 {
  text-align: center;
  color: #2575fc;
  margin-bottom: 20px;
}

/* 뉴스 카드 스타일 */
.news-card {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.news-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 10px;
}

.news-meta {
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 10px;
  text-align: right;
}

.news-content {
  margin-top: 15px;
  font-size: 1rem;
  color: #444;
  text-align: justify;
}
/* 뉴스 키워드 스타일 */
.news-keyword {
  font-size: 0.9rem;
  color: #ffffff;
  font-weight: bold;
  margin-top: 15px;
  display: inline-block;
  background: linear-gradient(45deg, #2575fc, #6c63ff); /* 그라데이션 배경 */
  padding: 5px 10px;
  border-radius: 12px;
  text-transform: uppercase; /* 대문자로 변환 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  letter-spacing: 1px; /* 글자 간격 */
}

.news-keyword:hover {
  background: linear-gradient(45deg, #6c63ff, #2575fc); /* 호버 시 반전된 그라데이션 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 강조 */
  transform: scale(1.05); /* 살짝 확대 효과 */
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
}

.like-button {
  display: inline-block;
  background-color: #2575fc;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

.like-button:hover {
  background-color: #1b5ab6;
}

/* 챗봇 메시지 영역 */
.chatbot-messages {
  flex: 1; /* 남은 공간을 모두 사용 */
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chatbot-message {
  margin-bottom: 10px;
}

/* 챗봇 입력 영역 */
.chatbot-input {
  display: flex;
  gap: 10px;
}

.chatbot-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
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

