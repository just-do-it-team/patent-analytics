import { MainPage } from "@/pages/main-page"

export enum RouteNames {
  MAIN = "/",
  NAVIGATE = "*",
}

export const privateRoutes = [{ path: RouteNames.MAIN, component: MainPage }]
