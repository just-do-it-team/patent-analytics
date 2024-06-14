import { configureStore } from "@reduxjs/toolkit"
import { combineReducers } from "redux"
import { analyticsReducer } from "@/entities/analytics"
import { exportReducer } from "@/entities/export"
import { importReducer } from "@/entities/import"

export const rootReducer = combineReducers({
  analytics: analyticsReducer,
  export: exportReducer,
  import: importReducer,
})

const store = configureStore({
  reducer: rootReducer,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
  devTools: true,
})

export default store

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
