"""
NYC Open Data Downloaders - Refactored with Base Class

Base class and specific downloaders for NYC Open Data CSV files.
"""

import requests
import argparse
from typing import Optional
from abc import ABC, abstractmethod


class NYCDataDownloader(ABC):
    """Base class for NYC Open Data CSV downloaders"""
    
    def __init__(self, app_token: Optional[str] = None):
        self.session = requests.Session()
        if app_token:
            self.session.headers.update({'X-App-Token': app_token})
    
    @property
    @abstractmethod
    def BASE_URL(self) -> str:
        """Each subclass must define its specific URL"""
        pass
    
    @property
    @abstractmethod
    def DATASET_NAME(self) -> str:
        """Each subclass must define its dataset name for descriptions"""
        pass
    
    def download_csv(self, output_path: str, timeout: int = 10) -> None:
        """Download the CSV file and save it to disk"""
        print(f"📥 Requesting CSV data from: {self.BASE_URL}")
        try:
            response = self.session.get(self.BASE_URL, timeout=timeout)
            print(f"🔄 Status code: {response.status_code}")
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ CSV file successfully downloaded to: {output_path}")
        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")
    
    def create_argument_parser(self) -> argparse.ArgumentParser:
        """Create standardized argument parser"""
        parser = argparse.ArgumentParser(description=f"Download NYC {self.DATASET_NAME} CSV data")
        parser.add_argument("-o", "--output", required=True, 
                          help="Path to save the downloaded CSV file")
        parser.add_argument("--app-token", 
                          help="Optional Socrata API app token")
        parser.add_argument("--timeout", type=int, default=10,
                          help="Request timeout in seconds (default: 10)")
        return parser
    
    def run(self) -> None:
        """Main execution method"""
        parser = self.create_argument_parser()
        args = parser.parse_args()
        self.download_csv(args.output, timeout=args.timeout)