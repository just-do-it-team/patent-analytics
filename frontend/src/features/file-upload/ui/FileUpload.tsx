import { FC, useEffect, useState } from "react"
import { Upload, Button, message, Typography } from "antd"
import classes from "./fileUpload.module.scss"
import { UploadOutlined, FileDoneOutlined } from "@ant-design/icons"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import {
  downloadAnalyticsFile,
  uploadAnalyticsFile,
} from "@/entities/export/model/services/exportServices"
import { setDownloadLink } from "@/entities/export/model/slice/exportSlice"

export const FileUpload: FC = () => {
  const dispatch = useAppDispatch()
  const { downloadLink } = useAppSelector(state => state.export)
  const [fileList, setFileList] = useState<any[]>([])
  // const [downloadLink, setDownloadLink] = useState<string | null>()

  useEffect(() => {
    if (downloadLink) {
      setFileList([])
    }
  }, [downloadLink])

  const alowedFileTypes: string[] = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ]

  const onUpload = async () => {
    const formData = new FormData()
    fileList.forEach(file => {
      formData.append("files", file.originFileObj)
    })

    dispatch(uploadAnalyticsFile({ formData }))
  }
  const handleFileChange = (info: any) => {
    if (
      info.fileList[0] &&
      !alowedFileTypes.find(t => t === info.fileList[0].type)
    ) {
      message.error({
        content: "Неподдерживаемый формат файла, поддерживаемые форматы: .xlsx",
        duration: 3,
      })
    } else {
      setFileList(info.fileList)
    }
  }

  const onCancel = () => {
    dispatch(setDownloadLink(null))
  }

  return (
    <>
      <Typography.Title level={3} className={classes.title}>
        Получение аналитики из файла
      </Typography.Title>
      <Typography className={classes.description}>
        Загрузите необходимый файл шаблона для получения патентной аналитики
      </Typography>
      {!downloadLink ? (
        <>
          <Upload.Dragger
            // action={`${SERVER_URL}/upload/`}
            fileList={fileList}
            onChange={handleFileChange}
            className={classes.upload}
            maxCount={1}
            beforeUpload={(file, fileList) => {
              // Access file content here and do something with it
              // console.log(file)
              // Prevent upload
              return false
            }}
          >
            <div className={classes["upload-wrapper"]}>
              <div className={classes["upload-icon"]}>
                <p>
                  <FileDoneOutlined />
                </p>
              </div>
              <div className={classes["upload-text-wrapper"]}>
                <p className={classes["upload-text"]}>Приложите файл</p>
                <p className={classes["upload-hint"]}>
                  Нажмите на поле или перетащите в него файл
                </p>
                <p className={classes["upload-hint"]}>
                  Допустимый формат: .xlsx
                </p>
              </div>
            </div>
          </Upload.Dragger>
          {!!fileList.length && (
            <Button
              disabled={!fileList.length}
              onClick={onUpload}
              type="primary"
              className={classes["upload-btn"]}
              icon={<UploadOutlined />}
            >
              Загрузить
            </Button>
          )}
        </>
      ) : (
        <>
          <Button
            onClick={onCancel}
            type="default"
            className={classes["upload-btn"]}
          >
            Назад
          </Button>
          <Button
            onClick={() => dispatch(downloadAnalyticsFile())}
            type="primary"
            className={classes["upload-btn"]}
            icon={<UploadOutlined />}
          >
            Скачать
          </Button>
        </>
      )}
    </>
  )
}
