import random
import string
import math
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector


class OlaDataGenerator:
    def __init__(self, rows=100000):
        self.rows = rows
        self.start_date = datetime(2025, 11, 1)

        self.vehicle_types = [
            "Auto", "Prime Plus", "Prime Sedan", "Mini",
            "Bike", "eBike", "Prime SUV"
        ]

        self.payment_methods = [
            "UPI", "Cash", "Credit Card", "Debit Card", "Ola Money"
        ]

        self.driver_cancel_reasons = [
            "Personal & Car related issues",
            "Customer related issue",
            "The customer was coughing/sick",
            "More than permitted people in there"
        ]

        self.pune_areas = [
            "Hinjewadi","Baner","Aundh","Wakad","Kothrud","Karve Nagar",
            "Shivaji Nagar","Deccan","Swargate","Hadapsar","Magarpatta",
            "Viman Nagar","Kharadi","Yerwada","Kalyani Nagar","Kondhwa",
            "Bibwewadi","Dhankawadi","Warje","Pashan","Balewadi",
            "Bavdhan","Sinhagad Road","Manjri","Mundhwa","Camp",
            "Fatima Nagar","Wanowrie","Nigdi","Akurdi","Chinchwad",
            "Pimpri","Bhosari","Alandi","Mosshi","Narhe","Ambegaon",
            "Katraj","Taljai","FC Road","JM Road","Model Colony",
            "Erandwane","Prabhat Road","Sadashiv Peth","Rasta Peth",
            "Kasba Peth"
        ]

    def booking_id(self):
        return "CNR" + "".join(random.choices(string.digits, k=7))

    def booking_status(self):
        return random.choices(
            ["Successfull", "Cancelled by Customer", "Cancelled by Driver", "Incomplete"],
            weights=[62, 7, 18, 5],
            k=1
        )[0]

    def order_value(self):
        r = random.random()
        if r <= 0.70:
            return random.randint(100, 499)
        elif r <= 0.98:
            return random.randint(500, 999)
        else:
            return random.randint(1000, 1800)

    def generate(self):
        rows = []

        for _ in range(self.rows):
            date = self.start_date + timedelta(days=random.randint(0, 29))
            status = self.booking_status()
            vehicle = random.choice(self.vehicle_types)

            row = {
                "Date": date.date(),
                "Time": f"{random.randint(0,23)}:{random.randint(0,59):02}",
                "Booking_ID": self.booking_id(),
                "Booking_Status": status,
                "Customer_ID": f"CUST{random.randint(10000,99999)}",
                "Vehicle_Type": vehicle,
                "Pickup_Location": random.choice(self.pune_areas),
                "Drop_Location": random.choice(self.pune_areas),
                "Avg_VTAT": None,
                "Avg_CTAT": None,
                "Cancelled_Rides_by_Customer": None,
                "Reason_for_cancelling_by_Customer": None,
                "Cancelled_Rides_by_Driver": None,
                "Driver_Cancel_Reason": None,
                "Incomplete_Rides": None,
                "Incomplete_Rides_Reason": None,
                "Booking_Value": None,
                "Payment_Method": None,
                "Ride_Distance": None,
                "Driver_Ratings": None,
                "Customer_Rating": None
            }

            if status == "Successfull":
                row["Avg_VTAT"] = round(random.uniform(2, 10), 2)
                row["Avg_CTAT"] = round(random.uniform(5, 15), 2)
                row["Booking_Value"] = self.order_value()
                row["Ride_Distance"] = round(random.uniform(1, 35), 2)
                row["Driver_Ratings"] = round(random.uniform(3.5, 5.0), 1)
                row["Customer_Rating"] = round(random.uniform(3.5, 5.0), 1)
                row["Payment_Method"] = random.choices(
                    self.payment_methods,
                    weights=[45, 20, 15, 10, 10],
                    k=1
                )[0]

            elif status == "Cancelled by Customer":
                row["Cancelled_Rides_by_Customer"] = 1
                row["Reason_for_cancelling_by_Customer"] = random.choice([
                    "Driver is not moving towards pickup location",
                    "Driver asked to cancel",
                    "Change of plans",
                    "Wrong Address",
                    "AC is not working" if vehicle not in ["Auto","Bike","eBike"] else "Change of plans"
                ])

            elif status == "Cancelled by Driver":
                row["Cancelled_Rides_by_Driver"] = 1
                row["Driver_Cancel_Reason"] = random.choice(self.driver_cancel_reasons)

            else:
                row["Incomplete_Rides"] = 1
                row["Incomplete_Rides_Reason"] = random.choice(
                    ["Customer Demand", "Vehicle Breakdown", "Other Issue"]
                )

            rows.append(row)

        return pd.DataFrame(rows)

    def save_csv(self, df):
        df.to_csv("ola_bookings.csv", index=False)
        print("CSV saved successfully")

    def save_mysql(self, df):
        print("Connecting to MySQL...")

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            port=3306
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS ola_data")
        cursor.execute("USE ola_data")
        cursor.execute("DROP TABLE IF EXISTS bookings")

        cursor.execute("""
        CREATE TABLE bookings (
            `Date` DATE,
            `Time` VARCHAR(5),
            `Booking_ID` VARCHAR(12),
            `Booking_Status` VARCHAR(30),
            `Customer_ID` VARCHAR(20),
            `Vehicle_Type` VARCHAR(20),
            `Pickup_Location` VARCHAR(50),
            `Drop_Location` VARCHAR(50),
            `Avg_VTAT` FLOAT,
            `Avg_CTAT` FLOAT,
            `Cancelled_Rides_by_Customer` INT,
            `Reason_for_cancelling_by_Customer` VARCHAR(100),
            `Cancelled_Rides_by_Driver` INT,
            `Driver_Cancel_Reason` VARCHAR(100),
            `Incomplete_Rides` INT,
            `Incomplete_Rides_Reason` VARCHAR(50),
            `Booking_Value` INT,
            `Payment_Method` VARCHAR(20),
            `Ride_Distance` FLOAT,
            `Driver_Ratings` FLOAT,
            `Customer_Rating` FLOAT
        )
        """)

        columns = ",".join(f"`{c}`" for c in df.columns)
        placeholders = ",".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO bookings ({columns}) VALUES ({placeholders})"

        def clean(x):
            if x is None:
                return None
            if isinstance(x, float) and math.isnan(x):
                return None
            return x

        data = [
            tuple(clean(v) for v in row)
            for row in df.itertuples(index=False, name=None)
        ]

        BATCH_SIZE = 1000
        total = len(data)

        for i in range(0, total, BATCH_SIZE):
            cursor.executemany(insert_query, data[i:i+BATCH_SIZE])
            print(f"Inserted {min(i+BATCH_SIZE, total)} / {total}")

        cursor.execute("SELECT COUNT(*) FROM bookings")
        print("Final rows in table:", cursor.fetchone()[0])

        cursor.close()
        conn.close()
        print("MySQL save completed successfully")


if __name__ == "__main__":
    generator = OlaDataGenerator(rows=100000)

    df = generator.generate()
    print(df.head())
    print(df.shape)

    generator.save_csv(df)
    generator.save_mysql(df)
