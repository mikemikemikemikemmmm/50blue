import axios, { AxiosRequestConfig } from "axios";
import { ICE_CONTENT, SUGAR_CONTENT, USER_ROLE } from "../const";
import { getToken, removeTokenAndRedirectToLogin } from "../utils";
import { useGlobalStore } from "../store";

export namespace BaseApi {
    export interface ErrorResponseData {
        message: string,
        response: {
            data: {
                detail: string
            },
            status: number,
            statusText: string
        }
    }
    interface CustomAxiosRequestConfig extends AxiosRequestConfig {
        _successText?: string
    }
    const apiClient = axios.create({
        baseURL: import.meta.env.VITE_BASE_URL,
        timeout: 3000,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    apiClient.interceptors.request.use((config) => {
        const store = useGlobalStore()
        store.setIsLoading(true)
        const token = getToken()
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    }, (error) => {
        const store = useGlobalStore()
        store.setIsLoading(false)
        store.createAlertData({ type: "error", text: error })
        return Promise.reject(error)
    });

    apiClient.interceptors.response.use((response) => {
        const store = useGlobalStore()
        store.setIsLoading(false)
        return response
    }, (error) => {
        const store = useGlobalStore()
        store.setIsLoading(false)
        if (error.code === 'ECONNABORTED') {
            store.createAlertData({ type: "error", text: "請求超時" })
        } else {
            const errorMessage = error?.response?.data?.detail || error.message
            store.createAlertData({ type: "error", text: errorMessage })

            const httpCode = error.response.status
            if (httpCode === 401) { //未認證
                removeTokenAndRedirectToLogin()
            }
        }
        return Promise.reject(error)
    });

    interface ErrorType { }
    interface FailResponse {
        response: undefined;
        error: ErrorType;
    }
    interface SuccessResponse<T = any> {
        response: T;
        error: undefined;
    }
    export type ResponseType<T> = SuccessResponse<T> | FailResponse
    export const getApi = async <responseData>(url: string, config?: AxiosRequestConfig, successText?: string): Promise<ResponseType<responseData>> => {
        return await apiClient.get(url, config).then(response => {
            const store = useGlobalStore()
            if (successText) {
                store.createAlertData({ type: "success", text: successText })
            }
            return { response: response.data as responseData, error: undefined }
        }).catch(error => {
            return { response: undefined, error }
        })
    };

    export const postApi = async <postData, responseData>(url: string, data?: postData, config?: CustomAxiosRequestConfig, successText?: string): Promise<ResponseType<responseData>> => {
        return await apiClient.post(url, data, config).then(response => {
            const store = useGlobalStore()
            if (successText) {
                store.createAlertData({ type: "success", text: successText || "新增成功" })
            }
            return { response: response.data as responseData, error: undefined }
        }).catch(error => {
            return { response: undefined, error }
        })
    };

    export const putApi = async <putData, responseData>(url: string, data: putData, config?: CustomAxiosRequestConfig, successText?: string): Promise<ResponseType<responseData>> => {
        return await apiClient.put(url, data, config).then(response => {
            const store = useGlobalStore()
            if (successText) {
                store.createAlertData({ type: "success", text: successText || "更新成功" })
            }
            return { response: response.data as responseData, error: undefined }
        }).catch(error => {
            return { response: undefined, error }
        })
    };
    export const deleteApi = async <responseData>(url: string, config?: CustomAxiosRequestConfig, successText?: string): Promise<ResponseType<responseData>> => {
        return await apiClient.delete(url, config).then(response => {
            const store = useGlobalStore()
            if (successText) {
                store.createAlertData({ type: "success", text: successText || "刪除成功" })
            }
            return { response: response.data as responseData, error: undefined }
        }).catch(error => {
            return { response: undefined, error }
        })
    };
}

class CrudCommonClass<
    CreateData,
    UpdateData = Partial<CreateData>,
    ReadData = CreateData & { id: number }
> {
    crudPrefix: string
    constructor(private urlPrefix: string) {
        this.crudPrefix = "crud"
    }
    getByIdApi(id: number) {
        return BaseApi.getApi<ReadData>(`${this.crudPrefix}/${this.urlPrefix}/${id}`)
    }
    getAllApi() {
        return BaseApi.getApi<ReadData[]>(`${this.crudPrefix}/${this.urlPrefix}`)
    }
    createApi(createData: CreateData) {
        return BaseApi.postApi<CreateData, ReadData>(`${this.crudPrefix}/${this.urlPrefix}`, createData, undefined, "新增成功")
    }
    updateApi(id: number, updateData: UpdateData) {
        return BaseApi.putApi<UpdateData, ReadData>(`${this.crudPrefix}/${this.urlPrefix}/${id}`, updateData, undefined, "修改成功")
    }
    deleteApi(id: number) {
        return BaseApi.deleteApi(`${this.crudPrefix}/${this.urlPrefix}/${id}`, undefined, "刪除成功")
    }
}
export namespace ToppingApi {
    export type CreateData = { name: string, price: number }
    export type UpdateData = CreateData
    export type GetResponse = CreateData & { id: number }
    export const CRUD =
        new CrudCommonClass<CreateData, UpdateData, GetResponse>("topping")
}

export namespace DrinkApi {
    export type CreateData = { name: string, price: number }
    export type UpdateData = CreateData
    export type GetResponse = CreateData & { id: number }
    export const CRUD =
        new CrudCommonClass<CreateData, UpdateData, GetResponse>("drink")
}

// export namespace StoreApi {
//     export type CreateData = { name: string }
//     export type UpdateData = CreateData
//     export type GetResponse = CreateData & { id: number }
//     export const CRUD =
//         new CrudCommonClass<CreateData, UpdateData, GetResponse>("store")
// }

export namespace UserApi {
    export type GetResponse = { id: number, email: string, role_str: USER_ROLE }
    export type CreateData = { email: string, password: string, role: USER_ROLE, password2: string }
    export type UpdateData = { password: string, role: USER_ROLE }
    export const CRUD =
        new CrudCommonClass<CreateData, UpdateData, GetResponse>("user")
    export const updatePasswordApi = async (id: number, new_password: string) => {
        return await BaseApi.putApi(`crud/user/put_password/${id}`, { new_password }, undefined, "密碼修改成功")
    }
    export const updateRoleApi = async (id: number, new_role: USER_ROLE) => {
        return await BaseApi.putApi(`crud/user/put_role/${id}`, { new_role }, undefined, "角色修改成功")
    }
}
export namespace OrderItemApi {
    export type CreateData = {
        drink_id: number
        topping_ids: number[]
        ice_content: ICE_CONTENT
        sugar_content: SUGAR_CONTENT
    }
}

export namespace OrderApi {
    export type GetResponse = {
        id: number,
        created_at: string,
        total_price: number,
        order_items: {
            price: number
            ice_content: string
            sugar_content: string
            drink_id: number
            drink_name: string
            topping_name_list: string[]
        }[]
    }
    export type CreateData = OrderItemApi.CreateData[]
    export const getAllApi = async () => {
        return await BaseApi.getApi<GetResponse[]>("crud/order")
    }
    export const createApi = async (createData: CreateData) => {
        return await BaseApi.postApi("crud/order", createData, undefined, "訂單新增成功")
    }
    export const deleteApi = async (id: number) => {
        return await BaseApi.deleteApi(`crud/order/${id}`)
    }
}
