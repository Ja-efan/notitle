import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
// useRouter: 특정 경로로 보낼 때
// useRoute: 받을 때
import { useRouter, useRoute } from 'vue-router'

const LOGIN_API_URL = import.meta.env.VITE_LOGIN_API_URL;
const USERINFO_API_URL = import.meta.env.VITE_USERINFO_API_URL;
const REGIST_API_URL = import.meta.env.VITE_REGISTRATION_API_URL;


export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  const token = ref(null)
  const loginUsername = ref(null)

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
      // logIn({ username, password: password1 })
    })
    .catch((error) => {
      console.log(error)
    })
  }

  return { token, loginUsername, login, regist }
}, { persist: true })
