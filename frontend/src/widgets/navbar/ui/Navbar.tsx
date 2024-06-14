import { Menu, MenuProps } from "antd"
import { FC, memo, useEffect, useState } from "react"
import {
  HomeOutlined,
  BarChartOutlined,
  ImportOutlined,
} from "@ant-design/icons"
import classes from "./navbar.module.scss"
import { Link, useLocation } from "react-router-dom"
import { RouteNames } from "@/app/providers/router/config/routeConfig"

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
      icon: <ImportOutlined />,
      label: <Link to={RouteNames.IMPORT}>Отчет</Link>,
      key: RouteNames.IMPORT,
    },
    {
      icon: <BarChartOutlined />,
      label: <Link to={RouteNames.VISUALIZATION}>Визуализация</Link>,
      key: RouteNames.VISUALIZATION,
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
