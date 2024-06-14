import { Button, Form, Typography } from "antd"
import { FC, memo } from "react"
import classes from "./filterHistoryForm.module.scss"
import { Description } from "@/shared/ui/description"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import {
  formatDateToString,
  formatDateToStringWithHours,
} from "@/shared/config/date/date-formats"
import { Spinner } from "@/shared/ui/spinner/Spinner"
import { DownloadOutlined } from "@ant-design/icons"
import { downloadFilterHistoryReport } from "@/entities/import/model/services/importServices"

export const FilterHistoryForm: FC = memo(() => {
  const [form] = Form.useForm()
  const dispatch = useAppDispatch()
  const { selected } = useAppSelector(state => state.import)

  const caption = `Отчет от ${formatDateToStringWithHours(selected.data?.datetime!)}`

  const onDownload = async () => {
    await dispatch(downloadFilterHistoryReport(selected.data?.id!))
  }

  if (selected.isLoading) {
    return <Spinner className={classes.spinner} />
  }

  return (
    <Form
      form={form}
      name="filter_history_form"
      className={classes.form}
      autoComplete="off"
    >
      <div className={classes.caption}>
        {" "}
        <Typography className={classes.title}>{caption}</Typography>
      </div>
      <Description title="ИНН">{selected.data?.inn || "-"}</Description>
      <Description title="ОКОПФ расшифровки">
        {selected.data?.okopf || "-"}
      </Description>
      <Description title="ОКОПФ коды">
        {selected.data?.okopf_code || "-"}
      </Description>
      {/*<Description title="ОКФС расшифровки">*/}
      {/*  {selected.data?.okfs || "-"}*/}
      {/*</Description>*/}
      {/*<Description title="ОКФС коды">*/}
      {/*  {selected.data?.okfs_code || "-"}*/}
      {/*</Description>*/}
      <Description title="Даты">
        {formatDateToString(selected.data?.start_date!)} -{" "}
        {formatDateToString(selected.data?.end_date!)}
      </Description>

      <div className={classes["form-actions"]}>
        <Button
          block
          type="primary"
          onClick={onDownload}
          icon={<DownloadOutlined />}
          disabled={selected.isLoading || !!selected.error}
        >
          Скачать отчет
        </Button>
      </div>
    </Form>
  )
})
