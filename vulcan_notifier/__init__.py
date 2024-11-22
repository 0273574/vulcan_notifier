"""
Vulcan Notifier - Moduł powiadomień o ocenach i wydarzeniach szkolnych

Główne komponenty:
- config.py: Zarządzanie konfiguracją
- vulcan_connector.py: Połączenie z Vulcan API
- email_sender.py: Wysyłanie powiadomień e-mail
- notification_manager.py: Przetwarzanie powiadomień
"""

__version__ = "0.1.0"
__author__ = "Twoje Imię"
__email__ = "twoj_email@example.com"

# Lista wszystkich dostępnych modułów przy imporcie *
__all__ = [
    'VulcanConfig', 
    'VulcanConnector', 
    'EmailSender', 
    'NotificationManager'
]

from .config import VulcanConfig
from .vulcan_connector import VulcanConnector
from .email_sender import EmailSender
from .notification_manager import NotificationManager
