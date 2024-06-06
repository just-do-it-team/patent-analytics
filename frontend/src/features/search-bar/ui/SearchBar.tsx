import React, { ChangeEvent, useEffect, useState } from "react"
import { Button, Input, Tag, Typography } from "antd"
import { SearchOutlined } from "@ant-design/icons"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import classes from "./searchBar.module.scss"

export const SearchBar = () => {
  const dispatch = useAppDispatch()
  const [string, setString] = useState<string>()
  const { searchString, searchResult } = useAppSelector(state => state.category)

  useEffect(() => {
    if (searchString === "") setString("")
  }, [searchString])

  const onSearch = () => {}

  const onSearchChange = (e: ChangeEvent<HTMLInputElement>) => {
    setString(e.target.value)
  }

  const onCloseTag = () => {
    setString("")
  }

  return (
    <div className={classes.container}>
      <div className={classes["search-bar"]}>
        <Input
          value={string}
          onChange={e => onSearchChange(e)}
          onPressEnter={onSearch}
          prefix={<SearchOutlined />}
          placeholder="Введите название"
        />
        <Button className={classes["search-btn"]} onClick={onSearch}>
          Найти
        </Button>
      </div>
      {searchString && (
        <div className={classes["tag-bar"]}>
          <Typography>Найдено: {searchResult}</Typography>
          <Tag className={classes.tag} closable onClose={onCloseTag}>
            {searchString}
          </Tag>
        </div>
      )}
    </div>
  )
}
