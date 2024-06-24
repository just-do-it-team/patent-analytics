import { ColumnsType } from "antd/es/table"
import { formatDateToString } from "@/shared/config/date/date-formats"
import { FilterHistoryDataType } from "@/entities/import/model/types/importSchema"

export const useColumns = () => {
  const filterHistoryColumns: ColumnsType<FilterHistoryDataType> = [
    {
      title: "ИНН",
      dataIndex: "inn",
      key: "inn",
      width: "20%",
      ellipsis: true,

      onCell: () => {
        return {
          style: {
            whiteSpace: "nowrap",
            maxWidth: 20,
          },
        }
      },
      render: inn => <span>{inn ? inn : "-"}</span>,
    },
    {
      title: "ОКОПФ расшифровки",
      dataIndex: "okopf",
      key: "okopf",
      width: "25%",
      onCell: () => {
        return {
          style: {
            whiteSpace: "nowrap",
            maxWidth: 25,
          },
        }
      },
      render: okopf => <span>{okopf ? okopf : "-"}</span>,
    },
    {
      title: "ОКОПФ коды",
      dataIndex: "okopf_code",
      key: "okopf_code",
      width: "25%",
      ellipsis: true,
      onCell: () => {
        return {
          style: {
            whiteSpace: "nowrap",
            maxWidth: 25,
          },
        }
      },
      render: okopf_code => <span>{okopf_code ? okopf_code : "-"}</span>,
    },
    // {
    //   title: "ОКФС расшифровки",
    //   dataIndex: "okfs",
    //   key: "okfs",
    //   width: "20%",
    //   ellipsis: true,
    //   onCell: () => {
    //     return {
    //       style: {
    //         whiteSpace: "nowrap",
    //         maxWidth: 20,
    //       },
    //     }
    //   },
    //   render: okfs => <span>{okfs ? okfs : "-"}</span>,
    // },
    // {
    //   title: "ОКФС коды",
    //   dataIndex: "okfs_code",
    //   key: "okfs_code",
    //   width: "10%",
    //   ellipsis: true,
    //   onCell: () => {
    //     return {
    //       style: {
    //         whiteSpace: "nowrap",
    //         maxWidth: 10,
    //       },
    //     }
    //   },
    //   render: okfs_code => <span>{okfs_code ? okfs_code : "-"}</span>,
    // },
    {
      title: "С даты",
      dataIndex: "start_date",
      key: "start_date",
      width: "10%",
      ellipsis: true,
      render: value => <span>{formatDateToString(value)}</span>,
    },
    {
      title: "По дату",
      dataIndex: "end_date",
      key: "end_date",
      width: "10%",
      ellipsis: true,
      render: value => <span>{formatDateToString(value)}</span>,
    },
    {
      title: "Дата создания",
      dataIndex: "datetime",
      key: "datetime",
      width: "10%",
      ellipsis: true,
      render: value => <span>{formatDateToString(value)}</span>,
    },
  ]

  return filterHistoryColumns
}
