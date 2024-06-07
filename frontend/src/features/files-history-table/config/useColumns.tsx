import { ColumnsType } from "antd/es/table"
import { formatDateToString } from "@/shared/config/date/date-formats"

export const useColumns = () => {
  const historyColumns: ColumnsType<any> = [
    {
      title: "Имя файла",
      dataIndex: "chn",
      key: "chn",
      width: "70%",
    },
    {
      title: "Статус",
      dataIndex: ["chstatusid", "chstatusname"],
      key: "chstatusname",
      width: "15%",
    },
    {
      title: "Дата загрузки",
      dataIndex: "dplan",
      key: "dplan",
      width: "15%",
      render: value => <span>{formatDateToString(value)}</span>,
    },
  ]

  return historyColumns
}
