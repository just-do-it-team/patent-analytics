import classes from "./mainPage.module.scss"
import { Typography } from "antd"
import { FileUpload } from "@/features/file-upload"
import { Block } from "@/shared/ui/block/Block"

const MainPage = () => {
  return (
    <div className={classes["main-page"]}>
      <Block>
        <Typography.Title level={2} className={classes.title}>
          Загрузить файл
        </Typography.Title>
        <Typography className={classes.description}>
          Загрузите необходимый файл шаблона для аналитики
        </Typography>
        <FileUpload />
      </Block>
    </div>
  )
}

export default MainPage
