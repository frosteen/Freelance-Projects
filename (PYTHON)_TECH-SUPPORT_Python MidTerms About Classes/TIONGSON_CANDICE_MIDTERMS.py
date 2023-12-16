class Phone:
    def __init__(self, brand, phone_name, performance, display, storage, camera, battery, ram, price):
        self.brand = brand
        self.phone_name = phone_name
        self.performance = performance
        self.display = display
        self.storage = storage
        self.camera = camera
        self.battery = battery
        self.ram = ram
        self.available = "No"
        self.second_hand = "No"
        self.price = price

    def mark_as_available(self):
        self.available = "Yes"

    def mark_as_second_hand(self):
        self.second_hand = "Yes"

    def print_phone(self):
        print(
"""{} {}:
SUMMARY:
Performance: {}
Display: {}" ({} cm)
Storage: {} GB
Camera: {} MP
Battery: {} mAh
Ram: {} GB
Price: P{}
Available: {}
2nd Hand: {}""".format(self.brand,self.phone_name,self.performance,self.display,round(self.display*2.54,2),self.storage,
           self.camera,self.battery,self.ram,self.price,self.available,self.second_hand))

phone_1 = Phone("APPLE", "IPHONE 5S", "Dual Core", 4, 16, 8, 1560, 1, 8000)
phone_1.mark_as_available()
phone_1.mark_as_second_hand()
phone_1.print_phone()

print("----------------------------------")

phone_2 = Phone("ASUS", "ZENFONE MAX M2", "Octa Core", 6.26, 32, 15, 4000, 3, 9000)
phone_2.mark_as_available()
phone_2.print_phone()

print("----------------------------------")

phone_3 = Phone("VIVO", "Y95", "Octa Core", 6.22, 64, 15, 4030, 4, 14000)
phone_3.print_phone()

print("----------------------------------")

phone_4 = Phone("MICROMAX", "INFINITY N12", "Octa Core", 6.19, 32, 18, 4000, 3, 5000)
phone_4.mark_as_available()
phone_4.mark_as_second_hand()
phone_4.print_phone()
