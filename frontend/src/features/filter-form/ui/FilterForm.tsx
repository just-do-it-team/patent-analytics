import {
  Button,
  DatePicker,
  Flex,
  Form,
  Input,
  Switch,
  Tag,
  Tooltip,
  Typography,
} from "antd"
import { ChangeEvent, FC, memo, ReactNode, useEffect, useState } from "react"
import classes from "./filterForm.module.scss"
import { DownloadOutlined, QuestionCircleOutlined } from "@ant-design/icons"
import {
  getDateToString,
  USER_DATE_FORMAT,
} from "@/shared/config/date/date-formats"
import { disabledPeriodDate } from "@/shared/config/date/disabled-date"
import { FilterHistoryDataType } from "@/entities/import/model/types/importSchema"
import {
  getReport,
  getReportAll,
} from "@/entities/import/model/services/importServices"
import { useAppDispatch } from "@/app/providers/store-provider/config/hooks"

const { RangePicker } = DatePicker

export const FilterForm: FC = memo(() => {
  const dispatch = useAppDispatch()
  const [form] = Form.useForm()
  const [innValue, setInnValue] = useState<string>()
  const [okopfNameValue, setOkopfNameValue] = useState<string>()
  const [okopfCodeValue, setOkopfCodeValue] = useState<string>()
  // const [ofksNameValue, setOfksNameValue] = useState<string>()
  // const [ofksCodeValue, setOfksCodeValue] = useState<string>()
  const [startDateValue, setStartDateValue] = useState<string>()
  const [endDateValue, setEndDateValue] = useState<string>()
  const [rangeValue, setRangeValue] = useState<any>()
  const [selectedTags, setSelectedTags] = useState<string[]>(["Изобретения"])
  const [importAll, setImportAll] = useState<boolean>(false)

  const tagsData = ["Изобретения", "Промышленные образцы", "Полезные модели"]

  useEffect(() => {
    form.setFieldsValue({
      inn: innValue,
      okopf: okopfNameValue,
      okopf_code: okopfCodeValue,
      // okfs: ofksNameValue,
      // okfs_code: ofksCodeValue,
    })
  }, [form])

  useEffect(() => {
    if (importAll)
      setSelectedTags([
        "Изобретения",
        "Промышленные образцы",
        "Полезные модели",
      ])
  }, [importAll])

  const onTagChange = (tag: string, checked: boolean) => {
    if (!importAll) {
      const nextSelectedTags = checked
        ? [...selectedTags, tag]
        : selectedTags.filter(t => t !== tag)
      setSelectedTags(nextSelectedTags)
    }
  }

  const onInnChange = (e: ChangeEvent<HTMLInputElement>) => {
    // const formatValue = e.target.value.replace(/[^(\d+;)*\d*$]/gi, "")
    let formatValue = e.target.value
    formatValue = formatValue.replace(/[^0-9;]+/g, "") // Remove any character that is not a number or semicolon
    formatValue = formatValue.replace(/;;+/g, ";") // Replace any sequence of two or more semicolons with a single semicolon
    setInnValue(formatValue)
    form.setFieldsValue({ inn: formatValue })
  }

  const onOkopfNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    // const formatValue = e.target.value.replace(/[^а-яА-Я\; ]/gi, "")

    let formatValue = e.target.value

    // Replace any invalid sequence
    formatValue = formatValue.replace(/[^а-яА-ЯёЁ ;]+/g, "") // Remove any character that is not a Russian letter, space, or semicolon
    formatValue = formatValue.replace(/ {2,}/g, " ") // Replace any sequence of two or more spaces with a single space
    formatValue = formatValue.replace(/;;+/g, ";") // Replace any sequence of two or more semicolons with a single semicolon

    setOkopfNameValue(formatValue)
    form.setFieldsValue({ okopfName: formatValue })
  }

  const onOkopfCodeChange = (e: ChangeEvent<HTMLInputElement>) => {
    // const formatValue = e.target.value.replace(/[^?:\d\;]/gi, "")

    let formatValue = e.target.value

    // Replace any invalid sequence
    formatValue = formatValue.replace(/[^0-9;]+/g, "")
    formatValue = formatValue.replace(/;;+/g, ";")

    setOkopfCodeValue(formatValue)
    form.setFieldsValue({ okopfCode: formatValue })
  }

  // const onOfksNameChange = (e: ChangeEvent<HTMLInputElement>) => {
  //   const formatValue = e.target.value.replace(/[^а-яА-Я\; ]/gi, "")
  //   setOfksNameValue(formatValue)
  //   form.setFieldsValue({ ofksName: formatValue })
  // }
  //
  // const onOfksCodeChange = (e: ChangeEvent<HTMLInputElement>) => {
  //   const formatValue = e.target.value.replace(/[^?:\d\.;]/gi, "")
  //   setOfksCodeValue(formatValue)
  //   form.setFieldsValue({ ofksCode: formatValue })
  // }

  const onChangeDate = (value: any) => {
    const stringDate = getDateToString(value)

    setStartDateValue(stringDate.startDate)
    setEndDateValue(stringDate.endDate)
  }

  const onImportAllChange = () => {
    setImportAll(!importAll)
  }

  const onSubmit = (values: FilterHistoryDataType) => {
    const data = {
      inn: values.inn || null,
      okopf: values.okopf || null,
      okopf_code: values.okopf_code || null,
      // okfs: values.okfs || null,
      // okfs_code: values.okfs_code || null,
      start_date: startDateValue || null,
      end_date: endDateValue || null,
      invention_bd: selectedTags.includes("Изобретения"),
      prom_bd: selectedTags.includes("Промышленные образцы"),
      pmodels_bd: selectedTags.includes("Полезные модели"),
    }

    if (importAll) dispatch(getReportAll())

    if (!importAll) dispatch(getReport({ upload: data }))
  }

  return (
    <Form
      form={form}
      name="filter_form"
      className={classes.form}
      autoComplete="off"
      onFinish={values => onSubmit(values)}
    >
      <div className={classes.filter}>
        <Typography.Title level={3} className={classes.title}>
          Выгрузить отчет
        </Typography.Title>

        <div className={classes.tags}>
          <Flex gap={1} wrap={"wrap"}>
            <span className={classes["tags-title"]}>Виды патентов:</span>
            {tagsData.map<ReactNode>(tag => (
              <Tag.CheckableTag
                key={tag}
                checked={selectedTags.includes(tag)}
                onChange={checked => onTagChange(tag, checked)}
                className={
                  selectedTags.includes(tag)
                    ? classes["tags-item-active"]
                    : classes["tags-item"]
                }
              >
                {tag}
              </Tag.CheckableTag>
            ))}
          </Flex>
        </div>

        <Form.Item name="inn" className={classes.field}>
          <div className={classes.item}>
            <Input
              disabled={importAll}
              value={innValue}
              onChange={e => onInnChange(e)}
              size={"large"}
              placeholder={"ИНН"}
            />
            <Tooltip
              placement="bottom"
              title="Укажите номера ИНН компаний через точку с запятой, которые должны быть в отчете (по умолчанию будут учитыватся все ИНН)"
            >
              <QuestionCircleOutlined className={classes.icon} />
            </Tooltip>
          </div>
        </Form.Item>

        <Form.Item name="okopf" className={classes.field}>
          <div className={classes.item}>
            <Input
              disabled={importAll}
              value={okopfNameValue}
              onChange={e => onOkopfNameChange(e)}
              size={"large"}
              placeholder={"ОКОПФ расшифровки"}
            />
            <Tooltip
              placement="bottom"
              title="Укажите ОКОПФ расшифровки компаний через точку с запятой, которые должны быть в отчете (по умолчанию будут учитыватся все компании)"
            >
              <QuestionCircleOutlined className={classes.icon} />
            </Tooltip>
          </div>
        </Form.Item>

        <Form.Item name="okopf_code" className={classes.field}>
          <div className={classes.item}>
            <Input
              disabled={importAll}
              value={okopfCodeValue}
              onChange={e => onOkopfCodeChange(e)}
              size={"large"}
              placeholder={"ОКОПФ коды"}
            />
            <Tooltip
              placement="bottom"
              title="Укажите ОКОПФ коды компаний через точку с запятой, которые должны быть в отчете (по умолчанию будут учитыватся все коды)"
            >
              <QuestionCircleOutlined className={classes.icon} />
            </Tooltip>
          </div>
        </Form.Item>

        {/*<Form.Item name="okfs" className={classes.field}>*/}
        {/*  <div className={classes.item}>*/}
        {/*    <Input*/}
        {/*      disabled={importAll}*/}
        {/*      value={ofksNameValue}*/}
        {/*      onChange={e => onOfksNameChange(e)}*/}
        {/*      size={"large"}*/}
        {/*      placeholder={"ОКФС расшифровки"}*/}
        {/*    />*/}
        {/*    <Tooltip*/}
        {/*      placement="bottom"*/}
        {/*      title="Укажите ОКФС расшифровки компаний через запятую, которые должны быть в отчете (по умолчанию - все)"*/}
        {/*    >*/}
        {/*      <QuestionCircleOutlined className={classes.icon} />*/}
        {/*    </Tooltip>*/}
        {/*  </div>*/}
        {/*</Form.Item>*/}

        {/*<Form.Item name="okfs_code" className={classes.field}>*/}
        {/*  <div className={classes.item}>*/}
        {/*    <Input*/}
        {/*      disabled={importAll}*/}
        {/*      value={ofksCodeValue}*/}
        {/*      onChange={e => onOfksCodeChange(e)}*/}
        {/*      size={"large"}*/}
        {/*      placeholder={"ОКФС коды"}*/}
        {/*    />*/}
        {/*    <Tooltip*/}
        {/*      placement="bottom"*/}
        {/*      title="Укажите ОКФС коды компаний через запятую, которые должны быть в отчете (по умолчанию - все)"*/}
        {/*    >*/}
        {/*      <QuestionCircleOutlined className={classes.icon} />*/}
        {/*    </Tooltip>*/}
        {/*  </div>*/}
        {/*</Form.Item>*/}

        <Form.Item name="dateTime" className={classes.field}>
          <div className={classes.item}>
            <RangePicker
              disabled={importAll}
              value={rangeValue}
              onChange={onChangeDate}
              format={USER_DATE_FORMAT}
              size={"large"}
              placeholder={["Начало", "Конец"]}
              disabledDate={disabledPeriodDate}
            />
            <Tooltip
              placement="bottom"
              title="Укажите диапазон дат регистрации патентов для получения отчета (по умолчанию будут учитыватся последние 365 дней)"
            >
              <QuestionCircleOutlined className={classes.icon} />
            </Tooltip>
          </div>
        </Form.Item>
        <div className={classes["expired-date-field"]}>
          <Switch
            onChange={onImportAllChange}
            checked={importAll}
            className={classes["expiration-switch"]}
          />
          <Typography className={classes.title}>Выгрузить всю базу</Typography>
        </div>
      </div>
      <div className={classes.actions}>
        <Button
          disabled={!selectedTags.length}
          className={classes["submit-button"]}
          htmlType="submit"
          type="primary"
          size={"large"}
          icon={<DownloadOutlined />}
        >
          Выгрузить
        </Button>
      </div>
    </Form>
  )
})
