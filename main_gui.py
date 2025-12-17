import dearpygui.dearpygui as dpg
from transport.client import Client
from transport.van import Van
from transport.ship import Ship
from transport.company import TransportCompany
import json

transport_company = TransportCompany("Транспортная компания'би-би'")

status_message = ""

def update_status(message):
    global status_message
    status_message = message
    dpg.set_value("status_text", f"Статус: {status_message}")

def clients_table():
    with dpg.table(header_row=True, tag="clients_table"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Имя")
        dpg.add_table_column(label="Вес груза (т)")
        dpg.add_table_column(label="VIP")

def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    for i, client in enumerate(transport_company.clients, start=1):
        with dpg.table_row(parent="clients_table"):
            dpg.add_text(str(i))
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.is_vip else "Нет")

def add_client_window():
    with dpg.window(label="Добавить клиента", modal=True, tag="client_window"):
        dpg.add_text("ИМя клиента:")
        name_input = dpg.add_input_text()
        dpg.add_text("Вес груза (тонн):")
        cargo_weight = dpg.add_input_text()
        is_vip = dpg.add_checkbox(label="VIP-клиент")
        
        def save_client():
            try:
                name = dpg.get_value(client_name_input)
                if not name:
                    raise ValueError("Имя клиента не может быть пустым.")

                weight = float(dpg.get_value(cargo_weight_input))
                if weight <= 0:
                    raise ValueError("Вес груза должен быть положительным числом.")

                is_vip = dpg.get_value(is_vip_checkbox)

                client = Client(name,weight,is_vip)
                transport_company.add_client(client)
                dpg.delete_item("client_window")
                update_clients_table()
            except ValueError as e:
                update_status(f"Ошибка: {e}")
                dpg.set_value(cargo_weight_input, "")
            except: pass
        
        dpg.add_button(label="Save", callback=save)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("win1"))

def add_vehicle():
    with dpg.window(label="Add Vehicle", modal=True, tag="win2"):
        t = dpg.add_combo(items=["Van", "Ship"])
        dpg.add_text("Capacity (t):")
        c = dpg.add_input_text()
        dpg.add_text("Name:")
        n = dpg.add_input_text()
        f = dpg.add_checkbox(label="Refrigerator")
        
        def save():
            try:
                name = dpg.get_value(name_input)
                weight = float(dpg.get_value(cargo_weight))
                is_vip = dpg.get_value(is_vip)
                
                new_client = Client(name,weight,is_vip)
                transport_company.add_client(new_client)
                dpg.delete_item("client_window")
            except:
                pass
        dpg.add_button(label="Сохранить", callback=save_client)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("client_window"))

def add_vehicle():
    with dpg.window(label="Добавить транспорт", modal=True, tag="vehicle_window"):
        vehicle_type_combo = dpg.add_combo(items=["Фургон", "Корабль"])
        dpg.add_text("Грузоподъёмность (тонн):")
        capacity_input = dpg.add_input_text()

        dpg.add_text("Название (только для корабля):")
        ship_name_input = dpg.add_input_text()

        has_refrigerator_checkbox = dpg.add_checkbox(label="Есть холодильник")

def save_vehicle():
    vehicle_type = dpg.get_value(vehicle_type_combo)
    capacity = float(dpg.get_value(capacity_input))
    if capacity <= 0:
        raise ValueError("Грузоподъёмность должна быть положительным числом.")

    ship_name = dpg.get_value(ship_name_input)
    if vehicle_type == "Корабль" and not ship_name:
        raise ValueError("Название корабля не может быть пустым.")

    has_refrigerator = dpg.get_value(has_refrigerator_checkbox)

    if vehicle_type == "Фургон":
        new_vehicle = Van(capacity, has_refrigerator)
    else:
        new_vehicle = Ship(capacity, ship_name)

    transport_company.add_vehicle(new_vehicle)
    update_status(f"Транспортное средство добавлено.")
    dpg.delete_item("vehicle_window")
    dpg.set_value(capacity_input, "")

dpg.add_button(label="Сохранить", callback=save_vehicle)
dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_window"))

def optimize():
    try:
        transport_company.optimize_distibution()
    except:
        pass

def export():
    try:
        data = {"clients":[], "vehicles": []}

        for client in transport_company.clients:
            data["clients"].append({
                "name":client.name,
                "weight": client.cargo_weight,
                "vip": client.is_vip
            })
        
        for vehicle in transport_company.vehicles:
            if isinstance(vehicle, Van):
                data["vehicles"].append({
                    "type":"van",
                    "id":vehicle.vehicle_id,
                    "capacity":vehicle.capacity,
                    "refrigerator":vehicle.has_refrigerator
                }) 
            elif isinstance(vehicle,Ship):
                data["vehicles"].append({
                    "type": "ship",
                    "id": vehicle.vehicle_id,
                    "name": vehicle.name,
                    "capacity": vehicle.capacity
                })
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except:
        pass

def main():
    dpg.create_context()

    dpg.create_viewport(title='Логистика транспорта', width=600, height=400)

    with dpg.window(label="Главное окно", width=600, height=400):
        dpg.add_button(label="Добавить клиента", callback=add_client_window)
        dpg.add_button(label="Добавить транспорт", callback=add_vehicle_window)
        dpg.add_button(label="Оптимизировать", callback=optimize_cargo)
        dpg.add_button(label="Экспорт в JSON", callback=export_to_json)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
if __name__ == "__main__":
    main()