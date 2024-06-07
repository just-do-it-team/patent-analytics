import moment from "moment"

export const USER_DATE_FORMAT = "DD.MM.YYYY"
export const USER_DATE_TIME_FORMAT = "DD.MM.YYYY HH:mm:ss"
export const USER_DATE_TIME_FORMAT_MIN = "DD.MM.YYYY HH:mm"
export const USER_TIME_FORMAT = "HH:mm"
export const DAY_MONTH_FORMAT = "dddd, D MMMM"
export const DAY_MONTH_YEAR_FORMAT = "D MMMM YYYY"
export const MONTH_FORMAT = "D MMMM"
export const BACKEND_DATE_FORMAT = "YYYY-MM-DD"

export const today = moment().format("YYYY-MM-DD")

export const currentDay = [
  moment().subtract(1, "d").format("YYYY-MM-DD"),
  moment().format("YYYY-MM-DD"),
]

export const currentWeek = [
  moment().subtract(1, "w").format("YYYY-MM-DD"),
  today,
]

export const currentMonth = [
  moment().subtract(1, "M").format("YYYY-MM-DD"),
  today,
]

export function formatDateToString(date: string) {
  if (!date) {
    return ""
  }
  return moment(date).format(USER_DATE_FORMAT)
}
