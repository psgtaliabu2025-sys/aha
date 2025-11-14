# Bot Trading - Strategi Spesifik & Trading Rules

## 📋 STRATEGI 1: Mean Reversion (Cocok untuk Crypto & Range Markets)

### Konsep Dasar
Mean reversion berasumsi bahwa harga akan kembali ke rata-ratanya setelah deviation ekstrim. Cocok untuk:
- Range-bound markets
- Cryptocurrency (24/7 trading)
- Highly liquid pairs
- Scalping & day trading

### Setup Teknis
```
Timeframe: 1 hour atau 15 minutes
Indicators:
├─ Bollinger Bands (20, 2)
├─ RSI (14)
├─ SMA (20)
└─ Volume (average of 20 periods)

Entry Conditions (BUY):
├─ Price touches Bollinger Band lower band
├─ RSI < 30 (oversold)
├─ Volume > 20 period average
├─ Close > SMA 20
└─ Support level holds

Entry Conditions (SELL):
├─ Price touches Bollinger Band upper band
├─ RSI > 70 (overbought)
├─ Volume > 20 period average
├─ Close < SMA 20
└─ Resistance level holds

Position Management:
├─ Entry: At Bollinger Band touch
├─ Stop Loss: Below/above band + 0.5 ATR
├─ Take Profit 1: SMA 20 (50% of position)
├─ Take Profit 2: Opposite band (50% of position)
└─ Risk-Reward Ratio: 1:2 minimum

Risk Management:
├─ Position Size: 2% risk per trade
├─ Max Daily Loss: -5% from account
├─ Max Positions: 3 simultaneously
└─ Max Drawdown: 20%
```

### Trading Rules
```
Rule 1: ENTRY CRITERIA (ALL must be true)
  ✓ Price touches Bollinger Band (upper or lower)
  ✓ RSI confirmation (< 30 for buy, > 70 for sell)
  ✓ Volume > 20 MA (shows conviction)
  ✓ Support/Resistance holds
  ✓ No news/events in next 1 hour
  → EXECUTE TRADE

Rule 2: POSITION MANAGEMENT
  ✓ Always set stop loss (MANDATORY)
  ✓ Set partial take profit at 50%
  ✓ Let winners run with trailing stop
  → MONITOR POSITIONS

Rule 3: EXIT CRITERIA
  ✓ Exit at predefined SL or TP
  ✓ Exit if technical setup breaks
  ✓ Exit if price closes opposite side of SMA
  ✓ Exit if RSI returns to 50 level
  → CLOSE POSITION

Rule 4: SKIP CONDITIONS (Don't trade if)
  ✗ News/Economic data due in next 1 hour
  ✗ Volatility ATR > 2 standard deviations
  ✗ Previous trade lost, skip next 1 hour
  ✗ Already 3 open positions
  → WAIT FOR BETTER SETUP
```

### Performance Expected
```
Win Rate: 55-65%
Profit Factor: 1.8-2.2
Sharpe Ratio: 1.2-1.5
Monthly ROI: 8-15%
Max Drawdown: 10-15%
Avg Win/Loss: 1:2

Example on $10,000 account:
├─ Risk per trade: $200
├─ Avg Win: $400
├─ Avg Loss: $200
├─ 20 trades per month:
│  ├─ Winners: 12 × $400 = $4,800
│  ├─ Losers: 8 × $200 = -$1,600
│  ├─ Net Profit: $3,200
│  └─ Monthly ROI: 32% (aggressive but possible)
```

---

## 📈 STRATEGI 2: Trend Following (Cocok untuk Long-term Trends)

### Konsep Dasar
Follow harga yang trending naik atau turun dengan confirmation dari volume dan momentum. Cocok untuk:
- Forex markets
- Stock markets
- Cryptocurrency trending
- Swing trading & position trading
- Longer timeframes (4h, daily, weekly)

