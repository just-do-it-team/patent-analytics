import { MainPage } from "@/pages/main-page"
import { AnalyticsPage } from "@/pages/analytics-page"

export enum RouteNames {
  MAIN = "/",
  ANALYTICS = "/analytics",
  NAVIGATE = "*",
}

export const privateRoutes = [
  { path: RouteNames.MAIN, component: MainPage },
  { path: RouteNames.ANALYTICS, component: AnalyticsPage },
]
