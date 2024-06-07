import { Button, DatePicker, Form, Input, Switch, Typography } from "antd"
import { ChangeEvent, FC, memo, useEffect, useState } from "react"
import classes from "./filterForm.module.scss"
import { Block } from "@/shared/ui/block/Block"
import { SearchOutlined } from "@ant-design/icons"
import { USER_DATE_FORMAT } from "@/shared/config/date/date-formats"
import { disabledPeriodDate } from "@/shared/config/date/disabled-date"

const { RangePicker } = DatePicker

export const FilterForm: FC = memo(() => {
  const [form] = Form.useForm()
  const [expiredDate, setExpiredDate] = useState<boolean>(false)
  const [tinValue, setTinValue] = useState<string>()
  const [numberValue, setNumberValue] = useState<string>()
  const [rangeValue, setRangeValue] = useState<any>()

  useEffect(() => {
    form.setFieldsValue({
      tin: tinValue,
      number: numberValue,
    })
  }, [form])

  const onTinChange = (e: ChangeEvent<HTMLInputElement>) => {
    const formatValue = e.target.value.replace(/[^0-9\s]/gi, "")
    setTinValue(formatValue)
    form.setFieldsValue({ tin: formatValue })
  }

  const onNumberChange = (e: ChangeEvent<HTMLInputElement>) => {
    const formatValue = e.target.value.replace(/[^0-9\s]/gi, "")
    setNumberValue(formatValue)
    form.setFieldsValue({ number: formatValue })
  }

  const onSwitchChange = () => {
    setExpiredDate(!expiredDate)
  }

  const onSubmit = () => {}

  return (
    <Form
      form={form}
      name="filter_form"
      className={classes.form}
      autoComplete="off"
      onFinish={onSubmit}
    >
      <Block>
        <div className={classes.filter}>
          <Typography.Title level={2} className={classes.title}>
            Выгрузить отчет
          </Typography.Title>
          <Form.Item name="tin" className={classes.field}>
            <Input
              value={tinValue}
              onChange={e => onTinChange(e)}
              size={"large"}
              placeholder={"ИНН"}
            />
          </Form.Item>
          <Form.Item name="number" className={classes.field}>
            <Input
              value={numberValue}
              onChange={e => onNumberChange(e)}
              size={"large"}
              placeholder={"Номера патентов"}
            />
          </Form.Item>
          <Form.Item name="rangeDate" className={classes.field}>
            <RangePicker
              value={rangeValue}
              onChange={setRangeValue}
              format={USER_DATE_FORMAT}
              size={"large"}
              placeholder={["Начало", "Конец"]}
              disabledDate={disabledPeriodDate}
            />
          </Form.Item>

          <div className={classes.expiredDateField}>
            <Switch
              onChange={onSwitchChange}
              checked={expiredDate}
              className={classes.expirationSwitch}
            />
            <Typography>Патенты с истекшим сроком</Typography>
          </div>
        </div>
        <div className={classes.actions}>
          <Button
            className={classes.submitButton}
            htmlType="submit"
            type={"default"}
            size={"large"}
            icon={<SearchOutlined />}
          >
            Поиск
          </Button>
        </div>
      </Block>
    </Form>
  )
})
