import psycopg2
import random
import string
import uuid  # uuid.uuid4()
import datetime

con = psycopg2.connect(
    database="postgres", user="postgres", password="1029", host="127.0.0.1", port="5432"
)

print("Database opened successfully")

cur = con.cursor()

cars_models = ["Tatra", "Man", "Renault", "Mercedes-Benz", "Камаз", "Volvo", "Iveco"]

drivers_names = [
    "Олег",
    "Вячеслав",
    "Станислав",
    "Антон",
    "Евгений",
    "Степан",
    "Илья",
    "Владислав",
    "Владимир",
    "Пётр",
]
drivers_surname = [
    "Алебашевский",
    "Голуб",
    "Даничкин",
    "Иванов",
    "Степанов",
    "Джугашвили",
    "Сидоров",
    "Петров",
    "Сырцев",
    "Андреев",
    "Дмитриенко",
    "Пуртов",
]
drivers_patronymic = [
    "Бабиджонович",
    "Александрович",
    "Иванович",
    "Георгиевич",
    "Антонович",
    "Евгеньевич",
    "Робертович",
    "Давидович",
    "Шамилевич",
    "Джейсонович",
]
fuel_brands = ["Лукоил", "Газпром", "Башнефть", "Татнефть", "Роснефть", "Шелл"]
fuel_country = [
    "Россия",
    "Венесуэла",
    "ОАЭ",
    "Саудовская Аравия",
    "Уругвай",
    "Зимбабве",
    "США",
]
transportations_citys = [
    "Москва",
    "Тюмень",
    "Новый Уренгой",
    "Нефтеюганск",
    "Сургут",
    "Санкт-Петербург",
    "Новосибирск",
    "Ростов-на-Дону",
    "Краснодар",
    "Белгород",
]
transportations_streets = [
    "Ленина",
    "Перекопская",
    "Киевская",
    "Мира",
    "Невская",
    "Колосистая",
    "Юрия Гагарина",
    "Первомайская",
    "Моторостроительная",
    "Энергетиков",
    "Первых Космонавтов",
    "Севастопольская",
    "Республики",
    "50 Лет Октября",
    "30 Лет Победы",
    "50 Лет ВЛКСМ",
    "Пермякова",
    "Текстильная",
    "Олимпийская",
    "Сургутская",
    "Суходольская",
]


cars_query = 'INSERT INTO "cars" (model, load_capacity_kg, "vin") VALUES (%(model)s, %(load_capacity_kg)s, %(vin)s)'
drivers_query = 'INSERT INTO "drivers" (name, work_experience_month, "id") VALUES (%(name)s, %(work_experience_month)s, %(id)s)'
fuel_query = (
    'INSERT INTO "fuel" (brand, "id", country) VALUES (%(brand)s, %(id)s, %(country)s)'
)
transportations_query = 'INSERT INTO "transportations" (start_date, distance_km, destination_address, "id", driver, car, fuel_1_volume_liter, fuel_1_id, fuel_2_volume_liter, fuel_2_id) VALUES (%(date)s, %(distance_km)s, %(destination_address)s, %(id)s, %(driver)s, %(car)s, %(fuel_1_volume_liter)s, %(fuel_1_id)s, %(fuel_2_volume_liter)s, %(fuel_2_id)s)'
cars_drivers_query = 'INSERT INTO "cars_drivers" (driver_id, car_vin) VALUES (%(driver_id)s, %(car_vin)s)'

drivers_id = []
cars_vin = []
fuel_id = []
transportations_id = []


# заполняем "drivers", "cars", "fuel"
for i in range(20):
    car_args = {
        "model": f"{random.choice(cars_models)}-{random.randint(100,9000)}",
        "load_capacity_kg": random.randint(1, 25) * 1000,
        "vin": "".join(random.choices(string.ascii_uppercase + string.digits, k=17)),
    }
    cars_vin.append(car_args["vin"])
    cur.execute(cars_query, car_args)

    driver_name = f"{random.choice(drivers_surname)} {random.choice(drivers_names)} {random.choice(drivers_patronymic)}"
    driver_args = {
        "name": driver_name,
        "work_experience_month": random.randint(1, 600),
        "id": str(uuid.uuid4()),
    }
    drivers_id.append(driver_args["id"])
    cur.execute(drivers_query, driver_args)

    fuel_args = {
        "brand": random.choice(fuel_brands),
        "id": str(uuid.uuid4()),
        "country": random.choice(fuel_country),
    }
    fuel_id.append(fuel_args["id"])
    cur.execute(fuel_query, fuel_args)

datetime_start = datetime.datetime(2009, 9, 15, 12, 45, 35)  # starts for, year month day h:m:s


# заполняем "transportations"
for i in range(1000):
    datetime_start += datetime.timedelta(
        hours=random.randint(1, 10),
        minutes=random.randint(1, 60),
        seconds=random.randint(1, 60),
    )
    choice = random.randint(0,1)
    transportation_args = {
        "date": f'{datetime_start.strftime("%Y-%b-%d %H:%M:%S")}+02',
        "distance_km": random.randint(1, 3500),
        "destination_address": f"{random.choice(transportations_citys)}, Ул. {random.choice(transportations_streets)}, {random.randint(1,200)}",
        "id": str(uuid.uuid4()),
        "driver": random.choice(drivers_id),
        "car": random.choice(cars_vin),
        "fuel_1_volume_liter": random.randint(500, 6000),
        "fuel_1_id": random.choice(fuel_id),
        "fuel_2_volume_liter": random.randint(500, 6000) if choice else None,
        "fuel_2_id": random.choice(fuel_id) if choice else None,
    }
    transportations_id.append(transportation_args["id"])
    cur.execute(transportations_query, transportation_args)

#  заполняем промежуточные таблицы "cars_drivers"
for i in range(1000):
    cars_drivers_args = {
        "car_vin": random.choice(cars_vin),
        "driver_id": random.choice(drivers_id),
    }
    cur.execute(cars_drivers_query, cars_drivers_args)
    

con.commit()
con.close()

print("ALL data pasted!\nDone!")
