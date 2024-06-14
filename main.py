import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import re
from client_functions import ClientFunctions
from realtor_functions import RealtorFunctions
from manager_functions import ManagerFunctions


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Management")
        self.root.geometry("800x600")

        # Load background image
        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_menu()

    def main_menu(self):
        self.clear_window()
        self.create_title("Виберіть свою роль")

        self.create_button("Клієнт", self.client_menu).pack(pady=5)
        self.create_button("Ріелтор", self.realtor_menu).pack(pady=5)
        self.create_button("Менеджер", self.manager_menu).pack(pady=5)
        self.create_button("Вихід", self.root.quit).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_button(self, text, command):
        return tk.Button(self.root, text=text, command=command, width=35, height=2)

    def create_title(self, text):
        label = tk.Label(self.root, text=text, font=('Helvetica', 18, 'bold'), bg='#add8e6')
        label.pack(pady=10)
        return label

    def create_table(self, columns, data):
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=100)
        for item in data:
            tree.insert('', tk.END, values=item)
        tree.pack(pady=5, fill=tk.BOTH, expand=True)
        return tree

    def client_menu(self):
        self.clear_window()
        self.create_title("Клієнт")

        self.create_button("Реєстрація", self.client_registration).pack(pady=5)
        self.create_button("Перегляд списку нерухомостей", self.view_properties).pack(pady=5)
        self.create_button("Найдорожча нерухомість", self.most_expensive_property).pack(pady=5)
        self.create_button("Середня вартість нерухомостей", self.average_property_price).pack(pady=5)
        self.create_button("Нерухомість з найбільшою кількістю кімнат", self.property_with_most_rooms).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def client_registration(self):
        self.clear_window()
        self.create_title("Реєстрація")

        tk.Label(self.root, text="Назва фірми", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=52)
        firm_entry = tk.Entry(self.root)
        firm_entry.place(x=340, y=54)
        firm_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        firm_error.place(x=340, y=78)

        tk.Label(self.root, text="Ім'я", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=92)
        name_entry = tk.Entry(self.root)
        name_entry.place(x=340, y=94)
        name_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        name_error.place(x=340, y=118)

        tk.Label(self.root, text="Номер телефону", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=132)
        phone_entry = tk.Entry(self.root)
        phone_entry.place(x=340, y=134)
        phone_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        phone_error.place(x=340, y=158)

        tk.Label(self.root, text="Тип послуги", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=172)
        type_combobox = ttk.Combobox(self.root, values=["Купівля", "Оренда"])
        type_combobox.place(x=340, y=174)
        type_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        type_error.place(x=340, y=198)

        def validate_phone(phone):
            pattern = r'^0\d{9}$'
            return re.match(pattern, phone)

        def register():
            firm = firm_entry.get()
            name = name_entry.get()
            phone = phone_entry.get()
            type = type_combobox.get()
            valid = True

            if not firm:
                firm_error.config(text="Назва фірми не може бути порожньою")
                valid = False
            else:
                firm_error.config(text="")

            if not name:
                name_error.config(text="Ім'я не може бути порожнім")
                valid = False
            else:
                name_error.config(text="")

            if not phone:
                phone_error.config(text="Номер телефону не може бути порожнім")
                valid = False
            elif not validate_phone(phone):
                phone_error.config(text="Номер телефону повинен бути у форматі 0ХХХХХХХХХ")
                valid = False
            else:
                phone_error.config(text="")
                phone = "380" + phone[1:]  # Додавання коду країни 380

            if not type:
                type_error.config(text="Тип послуги не може бути порожнім")
                valid = False
            else:
                type_error.config(text="")

            if valid:
                ClientFunctions.registration(firm, name, phone, type)
                messagebox.showinfo("Успіх", "Реєстрація успішна")
                self.client_menu()
            else:
                messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")

        self.create_button("Зареєструватись", register).place(x=300, y=222)
        self.create_button("Назад", self.client_menu).place(x=300, y=272)

    def view_properties(self):
        self.clear_window()
        self.create_title("Список нерухомостей")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        properties = ClientFunctions.view_properties()
        self.create_table(columns, properties)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def most_expensive_property(self):

        self.clear_window()
        self.create_title("Найдорожча нерухомість")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        property = [ClientFunctions.most_expensive_property()]
        print(property)
        self.create_table(columns, property)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def average_property_price(self):
        self.clear_window()
        self.create_title("Середня вартість нерухомостей")

        avg_price = ClientFunctions.average_property_price()
        tk.Label(self.root, text=f"Середня вартість: {avg_price}").pack(pady=10)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def property_with_most_rooms(self):
        self.clear_window()
        self.create_title("Нерухомість з найбільшою кількістю кімнат")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        property = [ClientFunctions.property_with_most_rooms()]
        self.create_table(columns, property)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def realtor_menu(self):
        self.clear_window()
        self.create_title("Ріелтор")

        self.create_button("Перегляд списку нерухомостей", self.view_properties_realtor).pack(pady=5)
        self.create_button("Додати нову нерухомість", self.add_property).pack(pady=5)
        self.create_button("Видалити нерухомість", self.delete_property).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def view_properties_realtor(self):
        self.clear_window()
        self.create_title("Список нерухомостей")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        properties = RealtorFunctions.view_properties()
        self.create_table(columns, properties)

        self.create_button("Назад", self.realtor_menu).pack(pady=5)

    def add_property(self):
        self.clear_window()
        self.create_title("Додати нову нерухомість")

        tk.Label(self.root, text="Адреса", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=52)
        address_entry = tk.Entry(self.root)
        address_entry.place(x=340, y=54)
        address_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        address_error.place(x=340, y=78)

        tk.Label(self.root, text="Площа", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=92)
        area_entry = tk.Entry(self.root)
        area_entry.place(x=340, y=94)
        area_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        area_error.place(x=340, y=118)

        tk.Label(self.root, text="Рік побудови", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=132)
        year_entry = tk.Entry(self.root)
        year_entry.place(x=340, y=134)
        year_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        year_error.place(x=340, y=158)

        tk.Label(self.root, text="Поверх", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=172)
        floor_entry = tk.Entry(self.root)
        floor_entry.place(x=340, y=174)
        floor_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        floor_error.place(x=340, y=198)

        tk.Label(self.root, text="Ціна", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=212)
        price_entry = tk.Entry(self.root)
        price_entry.place(x=340, y=214)
        price_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        price_error.place(x=340, y=238)

        tk.Label(self.root, text="Кількість кімнат", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=252)
        rooms_entry = tk.Entry(self.root)
        rooms_entry.place(x=340, y=254)
        rooms_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        rooms_error.place(x=340, y=278)

        def add():
            address = address_entry.get()
            area = area_entry.get()
            year = year_entry.get()
            floor = floor_entry.get()
            price = price_entry.get()
            rooms = rooms_entry.get()
            valid = True

            if not address:
                address_error.config(text="Адреса не може бути порожньою")
                valid = False
            else:
                address_error.config(text="")

            if not area:
                area_error.config(text="Площа не може бути порожньою")
                valid = False
            else:
                area_error.config(text="")

            if not year:
                year_error.config(text="Рік побудови не може бути порожнім")
                valid = False
            else:
                year_error.config(text="")

            if not floor:
                floor_error.config(text="Поверх не може бути порожнім")
                valid = False
            else:
                floor_error.config(text="")

            if not price:
                price_error.config(text="Ціна не може бути порожньою")
                valid = False
            else:
                price_error.config(text="")

            if not rooms:
                rooms_error.config(text="Кількість кімнат не може бути порожньою")
                valid = False
            else:
                rooms_error.config(text="")

            if valid:
                area = int(area)
                year = int(year)
                floor = int(floor)
                price = float(price)
                rooms = int(rooms)

                RealtorFunctions.add_property(address, area, year, floor, price, rooms)
                messagebox.showinfo("Успіх", "Нерухомість додана успішно")
                self.realtor_menu()
            else:
                messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")

        self.create_button("Додати", add).place(x=280, y=302)
        self.create_button("Назад", self.realtor_menu).place(x=280, y=362)

    def delete_property(self):
        self.clear_window()
        self.create_title("Видалити нерухомість")

        tk.Label(self.root, text="ID нерухомості", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=72)
        id_entry = tk.Entry(self.root)
        id_entry.place(x=340, y=74)
        id_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        id_error.place(x=340, y=98)

        def delete():
            property_id = id_entry.get()
            if not property_id:
                id_error.config(text="ID нерухомості не може бути порожнім")
                messagebox.showerror("Помилка", "Будь ласка, введіть ID нерухомості")
                return
            else:
                id_error.config(text="")

            property_id = int(property_id)
            RealtorFunctions.delete_property(property_id)
            messagebox.showinfo("Успіх", "Нерухомість видалена успішно")
            self.realtor_menu()

        self.create_button("Видалити", delete).place(x=280, y=112)
        self.create_button("Назад", self.realtor_menu).place(x=280, y=162)

    def manager_menu(self):
        self.clear_window()
        self.create_title("Менеджер")

        self.create_button("Перегляд списку клієнтів", self.view_clients).pack(pady=5)
        self.create_button("Перегляд списку ріелторів", self.view_realtors).pack(pady=5)
        self.create_button("Додати нового ріелтора", self.add_realtor).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def view_clients(self):
        self.clear_window()
        self.create_title("Список клієнтів")

        columns = ('ID', 'Назва фірми', 'Ім\'я', 'Номер телефону', 'Тип послуги', 'ID нерухомості')
        clients = ManagerFunctions.view_clients()
        self.create_table(columns, clients)

        self.create_button("Назад", self.manager_menu).pack(pady=5)

    def view_realtors(self):
        self.clear_window()
        self.create_title("Список ріелторів")

        columns = ('ID', 'Назва фірми', 'Ім\'я', 'Адреса', 'Номер телефону')
        realtors = ManagerFunctions.view_realtors()
        self.create_table(columns, realtors)

        self.create_button("Назад", self.manager_menu).pack(pady=5)

    def add_realtor(self):
        self.clear_window()
        self.create_title("Додати нового ріелтора")

        tk.Label(self.root, text="Назва фірми", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=52)
        firm_entry = tk.Entry(self.root)
        firm_entry.place(x=340, y=54)
        firm_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        firm_error.place(x=340, y=78)

        tk.Label(self.root, text="Ім'я", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=92)
        name_entry = tk.Entry(self.root)
        name_entry.place(x=340, y=94)
        name_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        name_error.place(x=340, y=118)

        tk.Label(self.root, text="Адреса", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=132)
        address_entry = tk.Entry(self.root)
        address_entry.place(x=340, y=134)
        address_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        address_error.place(x=340, y=158)

        tk.Label(self.root, text="Номер телефону", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=172)
        phone_entry = tk.Entry(self.root)
        phone_entry.place(x=340, y=174)
        phone_error = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
        phone_error.place(x=340, y=198)

        def validate_phone(phone):
            pattern = r'^0\d{9}$'
            return re.match(pattern, phone)

        def add():
            firm = firm_entry.get()
            name = name_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            valid = True

            if not firm:
                firm_error.config(text="Назва фірми не може бути порожньою")
                valid = False
            else:
                firm_error.config(text="")

            if not name:
                name_error.config(text="Ім'я не може бути порожнім")
                valid = False
            else:
                name_error.config(text="")

            if not address:
                address_error.config(text="Адреса не може бути порожньою")
                valid = False
            else:
                address_error.config(text="")

            if not phone:
                phone_error.config(text="Номер телефону не може бути порожнім")
                valid = False
            elif not validate_phone(phone):
                phone_error.config(text="Номер телефону повинен бути у форматі 0ХХХХХХХХХ")
                valid = False
            else:
                phone_error.config(text="")
                phone = "380" + phone[1:]  # Додавання коду країни 380

            if valid:
                ManagerFunctions.add_realtor(firm, name, address, phone)
                messagebox.showinfo("Успіх", "Ріелтор доданий успішно")
                self.manager_menu()
            else:
                messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")

        self.create_button("Додати", add).place(x=280, y=222)
        self.create_button("Назад", self.manager_menu).place(x=280, y=272)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
