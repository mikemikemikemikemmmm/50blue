import { BaseApi } from "."
interface LoginApiResponse {
  access_token: string
  token_type: string
  allow_route_name_list: string[]
}
export const loginApi = async (email: string, password: string) => {
  const formData = new FormData()
  formData.set("username", email)
  formData.set("password", password)
  return await BaseApi.
    postApi<FormData, LoginApiResponse>(
      '/auth/login',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }, "登入成功");
}
export const checkTokenWhenFristEnterApi = async () => {
  return await BaseApi.getApi<{
    "is_token_legal": true,
    "allow_route_name_list": string[]
  }>('/auth/check_token_when_first_enter', undefined, "登入成功");
}