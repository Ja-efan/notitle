import { defineStore } from 'pinia'
import axios from 'axios'

// API URL 환경 변수 가져오기
const ANALYSIS_API_URL = import.meta.env.VITE_ANALYSIS_API_URL

export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    analysisData: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchAnalysisData() {
      this.loading = true; // 로딩 상태 시작
      this.error = null; // 에러 초기화
      try {
        console.log("요청 URL: ", ANALYSIS_API_URL);
        const response = await axios.get(
          ANALYSIS_API_URL,
          {
            headers: {
              Authorization: `Token ${localStorage.getItem('token')}`, // dj-rest-auth 토큰 사용
            },
          }
        ); // API 엔드포인트
        this.analysisData = response.data;
        console.log(response.data)
      } catch (error) {
        // this.analysisData = null; // 기존 데이터를 초기화
        this.error = '데이터를 가져오는 데 실패했습니다.';
      } finally {
        this.loading = false; // 로딩 상태 종료
      }
    }
    ,
  },
})
