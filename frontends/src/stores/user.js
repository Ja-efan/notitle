import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const LOGIN_API_URL = import.meta.env.VITE_LOGIN_API_URL;
const USERINFO_API_URL = import.meta.env.VITE_USERINFO_API_URL;
const REGIST_API_URL = import.meta.env.VITE_REGISTRATION_API_URL;

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const token = ref(null)
  const loginUsername = ref(null)

  const isLoggedIn = () => {
    return !!token.value // 토큰이 있으면 로그인 상태로 간주
  }

  const login = async function (payload) {
    const { username, password } = payload
  
    try {
      const response = await axios({
        method: 'post',
        url: LOGIN_API_URL,
        data: {
          username,
          password
        }
      })
  
      console.log("response = ", response)
      token.value = response.data.key // 토큰 저장
      loginUsername.value = username // 사용자 이름 저장
      return response // 비동기 결과 반환
    } catch (error) {
      console.error("error = ", error)
      throw error // 에러를 호출한 곳으로 전달
    }
  }

  const regist = function (payload) {
    const { username, email, password1, password2 } = payload

    axios({
      method: 'post',
      url: REGIST_API_URL,
      data: {
        username,
        email,
        password1,
        password2
      }
    }).then((response) => {
      alert('회원가입 성공! 로그인 페이지로 이동합니다.')
      router.push('/login')
    })
    .catch((error) => {
      console.log(error)
    })
  }

  const logout = async function () {
    try {
      token.value = null // 토큰 초기화
      loginUsername.value = null // 사용자 이름 초기화
      localStorage.removeItem('token') // 로컬스토리지에서 토큰 삭제
      alert('로그아웃 되었습니다.')
      router.push('/login') // 로그아웃 후 로그인 페이지로 이동
    } catch (error) {
      console.error('로그아웃 실패:', error)
    }
  }

  return { token, isLoggedIn, loginUsername, login, regist, logout }
}, {
  persist: {
    enabled: true, // persist 활성화
    strategies: [
      {
        key: 'user', // 로컬 스토리지에 저장될 키 이름
        storage: localStorage, // 저장소: localStorage
      }
    ],
  },
})