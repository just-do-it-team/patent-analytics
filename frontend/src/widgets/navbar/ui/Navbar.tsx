import { Menu, MenuProps } from "antd"
import React, { FC, memo, useEffect, useState } from "react"
import { HomeOutlined, BarChartOutlined } from "@ant-design/icons"
import classes from "./navbar.module.scss"
import { Link, useLocation } from "react-router-dom"
import { RouteNames } from "@/app/providers/router/config/routeConfig"

type MenuItem = Required<MenuProps>["items"][number]
export const Navbar: FC = memo(() => {
  const location = useLocation()
  const [current, setCurrent] = useState(location.pathname)

  useEffect(() => {
    setCurrent(location.pathname)
  }, [location])

  const onClick: MenuProps["onClick"] = e => {
    setCurrent(e.key)
  }

  const items: MenuProps["items"] = [
    {
      icon: <HomeOutlined />,
      label: <Link to={RouteNames.MAIN}>Главная</Link>,
      key: RouteNames.MAIN,
    },
    {
      icon: <BarChartOutlined />,
      label: <Link to={RouteNames.ANALYTICS}>Аналитика</Link>,
      key: RouteNames.ANALYTICS,
    },
  ]

  return (
    <div className={classes.Navbar}>
      <Menu
        onClick={onClick}
        className={classes.menu}
        mode="inline"
        items={items}
        selectedKeys={[current]}
      />
    </div>
  )
})
