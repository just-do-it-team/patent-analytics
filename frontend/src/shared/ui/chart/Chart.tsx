import { useEffect } from "react"
import {
  CartesianGrid,
  Label,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import {
  useAppDispatch,
  useAppSelector,
} from "@/app/providers/store-provider/config/hooks"
import { Spinner } from "@/shared/ui/spinner/Spinner"
import { FetchError } from "@/features/fetch-error"
import {
  getAdvancedData,
  getAnalyticsData,
} from "@/entities/analytics/model/services/analyticsService"
import { currentWeek } from "@/shared/config/date/date-formats"
import moment from "moment"
import { Card, Typography } from "antd"
import classes from "./chart.module.scss"

export const Chart = () => {
  const { activeTab } = useAppSelector(state => state.analytics)
  const dispatch = useAppDispatch()

  useEffect(() => {
    if (activeTab === "1") dispatch(getAnalyticsData())
    if (activeTab === "2") {
      dispatch(
        getAdvancedData({
          startDate: currentWeek[0],
          endDate: currentWeek[1],
          server: "",
        }),
      )
    }
  }, [dispatch, activeTab])

  const mockData = [
    {
      name: "Page A",
      time: 1000,
      busy: 0,
    },
    {
      name: "Page B",
      time: 2000,
      busy: 50,
    },
    {
      name: "Page C",
      time: 3000,
      busy: 25,
    },
    {
      name: "Page D",
      time: 4000,
      busy: 75,
    },
    {
      name: "Page E",
      time: 5000,
      busy: 0,
    },
    {
      name: "Page F",
      time: 6000,
      busy: 25,
    },
    {
      name: "Page G",
      time: 7000,
      busy: 75,
    },
  ]
  const formatXAxis = (tickItem: any) => {
    return moment(tickItem).locale("ru").format("DD MMMM")
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className={classes.tooltip}>
          <Typography>{`Дата: ${moment(payload[0].payload?.time).locale("ru").format("DD.MM.YYYY HH:mm")}`}</Typography>
          <Typography>{`Занятость: ${payload[0]?.payload?.busy} %`}</Typography>
        </div>
      )
    }

    return null
  }

  // if (analyticsData.isLoading) {
  //   return <Spinner />
  // }
  // if (analyticsData.data.length === 0) {
  //   return <FetchError />
  // }

  return (
    <ResponsiveContainer width={"100%"} height={500}>
      <LineChart
        // data={analyticsData.data}
        data={mockData}
        // margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="time"
          tickFormatter={unixTime => moment(unixTime).format("DD MMM")}
        />
        <YAxis dataKey="busy" domain={[0, 100]} />
        <Tooltip content={<CustomTooltip />} />
        <Line type="monotone" dataKey="busy" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  )
}
