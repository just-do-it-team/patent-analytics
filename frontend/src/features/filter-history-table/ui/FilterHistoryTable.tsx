import { memo, useEffect, useState } from "react"
import { TablePaginationConfig, Typography } from "antd"
import classes from "./filterHistoryTable.module.scss"
import { TableComponent } from "@/shared/ui/table"
import { useColumns } from "@/features/filter-history-table/config/useColumns"
import { openModal } from "@/entities/import/model/slice/importSlice"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import {
  getFilterHistoryData,
  getSelectedData,
} from "@/entities/import/model/services/importServices"
import { FilterHistoryDataType } from "@/entities/import/model/types/importSchema"
import { getAnalyticsData } from "@/entities/analytics/model/services/analyticsService"

export const FilterHistoryTable = memo(() => {
  const [page, setPage] = useState<number>(1)
  const [limit, setLimit] = useState<number>(10)
  const [total, setTotal] = useState<number>(1)

  const filterHistoryColumns = useColumns()

  const dispatch = useAppDispatch()
  const { filterHistory } = useAppSelector(state => state.import)

  useEffect(() => {
    dispatch(
      getFilterHistoryData({
        limit,
        page,
      }),
    )
  }, [dispatch, limit, page])

  useEffect(() => {
    if (filterHistory.data) setTotal(filterHistory.data.count)
  }, [filterHistory])

  const handleTableChange = (pagination: TablePaginationConfig) => {
    setPage(pagination.current!)
    setLimit(pagination.pageSize!)
    setTotal(filterHistory.data.count)
  }

  const onRowClick = (record: FilterHistoryDataType) => () => {
    const pathName = window.location.href.split("/").filter(Boolean).pop()

    if (record && pathName === "import") {
      dispatch(getSelectedData({ id: record.id! }))
      dispatch(openModal())
    }

    if (record && pathName === "visualization") {
      dispatch(getAnalyticsData({ id: record.id! }))
    }
  }

  return (
    <div className={classes.table}>
      <Typography.Title level={3} className={classes["table-title"]}>
        {"История отчетов"}
      </Typography.Title>
      <TableComponent
        onChange={handleTableChange}
        total={total}
        isLoading={filterHistory.isLoading}
        isError={!!filterHistory.error}
        columns={filterHistoryColumns}
        dataSource={filterHistory && filterHistory.data.results}
        rowKey={record => record.id}
        onRow={record => ({
          onClick: onRowClick(record),
        })}
      />
    </div>
  )
})
