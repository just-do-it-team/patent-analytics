import { Typography } from "antd"
import { FrownOutlined } from "@ant-design/icons"
import { memo } from "react"
import classes from "./fetchError.module.scss"

export const FetchError = memo(() => {
  return (
    <div className={classes.container}>
      <FrownOutlined className={classes.icon} />
      <Typography className={classes.message}>
        По данному запросу патентов не найдено
      </Typography>
    </div>
  )
})
