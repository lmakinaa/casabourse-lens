"""
Trading Tools Module
AI agent tools for market analysis and trading decisions
"""

import json
from typing import Dict, List

from .api import WafaBourseAPI
from .technical_analysis import TechnicalAnalysis


class TradingTools:
    """Trading analysis tools for AI agent"""
    
    def __init__(self, wafa_api: WafaBourseAPI = None, tech_analysis: TechnicalAnalysis = None):
        """
        Initialize trading tools
        
        Args:
            wafa_api: WafaBourseAPI instance (creates new one if not provided)
            tech_analysis: TechnicalAnalysis instance (creates new one if not provided)
        """
        self.wafa_api = wafa_api or WafaBourseAPI()
        self.tech_analysis = tech_analysis or TechnicalAnalysis()
    
    def get_tool_definitions(self) -> List[Dict]:
        """Get OpenAI-compatible tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_market_overview",
                    "description": "Get overall market status, MASI index, top gainers/losers, and market breadth. Use this first to understand market conditions.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "get_stock_snapshot",
                    "description": "Get current price, volume, and basic info for a specific stock symbol.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol (e.g., 'BCP', 'IAM', 'ATW')"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_technical_analysis",
                    "description": "Calculate technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands) for a stock. Requires historical data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"},
                            "indicators": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of indicators: 'sma20', 'sma50', 'ema12', 'rsi', 'macd', 'bollinger'"
                            }
                        },
                        "required": ["symbol", "indicators"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_order_book",
                    "description": "Get order book depth (bid/ask levels) to assess liquidity and buying/selling pressure.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_price_history",
                    "description": "Get historical price data (daily OHLCV) for trend analysis and pattern recognition.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"},
                            "days": {"type": "integer", "description": "Number of days of history (default 30)"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_volume_profile",
                    "description": "Analyze recent trading volume patterns and compare to historical averages.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_all_stocks",
                    "description": "Get complete list of all stocks trading on the exchange with current prices, changes, and volumes.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "description": "Maximum number of stocks to return (default: all)"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_company_profile",
                    "description": "Get detailed company profile including description, sector, IPO date, number of shares, market cap, and website. Useful for fundamental analysis and understanding what a company does.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol (e.g., 'ADH', 'BCP', 'IAM')"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_shareholders",
                    "description": "Get shareholder structure showing major shareholders and their ownership percentages. Important for understanding ownership concentration and float.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol (e.g., 'ADH', 'BCP', 'IAM')"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_financial_metrics",
                    "description": "Get key financial metrics and ratios including P/E ratio, dividend yield, P/B ratio, EPS, DPS, margins, revenue, and net income for the last 2 years. Essential for fundamental valuation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol (e.g., 'ADH', 'BCP', 'IAM')"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recent_trades",
                    "description": "Get the most recent executed trades for a stock showing time, price, quantity and trade direction. Essential for understanding real-time price action and detecting large trades.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol (e.g., 'BCP', 'IAM', 'ATW')"},
                            "limit": {"type": "integer", "description": "Maximum number of trades to return (default 20)"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "screen_stocks",
                    "description": "Screen stocks based on criteria like minimum volume, price change, and sector. Useful for finding trading opportunities and filtering the universe of stocks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min_volume_mad": {"type": "number", "description": "Minimum trading volume in MAD (millions)"},
                            "min_change_pct": {"type": "number", "description": "Minimum price change percentage"},
                            "max_change_pct": {"type": "number", "description": "Maximum price change percentage"},
                            "direction": {"type": "string", "description": "Filter by direction: 'up', 'down', or 'all'", "enum": ["up", "down", "all"]},
                            "limit": {"type": "integer", "description": "Maximum number of results (default 10)"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_volatility_analysis",
                    "description": "Get volatility metrics including Average True Range (ATR), daily range analysis, and volatility classification. Critical for position sizing and stop-loss placement.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"},
                            "period": {"type": "integer", "description": "ATR period in days (default 14)"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_support_resistance",
                    "description": "Calculate key support and resistance levels based on swing highs/lows, period highs/lows, and price action analysis. Essential for identifying entry/exit points.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"},
                            "lookback": {"type": "integer", "description": "Number of days to analyze (default 30)"}
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_breadth",
                    "description": "Get market breadth indicators showing overall market health: advance/decline ratio, new highs/lows, percent above moving averages. Use for market timing decisions.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_stocks",
                    "description": "Compare multiple stocks side by side on key metrics including price performance, volume, volatility, and technicals. Useful for relative value analysis and pair trading.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbols": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of stock symbols to compare (2-5 stocks)"
                            }
                        },
                        "required": ["symbols"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_intraday_momentum",
                    "description": "Analyze intraday momentum by examining price relative to open, high, low, VWAP proximity, and buying/selling pressure. Key for timing entries during the trading day.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Stock symbol"}
                        },
                        "required": ["symbol"]
                    }
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool and return results"""
        
        tool_handlers = {
            "get_market_overview": self._get_market_overview,
            "get_stock_snapshot": self._get_stock_snapshot,
            "get_technical_analysis": self._get_technical_analysis,
            "get_order_book": self._get_order_book,
            "get_price_history": self._get_price_history,
            "analyze_volume_profile": self._analyze_volume_profile,
            "get_all_stocks": self._get_all_stocks,
            "get_company_profile": self._get_company_profile,
            "get_shareholders": self._get_shareholders,
            "get_financial_metrics": self._get_financial_metrics,
            "get_recent_trades": self._get_recent_trades,
            "screen_stocks": self._screen_stocks,
            "get_volatility_analysis": self._get_volatility_analysis,
            "get_support_resistance": self._get_support_resistance,
            "get_market_breadth": self._get_market_breadth,
            "compare_stocks": self._compare_stocks,
            "get_intraday_momentum": self._get_intraday_momentum,
        }
        
        try:
            handler = tool_handlers.get(tool_name)
            if handler:
                return handler(tool_input) if tool_input else handler()
            return f"Error: Unknown tool {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def _get_market_overview(self, tool_input: Dict = None) -> str:
        """Get market overview data"""
        index = self.wafa_api.get_market_index()
        gainers = self.wafa_api.get_top_movers('H')
        losers = self.wafa_api.get_top_movers('B')
        active = self.wafa_api.get_top_movers('V')
        status = self.wafa_api.get_market_status()
        
        return json.dumps({
            "market_status": status.get('Statut') if status else 'Unknown',
            "masi_index": {
                "value": index['Cours'],
                "change_pct": index['VariationP'],
                "volume_mad": index['Volume'] / 1e6,
                "gainers": index['NbrHausse'],
                "losers": index['NbrBaisse']
            } if index else None,
            "top_gainers": [{"symbol": s['Symbol'], "price": s['Cours'], "change": s['Variation']} for s in (gainers or [])[:3]],
            "top_losers": [{"symbol": s['Symbol'], "price": s['Cours'], "change": s['Variation']} for s in (losers or [])[:3]],
            "most_active": [{"symbol": s['Symbol'], "volume": s['Qte']} for s in (active or [])[:3]]
        }, indent=2)
    
    def _get_stock_snapshot(self, tool_input: Dict) -> str:
        """Get stock snapshot data"""
        symbol = tool_input['symbol']
        details = self.wafa_api.get_stock_details(symbol)
        
        if not details:
            return f"Error: Could not fetch data for {symbol}"
        
        return json.dumps({
            "symbol": symbol,
            "current_price": details['Cours'],
            "change_pct": details['VariationP'],
            "open": details['Ouverture'],
            "high": details['PlusHaut'],
            "low": details['PlusBas'],
            "volume_mad": details['Volume'] / 1e6,
            "num_trades": details['NbrTransaction'],
            "ytd_change": details['VariationPDAnnee'],
            "year_high": details['PlusHautDAnnee'],
            "year_low": details['PlusBasDAnnee'],
            "buy_pressure_pct": details['PourcentageAchat'],
            "sell_pressure_pct": details['PourcentageVente']
        }, indent=2)
    
    def _get_technical_analysis(self, tool_input: Dict) -> str:
        """Get technical analysis for a symbol"""
        symbol = tool_input['symbol']
        indicators = tool_input.get('indicators', [])
        
        history = self.wafa_api.get_price_history(symbol)
        if not history:
            return f"Error: No historical data for {symbol}"
        
        prices = [float(d['Cours']) for d in history[-50:]]  # Last 50 days
        current_price = prices[-1]
        
        results = {"symbol": symbol, "current_price": current_price}
        
        if 'sma20' in indicators:
            results['sma20'] = self.tech_analysis.calculate_sma(prices, 20)
        if 'sma50' in indicators:
            results['sma50'] = self.tech_analysis.calculate_sma(prices, 50)
        if 'ema12' in indicators:
            results['ema12'] = self.tech_analysis.calculate_ema(prices, 12)
        if 'rsi' in indicators:
            results['rsi'] = self.tech_analysis.calculate_rsi(prices, 14)
        if 'macd' in indicators:
            results['macd'] = self.tech_analysis.calculate_macd(prices)
        if 'bollinger' in indicators:
            results['bollinger_bands'] = self.tech_analysis.calculate_bollinger_bands(prices, 20)
        
        return json.dumps(results, indent=2)
    
    def _get_order_book(self, tool_input: Dict) -> str:
        """Get order book data"""
        symbol = tool_input['symbol']
        order_book = self.wafa_api.get_order_book(symbol, 5)
        
        if not order_book:
            return f"Error: No order book data for {symbol}"
        
        best_bid = order_book[0]['Achat']
        best_ask = order_book[0]['Vente']
        spread = best_ask - best_bid
        spread_pct = (spread / best_bid) * 100
        
        total_bid_vol = sum(level['QteAchat'] for level in order_book)
        total_ask_vol = sum(level['QteVente'] for level in order_book)
        imbalance = (total_bid_vol - total_ask_vol) / (total_bid_vol + total_ask_vol) * 100
        
        return json.dumps({
            "symbol": symbol,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread_mad": spread,
            "spread_pct": spread_pct,
            "order_imbalance_pct": imbalance,
            "total_bid_volume": total_bid_vol,
            "total_ask_volume": total_ask_vol,
            "bid_levels": [{"price": l['Achat'], "qty": l['QteAchat']} for l in order_book],
            "ask_levels": [{"price": l['Vente'], "qty": l['QteVente']} for l in order_book]
        }, indent=2)
    
    def _get_price_history(self, tool_input: Dict) -> str:
        """Get price history data"""
        symbol = tool_input['symbol']
        days = tool_input.get('days', 30)
        
        history = self.wafa_api.get_price_history(symbol)
        if not history:
            return f"Error: No history for {symbol}"
        
        recent = history[-days:]
        
        return json.dumps({
            "symbol": symbol,
            "days": len(recent),
            "data": [{"date": d['Seance'], "close": d['Cours'], "volume": d['Volume']} for d in recent]
        }, indent=2)
    
    def _analyze_volume_profile(self, tool_input: Dict) -> str:
        """Analyze volume profile"""
        symbol = tool_input['symbol']
        history = self.wafa_api.get_price_history(symbol)
        details = self.wafa_api.get_stock_details(symbol)
        
        if not history or not details:
            return f"Error: Could not analyze volume for {symbol}"
        
        recent_volumes = [d['Volume'] for d in history[-20:]]
        avg_volume = sum(recent_volumes) / len(recent_volumes)
        current_volume = details['Volume']
        
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        return json.dumps({
            "symbol": symbol,
            "current_volume_mad": current_volume / 1e6,
            "avg_20day_volume_mad": avg_volume / 1e6,
            "volume_ratio": volume_ratio,
            "interpretation": "High" if volume_ratio > 1.5 else "Normal" if volume_ratio > 0.7 else "Low"
        }, indent=2)
    
    def _get_all_stocks(self, tool_input: Dict = None) -> str:
        """Get all stocks data"""
        tool_input = tool_input or {}
        limit = tool_input.get('limit', None)
        all_tickers = self.wafa_api.get_all_tickers()
        
        if not all_tickers:
            return "Error: Could not fetch all stocks"
        
        # Apply limit if specified
        if limit:
            all_tickers = all_tickers[:limit]
        
        # Format the data
        stocks = []
        for stock in all_tickers:
            stocks.append({
                "symbol": stock.get('Symbol', 'N/A'),
                "name": stock.get('Libelle', 'N/A'),
                "price": stock.get('Cours', 0),
                "change_pct": stock.get('VariationP', 0),
                "change_mad": stock.get('Variation', 0),
                "volume_mad": stock.get('Volume', 0) / 1e6 if stock.get('Volume') else 0,
                "high": stock.get('PlusHaut', 0),
                "low": stock.get('PlusBas', 0),
                "open": stock.get('Ouverture', 0)
            })
        
        return json.dumps({
            "total_stocks": len(stocks),
            "stocks": stocks
        }, indent=2)
    
    def _get_company_profile(self, tool_input: Dict) -> str:
        """Get company profile data"""
        symbol = tool_input['symbol']
        profile = self.wafa_api.get_company_profile(symbol)
        
        if not profile:
            return f"Error: Could not fetch company profile for {symbol}"
        
        # Clean up presentation text (replace $$ with newlines)
        presentation = profile.get('Presentation', '')
        presentation = presentation.replace('$$', '\n').replace('||', '\n\nNote: ')
        
        return json.dumps({
            "symbol": profile.get('Symbol'),
            "name": profile.get('Libelle'),
            "isin": profile.get('Ising'),
            "sector": profile.get('Secteur'),
            "description": presentation,
            "ipo_date": profile.get('DateIntroduction', '').split(' ')[0] if profile.get('DateIntroduction') else None,
            "total_shares": profile.get('NbrTitres'),
            "market_cap_mad": profile.get('Capitalisation'),
            "market_cap_million_mad": profile.get('Capitalisation', 0) / 1e6 if profile.get('Capitalisation') else 0,
            "website": profile.get('SiteInternet', '').strip()
        }, indent=2)
    
    def _get_shareholders(self, tool_input: Dict) -> str:
        """Get shareholders data"""
        symbol = tool_input['symbol']
        shareholders = self.wafa_api.get_shareholders(symbol)
        
        if not shareholders:
            return f"Error: Could not fetch shareholders for {symbol}"
        
        # Calculate float percentage
        float_pct = 0
        major_holders = []
        
        for holder in shareholders:
            name = holder.get('Libelle', '').strip()
            pct = holder.get('Pourcentage', 0)
            
            if 'flottant' in name.lower() or 'float' in name.lower():
                float_pct = pct
            else:
                major_holders.append({
                    "name": name,
                    "percentage": pct
                })
        
        return json.dumps({
            "symbol": symbol,
            "shareholders": [{
                "name": h.get('Libelle', '').strip(),
                "percentage": h.get('Pourcentage', 0)
            } for h in shareholders],
            "major_holders": major_holders,
            "float_percentage": float_pct,
            "ownership_concentration": sum(h['percentage'] for h in major_holders)
        }, indent=2)
    
    def _get_financial_metrics(self, tool_input: Dict) -> str:
        """Get financial metrics data"""
        symbol = tool_input['symbol']
        metrics = self.wafa_api.get_financial_metrics(symbol)
        
        if not metrics:
            return f"Error: Could not fetch financial metrics for {symbol}"
        
        # Organize metrics by category
        valuation = {}
        per_share = {}
        margins = {}
        income_statement = {}
        
        for metric in metrics:
            label = metric.get('Libelle', '')
            group = metric.get('IdGroupe', 0)
            
            # Get years dynamically (usually 2023, 2022)
            years = [k for k in metric.keys() if k.isdigit()]
            values = {year: metric.get(year) for year in years}
            
            if group == 1:  # Valuation ratios
                if 'earning' in label.lower() or 'P/E' in label:
                    valuation['pe_ratio'] = values
                elif 'yield' in label.lower():
                    valuation['dividend_yield_pct'] = values
                elif 'book' in label.lower():
                    valuation['price_to_book'] = values
            elif group == 2:  # Per share metrics
                if 'bénéfice' in label.lower() or 'eps' in label.lower():
                    per_share['earnings_per_share_dh'] = values
                elif 'dividende' in label.lower():
                    per_share['dividend_per_share_dh'] = values
                elif 'actif' in label.lower():
                    per_share['book_value_per_share_dh'] = values
            elif group == 3:  # Margins
                if 'opérationnelle' in label.lower():
                    margins['operating_margin_pct'] = values
                elif 'nette' in label.lower():
                    margins['net_margin_pct'] = values
            elif group == 4:  # Income statement
                if 'chiffre' in label.lower() or 'affaires' in label.lower():
                    income_statement['revenue_mdh'] = values
                elif 'exploitation' in label.lower():
                    income_statement['operating_income_mdh'] = values
                elif 'net' in label.lower():
                    income_statement['net_income_mdh'] = values
        
        return json.dumps({
            "symbol": symbol,
            "valuation_ratios": valuation,
            "per_share_metrics": per_share,
            "profitability_margins": margins,
            "income_statement": income_statement,
            "raw_data": [{"label": m.get('Libelle'), **{k: m.get(k) for k in m.keys() if k.isdigit()}} for m in metrics]
        }, indent=2)
    
    def _get_recent_trades(self, tool_input: Dict) -> str:
        """Get recent trades for a stock"""
        symbol = tool_input['symbol']
        limit = tool_input.get('limit', 20)
        
        trades = self.wafa_api.get_recent_trades(symbol)
        
        if not trades:
            return f"Error: Could not fetch recent trades for {symbol}"
        
        # Limit results
        trades = trades[:limit]
        
        # Analyze trade flow
        total_buy_volume = 0
        total_sell_volume = 0
        prices = []
        
        formatted_trades = []
        for trade in trades:
            price = trade.get('Cours', 0)
            qty = trade.get('Qte', 0)
            sens = trade.get('Sens', '')
            
            prices.append(price)
            
            if sens == 'A':  # Achat (Buy)
                total_buy_volume += qty
            elif sens == 'V':  # Vente (Sell)
                total_sell_volume += qty
            
            formatted_trades.append({
                "time": trade.get('Heure', ''),
                "price": price,
                "quantity": qty,
                "direction": "BUY" if sens == 'A' else "SELL" if sens == 'V' else "UNKNOWN",
                "value_mad": price * qty
            })
        
        total_volume = total_buy_volume + total_sell_volume
        buy_pct = (total_buy_volume / total_volume * 100) if total_volume > 0 else 0
        
        return json.dumps({
            "symbol": symbol,
            "num_trades": len(formatted_trades),
            "trades": formatted_trades,
            "trade_flow_analysis": {
                "total_buy_volume": total_buy_volume,
                "total_sell_volume": total_sell_volume,
                "buy_percentage": round(buy_pct, 2),
                "sell_percentage": round(100 - buy_pct, 2),
                "net_flow": "BUYING_PRESSURE" if buy_pct > 55 else "SELLING_PRESSURE" if buy_pct < 45 else "NEUTRAL"
            },
            "price_range": {
                "high": max(prices) if prices else 0,
                "low": min(prices) if prices else 0,
                "last": prices[0] if prices else 0
            }
        }, indent=2)
    
    def _screen_stocks(self, tool_input: Dict = None) -> str:
        """Screen stocks based on criteria"""
        tool_input = tool_input or {}
        min_volume = tool_input.get('min_volume_mad', 0) * 1e6  # Convert from millions
        min_change = tool_input.get('min_change_pct')
        max_change = tool_input.get('max_change_pct')
        direction = tool_input.get('direction', 'all')
        limit = tool_input.get('limit', 10)
        
        all_tickers = self.wafa_api.get_all_tickers()
        
        if not all_tickers:
            return "Error: Could not fetch stocks for screening"
        
        # Filter stocks
        filtered = []
        for stock in all_tickers:
            volume = stock.get('Volume', 0)
            change_pct = stock.get('VariationP', 0)
            
            # Volume filter
            if volume < min_volume:
                continue
            
            # Change percentage filters
            if min_change is not None and change_pct < min_change:
                continue
            if max_change is not None and change_pct > max_change:
                continue
            
            # Direction filter
            if direction == 'up' and change_pct <= 0:
                continue
            if direction == 'down' and change_pct >= 0:
                continue
            
            filtered.append({
                "symbol": stock.get('Symbol'),
                "name": stock.get('Libelle'),
                "price": stock.get('Cours', 0),
                "change_pct": change_pct,
                "volume_mad": volume / 1e6,
                "high": stock.get('PlusHaut', 0),
                "low": stock.get('PlusBas', 0)
            })
        
        # Sort by absolute change percentage for relevance
        filtered.sort(key=lambda x: abs(x['change_pct']), reverse=True)
        
        return json.dumps({
            "total_matches": len(filtered),
            "showing": min(limit, len(filtered)),
            "filters_applied": {
                "min_volume_mad": min_volume / 1e6 if min_volume else None,
                "min_change_pct": min_change,
                "max_change_pct": max_change,
                "direction": direction
            },
            "stocks": filtered[:limit]
        }, indent=2)
    
    def _get_volatility_analysis(self, tool_input: Dict) -> str:
        """Analyze volatility for a stock"""
        symbol = tool_input['symbol']
        period = tool_input.get('period', 14)
        
        history = self.wafa_api.get_price_history(symbol)
        details = self.wafa_api.get_stock_details(symbol)
        
        if not history or len(history) < period + 5:
            return f"Error: Insufficient historical data for {symbol}"
        
        # Extract OHLC data
        highs = [float(d.get('PlusHaut', d.get('Cours', 0))) for d in history]
        lows = [float(d.get('PlusBas', d.get('Cours', 0))) for d in history]
        closes = [float(d.get('Cours', 0)) for d in history]
        
        # Calculate ATR
        atr = self.tech_analysis.calculate_atr(highs, lows, closes, period)
        current_price = closes[-1]
        
        # Calculate ATR percentage
        atr_pct = (atr / current_price * 100) if atr and current_price > 0 else 0
        
        # Daily range analysis
        recent_ranges = []
        for i in range(-period, 0):
            if abs(i) <= len(highs):
                daily_range = highs[i] - lows[i]
                daily_range_pct = (daily_range / closes[i] * 100) if closes[i] > 0 else 0
                recent_ranges.append(daily_range_pct)
        
        avg_daily_range = sum(recent_ranges) / len(recent_ranges) if recent_ranges else 0
        max_daily_range = max(recent_ranges) if recent_ranges else 0
        
        # Volatility classification
        if atr_pct > 4:
            volatility_class = "HIGH"
        elif atr_pct > 2:
            volatility_class = "MODERATE"
        else:
            volatility_class = "LOW"
        
        # Today's range vs average
        today_range_pct = 0
        if details:
            today_high = details.get('PlusHaut', 0)
            today_low = details.get('PlusBas', 0)
            today_range = today_high - today_low
            today_range_pct = (today_range / current_price * 100) if current_price > 0 else 0
        
        return json.dumps({
            "symbol": symbol,
            "current_price": current_price,
            "atr": {
                "value": round(atr, 4) if atr else None,
                "percentage": round(atr_pct, 2),
                "period": period
            },
            "daily_range": {
                "average_pct": round(avg_daily_range, 2),
                "max_pct": round(max_daily_range, 2),
                "today_pct": round(today_range_pct, 2)
            },
            "volatility_classification": volatility_class,
            "suggested_stop_loss_pct": round(atr_pct * 1.5, 2) if atr_pct else None,
            "suggested_position_sizing_note": f"With {volatility_class} volatility, consider {'smaller' if volatility_class == 'HIGH' else 'larger' if volatility_class == 'LOW' else 'standard'} position sizes"
        }, indent=2)
    
    def _get_support_resistance(self, tool_input: Dict) -> str:
        """Calculate support and resistance levels"""
        symbol = tool_input['symbol']
        lookback = tool_input.get('lookback', 30)
        
        history = self.wafa_api.get_price_history(symbol)
        
        if not history or len(history) < lookback:
            return f"Error: Insufficient historical data for {symbol} (need {lookback} days)"
        
        # Extract OHLC data
        highs = [float(d.get('PlusHaut', d.get('Cours', 0))) for d in history]
        lows = [float(d.get('PlusBas', d.get('Cours', 0))) for d in history]
        closes = [float(d.get('Cours', 0)) for d in history]
        
        # Calculate support/resistance
        levels = self.tech_analysis.calculate_support_resistance(highs, lows, closes, lookback)
        
        if not levels:
            return f"Error: Could not calculate levels for {symbol}"
        
        # Add trading recommendations
        current = levels['current_price']
        
        # Find nearest levels
        nearest_resistance = levels['resistance_levels'][0] if levels['resistance_levels'] else None
        nearest_support = levels['support_levels'][0] if levels['support_levels'] else None
        
        # Position in range
        if nearest_resistance and nearest_support:
            range_size = nearest_resistance - nearest_support
            position_in_range = ((current - nearest_support) / range_size * 100) if range_size > 0 else 50
        else:
            position_in_range = 50
        
        return json.dumps({
            "symbol": symbol,
            "current_price": current,
            "resistance_levels": levels['resistance_levels'],
            "support_levels": levels['support_levels'],
            "period_high": levels['period_high'],
            "period_low": levels['period_low'],
            "key_metrics": {
                "distance_to_resistance_pct": levels['distance_to_resistance_pct'],
                "distance_to_support_pct": levels['distance_to_support_pct'],
                "position_in_range_pct": round(position_in_range, 1)
            },
            "trading_zones": {
                "buy_zone": f"Near {nearest_support:.2f}" if nearest_support else "N/A",
                "sell_zone": f"Near {nearest_resistance:.2f}" if nearest_resistance else "N/A",
                "current_zone": "NEAR_RESISTANCE" if position_in_range > 80 else "NEAR_SUPPORT" if position_in_range < 20 else "MID_RANGE"
            }
        }, indent=2)
    
    def _get_market_breadth(self, tool_input: Dict = None) -> str:
        """Get market breadth indicators"""
        all_tickers = self.wafa_api.get_all_tickers()
        index = self.wafa_api.get_market_index()
        
        if not all_tickers:
            return "Error: Could not fetch market data"
        
        # Count advances/declines
        advances = 0
        declines = 0
        unchanged = 0
        new_highs = 0
        new_lows = 0
        above_avg_volume = 0
        total_volume = 0
        
        for stock in all_tickers:
            change_pct = stock.get('VariationP', 0)
            volume = stock.get('Volume', 0)
            current = stock.get('Cours', 0)
            year_high = stock.get('PlusHautDAnnee', 0)
            year_low = stock.get('PlusBasDAnnee', 0)
            
            # Advance/Decline
            if change_pct > 0:
                advances += 1
            elif change_pct < 0:
                declines += 1
            else:
                unchanged += 1
            
            # New highs/lows (within 1% of yearly)
            if current and year_high and current >= year_high * 0.99:
                new_highs += 1
            if current and year_low and current <= year_low * 1.01:
                new_lows += 1
            
            total_volume += volume
        
        total_stocks = advances + declines + unchanged
        
        # Advance/Decline ratio
        ad_ratio = advances / declines if declines > 0 else float('inf') if advances > 0 else 1
        
        # Market sentiment based on breadth
        if ad_ratio > 2:
            sentiment = "STRONGLY_BULLISH"
        elif ad_ratio > 1.2:
            sentiment = "BULLISH"
        elif ad_ratio > 0.8:
            sentiment = "NEUTRAL"
        elif ad_ratio > 0.5:
            sentiment = "BEARISH"
        else:
            sentiment = "STRONGLY_BEARISH"
        
        return json.dumps({
            "market_index": {
                "value": index.get('Cours') if index else None,
                "change_pct": index.get('VariationP') if index else None
            },
            "breadth_indicators": {
                "advances": advances,
                "declines": declines,
                "unchanged": unchanged,
                "advance_decline_ratio": round(ad_ratio, 2) if ad_ratio != float('inf') else "INF",
                "advance_pct": round(advances / total_stocks * 100, 1) if total_stocks > 0 else 0
            },
            "extreme_movers": {
                "new_52w_highs": new_highs,
                "new_52w_lows": new_lows,
                "net_new_highs": new_highs - new_lows
            },
            "market_sentiment": sentiment,
            "interpretation": f"{'Broad buying' if sentiment.endswith('BULLISH') else 'Broad selling' if sentiment.endswith('BEARISH') else 'Mixed'} pressure with {advances} stocks up vs {declines} down"
        }, indent=2)
    
    def _compare_stocks(self, tool_input: Dict) -> str:
        """Compare multiple stocks"""
        symbols = tool_input.get('symbols', [])
        
        if len(symbols) < 2:
            return "Error: Need at least 2 symbols to compare"
        if len(symbols) > 5:
            symbols = symbols[:5]  # Limit to 5
        
        comparisons = []
        
        for symbol in symbols:
            details = self.wafa_api.get_stock_details(symbol)
            history = self.wafa_api.get_price_history(symbol)
            
            if not details:
                comparisons.append({"symbol": symbol, "error": "Could not fetch data"})
                continue
            
            # Calculate technical indicators
            prices = [float(d['Cours']) for d in history[-30:]] if history else []
            rsi = self.tech_analysis.calculate_rsi(prices, 14) if len(prices) >= 15 else None
            sma20 = self.tech_analysis.calculate_sma(prices, 20) if len(prices) >= 20 else None
            
            current_price = details.get('Cours', 0)
            
            comparisons.append({
                "symbol": symbol,
                "name": details.get('Libelle', ''),
                "price": current_price,
                "change_today_pct": details.get('VariationP', 0),
                "ytd_change_pct": details.get('VariationPDAnnee', 0),
                "volume_mad": details.get('Volume', 0) / 1e6,
                "rsi_14": round(rsi, 2) if rsi else None,
                "vs_sma20_pct": round((current_price - sma20) / sma20 * 100, 2) if sma20 and current_price else None,
                "52w_high": details.get('PlusHautDAnnee', 0),
                "52w_low": details.get('PlusBasDAnnee', 0),
                "from_52w_high_pct": round((current_price - details.get('PlusHautDAnnee', current_price)) / details.get('PlusHautDAnnee', current_price) * 100, 2) if details.get('PlusHautDAnnee') else None
            })
        
        # Rank stocks
        valid_comparisons = [c for c in comparisons if 'error' not in c]
        
        if valid_comparisons:
            # Best performer today
            best_today = max(valid_comparisons, key=lambda x: x.get('change_today_pct', -999))
            worst_today = min(valid_comparisons, key=lambda x: x.get('change_today_pct', 999))
            
            # Best RSI (closer to 50 is neutral, <30 oversold, >70 overbought)
            with_rsi = [c for c in valid_comparisons if c.get('rsi_14')]
            most_oversold = min(with_rsi, key=lambda x: x['rsi_14']) if with_rsi else None
            most_overbought = max(with_rsi, key=lambda x: x['rsi_14']) if with_rsi else None
        else:
            best_today = worst_today = most_oversold = most_overbought = None
        
        return json.dumps({
            "comparison": comparisons,
            "rankings": {
                "best_performer_today": best_today['symbol'] if best_today else None,
                "worst_performer_today": worst_today['symbol'] if worst_today else None,
                "most_oversold": most_oversold['symbol'] if most_oversold else None,
                "most_overbought": most_overbought['symbol'] if most_overbought else None
            }
        }, indent=2)
    
    def _get_intraday_momentum(self, tool_input: Dict) -> str:
        """Analyze intraday momentum"""
        symbol = tool_input['symbol']
        
        details = self.wafa_api.get_stock_details(symbol)
        order_book = self.wafa_api.get_order_book(symbol, 5)
        
        if not details:
            return f"Error: Could not fetch data for {symbol}"
        
        current = details.get('Cours', 0)
        open_price = details.get('Ouverture', 0)
        high = details.get('PlusHaut', 0)
        low = details.get('PlusBas', 0)
        buy_pressure = details.get('PourcentageAchat', 0)
        sell_pressure = details.get('PourcentageVente', 0)
        
        # Position in day's range
        day_range = high - low
        if day_range > 0:
            position_in_range = (current - low) / day_range * 100
        else:
            position_in_range = 50
        
        # Price vs Open
        if open_price > 0:
            change_from_open = (current - open_price) / open_price * 100
        else:
            change_from_open = 0
        
        # Order book imbalance
        if order_book:
            total_bid = sum(level.get('QteAchat', 0) for level in order_book)
            total_ask = sum(level.get('QteVente', 0) for level in order_book)
            if total_bid + total_ask > 0:
                book_imbalance = (total_bid - total_ask) / (total_bid + total_ask) * 100
            else:
                book_imbalance = 0
        else:
            book_imbalance = 0
            total_bid = total_ask = 0
        
        # Momentum classification
        momentum_signals = []
        
        if position_in_range > 80:
            momentum_signals.append("NEAR_HIGH")
        elif position_in_range < 20:
            momentum_signals.append("NEAR_LOW")
        
        if change_from_open > 1:
            momentum_signals.append("BULLISH_TREND")
        elif change_from_open < -1:
            momentum_signals.append("BEARISH_TREND")
        
        if book_imbalance > 20:
            momentum_signals.append("BID_SUPPORT")
        elif book_imbalance < -20:
            momentum_signals.append("ASK_PRESSURE")
        
        # Overall momentum
        bullish_count = sum(1 for s in momentum_signals if s in ['NEAR_HIGH', 'BULLISH_TREND', 'BID_SUPPORT'])
        bearish_count = sum(1 for s in momentum_signals if s in ['NEAR_LOW', 'BEARISH_TREND', 'ASK_PRESSURE'])
        
        if bullish_count > bearish_count:
            overall = "BULLISH"
        elif bearish_count > bullish_count:
            overall = "BEARISH"
        else:
            overall = "NEUTRAL"
        
        return json.dumps({
            "symbol": symbol,
            "price_action": {
                "current": current,
                "open": open_price,
                "high": high,
                "low": low,
                "change_from_open_pct": round(change_from_open, 2),
                "position_in_day_range_pct": round(position_in_range, 1)
            },
            "pressure_analysis": {
                "buy_pressure_pct": buy_pressure,
                "sell_pressure_pct": sell_pressure,
                "order_book_imbalance_pct": round(book_imbalance, 1),
                "bid_volume": total_bid,
                "ask_volume": total_ask
            },
            "momentum_signals": momentum_signals,
            "overall_momentum": overall,
            "interpretation": f"{'Buyers in control' if overall == 'BULLISH' else 'Sellers in control' if overall == 'BEARISH' else 'Balanced'} - price at {position_in_range:.0f}% of day range"
        }, indent=2)