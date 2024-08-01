import { USER_ROLE } from "../const"

export const toppingMock = [
    {
        id: 1, name: "珍珠", price: 20
    },
    {
        id: 2, name: "芋園", price: 20
    },
    {
        id: 3, name: "布丁", price: 20
    },
]
export const drinkMock = [
    {
        id: 1, name: "奶茶", price: 20
    },
    {
        id: 2, name: "綠茶", price: 20
    },
    {
        id: 3, name: "紅茶", price: 20
    },
]

export const storeMock = [
    {
        id: 1, name: "台北店"
    },
    {
        id: 2, name: "台中店"
    },
    {
        id: 3, name: "台南店"
    },
]
export const orderMock = [
    {
        id: 1,
        total_price: 1000,
        items: [
            {
                id: drinkMock[0].id,
                name: drinkMock[0].name,
                toppings: [
                    {
                        num: 2,
                        id: toppingMock[0].id,
                        name: toppingMock[0].name
                    }
                ]
            }
        ]
    },
]


