import { MainPage } from "@/pages/main-page"
import { VisualizationPage } from "@/pages/visualization-page"
import { ImportPage } from "@/pages/import-page"

export enum RouteNames {
  MAIN = "/",
  VISUALIZATION = "/visualization",
  IMPORT = "/import",
  NAVIGATE = "*",
}

export const privateRoutes = [
  { path: RouteNames.MAIN, component: MainPage },
  { path: RouteNames.VISUALIZATION, component: VisualizationPage },
  { path: RouteNames.IMPORT, component: ImportPage },
]
