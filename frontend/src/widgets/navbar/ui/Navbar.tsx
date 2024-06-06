import React, { FC, memo, SVGProps, useEffect, useState } from "react"
import { Menu, MenuProps } from "antd"
import { classNames } from "@/shared/lib/classNames/classNames"
import { Link, useLocation } from "react-router-dom"
import { RouteNames } from "@/app/providers/router/config/routeConfig"
import { useAppDispatch } from "@/app/providers/store-provider/config/hooks"
import classes from "./navbar.module.scss"

interface NavbarProps extends SVGProps<SVGSVGElement> {
  className?: string
}

export const Navbar: FC = memo((props: NavbarProps) => {
  const location = useLocation()
  const { className } = props

  const dispatch = useAppDispatch()
  const [current, setCurrent] = useState(location.pathname)

  useEffect(() => {
    setCurrent(location.pathname)
  }, [location])

  const onClick: MenuProps["onClick"] = e => {
    setCurrent(e.key)
  }

  const items: MenuProps["items"] = [
    {
      label: <Link to={RouteNames.MAIN}>Home</Link>,
      key: RouteNames.MAIN,
    },
    // {
    //     label: (
    //         <Link to={RouteNames.CATEGORIES}>
    //             Пример списка меню
    //         </Link>
    //     ),
    //     key: 'example1',
    //     children: [
    //         {
    //             type: 'group',
    //             label: 'Группа 1',
    //             children: [
    //                 {
    //                     label: 'Страница 1',
    //                     key: 'setting:1',
    //                 },
    //                 {
    //                     label: 'Страница 2',
    //                     key: 'setting:2',
    //                 },
    //             ],
    //         },
    //         {
    //             type: 'group',
    //             label: 'Группа 2',
    //             children: [
    //                 {
    //                     label: 'Страница 3',
    //                     key: 'setting:3',
    //                 },
    //                 {
    //                     label: 'Страница 4',
    //                     key: 'setting:4',
    //                 },
    //             ],
    //         },
    //     ],
    // },
    // {
    //     label: (
    //         <Link to={RouteNames.CATEGORY}>
    //             Пример закрытой страницы
    //         </Link>
    //     ),
    //     key: 'example2',
    //     disabled: true,
    // },
  ]

  return (
    <div className={classNames(classes.Navbar, {}, [className])}>
      <Menu
        className={classes["navbar-menu"]}
        onClick={onClick}
        selectedKeys={[current]}
        mode="horizontal"
        items={items}
      />
    </div>
  )
})
