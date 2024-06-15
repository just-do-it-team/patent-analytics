import { createAsyncThunk } from "@reduxjs/toolkit"
import { AnalyticsDataType } from "@/entities/analytics/model/types/analyticsSchema"
import { message } from "antd"
import { api } from "@/shared/api/api"
import { SERVER_URL } from "@/app/config"

export const getAnalyticsData = createAsyncThunk<
  AnalyticsDataType[],
  { id: number },
  { rejectValue: string }
>("analytics/getAnalyticsData", async (data, { rejectWithValue }) => {
  try {
    const response = await api.get(`${SERVER_URL}/visualisation/?id=${data.id}`)
    return response.data
  } catch (e) {
    message.error("Не удалось загрузить данные аналитики")
    return rejectWithValue("Не удалось загрузить данные аналитики")
  }
})
