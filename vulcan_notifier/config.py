import json
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EmailConfig:
    smtp_server: str
    smtp_port: int
    sender_email: str
    sender_password: str
    recipient_email: str

@dataclass
class VulcanConfig:
    username: str
    password: str
    symbol: str
    email_config: EmailConfig
    check_interval: int = 300  # Co 5 minut
    error_retry_interval: int = 1800  # Co 30 minut w razie błędu

    @classmethod
    def load_config(cls, config_path: str = 'config.json'):
        """
        Wczytuje konfigurację z pliku JSON
        
        Args:
            config_path (str): Ścieżka do pliku konfiguracyjnego
        
        Returns:
            VulcanConfig: Obiekt konfiguracji
        """
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            return cls(
                username=config_data['vulcan_username'],
                password=config_data['vulcan_password'],
                symbol=config_data['vulcan_symbol'],
                email_config=EmailConfig(
                    smtp_server=config_data['smtp_server'],
                    smtp_port=config_data['smtp_port'],
                    sender_email=config_data['sender_email'],
                    sender_password=config_data['sender_password'],
                    recipient_email=config_data['recipient_email']
                ),
                # Opcjonalne parametry z domyślnymi wartościami
                check_interval=config_data.get('check_interval', 300),
                error_retry_interval=config_data.get('error_retry_interval', 1800)
            )
        except FileNotFoundError:
            print(f"Nie znaleziono pliku konfiguracyjnego: {config_path}")
            raise
        except KeyError as e:
            print(f"Brak wymaganego klucza w konfiguracji: {e}")
            raise
