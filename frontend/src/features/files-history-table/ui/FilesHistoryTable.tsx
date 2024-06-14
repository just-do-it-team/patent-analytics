import { Key, memo, useEffect, useState } from "react"
import { Button, TablePaginationConfig, Typography } from "antd"
import classes from "./filesHistoryTable.module.scss"
import { useColumns } from "@/features/files-history-table/config/useColumns"
import { TableComponent } from "@/shared/ui/table"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import {
  downloadFilesHistoryAnalytics,
  getFilesHistoryData,
} from "@/entities/export/model/services/exportServices"
import { DownloadOutlined } from "@ant-design/icons"

export const FilesHistoryTable = memo(() => {
  const dispatch = useAppDispatch()
  const { filesHistory, downloadLink } = useAppSelector(state => state.export)
  const [page, setPage] = useState<number>(1)
  const [limit, setLimit] = useState<number>(10)
  const [total, setTotal] = useState<number>(1)
  const [selectedRowKeys, setSelectedRowKeys] = useState<Key[]>([])

  const filesHistoryColumns = useColumns()

  useEffect(() => {
    dispatch(
      getFilesHistoryData({
        limit,
        page,
      }),
    )
  }, [dispatch, limit, page, downloadLink])

  useEffect(() => {
    if (filesHistory.data) setTotal(filesHistory.data.count)
  }, [filesHistory])

  const handleTableChange = (pagination: TablePaginationConfig) => {
    setPage(pagination.current!)
    setLimit(pagination.pageSize!)
    setTotal(filesHistory.data.count)
  }

  const onSelectChange = (newSelectedRowKeys: Key[]) => {
    setSelectedRowKeys(newSelectedRowKeys)
  }

  const rowSelection = {
    selectedRowKeys,
    onChange: onSelectChange,
  }

  return (
    <div className={classes.table}>
      <Typography.Title level={3} className={classes["table-title"]}>
        {"История загруженых файлов"}
      </Typography.Title>
      <div className={classes["table-controls"]}>
        <Button
          disabled={!selectedRowKeys.length}
          type={"default"}
          onClick={() =>
            dispatch(downloadFilesHistoryAnalytics({ ids: selectedRowKeys }))
          }
          icon={<DownloadOutlined />}
        >
          {selectedRowKeys.length > 1
            ? "Объединить и скачать аналитику"
            : "Скачать аналитику"}
        </Button>
      </div>
      <TableComponent
        rowSelection={rowSelection}
        onChange={handleTableChange}
        total={total}
        isLoading={filesHistory.isLoading}
        isError={!!filesHistory.error}
        columns={filesHistoryColumns}
        dataSource={filesHistory && filesHistory.data.results}
        rowKey={record => record.id}
      />
    </div>
  )
})
