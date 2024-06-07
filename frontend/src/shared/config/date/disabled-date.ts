import moment from "moment"

export function disabledPeriodDate(current: any) {
  return current && current > moment().add(1, "d").startOf("day")
}