### Setup Teknis
```
Timeframe: 4 hours atau Daily
Indicators:
├─ Moving Averages (20, 50, 200)
├─ MACD (12, 26, 9)
├─ ADX (14) - for trend strength
├─ Volume (average of 20 periods)
└─ ATR (14) - for position sizing

Entry Conditions (BUY):
├─ Price above all three MAs (20 > 50 > 200)
├─ MACD line > signal line
├─ MACD histogram positive & increasing
├─ ADX > 25 (strong trend)
├─ Volume > 20 period average
└─ Close > 50 MA for confirmation

Entry Conditions (SELL):
├─ Price below all three MAs (20 < 50 < 200)
├─ MACD line < signal line
├─ MACD histogram negative & decreasing
├─ ADX > 25 (strong trend)
├─ Volume > 20 period average
└─ Close < 50 MA for confirmation

Position Management:
├─ Entry: Breakout above/below 20 MA
├─ Stop Loss: Below/above 50 MA or 2 ATR
├─ Take Profit 1: 1 ATR × 2 (50% of position)
├─ Take Profit 2: Previous resistance/support (50%)
├─ Trailing Stop: 1 ATR after breakeven
└─ Risk-Reward Ratio: 1:3 or better

Risk Management:
├─ Position Size: 1.5% risk per trade
├─ Max Daily Loss: -5%
├─ Max Positions: 2 simultaneously
├─ Max Drawdown: 20%
└─ Hold winners until trend breaks
```

### Trading Rules
```
Rule 1: TREND CONFIRMATION (ALL must be true)
  ✓ All three MAs in correct order (20/50/200)
  ✓ Price is above/below all three
  ✓ MACD crossover confirmed
  ✓ ADX > 25 (strong trend exists)
  ✓ Volume increasing
  → TREND CONFIRMED

Rule 2: ENTRY EXECUTION
  ✓ Wait for 2 consecutive closes in trend direction
  ✓ Enter at breakout of recent high/low
  ✓ Set stop loss at 50 MA or 2 ATR below entry
  ✓ Set first take profit at 2 ATR above entry
  → EXECUTE AT BREAKOUT

Rule 3: POSITION MANAGEMENT
  ✓ Let winners run (use trailing stop)
  ✓ Move stop to breakeven after 1 ATR profit
  ✓ Take 50% profit at first target
  ✓ Hold 50% for larger move
  ✓ Trail stop by 1-1.5 ATR
  → MAXIMIZE WINNERS

Rule 4: EXIT SIGNALS
  ✓ Exit all if trend breaks (ADX falls below 25)
  ✓ Exit all if close below 50 MA (for uptrend)
  ✓ Exit if MACD turns (histogram changes)
  ✓ Exit if ATR contracts significantly (low volatility)
  ✓ Take remaining profit at support/resistance
  → PRESERVE CAPITAL

Rule 5: FILTER CONDITIONS
  ✗ Don't trade if ADX < 20 (no trend)
  ✗ Don't trade against 200 MA
  ✗ Don't trade near major support/resistance
  ✗ Don't add to losing positions
  → WAIT FOR CLEAR TREND
```

### Performance Expected
```
Win Rate: 45-55% (winners are much larger)
Profit Factor: 2.2-3.0
Sharpe Ratio: 1.3-1.8
Monthly ROI: 5-12%
Max Drawdown: 12-18%
Avg Win/Loss: 1:3

Example on $10,000 account:
├─ Risk per trade: $150
├─ Avg Win: $450 (3:1 RR)
├─ Avg Loss: $150
├─ 15 trades per month:
│  ├─ Winners: 6 × $450 = $2,700
│  ├─ Losers: 9 × $150 = -$1,350
│  ├─ Net Profit: $1,350
│  └─ Monthly ROI: 13.5%
```

---

## ⚡ STRATEGI 3: Momentum Trading (Cocok untuk Volatile Markets)

