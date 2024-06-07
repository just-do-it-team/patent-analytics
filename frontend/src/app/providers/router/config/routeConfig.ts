import { MainPage } from "@/pages/main-page"
import { AnalyticsPage } from "@/pages/analytics-page"
import { ImportPage } from "@/pages/import-page"

export enum RouteNames {
  MAIN = "/",
  ANALYTICS = "/analytics",
  IMPORT = "/import",
  NAVIGATE = "*",
}

export const privateRoutes = [
  { path: RouteNames.MAIN, component: MainPage },
  { path: RouteNames.ANALYTICS, component: AnalyticsPage },
  { path: RouteNames.IMPORT, component: ImportPage },
]
