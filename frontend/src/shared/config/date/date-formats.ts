import moment, { Moment } from "moment"

export const BACKEND_FORMAT = "YYYY-MM-DD"
export const USER_DATE_FORMAT = "DD.MM.YYYY"
export const USER_DATE_FORMAT_HOURS = "DD.MM.YYYY HH:MM"

export const today = moment().format("YYYY-MM-DD")

export function formatDateToBackend(date?: string): string {
  return moment(date).format(BACKEND_FORMAT)
}

export function formatDateToString(date: string) {
  if (!date) {
    return ""
  }
  return moment(date).format(USER_DATE_FORMAT)
}

export function formatDateToStringWithHours(date: string) {
  if (!date) {
    return ""
  }
  return moment(date).format(USER_DATE_FORMAT_HOURS)
}

export function getDateToString(value: Moment[] | null) {
  return {
    startDate: value ? value[0].format(BACKEND_FORMAT) : "",
    endDate: value ? value[1].format(BACKEND_FORMAT) : "",
  }
}
