import { FC, Suspense } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import { Layout } from "antd"
import { Spinner, SpinnerType } from "@/shared/ui/spinner/Spinner"
import {
  privateRoutes,
  RouteNames,
} from "@/app/providers/router/config/routeConfig"
import { Footer } from "@/widgets/footer"
import { Header } from "@/widgets/header"
import { Navbar } from "@/widgets/navbar"
import Sider from "antd/es/layout/Sider"

const { Content } = Layout

const AppRouter: FC = () => {
  return (
    <Suspense fallback={<Spinner size="large" type={SpinnerType.GLOBAL} />}>
      <Layout>
        <Header />
        <Layout>
          <Sider width="15%">
            <Navbar />
          </Sider>
          <Content>
            <Routes>
              {privateRoutes.map(route => (
                <Route
                  key={route.path}
                  path={route.path}
                  element={<route.component />}
                />
              ))}
              <Route
                path={RouteNames.NAVIGATE}
                element={<Navigate replace to={RouteNames.MAIN} />}
              />
            </Routes>
          </Content>
        </Layout>
        <Footer />
      </Layout>
    </Suspense>
  )
}

export default AppRouter
