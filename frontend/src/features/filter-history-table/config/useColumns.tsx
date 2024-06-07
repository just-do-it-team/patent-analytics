import { ColumnsType } from "antd/es/table"
import { formatDateToString } from "@/shared/config/date/date-formats"

export const useColumns = () => {
  const historyColumns: ColumnsType<any> = [
    {
      title: "ИНН",
      dataIndex: "tin",
      key: "tin",
      width: "40%",
    },
    {
      title: "Номера патентов",
      dataIndex: "numbers",
      key: "numbers",
      width: "40%",
    },
    {
      title: "Дата",
      dataIndex: "dateRange",
      key: "dateRange",
      width: "20%",
      render: value => <span>{formatDateToString(value)}</span>,
    },
  ]

  return historyColumns
}
