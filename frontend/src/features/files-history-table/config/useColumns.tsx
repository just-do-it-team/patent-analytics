import { ColumnsType } from "antd/es/table"
import { formatDateToString } from "@/shared/config/date/date-formats"
import { FilesHistoryDataType } from "@/entities/export/model/types/exportSchema"

export const useColumns = () => {
  const filesHistoryColumns: ColumnsType<FilesHistoryDataType> = [
    {
      title: "Имя файла",
      dataIndex: "file",
      key: "file",
    },

    {
      title: "Процент",
      dataIndex: "percent",
      key: "percent",
      render: value => <span>{value} %</span>,
    },
    {
      title: "Дата загрузки",
      dataIndex: "datetime",
      key: "datetime",
      render: value => <span>{formatDateToString(value)}</span>,
    },
  ]

  return filesHistoryColumns
}
