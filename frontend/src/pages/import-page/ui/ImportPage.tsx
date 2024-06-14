import classes from "./importPage.module.scss"
import { FilterForm } from "@/features/filter-form"
import { FilterHistoryTable } from "@/features/filter-history-table"
import { Block } from "@/shared/ui/block/Block"
import { FilterHistoryModal } from "@/features/filter-history-modal"

const ImportPage = () => {
  return (
    <div className={classes["import-page"]}>
      <Block className={classes["filter-block"]}>
        <FilterForm />
      </Block>

      <Block className={classes["history-table-block"]}>
        <FilterHistoryModal />
        <FilterHistoryTable />
      </Block>
    </div>
  )
}

export default ImportPage
