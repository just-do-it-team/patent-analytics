import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { AnalyticsSchema } from "@/entities/analytics/model/types/analyticsSchema"

const initialState: AnalyticsSchema = {
  activeTab: "1",
}

const analyticsSlice = createSlice({
  name: "analytics",
  initialState,
  reducers: {
    setActiveTab(state, action: PayloadAction<string>) {
      state.activeTab = action.payload
    },
  },
})

export const { setActiveTab } = analyticsSlice.actions
export const { reducer: analyticsReducer } = analyticsSlice
