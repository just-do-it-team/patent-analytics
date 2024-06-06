import { FC, Suspense } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import { Layout } from "antd"
import { Spinner, SpinnerType } from "@/shared/ui/spinner/Spinner"
import { Navbar } from "@/widgets/navbar"
import {
  privateRoutes,
  RouteNames,
} from "@/app/providers/router/config/routeConfig"
import { Footer } from "@/widgets/footer"
import { Header } from "@/widgets/header"

const { Content } = Layout

const AppRouter: FC = () => {
  return (
    <Suspense fallback={<Spinner size="large" type={SpinnerType.GLOBAL} />}>
      <Layout>
        <>
          <Header />
          <Navbar />
        </>
        <Layout>
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
