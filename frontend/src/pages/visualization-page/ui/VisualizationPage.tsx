import classes from "./visualizationPage.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { Chart } from "@/shared/ui/chart/Chart"
import { FilterHistoryTable } from "@/features/filter-history-table"
import { FilterHistoryModal } from "@/features/filter-history-modal"
import { BarComponent } from "@/shared/ui/bar/Bar"
import { useAppSelector } from "@/app/providers/store-provider/config/hooks"
import { BarChartOutlined, FrownOutlined } from "@ant-design/icons"
import { Typography } from "antd"

const VisualizationPage = () => {
  const { analyticsData } = useAppSelector(state => state.analytics)
  const { selectedFilterRow } = useAppSelector(state => state.import)

  const chartsContent = () => {
    if (!selectedFilterRow) {
      return (
        <Block className={classes["error-block"]}>
          <div className={classes.container}>
            <BarChartOutlined className={classes.icon} />
            <Typography className={classes.message}>
              Выберите отчет для визуализации
            </Typography>
          </div>
        </Block>
      )
    }

    if (
      selectedFilterRow &&
      analyticsData.data.length === 0 &&
      !analyticsData.isLoading
    ) {
      return (
        <Block className={classes["error-block"]}>
          <div className={classes.container}>
            <FrownOutlined className={classes.icon} />
            <Typography className={classes.message}>
              По данному запросу патентов не найдено
            </Typography>
          </div>
        </Block>
      )
    }

    return (
      <>
        <Chart />
        <BarComponent />
      </>
    )
  }

  return (
    <div className={classes["visualization-page"]}>
      <div className={classes["charts-wrapper"]}>{chartsContent()}</div>
      <Block
        className={
          analyticsData.isLoading
            ? classes["history-table-block-disabled"]
            : classes["history-table-block"]
        }
      >
        <FilterHistoryModal />
        <FilterHistoryTable />
      </Block>
    </div>
  )
}

export default VisualizationPage
