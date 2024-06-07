import classes from "./importPage.module.scss"
import { FilterForm } from "@/features/filter-form"
import { FilterHistoryTable } from "@/features/filter-history-table"
import { Block } from "@/shared/ui/block/Block"

const ImportPage = () => {
  return (
    <div className={classes["import-page"]}>
      <FilterForm />
      <Block className={classes["table-block"]}>
        <FilterHistoryTable />
      </Block>
    </div>
  )
}

export default ImportPage
