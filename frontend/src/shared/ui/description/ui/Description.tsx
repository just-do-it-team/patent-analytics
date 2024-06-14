import { memo, ReactNode } from "react"
import { Typography } from "antd"
import classes from "./description.module.scss"

export type AsmoDropdownProps = {
  children?: ReactNode
  title: string
}

export const Description = memo((props: AsmoDropdownProps) => {
  const { children, title } = props

  return (
    <>
      <Typography className={classes["form-description-title"]}>
        {title}
      </Typography>
      <Typography className={classes["form-description-content"]}>
        {children}
      </Typography>
    </>
  )
})
