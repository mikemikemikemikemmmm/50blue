export enum USER_ROLE {
    "CLERK" = "CLERK",
    "MANAGER" = "MANAGER"
}
export const USER_ROLE_LIST = Object.values(USER_ROLE)
export const TOKEN_KEY_IN_LOCALSTORAGE = "token"

export enum ICE_CONTENT {
    "less" = "less",
    "regular" = "regular",
    "half" = "half"
}
export enum SUGAR_CONTENT {
    "less" = "less",
    "regular" = "regular",
    "half" = "half"
}
export const ICE_CONTENT_VALUE_LIST = Object.values(ICE_CONTENT)
export const SUGAR_CONTENT_VALUE_LIST = Object.values(SUGAR_CONTENT)