### Konsep Dasar
Trade momentum menggunakan RSI, MACD, dan volume acceleration. Cocok untuk:
- High volatility periods
- Breakout trading
- Cryptocurrency in bull/bear markets
- Short timeframes (15m, 1h)
- News-driven events

### Setup Teknis
```
Timeframe: 15 minutes atau 1 hour
Indicators:
├─ RSI (14)
├─ MACD (12, 26, 9)
├─ Stochastic (14, 3, 3)
├─ Volume (average of 20 periods)
├─ EMA (20, 50)
└─ ATR (14)

Entry Conditions (BUY):
├─ RSI rising from 30-50 zone (positive momentum)
├─ RSI < 70 (not yet overbought)
├─ MACD histogram turns positive
├─ Price above EMA 20
├─ Volume increasing
├─ Stochastic cross above 20
└─ Candle closes with long body (conviction)

Entry Conditions (SELL):
├─ RSI falling from 50-70 zone (negative momentum)
├─ RSI > 30 (not yet oversold)
├─ MACD histogram turns negative
├─ Price below EMA 20
├─ Volume increasing
├─ Stochastic cross below 80
└─ Candle closes with long wick (rejection)

Position Management:
├─ Entry: At candle close with momentum signal
├─ Stop Loss: Below previous candle low
├─ Take Profit 1: +50 pips or 1% (50% of position)
├─ Take Profit 2: +100 pips or 2% (50% of position)
├─ Max Hold: 4 hours or to next support/resistance
└─ Risk-Reward Ratio: 1:1.5 to 1:2

Risk Management:
├─ Position Size: 1.5% risk per trade
├─ Max Daily Trades: 5-6 per day
├─ Max Daily Loss: -5%
├─ Max Consecutive Losses: 3, then skip 1 hour
└─ Max Drawdown: 20%
```

### Trading Rules
```
Rule 1: MOMENTUM CONFIRMATION (ALL must be true)
  ✓ RSI showing momentum in one direction
  ✓ MACD turning in same direction
  ✓ Stochastic crossing confirming direction
  ✓ Volume increasing significantly
  ✓ Price above/below EMA 20
  → MOMENTUM CONFIRMED

Rule 2: ENTRY EXECUTION
  ✓ Enter on candle close with all signals aligned
  ✓ Enter only if previous candle shows momentum
  ✓ Don't chase if already 50+ pips moved
  ✓ Set stop at previous candle extreme
  ✓ Set first TP at 50% of position
  → EXECUTE AT OPTIMAL TIMING

Rule 3: POSITION MANAGEMENT
  ✓ Take first profit automatically at 50%
  ✓ Move stop to breakeven when 50 pips profit
  ✓ Let second 50% run with trailing stop
  ✓ Hold max 4 hours then close
  ✓ Never hold overnight (gap risk)
  → SECURE PROFITS

Rule 4: EXIT SIGNALS
  ✓ Exit all if RSI reverses
  ✓ Exit all if MACD turns (histogram changes)
  ✓ Exit all if volume dries up
  ✓ Exit all if price breaks EMA 20
  ✓ Exit immediately at stop loss
  → CUT LOSSES QUICK

Rule 5: TIMING RULES
  ✓ Trade only during peak hours (9-17 UTC for forex)
  ✓ Avoid 1 hour before major news
  ✓ Avoid 2 hours after major news (whipsaw)
  ✓ Skip if ATR is < 20 pips (low volatility)
  ✓ Trade most active times of day
  → TRADE ACTIVE SESSIONS

Rule 6: SKIP CONDITIONS
  ✗ Don't trade if 3+ consecutive losses
  ✗ Don't trade if daily loss > -5%
  ✗ Don't trade around news
  ✗ Don't chase if already moved 100+ pips
  ✗ Don't add to losing positions
  → PRESERVE CAPITAL
```

