export type AnalyticsDataType = {
  time: string
  sum: string
}

export type AnalyticsSchema = {
  analyticsData: {
    data: AnalyticsDataType[]
    isLoading: boolean
    error: string | undefined | null
  }
}
