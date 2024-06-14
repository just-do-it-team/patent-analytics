import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { ExportSchema } from "@/entities/export/model/types/exportSchema"
import { getFilesHistoryData } from "@/entities/export/model/services/exportServices"

const initialState: ExportSchema = {
  downloadLink: null,
  filesHistory: {
    data: {
      results: [],
      next: null,
      previous: null,
      count: 0,
    },
    isLoading: false,
    error: null,
  },
}

const exportSlice = createSlice({
  name: "export",
  initialState,
  reducers: {
    setDownloadLink(state, action: PayloadAction<string | null>) {
      state.downloadLink = action.payload
    },
  },
  extraReducers: builder => {
    builder
      .addCase(getFilesHistoryData.pending, state => {
        state.filesHistory.isLoading = true
      })
      .addCase(getFilesHistoryData.fulfilled, (state, action) => {
        state.filesHistory.data = action.payload
        state.filesHistory.isLoading = false
        state.filesHistory.error = ""
      })
      .addCase(getFilesHistoryData.rejected, (state, action) => {
        state.filesHistory.isLoading = false
        state.filesHistory.error = action.payload
      })
  },
})

export const { setDownloadLink } = exportSlice.actions
export const { reducer: exportReducer } = exportSlice
