import { memo } from "react"
import { Modal, ModalProps } from "antd"
import classes from "./modalComponent.module.scss"
import { Spinner } from "@/shared/ui/spinner/Spinner"

export type AsmoModalProps = {
  isLoading?: boolean
  isFetching?: boolean
  isError?: boolean
}

export const ModalComponent = memo((props: AsmoModalProps & ModalProps) => {
  const { isLoading, isFetching, isError, ...rest } = props

  if (isLoading || isFetching) {
    return <Spinner />
  }

  return (
    <Modal className={classes.ModalComponent} footer={null} {...rest}>
      {props.children}
    </Modal>
  )
})
