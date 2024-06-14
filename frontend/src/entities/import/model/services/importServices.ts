import { api } from "@/shared/api/api"
import { createAsyncThunk } from "@reduxjs/toolkit"
import { SERVER_URL } from "@/app/config"
import { message } from "antd"
import {
  FilterHistoryDataSchema,
  FilterHistoryDataType,
} from "@/entities/import/model/types/importSchema"
import store from "@/app/providers/store-provider/config/store"
import { formatDateToStringWithHours } from "@/shared/config/date/date-formats"

export const getReportAll = createAsyncThunk<
  any,
  void,
  { rejectValue: string }
>("import/getReportAll", async (_, { rejectWithValue }) => {
  message.loading({
    content: "Cкачивание файла",
    key: "getReportAll",
    duration: 0,
  })
  try {
    const response = await fetch(`${SERVER_URL}/full_report/`, {
      method: "GET",
    })
    if (!response.ok) {
      message.error({
        content: "Не удалось скачать файл",
        key: "getReportAll",
      })
    }
    if (response.ok) {
      const blob = await response.blob()
      const href = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = href
      link.download = `Вся база патентов.zip`
      document.body.append(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(href)
      message.success({
        content: "Файл успешно скачан",
        key: "getReportAll",
      })
    }
  } catch (e) {
    return rejectWithValue("Не удалось скачать файл")
  }
})

export const getReport = createAsyncThunk<
  any,
  { upload: FilterHistoryDataType },
  { rejectValue: string }
>("import/getReport", async (data, { rejectWithValue }) => {
  message.loading({
    content: "Cкачивание файла",
    key: "getReport",
    duration: 0,
  })
  try {
    const response = await fetch(`${SERVER_URL}/report/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data.upload),
    })
    if (!response.ok) {
      const res = await response.json()
      message.error({
        content: res.error,
        key: "getReport",
      })
    }
    if (response.ok) {
      const blob = await response.blob()
      const href = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = href
      link.download = `Отчет.xlsx`
      document.body.append(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(href)
      message.success({
        content: "Файл успешно скачан",
        key: "getReport",
      })
    }
  } catch (e) {
    message.error({
      content: "Не удалось скачать файл",
      key: "getReport",
    })
    return rejectWithValue("Не удалось скачать файл")
  }
})

export const getFilterHistoryData = createAsyncThunk<
  FilterHistoryDataSchema,
  { limit: number; page: number },
  { rejectValue: string }
>("import/getFilterHistoryData", async (data, { rejectWithValue }) => {
  try {
    const response = await api.get(
      `${SERVER_URL}/filter_history?limit=${data.limit}&offset=${(data.page - 1) * data.limit}`,
    )
    return response.data
  } catch (e) {
    message.error("Не удалось загрузить данные")
    return rejectWithValue("Не удалось загрузить данные")
  }
})

export const getSelectedData = createAsyncThunk<
  FilterHistoryDataType,
  { id: number },
  { rejectValue: string }
>("import/getSelectedData", async (data, { rejectWithValue }) => {
  try {
    const response = await api.get(
      `${SERVER_URL}/filter_history_view?id=${data.id}`,
    )
    return response.data
  } catch (e) {
    message.error("Не удалось загрузить данные")
    return rejectWithValue("Не удалось загрузить данные")
  }
})

export const downloadFilterHistoryReport = createAsyncThunk<
  any,
  number,
  { rejectValue: string }
>("import/downloadFilterHistoryReport", async (id, { rejectWithValue }) => {
  const { selected } = await store.getState().import
  message.loading({
    content: "Cкачивание файла",
    key: "downloadFilterHistoryReport",
    duration: 0,
  })
  try {
    const response = await fetch(
      `${SERVER_URL}/filter_history_report?id=${id}`,
      {
        method: "GET",
      },
    )
    if (!response.ok) {
      message.error({
        content: "Не удалось скачать файл",
        key: "downloadFilterHistoryReport",
      })
    }
    if (response.ok) {
      const blob = await response.blob()
      const href = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = href
      link.download = `Отчет от ${formatDateToStringWithHours(selected.data?.datetime!)}.xlsx`
      document.body.append(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(href)
      message.success({
        content: "Файл успешно скачан",
        key: "downloadFilterHistoryReport",
      })
    }
  } catch (e) {
    return rejectWithValue("Не удалось скачать файл")
  }
})
