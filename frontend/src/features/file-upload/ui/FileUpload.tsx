import { FC, useEffect, useState } from "react"
import { Upload, Button, message, Typography } from "antd"
import classes from "./fileUpload.module.scss"
import axios from "axios"
import { SERVER_URL } from "@/app/config"
import { FileDoneOutlined } from "@ant-design/icons"

export const FileUpload: FC = () => {
  const [fileList, setFileList] = useState<any[]>([])
  const [downloadLink, setDownloadLink] = useState<string>()

  useEffect(() => {
    if (downloadLink) {
      setFileList([])
    }
  }, [downloadLink])

  const handleUpload = async () => {
    const formData = new FormData()
    fileList.forEach(file => {
      formData.append("files", file.originFileObj)
    })

    try {
      message.loading({
        content: "Загрузка...",
        key: "uploadFile",
        duration: 0,
      })
      const response = await axios.post(`${SERVER_URL}/api/upload/`, formData)
      const newLink = response.data.processed_files
      setDownloadLink(newLink)
      message.success({ content: "Успешно загружено", key: "uploadFile" })
    } catch (error) {
      message.error({ content: "Не удалось загрузить", key: "uploadFile" })
    }
  }
  const handleFileChange = (info: any) => {
    setFileList(info.fileList)
  }

  const downloadFile = async () => {
    try {
      message.loading({
        content: "Cкачивание...",
        key: "downloadFile",
        duration: 0,
      })
      await fetch(`${SERVER_URL}/api/download/`, {
        method: "GET",
      })
        .then(res => res.blob())
        .then(data => {
          const url = URL.createObjectURL(data)
          const anchor = document.createElement("a")
          anchor.href = url
          anchor.download = "downloadLink"
          document.body.append(anchor)
          anchor.click()
          anchor.remove()

          URL.revokeObjectURL(url)
        })
      message.success({ content: "Файл скачан", key: "downloadFile" })
    } catch (error) {
      message.error({ content: "Не удалось скачать файл", key: "downloadFile" })
    }
  }

  return (
    <>
      <div className={classes.container}>
        <Upload.Dragger
          fileList={fileList}
          onChange={handleFileChange}
          className={classes.upload}
        >
          <div className={classes["upload-wrapper"]}>
            <div className={classes["upload-icon"]}>
              <p>
                <FileDoneOutlined />
              </p>
            </div>
            <div>
              <p className={classes["upload-text"]}>Приложите файл</p>
              <p className={classes["upload-hint"]}>
                Нажмите на поле или перетащите в него файл
              </p>
            </div>
          </div>
        </Upload.Dragger>

        {downloadLink && (
          <div className={classes.attachment}>
            <Typography className={classes["attachment-title"]}>
              Ссылка на готовый файл:
            </Typography>
            <div onClick={downloadFile}>
              <Button className={classes.link}>Скачать файл</Button>
            </div>
          </div>
        )}
      </div>
      <Button
        disabled={!fileList.length}
        onClick={handleUpload}
        type="primary"
        className={classes["upload-btn"]}
      >
        Загрузить
      </Button>
    </>
  )
}
