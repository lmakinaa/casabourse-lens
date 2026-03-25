"""
Technical Analysis Module
Calculate various technical indicators for stock analysis
"""

from typing import Dict, List, Optional


class TechnicalAnalysis:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> Optional[float]:
        """
        Simple Moving Average
        
        Args:
            prices: List of price values
            period: Number of periods for the moving average
            
        Returns:
            SMA value or None if insufficient data
        """
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> Optional[float]:
        """
        Exponential Moving Average
        
        Args:
            prices: List of price values
            period: Number of periods for the moving average
            
        Returns:
            EMA value or None if insufficient data
        """
        if len(prices) < period:
            return None
        
        sma = sum(prices[:period]) / period
        multiplier = 2 / (period + 1)
        ema = sma
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
        """
        Relative Strength Index
        
        Args:
            prices: List of price values
            period: RSI period (default 14)
            
        Returns:
            RSI value (0-100) or None if insufficient data
        """
        if len(prices) < period + 1:
            return None
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Optional[Dict]:
        """
        MACD (Moving Average Convergence Divergence) Indicator
        
        Uses standard 12/26/9 periods
        
        Args:
            prices: List of price values
            
        Returns:
            Dict with macd, signal, and histogram values or None if insufficient data
        """
        if len(prices) < 26:
            return None
        
        ema12 = TechnicalAnalysis.calculate_ema(prices, 12)
        ema26 = TechnicalAnalysis.calculate_ema(prices, 26)
        
        if ema12 is None or ema26 is None:
            return None
        
        macd_line = ema12 - ema26
        
        # Signal line (9-day EMA of MACD)
        macd_values = []
        for i in range(26, len(prices) + 1):
            e12 = TechnicalAnalysis.calculate_ema(prices[:i], 12)
            e26 = TechnicalAnalysis.calculate_ema(prices[:i], 26)
            if e12 and e26:
                macd_values.append(e12 - e26)
        
        signal_line = TechnicalAnalysis.calculate_ema(macd_values, 9) if len(macd_values) >= 9 else None
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": macd_line - signal_line if signal_line else None
        }
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20) -> Optional[Dict]:
        """
        Bollinger Bands
        
        Args:
            prices: List of price values
            period: Moving average period (default 20)
            
        Returns:
            Dict with upper, middle, and lower band values or None if insufficient data
        """
        if len(prices) < period:
            return None
        
        sma = TechnicalAnalysis.calculate_sma(prices, period)
        if sma is None:
            return None
        
        variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
        std_dev = variance ** 0.5
        
        return {
            "upper": sma + (2 * std_dev),
            "middle": sma,
            "lower": sma - (2 * std_dev)
        }
    
    @staticmethod
    def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
        """
        Average True Range - measures volatility
        
        Args:
            highs: List of high prices
            lows: List of low prices
            closes: List of closing prices
            period: ATR period (default 14)
            
        Returns:
            ATR value or None if insufficient data
        """
        if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
            return None
        
        true_ranges = []
        for i in range(1, len(closes)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i-1])
            low_close = abs(lows[i] - closes[i-1])
            true_range = max(high_low, high_close, low_close)
            true_ranges.append(true_range)
        
        if len(true_ranges) < period:
            return None
        
        # Simple average for ATR
        return sum(true_ranges[-period:]) / period
    
    @staticmethod
    def calculate_vwap(prices: List[float], volumes: List[float]) -> Optional[float]:
        """
        Volume Weighted Average Price
        
        Args:
            prices: List of prices (typically close or typical price)
            volumes: List of volumes
            
        Returns:
            VWAP value or None if insufficient data
        """
        if not prices or not volumes or len(prices) != len(volumes):
            return None
        
        total_volume = sum(volumes)
        if total_volume == 0:
            return None
        
        vwap = sum(p * v for p, v in zip(prices, volumes)) / total_volume
        return vwap
    
    @staticmethod
    def calculate_support_resistance(highs: List[float], lows: List[float], closes: List[float], lookback: int = 20) -> Optional[Dict]:
        """
        Calculate support and resistance levels based on swing highs/lows
        
        Args:
            highs: List of high prices
            lows: List of low prices
            closes: List of closing prices
            lookback: Number of periods to look back
            
        Returns:
            Dict with support and resistance levels or None if insufficient data
        """
        if len(highs) < lookback or len(lows) < lookback or len(closes) < lookback:
            return None
        
        recent_highs = highs[-lookback:]
        recent_lows = lows[-lookback:]
        recent_closes = closes[-lookback:]
        
        current_price = closes[-1]
        
        # Find swing highs (local maxima)
        swing_highs = []
        for i in range(2, len(recent_highs) - 2):
            if (recent_highs[i] > recent_highs[i-1] and 
                recent_highs[i] > recent_highs[i-2] and
                recent_highs[i] > recent_highs[i+1] and 
                recent_highs[i] > recent_highs[i+2]):
                swing_highs.append(recent_highs[i])
        
        # Find swing lows (local minima)
        swing_lows = []
        for i in range(2, len(recent_lows) - 2):
            if (recent_lows[i] < recent_lows[i-1] and 
                recent_lows[i] < recent_lows[i-2] and
                recent_lows[i] < recent_lows[i+1] and 
                recent_lows[i] < recent_lows[i+2]):
                swing_lows.append(recent_lows[i])
        
        # Key levels
        period_high = max(recent_highs)
        period_low = min(recent_lows)
        prev_close = closes[-2] if len(closes) > 1 else current_price
        
        # Resistance levels (above current price)
        resistances = sorted([h for h in swing_highs if h > current_price])[:3]
        if not resistances:
            resistances = [period_high]
        
        # Support levels (below current price)
        supports = sorted([l for l in swing_lows if l < current_price], reverse=True)[:3]
        if not supports:
            supports = [period_low]
        
        return {
            "current_price": current_price,
            "resistance_levels": resistances,
            "support_levels": supports,
            "period_high": period_high,
            "period_low": period_low,
            "previous_close": prev_close,
            "distance_to_resistance_pct": ((resistances[0] - current_price) / current_price * 100) if resistances else None,
            "distance_to_support_pct": ((current_price - supports[0]) / current_price * 100) if supports else None
        }
