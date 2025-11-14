"""
Bot Trading Implementation - Complete Example
Strategi: Simple Moving Average Crossover + RSI Filter
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


# ============================================================================
# 1. CONFIGURATION & SETUP
# ============================================================================

@dataclass
class BotConfig:
    """Konfigurasi Bot Trading"""
    # Strategy Parameters
    fast_ma_period: int = 20
    slow_ma_period: int = 50
    rsi_period: int = 14
    rsi_overbought: float = 70
    rsi_oversold: float = 30
    
    # Risk Management
    account_size: float = 10000.0
    risk_per_trade: float = 0.02  # 2% per trade
    max_position_size: float = 0.05  # Max 5% per position
    max_daily_loss: float = 0.05  # Max 5% daily loss
    max_drawdown: float = 0.20  # Max 20% drawdown
    
    # Trade Management
    rr_ratio: float = 2.0  # Risk-Reward 1:2
    atr_multiplier_sl: float = 1.5  # Stop Loss = Entry - ATR * 1.5
    atr_multiplier_tp: float = 2.0  # Take Profit = Entry + ATR * 2.0
    atr_period: int = 14
    
    # Execution
    order_type: str = "market"  # "market" or "limit"
    max_slippage: float = 0.01  # 1% max slippage
    
    # Monitoring
    log_level: str = "INFO"
    save_trades: bool = True
    # strategy selector: 'macrossover_rsi' or 'mean_reversion'
    strategy: str = "macrossover_rsi"


class OrderType(Enum):
    """Tipe Order"""
    BUY = "BUY"
    SELL = "SELL"
    CLOSE = "CLOSE"


class OrderStatus(Enum):
    """Status Order"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass
class Order:
    """Representasi Order"""
    order_id: str
    order_type: OrderType
    symbol: str
    quantity: float
    price: float
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    created_at: datetime = None
    filled_at: Optional[datetime] = None
    execution_price: Optional[float] = None


@dataclass
class Trade:
    """Representasi Trade (Open atau Closed)"""
    trade_id: str
    symbol: str
    entry_price: float
    entry_time: datetime
    quantity: float
    
    # Risk Management
    stop_loss: float
    take_profit: float
    
    # Exit Info
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    exit_reason: Optional[str] = None
    
    @property
    def pnl(self) -> float:
        """Calculate P&L jika closed"""
        if self.exit_price is None:
            return 0.0
        return (self.exit_price - self.entry_price) * self.quantity
    
    @property
    def pnl_percent(self) -> float:
        """Calculate P&L % jika closed"""
        if self.exit_price is None:
            return 0.0
        return ((self.exit_price - self.entry_price) / self.entry_price) * 100
    
    @property
    def is_win(self) -> bool:
        """Apakah trade menguntungkan"""
        return self.pnl > 0 if self.exit_price is not None else False
    
    @property
    def risk_reward_actual(self) -> float:
        """Actual risk-reward ratio"""
        if self.exit_price is None:
            return 0.0
        
        risk = self.entry_price - self.stop_loss
        reward = abs(self.exit_price - self.entry_price)
        
        if risk == 0:
            return 0.0
        return reward / risk


# ============================================================================
# 2. TECHNICAL INDICATORS
# ============================================================================

