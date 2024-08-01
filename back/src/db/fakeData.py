from src.models.drink import DrinkModel
from src.models.order import CreateSchema as OrderCreate
from src.models.order_item import CreateSchema as OrderItemCreate
from src.models.store import CreateSchema as StoreCreate
from src.models.topping import CreateSchema as ToppingCreate
from src.models.user import CreateSchema as UserCreate, Role
# from src.depends.index import get_db


# async def create_fake_data():
#     session = get_db().__next__()
#     drink1 = DrinkModel(name="奶茶", price=20,order_item=[])
#     drink2 = DrinkModel(name="紅茶", price=10,order_item=[])
#     drink3 = DrinkModel(name="綠茶", price=15,order_item=[])
#     # store1 = StoreCreate(name="台北店")
#     # store2 = StoreCreate(name="台南店")
#     # store3 = StoreCreate(name="台中店")
#     # topping1 = ToppingCreate(name="珍珠", price=20)
#     # topping2 = ToppingCreate(name="紅豆", price=10)
#     # topping3 = ToppingCreate(name="芋圓", price=15)
#     # user1 = UserCreate(email="a@gmail.com", password="123", role=Role.CEO)
#     # user2 = UserCreate(email="b@gmail.com", password="123", role=Role.MANAGER)
#     # user3 = UserCreate(email="c@gmail.com", password="123", role=Role.CLERK)
#     session.add_all([
#         drink1,
#         drink2,
#         drink3]
#         # store1,
#         # store2,
#         # store3,
#         # topping1,
#         # topping2,
#         # topping3,
#         # user1,
#         # user2,
#         # user3]
#     )
#     session.commit()
#     # order_item1 = OrderItemCreate(
#     #     drink_id=1, ice_content="half", toppings_ids=[1, 2], price=400
#     # )
