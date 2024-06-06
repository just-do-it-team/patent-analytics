import moment from "moment"

export const USER_DATE_FORMAT = "DD.MM.YYYY"

export function formatDateToString(date: string) {
  if (!date) {
    return ""
  }
  return moment(date).format(USER_DATE_FORMAT)
}