class TechnicalIndicators:
    """Calculate Technical Indicators"""
    
    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, 
                     period: int = 14) -> pd.Series:
        """Average True Range"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, period: int = 20, 
                                 std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands"""
        sma = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, 
                      signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD Indicator"""
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram


# ============================================================================
# 3. STRATEGY BASE CLASS
# ============================================================================

class BaseStrategy(ABC):
    """Base class untuk semua strategi trading"""
    
    def __init__(self, config: BotConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame, current_idx: int) -> Dict:
        """
        Generate trading signal
        
        Returns:
            {
                'action': 'BUY' | 'SELL' | 'HOLD',
                'confidence': 0.0-1.0,
                'reason': str
            }
        """
        pass
    
    @abstractmethod
    def calculate_stop_loss_take_profit(self, entry_price: float, 
                                       data: pd.DataFrame, 
                                       current_idx: int) -> Tuple[float, float]:
        """
        Calculate stop loss dan take profit
        
        Returns:
            (stop_loss_price, take_profit_price)
        """
        pass
    
    def validate_signal(self, signal: Dict, balance: float, 
                       entry_price: float) -> bool:
        """Validate apakah signal valid untuk entry"""
        
        if signal['action'] == 'HOLD':
            return False
        
        if signal['confidence'] < 0.5:
            self.logger.debug(f"Signal confidence terlalu rendah: {signal['confidence']}")
            return False
        
        if balance <= 0:
            self.logger.warning("Insufficient balance")
            return False
        
        return True


# ============================================================================
# 4. STRATEGY IMPLEMENTATION
# ============================================================================

class MACrossoverRSIStrategy(BaseStrategy):
    """
    Strategi: Moving Average Crossover dengan RSI Filter
    
    Entry Buy:
    - Fast MA (20) > Slow MA (50)
    - RSI > 30 (not oversold)
    - Volume increasing
    
    Entry Sell:
    - Fast MA (20) < Slow MA (50)
    - RSI < 70 (not overbought)
    
    Exit:
    - Stop Loss: Entry - ATR*1.5
    - Take Profit: Entry + ATR*2.0
    """
    
    def __init__(self, config: BotConfig, logger: logging.Logger):
        super().__init__(config, logger)
        self.indicators = TechnicalIndicators()
        self.last_signal = None
    
    def generate_signal(self, data: pd.DataFrame, current_idx: int) -> Dict:
        """Generate buy/sell signal"""
        
        # Ensure sufficient data
        if current_idx < self.config.slow_ma_period + 1:
            return {'action': 'HOLD', 'confidence': 0.0, 'reason': 'Insufficient data'}
        
        # Calculate indicators
        close = data['close'].iloc[:current_idx+1]
        high = data['high'].iloc[:current_idx+1]
        low = data['low'].iloc[:current_idx+1]
        volume = data['volume'].iloc[:current_idx+1]
        
        # Moving Averages
        sma_fast = self.indicators.calculate_sma(close, self.config.fast_ma_period)
        sma_slow = self.indicators.calculate_sma(close, self.config.slow_ma_period)
        
        # RSI
        rsi = self.indicators.calculate_rsi(close, self.config.rsi_period)
        
        # Current values
        current_price = close.iloc[-1]
        current_sma_fast = sma_fast.iloc[-1]
        current_sma_slow = sma_slow.iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_volume = volume.iloc[-1]
        avg_volume = volume.iloc[-50:].mean()
        
        # Crossover signals
        prev_sma_fast = sma_fast.iloc[-2]
        prev_sma_slow = sma_slow.iloc[-2]
        
        signal = {'action': 'HOLD', 'confidence': 0.0, 'reason': ''}
        
        # BUY Signal
        if (prev_sma_fast <= prev_sma_slow and 
            current_sma_fast > current_sma_slow and
            current_rsi > self.config.rsi_oversold and
            current_rsi < self.config.rsi_overbought and
            current_volume > avg_volume):
            
            confidence = min(0.95, 0.7 + (current_rsi - 30) / 100)  # Higher RSI = higher confidence
            signal = {
                'action': 'BUY',
                'confidence': confidence,
                'reason': f'MA Crossover Up | RSI:{current_rsi:.1f} | Volume:{current_volume/avg_volume:.1f}x'
            }
        
        # SELL Signal
        elif (prev_sma_fast >= prev_sma_slow and 
              current_sma_fast < current_sma_slow and
              current_rsi < self.config.rsi_overbought and
              current_volume > avg_volume):
            
            confidence = min(0.95, 0.7 + (70 - current_rsi) / 100)
            signal = {
                'action': 'SELL',
                'confidence': confidence,
                'reason': f'MA Crossover Down | RSI:{current_rsi:.1f} | Volume:{current_volume/avg_volume:.1f}x'
            }
        
        self.last_signal = signal
        return signal
    
    def calculate_stop_loss_take_profit(self, entry_price: float, 
                                       data: pd.DataFrame, 
                                       current_idx: int) -> Tuple[float, float]:
        """Calculate SL and TP based on ATR"""
        
        high = data['high'].iloc[:current_idx+1]
        low = data['low'].iloc[:current_idx+1]
        close = data['close'].iloc[:current_idx+1]
        
        atr = self.indicators.calculate_atr(high, low, close, self.config.atr_period)
        current_atr = atr.iloc[-1]
        
        # Stop Loss: entry - ATR*1.5
        stop_loss = entry_price - (current_atr * self.config.atr_multiplier_sl)
        
        # Take Profit: entry + ATR*2.0
        take_profit = entry_price + (current_atr * self.config.atr_multiplier_tp)
        
        return stop_loss, take_profit


class MeanReversionStrategy(BaseStrategy):
    """
    Mean Reversion Strategy:
    - Uses Bollinger Bands (20,2) and RSI filter
    - Buy when price touches lower band and RSI < oversold
    - Sell when price touches upper band and RSI > overbought
    """

    def __init__(self, config: BotConfig, logger: logging.Logger):
        super().__init__(config, logger)
        self.indicators = TechnicalIndicators()
        self.last_signal = None

    def generate_signal(self, data: pd.DataFrame, current_idx: int) -> Dict:
        if current_idx < 30:
            return {'action': 'HOLD', 'confidence': 0.0, 'reason': 'Insufficient data'}

        close = data['close'].iloc[:current_idx+1]
        high = data['high'].iloc[:current_idx+1]
        low = data['low'].iloc[:current_idx+1]
        volume = data['volume'].iloc[:current_idx+1]

        upper, mid, lower = self.indicators.calculate_bollinger_bands(close, period=20, std_dev=2)
        rsi = self.indicators.calculate_rsi(close, period=self.config.rsi_period)

        current_price = close.iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_volume = volume.iloc[-1]
        avg_volume = volume.iloc[-50:].mean()

        signal = {'action': 'HOLD', 'confidence': 0.0, 'reason': ''}

        # Buy condition: touch lower band, RSI oversold and volume confirmation
        if current_price <= lower.iloc[-1] and current_rsi <= self.config.rsi_oversold and current_volume >= 0.8 * avg_volume:
            confidence = min(0.95, 0.6 + (self.config.rsi_oversold - current_rsi) / 100)
            signal = {'action': 'BUY', 'confidence': confidence, 'reason': f'MeanReversion Buy | RSI:{current_rsi:.1f}'}

        # Sell condition: touch upper band, RSI overbought and volume confirmation
        elif current_price >= upper.iloc[-1] and current_rsi >= self.config.rsi_overbought and current_volume >= 0.8 * avg_volume:
            confidence = min(0.95, 0.6 + (current_rsi - self.config.rsi_overbought) / 100)
            signal = {'action': 'SELL', 'confidence': confidence, 'reason': f'MeanReversion Sell | RSI:{current_rsi:.1f}'}

        self.last_signal = signal
        return signal

    def calculate_stop_loss_take_profit(self, entry_price: float, data: pd.DataFrame, current_idx: int) -> Tuple[float, float]:
        high = data['high'].iloc[:current_idx+1]
        low = data['low'].iloc[:current_idx+1]
        close = data['close'].iloc[:current_idx+1]

        atr = self.indicators.calculate_atr(high, low, close, self.config.atr_period)
        current_atr = atr.iloc[-1]

        # For mean reversion, tighter SL and moderate TP
        stop_loss = entry_price - (current_atr * self.config.atr_multiplier_sl)
        take_profit = entry_price + (current_atr * self.config.atr_multiplier_tp)
        return stop_loss, take_profit


# ============================================================================
# 5. RISK MANAGEMENT
# ============================================================================

class RiskManager:
    """Manage risk dan position sizing"""
    
    def __init__(self, config: BotConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    def calculate_position_size(self, account_balance: float, entry_price: float,
                               stop_loss: float) -> float:
        """
        Calculate position size based on:
        - Account balance
        - Risk per trade (2%)
        - Entry price & Stop Loss
        """
        
        # Risk amount
        risk_amount = account_balance * self.config.risk_per_trade
        
        # Risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit == 0:
            self.logger.error("Risk per unit is zero, cannot calculate position size")
            return 0.0
        
        # Position size
        position_size = risk_amount / risk_per_unit
        
        # Check max position size
        max_position = account_balance * self.config.max_position_size
        max_units = max_position / entry_price
        
        position_size = min(position_size, max_units)
        
        self.logger.debug(f"Calculated position size: {position_size} units")
        
        return position_size
    
    def check_daily_loss_limit(self, current_pnl: float, account_balance: float) -> bool:
        """Check apakah daily loss limit sudah exceeded"""
        
        max_daily_loss = account_balance * self.config.max_daily_loss
        
        if current_pnl < -max_daily_loss:
            self.logger.warning(f"Daily loss limit exceeded: {current_pnl:.2f} < {-max_daily_loss:.2f}")
            return False
        
        return True
    
    def check_max_drawdown(self, current_equity: float, peak_equity: float) -> bool:
        """Check apakah max drawdown limit sudah exceeded"""
        
        if peak_equity == 0:
            return True
        
        drawdown = (peak_equity - current_equity) / peak_equity
        
        if drawdown > self.config.max_drawdown:
            self.logger.warning(f"Max drawdown exceeded: {drawdown*100:.2f}% > {self.config.max_drawdown*100:.2f}%")
            return False
        
        return True


# ============================================================================
# 6. ORDER EXECUTOR
# ============================================================================

class OrderExecutor:
    """Handle order execution"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.open_orders: Dict[str, Order] = {}
        self.closed_orders: List[Order] = []
        self.order_counter = 0
    
    def create_buy_order(self, symbol: str, quantity: float, 
                        price: float, order_type: str = "market") -> Order:
        """Create buy order"""
        
        self.order_counter += 1
        order = Order(
            order_id=f"BUY_{symbol}_{self.order_counter}",
            order_type=OrderType.BUY,
            symbol=symbol,
            quantity=quantity,
            price=price,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.open_orders[order.order_id] = order
        self.logger.info(f"Created BUY order: {order.order_id} | {quantity} @ {price}")
        
        return order
    
    def create_sell_order(self, symbol: str, quantity: float,
                         price: float, order_type: str = "market") -> Order:
        """Create sell order"""
        
        self.order_counter += 1
        order = Order(
            order_id=f"SELL_{symbol}_{self.order_counter}",
            order_type=OrderType.SELL,
            symbol=symbol,
            quantity=quantity,
            price=price,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.open_orders[order.order_id] = order
        self.logger.info(f"Created SELL order: {order.order_id} | {quantity} @ {price}")
        
        return order
    
    def fill_order(self, order_id: str, execution_price: float,
                  filled_quantity: Optional[float] = None) -> bool:
        """Fill order dengan execution price"""
        
        if order_id not in self.open_orders:
            self.logger.error(f"Order not found: {order_id}")
            return False
        
        order = self.open_orders[order_id]
        filled_qty = filled_quantity if filled_quantity else order.quantity
        
        order.filled_quantity = filled_qty
        order.execution_price = execution_price
        order.filled_at = datetime.now()
        
        if abs(order.filled_quantity - order.quantity) < 0.001:  # Fully filled
            order.status = OrderStatus.FILLED
        else:
            order.status = OrderStatus.PARTIALLY_FILLED
        
        self.logger.info(f"Filled order {order_id}: {filled_qty} @ {execution_price}")
        
        return True


# ============================================================================
# 7. TRADING BOT MAIN ENGINE
# ============================================================================

class TradingBot:
    """Main Trading Bot Engine"""
    
    def __init__(self, config: BotConfig, strategy: BaseStrategy, 
                 logger: logging.Logger):
        self.config = config
        self.strategy = strategy
        self.logger = logger
        
        self.risk_manager = RiskManager(config, logger)
        self.order_executor = OrderExecutor(logger)
        
        # Account state
        self.balance = config.account_size
        self.equity = config.account_size
        self.peak_equity = config.account_size
        
        # Trading state
        self.open_trades: Dict[str, Trade] = {}
        self.closed_trades: List[Trade] = []
        self.trade_counter = 0
        
        # Performance tracking
        self.daily_trades: List[Trade] = []
        self.daily_pnl = 0.0
    
    def process_candle(self, data: pd.DataFrame, current_idx: int, 
                      current_price: float) -> None:
        """Process new candle and execute trading logic"""
        
        # Check for exit conditions on open trades
        self._check_open_trades(current_price, current_idx, data)
        
        # Generate signal
        signal = self.strategy.generate_signal(data, current_idx)
        
        # Validate signal
        if not self.strategy.validate_signal(signal, self.balance, current_price):
            return
        
        # Execute signal
        if signal['action'] == 'BUY':
            self._execute_buy_signal(signal, current_price, data, current_idx)
        elif signal['action'] == 'SELL':
            self._execute_sell_signal(signal, current_price, data, current_idx)
    
    def _execute_buy_signal(self, signal: Dict, current_price: float,
                           data: pd.DataFrame, current_idx: int) -> None:
        """Execute buy signal"""
        
        # Calculate SL & TP
        stop_loss, take_profit = self.strategy.calculate_stop_loss_take_profit(
            current_price, data, current_idx
        )
        
        # Calculate position size
        position_size = self.risk_manager.calculate_position_size(
            self.balance, current_price, stop_loss
        )
        
        if position_size <= 0:
            self.logger.warning("Invalid position size, skipping trade")
            return
        
        # Check if we have sufficient balance
        required_balance = position_size * current_price
        if required_balance > self.balance:
            self.logger.warning(f"Insufficient balance: {required_balance:.2f} > {self.balance:.2f}")
            return
        
        # Create trade
        self.trade_counter += 1
        trade = Trade(
            trade_id=f"TRADE_{self.trade_counter}",
            symbol="BTC/USD",  # Replace with actual symbol
            entry_price=current_price,
            entry_time=datetime.now(),
            quantity=position_size,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        # Create order
        order = self.order_executor.create_buy_order(
            trade.symbol, position_size, current_price
        )
        
        # Fill order immediately (market order)
        self.order_executor.fill_order(order.order_id, current_price, position_size)
        
        # Add to open trades
        self.open_trades[trade.trade_id] = trade
        
        # Update balance
        self.balance -= required_balance
        
        self.logger.info(
            f"BUY Trade Opened: {trade.trade_id}\n"
            f"  Entry: {current_price:.2f}\n"
            f"  SL: {stop_loss:.2f}\n"
            f"  TP: {take_profit:.2f}\n"
            f"  Size: {position_size:.4f}\n"
            f"  Signal: {signal['reason']}"
        )
    
    def _execute_sell_signal(self, signal: Dict, current_price: float,
                            data: pd.DataFrame, current_idx: int) -> None:
        """Execute sell signal - usually closes open positions"""
        
        # Close all open trades
        for trade_id, trade in list(self.open_trades.items()):
            self._close_trade(trade_id, current_price, "Sell Signal")
    
    def _check_open_trades(self, current_price: float, current_idx: int,
                          data: pd.DataFrame) -> None:
        """Check open trades for SL/TP hits"""
        
        for trade_id, trade in list(self.open_trades.items()):
            # Check Take Profit
            if current_price >= trade.take_profit:
                self._close_trade(trade_id, trade.take_profit, "Take Profit Hit")
            
            # Check Stop Loss
            elif current_price <= trade.stop_loss:
                self._close_trade(trade_id, trade.stop_loss, "Stop Loss Hit")
    
    def _close_trade(self, trade_id: str, exit_price: float,
                    exit_reason: str) -> None:
        """Close an open trade"""
        
        if trade_id not in self.open_trades:
            self.logger.error(f"Trade not found: {trade_id}")
            return
        
        trade = self.open_trades[trade_id]
        
        # Calculate P&L
        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.exit_reason = exit_reason
        
        pnl = trade.pnl
        pnl_percent = trade.pnl_percent
        
        # Update balance
        self.balance += (trade.quantity * exit_price) + pnl
        
        # Move to closed trades
        del self.open_trades[trade_id]
        self.closed_trades.append(trade)
        self.daily_trades.append(trade)
        self.daily_pnl += pnl
        
        # Update equity
        self.equity = self.balance + sum(t.quantity * (exit_price if t.exit_price else 0) 
                                         for t in self.open_trades.values())
        
        self.peak_equity = max(self.peak_equity, self.equity)
        
        self.logger.info(
            f"Trade Closed: {trade_id}\n"
            f"  Entry: {trade.entry_price:.2f}\n"
            f"  Exit: {exit_price:.2f} ({exit_reason})\n"
            f"  P&L: {pnl:.2f} ({pnl_percent:.2f}%)\n"
            f"  RR Ratio: {trade.risk_reward_actual:.2f}\n"
            f"  Balance: {self.balance:.2f}"
        )
    
    def get_daily_report(self) -> Dict:
        """Get daily performance report"""
        
        if not self.daily_trades:
            return {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0.0,
                'daily_pnl': 0.0,
                'daily_pnl_percent': 0.0
            }
        
        wins = sum(1 for t in self.daily_trades if t.is_win)
        losses = len(self.daily_trades) - wins
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'trades': len(self.daily_trades),
            'wins': wins,
            'losses': losses,
            'win_rate': (wins / len(self.daily_trades)) * 100 if self.daily_trades else 0.0,
            'daily_pnl': self.daily_pnl,
            'daily_pnl_percent': (self.daily_pnl / self.config.account_size) * 100,
            'balance': self.balance,
            'equity': self.equity
        }
    
    def get_overall_report(self) -> Dict:
        """Get overall performance report"""
        
        if not self.closed_trades:
            return {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0.0,
                'profit_factor': 0.0,
                'total_pnl': 0.0,
                'total_pnl_percent': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'max_win': 0.0,
                'max_loss': 0.0,
                'balance': self.balance,
                'max_drawdown': 0.0
            }
        
        wins = [t for t in self.closed_trades if t.is_win]
        losses = [t for t in self.closed_trades if not t.is_win]
        
        total_pnl = sum(t.pnl for t in self.closed_trades)
        gross_profit = sum(t.pnl for t in wins) if wins else 0
        gross_loss = abs(sum(t.pnl for t in losses)) if losses else 0
        
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0
        
        avg_win = (gross_profit / len(wins)) if wins else 0.0
        avg_loss = -(gross_loss / len(losses)) if losses else 0.0
        
        max_win = max([t.pnl for t in wins]) if wins else 0.0
        max_loss = min([t.pnl for t in losses]) if losses else 0.0
        
        max_drawdown = (self.peak_equity - self.equity) / self.peak_equity if self.peak_equity > 0 else 0.0
        
        return {
            'total_trades': len(self.closed_trades),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': (len(wins) / len(self.closed_trades)) * 100,
            'profit_factor': profit_factor,
            'total_pnl': total_pnl,
            'total_pnl_percent': (total_pnl / self.config.account_size) * 100,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_win': max_win,
            'max_loss': max_loss,
            'balance': self.balance,
            'equity': self.equity,
            'max_drawdown': max_drawdown * 100
        }


# ============================================================================
# 8. EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Create config
    config = BotConfig(
        account_size=10000.0,
        risk_per_trade=0.02,
        fast_ma_period=20,
        slow_ma_period=50,
        rsi_period=14
    )
    
    # Create strategy (select via environment variable STRATEGY or config)
    selected = os.getenv('STRATEGY', config.strategy).lower()
    if selected in ('mean_reversion', 'meanreversion', 'mean_rev'):
        strategy = MeanReversionStrategy(config, logger)
        logger.info('Selected strategy: MeanReversionStrategy')
    else:
        strategy = MACrossoverRSIStrategy(config, logger)
        logger.info('Selected strategy: MACrossoverRSIStrategy')
    
    # Create bot
    bot = TradingBot(config, strategy, logger)
    
    logger.info("Trading Bot Initialized")
    logger.info("="*60)
    
    # Example: Generate sample data
    # In real implementation, load dari exchange API
    dates = pd.date_range(start='2023-01-01', periods=500, freq='1H')
    data = pd.DataFrame({
        'timestamp': dates,
        'open': 100 + np.cumsum(np.random.randn(500) * 0.5),
        'high': 102 + np.cumsum(np.random.randn(500) * 0.5),
        'low': 98 + np.cumsum(np.random.randn(500) * 0.5),
        'close': 100 + np.cumsum(np.random.randn(500) * 0.5),
        'volume': 1000000 + np.random.randint(-100000, 100000, 500)
    })
    
    # Ensure high > close, low < close
    data['high'] = data[['high', 'close']].max(axis=1)
    data['low'] = data[['low', 'close']].min(axis=1)
    
    # Run backtest
    for idx in range(200, len(data)):
        current_price = data['close'].iloc[idx]
        bot.process_candle(data, idx, current_price)
    
    # Print reports
    print("\n" + "="*60)
    print("DAILY REPORT")
    print("="*60)
    print(json.dumps(bot.get_daily_report(), indent=2))
    
    print("\n" + "="*60)
    print("OVERALL REPORT")
    print("="*60)
    print(json.dumps(bot.get_overall_report(), indent=2))
    
    print("\n" + "="*60)
    print("TRADES CLOSED")
    print("="*60)
    for trade in bot.closed_trades[:10]:  # Print first 10 trades
        print(f"\nTrade: {trade.trade_id}")
        print(f"  Entry: {trade.entry_price:.2f} @ {trade.entry_time}")
        print(f"  Exit: {trade.exit_price:.2f} @ {trade.exit_time} ({trade.exit_reason})")
        print(f"  P&L: {trade.pnl:.2f} ({trade.pnl_percent:.2f}%)")
        print(f"  Size: {trade.quantity:.4f}")