### Performance Expected
```
Win Rate: 50-60% (quick profits)
Profit Factor: 1.6-2.0
Sharpe Ratio: 1.0-1.2
Monthly ROI: 8-15%
Max Drawdown: 8-12%
Avg Win/Loss: 1:1.5

Example on $10,000 account:
├─ Risk per trade: $150
├─ Avg Win: $225 (1.5:1 RR)
├─ Avg Loss: $150
├─ 30 trades per month:
│  ├─ Winners: 15 × $225 = $3,375
│  ├─ Losers: 15 × $150 = -$2,250
│  ├─ Net Profit: $1,125
│  └─ Monthly ROI: 11.25%
```

---

## 🔝 STRATEGI 4: Breakout Trading (Cocok untuk Range Breaks)

### Konsep Dasar
Enter ketika harga breakout dari range atau consolidation dengan volume confirmation. Cocok untuk:
- Breakout from support/resistance
- Cup and handle patterns
- After news/earnings
- Cryptocurrency breakouts
- Daily timeframe

### Setup Teknis
```
Timeframe: Daily
Indicators:
├─ Support & Resistance (visual)
├─ Bollinger Bands (20, 2)
├─ Volume (average of 20 days)
├─ ATR (14)
├─ EMA (20, 50)
└─ RSI (14) - divergence only

Entry Conditions (BUY BREAKOUT):
├─ Price breaks above 20-day high + close above
├─ Volume > 1.5× average volume
├─ ATR increasing (volatility expanding)
├─ Close > BB upper band
├─ Price above EMA 20 & 50
├─ Confirmation candle closes above breakout
└─ Previous support zone holds

Entry Conditions (SELL BREAKDOWN):
├─ Price breaks below 20-day low + close below
├─ Volume > 1.5× average volume
├─ ATR increasing
├─ Close < BB lower band
├─ Price below EMA 20 & 50
├─ Confirmation candle closes below breakdown
└─ Previous resistance zone cracks

Position Management:
├─ Entry: Breakout level + 1 pip above
├─ Stop Loss: Below breakout level - ATR
├─ Take Profit 1: Previous resistance/support (50%)
├─ Take Profit 2: 2× ATR from entry (50%)
├─ Trailing Stop: 1.5 ATR after breakeven
└─ Risk-Reward Ratio: 1:2.5 to 1:3

Risk Management:
├─ Position Size: 1% risk per trade (conservative)
├─ Max Daily Trades: 1-2
├─ Max Drawdown: 20%
├─ Hold longer term (days/weeks)
└─ Build positions on confirmation
```

### Trading Rules
```
Rule 1: RANGE IDENTIFICATION
  ✓ Identify consolidation/range zone
  ✓ Mark resistance & support clearly
  ✓ Confirm with multiple touches (min 2)
  ✓ Measure range width for target calculation
  ✓ Identify nearby support/resistance levels
  → RANGE MAPPED

Rule 2: BREAKOUT SETUP (ALL required)
  ✓ Price consolidating for 5-20 days
  ✓ Volume below average (contraction)
  ✓ ATR contracting (low volatility)
  ✓ No major news in near future
  → SETUP READY

Rule 3: BREAKOUT EXECUTION
  ✓ Entry: Candle close beyond range extreme
  ✓ Entry: Volume > 1.5× average
  ✓ Entry: ATR starting to expand
  ✓ Confirmation: Second candle continues move
  ✓ Stop: Below/above range opposite extreme
  → EXECUTE BREAKOUT

Rule 4: POSITION MANAGEMENT
  ✓ Partial profit at previous level
  ✓ Hold 50% for larger move
  ✓ Trail stop by 1-1.5 ATR
  ✓ Let winners run (can be 50-100 pips)
  ✓ Monitor daily closes for exit signal
  → CAPTURE FULL MOVE

Rule 5: EXIT CONDITIONS
  ✓ Stop loss at setup point
  ✓ Take profit at next major level
  ✓ Exit if close back inside range
  ✓ Exit if volume drops significantly
  ✓ Exit if trend line breaks
  → PROTECT PROFITS

Rule 6: FILTER CONDITIONS
  ✗ Don't trade if major news coming
  ✗ Don't trade breakouts against 200 MA
  ✗ Don't trade if range < 30 pips (too small)
  ✗ Don't short breakouts in uptrends
  ✗ Don't long breakdowns in downtrends
  → TRADE WITH TREND
```

