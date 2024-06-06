import { Layout } from "antd"
import { FC, memo } from "react"
import classes from "./footer.module.scss"

export const Footer: FC = memo(() => {
  const getYear = () => new Date().getFullYear()
  return (
    <Layout.Footer>
      <div className={classes.text}>© {getYear()} JustDoIt</div>
    </Layout.Footer>
  )
})
