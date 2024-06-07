import { memo } from "react"
import { Table, TableProps, Typography } from "antd"
import classes from "./tableComponent.module.scss"
import { FetchError } from "@/features/fetch-error"

export type TableComponentProps = {
  сaption?: string
  isLoading?: boolean
  isError?: boolean
  total: number
}

export const TableComponent = memo(
  (props: TableComponentProps & TableProps<any>) => {
    const { total, сaption, columns, dataSource, isLoading, isError, ...rest } =
      props

    if (isError) {
      return <FetchError />
    }

    return (
      <>
        <Typography.Title level={4} className={classes["table-title"]}>
          {сaption}
        </Typography.Title>
        <Table
          scroll={{ x: "max-content", scrollToFirstRowOnChange: false }}
          className={classes.table}
          columns={columns}
          dataSource={dataSource}
          loading={isLoading}
          pagination={{
            defaultPageSize: 6,
            pageSizeOptions: ["6", "10", "25", "50"],
            position: ["bottomLeft"],
            showSizeChanger: true,
            total,
          }}
          {...rest}
        />
      </>
    )
  },
)