### Performance Expected
```
Win Rate: 55-65% (stronger winners)
Profit Factor: 2.0-2.5
Sharpe Ratio: 1.2-1.5
Monthly ROI: 5-10%
Max Drawdown: 12-18%
Avg Win/Loss: 1:2.5

Example on $10,000 account:
├─ Risk per trade: $100
├─ Avg Win: $250 (2.5:1 RR)
├─ Avg Loss: $100
├─ 10 trades per month:
│  ├─ Winners: 6 × $250 = $1,500
│  ├─ Losers: 4 × $100 = -$400
│  ├─ Net Profit: $1,100
│  └─ Monthly ROI: 11%
```

---

## 🎯 QUICK STRATEGY COMPARISON

| Aspek | Mean Reversion | Trend Follow | Momentum | Breakout |
|------|----------------|-------------|----------|----------|
| Timeframe | 15m-1h | 4h-daily | 15m-1h | daily-weekly |
| Win Rate | 55-65% | 45-55% | 50-60% | 55-65% |
| Profit Factor | 1.8-2.2 | 2.2-3.0 | 1.6-2.0 | 2.0-2.5 |
| Avg Trade Duration | 1-4 hours | days-weeks | 30 min-4h | days-weeks |
| Risk per Trade | 2% | 1.5% | 1.5% | 1% |
| Difficulty | Medium | Medium-Hard | Easy-Medium | Hard |
| Capital Required | $5,000+ | $10,000+ | $5,000+ | $10,000+ |
| Best For | Range markets | Trending mkts | Volatile | Breakouts |

---

## 🚀 HYBRID STRATEGY: Best Practices

### Kombinasi Terbaik
```
PRIMARY STRATEGY: Trend Following (for direction)
├─ Use moving averages for trend identification
├─ Use ADX for trend strength
└─ Trade only with strong trends

SECONDARY STRATEGY: Mean Reversion (for timing)
├─ Find pullbacks within uptrend
├─ Use Bollinger Bands for reversal points
├─ Use RSI for oversold/overbought
└─ Enter on pullbacks to MA

CONFIRMATION: Momentum (for execution)
├─ Use MACD for entry signal
├─ Use volume for conviction
├─ Use Stochastic for timing
└─ Enter on momentum spike

RESULT: Highly Profitable Combination
├─ Trend ensures high-probability trades
├─ Mean reversion finds best entry
├─ Momentum confirms execution timing
└─ Win rate: 60%+, Profit Factor: 2.5+
```

---

## 💡 FINAL TIPS

### Top 5 Strategies untuk Beginners
1. ✅ **Mean Reversion** - Easiest to learn, consistent
2. ✅ **Trend Following** - High probability, longer holds
3. ✅ **Breakout** - Clear setup, easy rules
4. ⚠️ **Momentum** - Requires timing skills
5. ❌ **Scalping** - NOT recommended for beginners

### Common Mistakes dalam Strategy
❌ Too many indicators (keep it simple)
❌ Over-optimization (test out-of-sample)
❌ Ignoring risk management (size your positions)
❌ Not following rules (emotional trading)
❌ Changing strategy too often (give time to prove itself)

### Key Success Factors
✅ Simple strategy that you understand
✅ Rules written clearly, not ambiguous
✅ Backtested thoroughly (200+ trades)
✅ Risk management strictly enforced
✅ Emotional discipline & patience
✅ Regular performance monitoring
✅ Willingness to admit when wrong

