import classes from "./visualizationPage.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { Chart } from "@/shared/ui/chart/Chart"
import { Typography } from "antd"
import { FilterHistoryTable } from "@/features/filter-history-table"
import { FilterHistoryModal } from "@/features/filter-history-modal"

const VisualizationPage = () => {
  return (
    <div className={classes["visualization-page"]}>
      {/*<Info />*/}
      <Block className={classes["chart-block"]}>
        <Typography.Title level={3} className={classes.title}>
          Зарегестрированные патенты
        </Typography.Title>
        <Chart />
      </Block>
      <Block className={classes["history-table-block"]}>
        <FilterHistoryModal />
        <FilterHistoryTable />
      </Block>
    </div>
  )
}

export default VisualizationPage
