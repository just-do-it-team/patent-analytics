import classes from "./analyticsPage.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { FilesHistoryTable } from "@/features/files-history-table"

const AnalyticsPage = () => {
  return (
    <div className={classes["analytics-page"]}>
      <Block className={classes["table-block"]}>
        <FilesHistoryTable />
      </Block>
    </div>
  )
}

export default AnalyticsPage
