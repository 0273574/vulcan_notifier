import asyncio
import logging
from vulcan_notifier.config import VulcanConfig
from vulcan_notifier.vulcan_connector import VulcanConnector
from vulcan_notifier.email_sender import EmailSender
from vulcan_notifier.notification_manager import NotificationManager

class VulcanNotifier:
    def __init__(self, config_path='config.json'):
        self.config = VulcanConfig.load_config(config_path)
        self.vulcan_connector = VulcanConnector(self.config)
        self.email_sender = EmailSender(self.config.email_config)
        self.notification_manager = NotificationManager()

    async def run(self):
        logging.basicConfig(level=logging.INFO)
        
        while True:
            try:
                await self.check_notifications()
                await asyncio.sleep(self.config.check_interval)
            except Exception as e:
                logging.error(f"Błąd: {e}")
                await asyncio.sleep(self.config.error_retry_interval)

    async def check_notifications(self):
        new_grades = await self.vulcan_connector.get_new_grades()
        new_comments = await self.vulcan_connector.get_new_comments()
        upcoming_tests = await self.vulcan_connector.get_upcoming_tests()

        if new_grades:
            await self.notification_manager.process_grades(new_grades, self.email_sender)
        if new_comments:
            await self.notification_manager.process_comments(new_comments, self.email_sender)
        if upcoming_tests:
            await self.notification_manager.process_tests(upcoming_tests, self.email_sender)

async def main():
    notifier = VulcanNotifier()
    await notifier.run()

if __name__ == "__main__":
    asyncio.run(main())
