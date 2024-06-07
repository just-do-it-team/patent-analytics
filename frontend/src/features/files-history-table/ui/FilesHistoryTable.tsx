import React, { memo, useState } from "react"
import { TablePaginationConfig } from "antd"
import classes from "./filesHistoryTable.module.scss"
import { useColumns } from "@/features/files-history-table/config/useColumns"
import { TableComponent } from "@/shared/ui/table"

export const FilesHistoryTable = memo(() => {
  const [page, setPage] = useState<number>(1)
  const [limit, setLimit] = useState<number>(6)
  const [total, setTotal] = useState<number>(1)
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    console.log("selectedRowKeys changed: ", newSelectedRowKeys)
    setSelectedRowKeys(newSelectedRowKeys)
  }

  const rowSelection = {
    selectedRowKeys,
    onChange: onSelectChange,
  }
  const hasSelected = selectedRowKeys.length > 0

  const historyColumns = useColumns()

  // useEffect(() => {
  //   if (selectedListSI && selectedListSI?.id)
  //     dispatch(getHistoryData({ id: selectedListSI.id, page, limit }))
  // }, [dispatch, limit, page, selectedListSI, isOpenModal])

  // useEffect(() => {
  //   if (historyData) setTotal(historyData.count)
  // }, [historyData])

  // useEffect(() => {
  //   if (historyData) {
  //     dispatch(setLastHistorySI(historyData.list[1]))
  //     dispatch(setNextHistorySI(historyData.list[0]))
  //   }
  // }, [dispatch, historyData])

  const handleTableChange = (pagination: TablePaginationConfig) => {
    // setPage(pagination.current)
    // setLimit(pagination.pageSize)
    // setTotal(historyData.count)
  }

  const onRowClick = (record: any) => () => {
    if (record) {
      // dispatch(setSelectedHistorySI(record))
    }
  }

  return (
    <div className={classes.table}>
      <TableComponent
        rowSelection={rowSelection}
        сaption={"Загруженные файлы"}
        onChange={handleTableChange}
        total={total}
        columns={historyColumns}
        dataSource={[]}
        rowKey={record => record.id}
        // rowClassName={record =>
        //   record.id === selectedHistorySI.id && "ant-table-row-selected"
        // }
        onRow={record => ({
          onClick: onRowClick(record),
        })}
      />
    </div>
  )
})
