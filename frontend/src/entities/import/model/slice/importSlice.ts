import { createSlice } from "@reduxjs/toolkit"
import { ImportSchema } from "@/entities/import/model/types/importSchema"
import {
  getFilterHistoryData,
  getSelectedData,
} from "@/entities/import/model/services/importServices"

const initialState: ImportSchema = {
  isOpenModal: false,
  selected: {
    data: null,
    isLoading: false,
    error: null,
  },
  filterHistory: {
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

const imoprtSlice = createSlice({
  name: "import",
  initialState,
  reducers: {
    openModal(state = initialState) {
      state.isOpenModal = true
    },
    closeModal(state = initialState) {
      state.isOpenModal = false
    },
  },
  extraReducers: builder => {
    builder
      .addCase(getFilterHistoryData.pending, state => {
        state.filterHistory.isLoading = true
      })
      .addCase(getFilterHistoryData.fulfilled, (state, action) => {
        state.filterHistory.data = action.payload
        state.filterHistory.isLoading = false
        state.filterHistory.error = ""
      })
      .addCase(getFilterHistoryData.rejected, (state, action) => {
        state.filterHistory.isLoading = false
        state.filterHistory.error = action.payload
      })
      .addCase(getSelectedData.pending, state => {
        state.selected.isLoading = true
      })
      .addCase(getSelectedData.fulfilled, (state, action) => {
        state.selected.data = action.payload
        state.selected.isLoading = false
        state.selected.error = ""
      })
      .addCase(getSelectedData.rejected, (state, action) => {
        state.selected.isLoading = false
        state.selected.error = action.payload
      })
  },
})

export const { openModal, closeModal } = imoprtSlice.actions
export const { reducer: importReducer } = imoprtSlice
