import { Layout } from "antd"
import React, { FC, memo } from "react"
import classes from "./footer.module.scss"

export const Footer: FC = memo(() => {
  const getYear = () => new Date().getFullYear()
  return (
    <Layout.Footer>
      <div className={classes.text}>© {getYear()} Footer text</div>
    </Layout.Footer>
  )
})
