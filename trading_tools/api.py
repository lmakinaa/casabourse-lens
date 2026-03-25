"""
WafaBourse API Client
Handles all communication with the WafaBourse API
"""

import requests
from typing import Dict, List, Optional, Any

from .config import WAFABOURSE_API, DEFAULT_HEADERS, REQUEST_TIMEOUT


class WafaBourseAPI:
    """Wrapper for WafaBourse API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = DEFAULT_HEADERS.copy()
    
    def _request(self, action_name: str, params: List[Dict], action_type: str = "SELECT") -> Optional[Any]:
        """Generic API request"""
        payload = {
            "ACTIONS": [{
                "ACTION": {"NAME": action_name, "TYPE": action_type, "VALUE": action_name},
                "PARAMS": params
            }]
        }
        
        try:
            response = self.session.post(
                WAFABOURSE_API, 
                headers=self.headers, 
                json=payload, 
                timeout=REQUEST_TIMEOUT
            )
            data = response.json()
            if data and action_name in data[0] and data[0][action_name].get("Valid"):
                return data[0][action_name]["Data"]
        except Exception as e:
            print(f"API Error ({action_name}): {e}")
        return None
    
    # Market Data Methods
    def get_market_status(self) -> Optional[Dict]:
        """Get current market status"""
        data = self._request("MARKET-STATUS", [
            {"NAME": "Espace", "TYPE": "I", "VALUE": "1"},
            {"NAME": "Numseq_", "TYPE": "I", "VALUE": "0"}
        ])
        return data[0] if data else None
    
    def get_all_tickers(self) -> Optional[List[Dict]]:
        """Get all stock tickers with current data"""
        return self._request("TICKER", [
            {"NAME": "NumseqMin_", "TYPE": "I", "VALUE": "0"},
            {"NAME": "NumseqMax_", "TYPE": "I", "VALUE": "0"}
        ])
    
    def get_market_index(self) -> Optional[Dict]:
        """Get MASI index data"""
        data = self._request("INDICE-SYNTHESE", [
            {"NAME": "Indice_", "TYPE": "S", "VALUE": "MASI"}
        ])
        return data[0] if data else None
    
    def get_top_movers(self, type_: str) -> Optional[List[Dict]]:
        """
        Get top movers by type
        
        Args:
            type_: H=gainers, B=losers, V=most active
        """
        return self._request("INDICE-TOPS", [
            {"NAME": "Indice_", "TYPE": "S", "VALUE": "MASI"},
            {"NAME": "TypePalmares_", "TYPE": "S", "VALUE": type_}
        ])
    
    # Stock Data Methods
    def get_stock_details(self, symbol: str) -> Optional[Dict]:
        """Get detailed stock information"""
        data = self._request("VALEUR-INFOS", [
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol}
        ])
        return data[0] if data else None
    
    def get_order_book(self, symbol: str, depth: int = 5) -> Optional[List[Dict]]:
        """Get order book depth for a stock"""
        return self._request("VALEUR-PROFONDEUR", [
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol},
            {"NAME": "Top_", "TYPE": "I", "VALUE": str(depth)},
            {"NAME": "NumSeq_", "TYPE": "I", "VALUE": "0"}
        ])
    
    def get_price_history(self, symbol: str) -> Optional[List[Dict]]:
        """Get historical price data for a stock"""
        return self._request("VALEUR-GRAPH", [
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol}
        ])
    
    def get_recent_trades(self, symbol: str) -> Optional[List[Dict]]:
        """Get recent trades for a stock"""
        return self._request("VALEUR-TRANSACTION", [
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol},
            {"NAME": "Top_", "TYPE": "I", "VALUE": "-1"}
        ])
    
    # Fundamental Data Methods
    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """Get company profile/description (VALEUR-FICHE)"""
        data = self._request("VALEUR-FICHE", [
            {"NAME": "Espace_", "TYPE": "S", "VALUE": "1"},
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol}
        ])
        return data[0] if data else None
    
    def get_shareholders(self, symbol: str) -> Optional[List[Dict]]:
        """Get shareholder structure (VALEUR-ACTIONNAIRES)"""
        return self._request("VALEUR-ACTIONNAIRES", [
            {"NAME": "Espace_", "TYPE": "S", "VALUE": "1"},
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol}
        ])
    
    def get_financial_metrics(self, symbol: str) -> Optional[List[Dict]]:
        """Get financial metrics and ratios (VALEUR-MFS)"""
        return self._request("VALEUR-MFS", [
            {"NAME": "Espace_", "TYPE": "S", "VALUE": "1"},
            {"NAME": "Symbol_", "TYPE": "S", "VALUE": symbol}
        ], action_type="PROCSELECT")
