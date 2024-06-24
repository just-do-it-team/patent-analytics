import {
  Bar,
  BarChart,
  CartesianGrid,
  Rectangle,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import moment from "moment"
import { Typography } from "antd"
import classes from "./bar.module.scss"
import { useAppSelector } from "@/app/providers/store-provider/config/hooks"
import { Spinner } from "@/shared/ui/spinner/Spinner"
import { Block } from "@/shared/ui/block/Block"

export const BarComponent = () => {
  const { analyticsData } = useAppSelector(state => state.analytics)

  const getMaxSum = (): number => {
    return Math.max(...analyticsData.data.map(item => parseFloat(item.sum)))
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className={classes.tooltip}>
          <Typography>{`Дата: ${moment(payload[0].payload?.time).locale("ru").format("DD.MM.YYYY")}`}</Typography>
          <Typography>{`Количество: ${payload[0]?.payload?.sum}`}</Typography>
        </div>
      )
    }
    return null
  }

  if (analyticsData.isLoading) {
    return (
      <Block className={classes["chart-block"]}>
        <Spinner />
      </Block>
    )
  }

  return (
    <>
      <Block className={classes["chart-block"]}>
        <>
          <Typography.Title level={3} className={classes.title}>
            Зарегестрированные патенты
          </Typography.Title>
          <ResponsiveContainer width={"100%"} height={500}>
            <BarChart
              data={analyticsData.data || []}
              // margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tickFormatter={unixTime => moment(unixTime).format("DD MMM")}
              />
              <YAxis dataKey="sum" domain={[0, getMaxSum()]} />
              <Tooltip content={<CustomTooltip />} />
              <Bar
                dataKey="sum"
                fill="#42a5f5"
                activeBar={<Rectangle fill="#e6eff6" stroke="blue" />}
              />
              <Bar
                dataKey="uv"
                fill="#82ca9d"
                activeBar={<Rectangle fill="white" stroke="purple" />}
              />
            </BarChart>
          </ResponsiveContainer>
        </>
      </Block>
    </>
  )
}
