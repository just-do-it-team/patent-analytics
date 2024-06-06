import React from "react"
import { createRoot } from "react-dom/client"
import { Provider } from "react-redux"
import App from "./app/App"
import { ConfigProvider } from "antd"
import ruRU from "antd/es/locale/ru_RU"
import { BrowserRouter } from "react-router-dom"
import { ErrorBoundary } from "@/app/providers/error-boundary"
import store from "@/app/providers/store-provider/config/store"
import "./app/styles/index.scss"

const container = document.getElementById("root")

if (container) {
  const root = createRoot(container)

  root.render(
    <BrowserRouter>
      <Provider store={store}>
        <ConfigProvider locale={ruRU} theme={{ hashed: false }}>
          <ErrorBoundary>
            <App />
          </ErrorBoundary>
        </ConfigProvider>
      </Provider>
    </BrowserRouter>,
  )
} else {
  throw new Error(
    "Root element with ID 'root' was not found in the document. Ensure there is a corresponding HTML element with the ID 'root' in your HTML file.",
  )
}
