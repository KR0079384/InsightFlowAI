import os
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
from src.config import settings

class DataLoader:
    _instance: Optional["DataLoader"] = None
    
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or settings.DATA_PATH
        self.orders: pd.DataFrame = pd.DataFrame()
        self.products: pd.DataFrame = pd.DataFrame()
        self.inventory: pd.DataFrame = pd.DataFrame()
        self.suppliers: pd.DataFrame = pd.DataFrame()
        self.marketing: pd.DataFrame = pd.DataFrame()
        self.customers: pd.DataFrame = pd.DataFrame()
        self.load_all()

    @classmethod
    def get_instance(cls) -> "DataLoader":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_all(self):
        """Loads all CSV datasets into memory and standardizes types."""
        def read_csv_safe(filename: str) -> pd.DataFrame:
            path = self.data_path / filename
            if not path.exists():
                return pd.DataFrame()
            return pd.read_csv(path)

        self.products = read_csv_safe("products.csv")
        self.suppliers = read_csv_safe("suppliers.csv")
        self.customers = read_csv_safe("customers.csv")
        
        # Load & parse dates for orders
        df_orders = read_csv_safe("orders.csv")
        if not df_orders.empty and "order_date" in df_orders.columns:
            df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
            df_orders["year_month"] = df_orders["order_date"].dt.strftime("%Y-%m")
        self.orders = df_orders

        # Load & parse dates for inventory
        df_inv = read_csv_safe("inventory.csv")
        if not df_inv.empty and "date" in df_inv.columns:
            df_inv["date"] = pd.to_datetime(df_inv["date"])
            df_inv["year_month"] = df_inv["date"].dt.strftime("%Y-%m")
        self.inventory = df_inv

        # Load & parse dates for marketing
        df_mkt = read_csv_safe("marketing.csv")
        if not df_mkt.empty and "date" in df_mkt.columns:
            df_mkt["date"] = pd.to_datetime(df_mkt["date"])
            df_mkt["year_month"] = df_mkt["date"].dt.strftime("%Y-%m")
        self.marketing = df_mkt

    def get_overview(self) -> Dict[str, Any]:
        """Provides summary metrics of loaded tables."""
        total_rev = float(self.orders["order_value"].sum()) if not self.orders.empty else 0.0
        min_date = self.orders["order_date"].min().strftime("%Y-%m-%d") if not self.orders.empty else ""
        max_date = self.orders["order_date"].max().strftime("%Y-%m-%d") if not self.orders.empty else ""
        
        return {
            "total_orders": len(self.orders),
            "total_revenue": round(total_rev, 2),
            "active_products": len(self.products),
            "date_range": f"{min_date} to {max_date}",
            "datasets": {
                "orders": len(self.orders),
                "products": len(self.products),
                "inventory": len(self.inventory),
                "suppliers": len(self.suppliers),
                "marketing": len(self.marketing),
                "customers": len(self.customers),
            }
        }

loader = DataLoader.get_instance()
