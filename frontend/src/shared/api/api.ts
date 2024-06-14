import axios from "axios"
import { SERVER_URL } from "@/app/config"

export const Endpoints = {
  FILE_HISTORY: "file_history",
}

export const api = axios.create({
  baseURL: SERVER_URL,
})
