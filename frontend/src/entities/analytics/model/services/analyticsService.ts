import { createAsyncThunk } from "@reduxjs/toolkit"
import { message } from "antd"
import { api, Endpoints } from "@/shared/api/api"

// export const getStatisticData = createAsyncThunk<
//   StatisticDataType[],
//   void,
//   { rejectValue: string }
// >("analytics/getStatisticData", async (_, { rejectWithValue }) => {
//   try {
//     const response = await api.get(Endpoints.METHODS.STATISTIC)
//     return response.data
//   } catch (e) {
//     message.error("Не удалось загрузить cтатистику")
//     return rejectWithValue("Не удалось загрузить cтатистику")
//   }
// })
//
// export const getAnalyticsData = createAsyncThunk<
//   AnalyticsDataType[],
//   void,
//   { rejectValue: string }
// >("analytics/getAnalyticsData", async (_, { rejectWithValue }) => {
//   try {
//     const response = await api.get(Endpoints.METHODS.MAIN)
//     return response.data
//   } catch (e) {
//     message.error("Не удалось загрузить данные аналитики")
//     return rejectWithValue("Не удалось загрузить данные аналитики")
//   }
// })
//
// export const getAdvancedData = createAsyncThunk<
//   AnalyticsDataType[],
//   { startDate: string; endDate: string; server: string },
//   { rejectValue: string }
// >("analytics/getAdvancedData", async (data, { rejectWithValue }) => {
//   try {
//     const response = await api.get(
//       `${Endpoints.METHODS.ADVANCED}/?d1=${data.startDate}&d2=${data.endDate}&srv=${data.server}`,
//     )
//     return response.data
//   } catch (e) {
//     message.error("Не удалось загрузить данные аналитики")
//     return rejectWithValue("Не удалось загрузить данные аналитики")
//   }
// })
