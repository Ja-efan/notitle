// django 의 urls.py 역할
// 사용자가 특정 경로로 들어오면, 
// 해당하는 컴포넌트(페이지)를 출력해줄 수 있도록 설정해주는 파일
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import NewsDetailView from '@/views/NewsDetailView.vue'
import NewsAnalysisView from '@/views/NewsAnalysisView.vue'
// import BoardCreateView from '@/views/BoardCreateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/news-analysis',
      name: 'NewsAnalysis',
      component: NewsAnalysisView,
      meta: {requiresAuth: true}, // 로그인 필요
    },
    {
      path: '/news/:id', // 동적 라우트 
      name: 'NewsDetail',
      component: NewsDetailView,
      props: true // ID를 props로 전달
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    // {
    //   path: '/create-board',
    //   name: 'createBorad',
    //   component: BoardCreateView,
    // },
  ],
})

// 네비게이션 가드
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token'); // 토큰 확인
    if (!token) {
      alert('로그인이 필요합니다.');
      next('/login'); // 로그인 페이지로 리디렉션
    } else {
      next(); // 인증된 경우 정상 이동
    }
  } else {
    next(); // 인증이 필요 없는 페이지는 자유롭게 접근
  }
});


export default router
