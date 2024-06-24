export type FilterHistoryDataType = {
  id?: number
  datetime?: string
  invention_bd?: boolean
  pmodels_bd?: boolean
  prom_bd?: boolean
  start_date?: string | null
  end_date?: string | null
  inn?: string | null
  okopf?: string | null
  okopf_code?: string | null
  // okfs: string | null
  // okfs_code: string | null
  file?: string
}

export type FilterHistoryDataSchema = {
  results: FilterHistoryDataType[]
  next: string | null
  previous: string | null
  count: number
}

export type ImportSchema = {
  isOpenModal: boolean
  selected: {
    data: FilterHistoryDataType | null
    isLoading: boolean
    error: string | undefined | null
  }
  filterHistory: {
    data: FilterHistoryDataSchema
    isLoading: boolean
    error: string | undefined | null
  }
  selectedFilterRow: FilterHistoryDataType | null
}
