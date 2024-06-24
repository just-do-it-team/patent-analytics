import { memo, useEffect, useState } from "react"
import { TablePaginationConfig, Typography } from "antd"
import classes from "./filterHistoryTable.module.scss"
import { TableComponent } from "@/shared/ui/table"
import { useColumns } from "@/features/filter-history-table/config/useColumns"
import {
  openModal,
  setSelectedFilterRow,
} from "@/entities/import/model/slice/importSlice"
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
  const pathName = window.location.href.split("/").filter(Boolean).pop()

  const dispatch = useAppDispatch()
  const { filterHistory, selectedFilterRow } = useAppSelector(
    state => state.import,
  )

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

  useEffect(() => {
    if (pathName === "import") {
      dispatch(setSelectedFilterRow(null))
    }
  }, [dispatch, pathName])

  const handleTableChange = (pagination: TablePaginationConfig) => {
    setPage(pagination.current!)
    setLimit(pagination.pageSize!)
    setTotal(filterHistory.data.count)
  }

  const onRowClick = (record: FilterHistoryDataType) => () => {
    // if (record) {
    //   dispatch(setSelectedFilterRow(record))
    // }

    if (record && pathName === "import") {
      dispatch(setSelectedFilterRow(null))
      dispatch(getSelectedData({ id: record.id! }))
      dispatch(openModal())
    }

    if (record && pathName === "visualization") {
      dispatch(setSelectedFilterRow(record))
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
        rowClassName={(record: any) =>
          selectedFilterRow && record.id === selectedFilterRow.id
            ? "ant-table-row-selected"
            : ""
        }
        onRow={record => ({
          onClick: onRowClick(record),
        })}
      />
    </div>
  )
})
