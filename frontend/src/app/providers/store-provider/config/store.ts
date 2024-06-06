import { configureStore } from "@reduxjs/toolkit"
import { combineReducers } from "redux"
// import { categoryReducer } from "@/entities/category"
// import { authReducer } from "@/entities/auth"

export const rootReducer = combineReducers({
  // category: categoryReducer,
  // auth: authReducer,
})

const store = configureStore({
  reducer: {},
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
  devTools: true,
})

export default store

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
