import classes from "./mainPage.module.scss"
import { FileUpload } from "@/features/file-upload"
import { Block } from "@/shared/ui/block/Block"
import { FilesHistoryTable } from "@/features/files-history-table"

const MainPage = () => {
  return (
    <div className={classes["main-page"]}>
      <Block className={classes["upload-block"]}>
        <FileUpload />
      </Block>
      <Block className={classes["table-block"]}>
        <FilesHistoryTable />
      </Block>
    </div>
  )
}

export default MainPage
