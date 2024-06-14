import { memo } from "react"
import { Table, TableProps } from "antd"
import classes from "./tableComponent.module.scss"

export type TableComponentProps = {
  isLoading?: boolean
  isError?: boolean
  total: number
}

export const TableComponent = memo(
  (props: TableComponentProps & TableProps) => {
    const { total, columns, dataSource, isLoading, isError, ...rest } = props

    // if (isError) {
    //   return <FetchError />
    // }

    return (
      <>
        <Table
          scroll={{ x: "max-content", scrollToFirstRowOnChange: false }}
          className={classes.table}
          columns={columns}
          dataSource={dataSource}
          loading={isLoading}
          pagination={{
            defaultPageSize: 10,
            pageSizeOptions: ["10", "15", "20"],
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
