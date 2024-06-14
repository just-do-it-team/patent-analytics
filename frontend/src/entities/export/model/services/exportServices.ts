import { api } from "@/shared/api/api"
import { createAsyncThunk } from "@reduxjs/toolkit"
import { FilesHistoryDataSchema } from "@/entities/export/model/types/exportSchema"
import { SERVER_URL } from "@/app/config"
import { message } from "antd"
import store from "@/app/providers/store-provider/config/store"
import { setDownloadLink } from "@/entities/export/model/slice/exportSlice"
import { Key } from "react"

export const getFilesHistoryData = createAsyncThunk<
  FilesHistoryDataSchema,
  { limit: number; page: number },
  { rejectValue: string }
>("export/getFilesHistoryData", async (data, { rejectWithValue }) => {
  try {
    const response = await api.get(
      `${SERVER_URL}/file_history?limit=${data.limit}&offset=${(data.page - 1) * data.limit}`,
    )
    return response.data
  } catch (e) {
    message.error("Не удалось загрузить данные")
    return rejectWithValue("Не удалось загрузить данные")
  }
})

export const uploadAnalyticsFile = createAsyncThunk<
  void,
  { formData: FormData },
  { rejectValue: string }
>("export/uploadAnalyticsFile", async (data, { rejectWithValue }) => {
  try {
    message.loading({
      content: "Загрузка файла",
      key: "uploadAnalyticsFile",
      duration: 0,
    })
    const response = await api.post(`${SERVER_URL}/upload/`, data.formData)
    store.dispatch(setDownloadLink(response.data.processed_files))
    message.success({
      content: "Файл успешно загружен",
      key: "uploadAnalyticsFile",
    })
    return response.data
  } catch (e) {
    message.error({
      content: "Не удалось загрузить файл",
      key: "uploadAnalyticsFile",
    })
    return rejectWithValue("Не удалось обновить")
  }
})

export const downloadAnalyticsFile = createAsyncThunk<
  any,
  void,
  { rejectValue: string }
>("export/downloadAnalyticsFile", async (_, { rejectWithValue }) => {
  const { downloadLink } = await store.getState().export
  message.loading({
    content: "Cкачивание файла",
    key: "downloadAnalyticsFile",
    duration: 0,
  })
  try {
    const response = await fetch(`${SERVER_URL}/download/`, {
      method: "GET",
    })
    if (!response.ok) {
      message.error({
        content: "Не удалось скачать файл",
        key: "downloadAnalyticsFile",
      })
    }
    if (response.ok) {
      const blob = await response.blob()
      const href = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = href
      link.download = `${downloadLink}` || "Патентная аналитика.xlsx"
      document.body.append(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(href)
      message.success({
        content: "Файл успешно скачан",
        key: "downloadAnalyticsFile",
      })
    }
  } catch (e) {
    return rejectWithValue("Не удалось скачать")
  }
})

export const downloadFilesHistoryAnalytics = createAsyncThunk<
  any,
  { ids: Key[] },
  { rejectValue: string }
>("export/downloadFilesHistoryAnalytics", async (data, { rejectWithValue }) => {
  message.loading({
    content: "Cкачивание файла",
    key: "downloadFilesHistoryAnalytics",
    duration: 0,
  })
  try {
    const response = await fetch(`${SERVER_URL}/file_history_get_file/`, {
      method: "POST",
      body: JSON.stringify({ ids: data.ids }),
    })
    if (!response.ok) {
      message.error({
        content: "Не удалось скачать файл",
        key: "downloadFilesHistoryAnalytics",
      })
    }
    if (response.ok) {
      const blob = await response.blob()
      const href = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = href
      link.download = "Патентная аналитика.xlsx"
      document.body.append(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(href)
      message.success({
        content: "Файл успешно скачан",
        key: "downloadFilesHistoryAnalytics",
      })
    }
  } catch (e) {
    return rejectWithValue("Не удалось скачать")
  }
})
