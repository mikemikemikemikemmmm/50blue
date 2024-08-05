// import { USER_ROLE } from "../const"

// const CLERK_ALLOW = ['/topping', "/drink", "/order", "/create_order", "/login"]

// type NavAllowMock = {
//     [key in USER_ROLE]: string[]
// }
// export const mockAllowData = {
//     "CLERK": CLERK_ALLOW,
//     "MANAGER": [...CLERK_ALLOW, "/store"],
//     "CEO": [...CLERK_ALLOW, "/store", "/user"]
// } as NavAllowMock

// export const userMock = [
//     {
//         id: 1,
//         email: "a@gmail.com",
//         password: 123456,
//         role: USER_ROLE.CEO,
//         allowRoute: mockAllowData[USER_ROLE.CEO],
//         token:"1111"
//     },
//     {
//         id: 2,
//         email: "b@gmail.com",
//         password: 123456,
//         role: USER_ROLE.MANAGER,
//         allowRoute: mockAllowData[USER_ROLE.MANAGER],
//         token:"2222"
//     },
//     {
//         id: 3,
//         email: "c@gmail.com",
//         password: 123456,
//         role: USER_ROLE.CLERK,
//         allowRoute: mockAllowData[USER_ROLE.CLERK],
//         token:"3333"
//     },
// ]