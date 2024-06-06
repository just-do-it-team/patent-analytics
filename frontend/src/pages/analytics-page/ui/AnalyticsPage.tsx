import classes from "./analyticsPage.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { FilesHistoryTable } from "@/features/files-history-table"
import { Chart } from "@/shared/ui/chart/Chart"

const AnalyticsPage = () => {
  return (
    <div className={classes["analytics-page"]}>
      {/*<Info />*/}
      <Block className={classes.chartBlock}>
        <Chart />
      </Block>
      <Block className={classes["table-block"]}>
        <FilesHistoryTable />
      </Block>
    </div>
  )
}

export default AnalyticsPage
