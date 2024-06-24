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
import { useAppSelector } from "@/app/providers/store-provider/config/hooks"

export const Navbar: FC = memo(() => {
  const location = useLocation()
  const [current, setCurrent] = useState(location.pathname)
  const { analyticsData } = useAppSelector(state => state.analytics)

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
      disabled: analyticsData.isLoading,
    },
    {
      icon: <ImportOutlined />,
      label: <Link to={RouteNames.IMPORT}>Отчет</Link>,
      key: RouteNames.IMPORT,
      disabled: analyticsData.isLoading,
    },
    {
      icon: <BarChartOutlined />,
      label: <Link to={RouteNames.VISUALIZATION}>Визуализация</Link>,
      key: RouteNames.VISUALIZATION,
      disabled: analyticsData.isLoading,
    },
  ]

  return (
    <div className={classes.Navbar}>
      <Menu
        onClick={onClick}
        className={
          analyticsData.isLoading ? classes["menu-disabled"] : classes.menu
        }
        mode="inline"
        items={items}
        selectedKeys={[current]}
      />
    </div>
  )
})
