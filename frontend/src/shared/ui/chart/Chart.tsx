import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import moment from "moment"
import { Typography } from "antd"
import classes from "./chart.module.scss"
import { useAppSelector } from "@/app/providers/store-provider/config/hooks"
import { Spinner } from "@/shared/ui/spinner/Spinner"

export const Chart = () => {
  const { analyticsData } = useAppSelector(state => state.analytics)
  // const mockData = [
  //   {
  //     name: "Page A",
  //     time: 0,
  //     sum: 0,
  //   },
  // ]

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
    return <Spinner />
  }
  // if (analyticsData.data.length === 0) {
  //   return <FetchError />
  // }

  return (
    <ResponsiveContainer width={"100%"} height={500}>
      <LineChart
        data={analyticsData.data || []}
        // margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="time"
          tickFormatter={unixTime => moment(unixTime).format("DD MMM")}
        />
        <YAxis dataKey="sum" domain={[0, 3000]} />
        <Tooltip content={<CustomTooltip />} />
        <Line type="monotone" dataKey="sum" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  )
}
