import { ref, computed } from 'vue'
// import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
// import { useUserStore } from './user'
import axios from 'axios'

// API URL 환경 변수 가져오기
const API_URL = import.meta.env.VITE_DJANGO_API_URL

export const useNewsStore = defineStore('news', () => {
  // const router = useRouter()
  // const userStore = useUserStore()

  const news = ref([])

  // 카테고리 목록
  const categories = ref (['전체', '정치', '경제', '사회', '생활', '세계', 'IT'])

  // 선택된 카테고리 상태 
  const selectedCategory = ref('전체')

  // 추천 뉴스 
  const recommendedNews = ref([])


  const fetchNews = async () => {
    try {
      console.log('Fetching news for category:', selectedCategory.value)
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/`,
        params: { category: selectedCategory.value },
        // headers: { 
        //   Authorization: `Token ${localStorage.getItem('token')}`
        // }
      });
      console.log(`${API_URL}/api/v1/`)
      console.log('API Response:', response.data)
      news.value = response.data
    } catch (error) {
      console.error('Failed to fetch news:', error.response || error.message)
    }
  }
  

  const selectCategory = (category) => {
    console.log('Selected category:', category)
    selectedCategory.value = category
    fetchNews() // API 호출
  }

  const fetchRecommendedNews = async () => {
    try {
      const response = await axios.get('/api/v1/recommended-news/', {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      });
      recommendedNews.value = response.data;
    } catch (error) {
      console.error('추천 뉴스 가져오기 실패:', error);
    }
  };

  return { news, selectedCategory, categories, fetchNews, selectCategory, fetchRecommendedNews}
})
