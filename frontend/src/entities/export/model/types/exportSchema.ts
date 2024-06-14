export type FilesHistoryDataType = {
  id: string
  file: string
  datetime: string
  percent: number
}

export type FilesHistoryDataSchema = {
  results: FilesHistoryDataType[]
  next: string | null
  previous: string | null
  count: number
}

export type ExportSchema = {
  downloadLink: string | null
  filesHistory: {
    data: FilesHistoryDataSchema
    isLoading: boolean
    error: string | undefined | null
  }
}
