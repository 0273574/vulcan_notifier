import asyncio
import logging
from typing import List, Dict
from vulcan import Vulcan, Keystore, Account, VulcanAPIException, InvalidSignatureValuesException

class VulcanConnector:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.last_grades = []
        self.last_comments = []
        self.last_tests = []

    async def connect(self):
        try:
            keystore = await Keystore.create()
            await keystore.load(self.config.firebase_token, self.config.symbol)  # Ensure token is passed correctly
            
            # Register account using PIN
            account = await Account.register(keystore, self.config.pin)
            self.client = Vulcan(keystore, account)
        except (VulcanAPIException, InvalidSignatureValuesException) as e:
            logging.error(f"Błąd logowania: {e}")
            raise

    async def get_new_grades(self) -> List[Dict]:
        if not self.client:
            await self.connect()
        
        try:
            grades = await self.client.data.get_grades()  # Fetch grades from API
            new_grades = [grade for grade in grades if grade not in self.last_grades]
            self.last_grades = grades
            return new_grades
        except Exception as e:
            logging.error(f"Błąd pobierania ocen: {e}")
            return []

    async def get_new_comments(self) -> List[Dict]:
        if not self.client:
            await self.connect()
        
        try:
            comments = await self.client.data.get_comments()  # Fetch comments from API
            new_comments = [comment for comment in comments if comment not in self.last_comments]
            self.last_comments = comments
            return new_comments
        except Exception as e:
            logging.error(f"Błąd pobierania komentarzy: {e}")
            return []

    async def get_upcoming_tests(self) -> List[Dict]:
        if not self.client:
            await self.connect()
        
        try:
            tests = await self.client.data.get_tests()  # Fetch tests from API
            new_tests = [test for test in tests if test not in self.last_tests]
            self.last_tests = tests
            return new_tests
        except Exception as e:
            logging.error(f"Błąd pobierania testów: {e}")
            return []

# Fix the config class to correctly use attributes
class VulcanConfig:
    def __init__(self, firebase_token: str, pin: str, symbol: str):
        # Ensure the attribute names match the ones used in VulcanConnector
        self.firebase_token = firebase_token  # Store the Firebase token
        self.pin = pin  # Store the PIN
        self.symbol = symbol  # Store the school symbol

# Example usage
async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        # Replace the following values with actual credentials
        firebase_token = "your_firebase_token"  # Replace with your Firebase token
        pin = "your_pin"  # PIN provided during account setup
        symbol = "your_symbol"  # School symbol for Vulcan API

        # Initialize the config with the correct values
        config = VulcanConfig(firebase_token, pin, symbol)

        # Initialize the connector with the config
        vulcan_connector = VulcanConnector(config)

        # Connect and fetch grades
        await vulcan_connector.connect()
        new_grades = await vulcan_connector.get_new_grades()
        print("New Grades:", new_grades)

    except Exception as e:
        logging.error(f"Błąd: {e}")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
