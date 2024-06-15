import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { AnalyticsSchema } from "@/entities/analytics/model/types/analyticsSchema"
import { getAnalyticsData } from "@/entities/analytics/model/services/analyticsService"

const initialState: AnalyticsSchema = {
  analyticsData: {
    data: [],
    isLoading: false,
    error: null,
  },
}

const analyticsSlice = createSlice({
  name: "analytics",
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getAnalyticsData.pending, state => {
        state.analyticsData.isLoading = true
      })
      .addCase(getAnalyticsData.fulfilled, (state, action) => {
        state.analyticsData.data = action.payload
        state.analyticsData.isLoading = false
        state.analyticsData.error = ""
      })
      .addCase(getAnalyticsData.rejected, (state, action) => {
        state.analyticsData.isLoading = false
        state.analyticsData.error = action.payload
      })
  },
})

export const { reducer: analyticsReducer } = analyticsSlice
