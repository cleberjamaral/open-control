#pip install RPi.GPIO
#sudo apt-get install sqlite3

import RPi.GPIO as GPIO
import sqlite3

DATABASE_NAME = "cards.db"
TABLE_NAME = "cards"

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Initialize SQLite database connection
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (card_number TEXT)")

print("Wiegand interface program started.")

try:
    while True:
        # Wait for falling edge on GPIO pin 14
        GPIO.wait_for_edge(14, GPIO.FALLING)
        
        # Read card number from GPIO pins 14 and 15
        card_number = ""
        for i in range(26):
            GPIO.wait_for_edge(15, GPIO.RISING)
            card_number += str(GPIO.input(15))
        
        # Insert card number into the database
        cursor.execute(f"INSERT INTO {TABLE_NAME} (card_number) VALUES (?)", (card_number,))
        conn.commit()
        print(f"Card number {card_number} stored in the database.")
        
except KeyboardInterrupt:
    pass

# Clean up GPIO and close database connection
GPIO.cleanup()
cursor.close()
conn.close()
print("Program terminated.")