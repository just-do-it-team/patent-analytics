import { memo, ReactNode } from "react"
import { classNames } from "@/shared/lib/classNames/classNames"
import classes from "./block.module.scss"

interface BlockProps {
  className?: string
  children?: ReactNode
}

export const Block = memo((props: BlockProps) => {
  const { className, children } = props

  return (
    <div className={classNames(classes.Block, {}, [className])}>{children}</div>
  )
})
