import { Button, Typography } from "antd"
import { RedoOutlined } from "@ant-design/icons"
import classes from "./errorPage.module.scss"
import { classNames } from "@/shared/lib/classNames/classNames"

interface ErrorPageProps {
  className?: string
}

export const ErrorPage = ({ className }: ErrorPageProps) => {
  const reloadPage = () => {
    // eslint-disable-next-line no-restricted-globals
    location.reload()
  }

  return (
    <div className={classNames(classes.ErrorPage, {}, [className])}>
      <Typography.Title level={3} className={classes.title}>
        Произошла непредвиденная ошибка...
      </Typography.Title>
      <Typography.Text className={classes.description}>
        Попробуйте перезагрузить страницу через некоторое время
      </Typography.Text>
      <Button onClick={reloadPage}>
        <RedoOutlined />
        Перезагрузить страницу
      </Button>
    </div>
  )
}
