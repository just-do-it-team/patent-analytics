import { Avatar, Layout, Typography } from "antd"
import { FC, memo } from "react"
import { UserOutlined } from "@ant-design/icons"
import { Link } from "react-router-dom"
import { RouteNames } from "@/app/providers/router/config/routeConfig"
import classes from "./header.module.scss"
import mainLogo from "@/app/assets/images/certificate.png"

export const Header: FC = memo(() => {
  return (
    <Layout.Header>
      <div className={classes.container}>
        <Link to={RouteNames.MAIN} className={classes.link}>
          <img src={mainLogo} className={classes.img} />
        </Link>
        <Typography.Title level={1} className={classes.title}>
          {"Патентная Аналитика <Just-do-iT>"}
        </Typography.Title>
      </div>
      <div className={classes.profile}>
        <>
          <Avatar size="large" icon={<UserOutlined />} />
          <Typography className={classes.role}>Username</Typography>
        </>
      </div>
    </Layout.Header>
  )
})
