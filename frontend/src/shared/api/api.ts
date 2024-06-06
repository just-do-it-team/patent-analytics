import axios from "axios"
import { SERVER_URL } from "@/app/config"
// import store from "@/app/providers/store-provider/config/store"

export const Endpoints = {
  AUTH: {
    LOGIN: "auth/login",
    TOKEN: "auth/token",
    REFRESH: "auth/refresh",
    LOGOUT: "auth/logout",
    PROFILE: "/userinfo",
  },
}

export const api = axios.create({
  baseURL: SERVER_URL,
})

const urlsSkipAuth = [
  Endpoints.AUTH.LOGIN,
  Endpoints.AUTH.TOKEN,
  Endpoints.AUTH.REFRESH,
]

// api.interceptors.request.use(async config => {
//   if (config.url && urlsSkipAuth.includes(config.url)) {
//     return config
//   }
//
//   // @ts-ignore
//   config.headers = {
//     ...config.headers,
//     authorization: `Bearer ${localStorage.getItem("accessToken")}`,
//   }
//
//   return config
// })

// api.interceptors.response.use(
//   config => config,
//   async error => {
//     const originalRequest = { ...error.config }
//     originalRequest._isRetry = true
//     if (
//       error.config.url.includes(SERVER_URL) &&
//       error.config &&
//       !error.config._isRetry
//     ) {
//       try {
//         await store.dispatch(refreshAccess())
//         return api.request(originalRequest)
//       } catch (error) {
//         console.log("Ошибка перехвата ошибки ответа")
//       }
//     }
//     store.dispatch(softLogout())
//     throw error
//   },
// )
