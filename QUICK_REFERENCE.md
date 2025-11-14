# 🎯 QUICK REFERENCE CARD - Bot Trading Cheat Sheet

Gunakan ini sebagai reference cepat saat trading atau development.

---

## 📊 KEY METRICS QUICK REFERENCE

### Win Rate
```
Poor:           < 40%
Acceptable:     40-50%
Good:           50-60%
Excellent:      > 60%

Formula: (Winning Trades / Total Trades) × 100
```

### Profit Factor
```
Poor:           < 1.0 (losing strategy)
Acceptable:     1.0-1.5
Good:           1.5-2.0
Excellent:      > 2.0

Formula: Gross Profit / Gross Loss
```

### Risk-Reward Ratio
```
Minimum:        1:1.5
Good:           1:2.0
Excellent:      1:3.0

Formula: Average Win / Average Loss
```

### Sharpe Ratio
```
Poor:           < 0.5
Acceptable:     0.5-1.0
Good:           1.0-2.0
Excellent:      > 2.0

Formula: (Return - Risk-Free Rate) / Volatility
```

### Maximum Drawdown
```
Poor:           > 30%
Acceptable:     20-30%
Good:           10-20%
Excellent:      < 10%

Formula: (Peak - Trough) / Peak × 100%
```

---

## 💰 POSITION SIZING FORMULA

```
Risk per Trade = Account Size × Risk Percentage
Position Size = Risk Amount / (Entry - Stop Loss)

Example:
├─ Account: $10,000
├─ Risk %: 2%
├─ Risk Amount: $200
├─ Entry: $100
├─ Stop Loss: $98
├─ Position Size: $200 / (100-98) = 100 units
└─ Check: 100 × $100 = $10,000 worth = Full account
   (This is too much! Reduce to 50 units)
```

---

## 🛑 STOP LOSS & TAKE PROFIT

### Fixed-Distance (Static)
```
Stop Loss = Entry - (ATR × Multiplier)
Take Profit = Entry + (ATR × Multiplier × 2)

Example (ATR=1.5):
├─ Entry: 100
├─ SL: 100 - (1.5 × 2) = 97
├─ TP: 100 + (1.5 × 2 × 2) = 106
└─ Risk-Reward: 1:2
```

### Dynamic Trailing Stop
```
Trailing Stop = Current Price - (ATR × Multiplier)

Move stop only UP (never down)
In downtrend: Sell if price below SL
```

### Partial Profit Taking
```
Position A: 50% at +50 pips (lock in)
Position B: 50% ride with trailing stop

Or:
1/3 at 1:1 RR
1/3 at 1:2 RR
1/3 ride full move
```

---

## 📈 DAILY/WEEKLY TRADING CHECKLIST

### Pre-Market
- [ ] Check overnight news
- [ ] Review price levels
- [ ] Check volatility (ATR)
- [ ] Prepare trading plan
- [ ] Verify systems operational

### During Trading
- [ ] Check trades per my rules
- [ ] Monitor P&L
- [ ] Watch for signals
- [ ] Exit at predefined levels
- [ ] No manual overrides!

### Post-Market
- [ ] Record all trades
- [ ] Calculate metrics
- [ ] Review journal entries
- [ ] Note lessons learned
- [ ] Plan for tomorrow

### Weekly
- [ ] Calculate win rate
- [ ] Calculate profit factor
- [ ] Calculate sharpe ratio
- [ ] Check max drawdown
- [ ] Compare vs targets
- [ ] Plan adjustments

---

## ⚠️ RISK MANAGEMENT RULES

### Position Sizing
```
✅ Always: 2% risk per trade maximum
✅ Always: Max position = 5% of account
✅ Always: Check balance before entering
❌ Never: Risk > 2% per trade
❌ Never: Overtrade when losing
```

### Daily Limits
```
✅ If lost 5% today → Stop trading
✅ If lost 3 consecutive trades → Skip next signal
✅ If won last 3 → Can add small size

❌ Never: Add to losing trades
❌ Never: Revenge trade after losses
❌ Never: Trade with high emotion
```

### Max Drawdown
```
Account at $10,000:
├─ 10% drawdown = $1,000 → Continue
├─ 20% drawdown = $2,000 → Reduce size 50%
└─ 30% drawdown = $3,000 → Stop trading

Action:
• Reduce position sizing 50%
• Reanalyze strategy
• Wait for recovery
```

---

## 🎯 SIGNAL CONFIRMATION CHECKLIST

Before entering any trade:
```
✅ Trend aligned? (Is signal with trend?)
✅ Volume confirmation? (Volume > average?)
✅ Support/Resistance holding? (Price making sense?)
✅ Timeframe aligned? (All timeframes same direction?)
✅ No news coming? (Next 1-4 hours clear?)
✅ Position size correct? (2% risk rule?)
✅ Stop loss set? (Before buying!)
✅ Take profit set? (At 1:2 minimum?)

If ANY ✅ is NO → SKIP THIS TRADE
```

---

## 🔄 TRADE EXECUTION CHECKLIST

1. **Pre-Entry**
   - [ ] Signal confirmed (all checkboxes ✅)
   - [ ] Calculate position size
   - [ ] Verify account balance sufficient
   - [ ] Set stop loss level
   - [ ] Set take profit level

2. **Entry**
   - [ ] Place order (market or limit)
   - [ ] Wait for fill confirmation
   - [ ] Record entry price & time
   - [ ] Set hard stops on exchange

3. **Management**
   - [ ] Monitor 5 min after entry
   - [ ] Check for quick reversal
   - [ ] Move stop if needed (profit protection)
   - [ ] DON'T add to position

4. **Exit**
   - [ ] Exit at SL or TP
   - [ ] Record exit price & time
   - [ ] Record P&L
   - [ ] Log trade in journal

---

## 📊 TRADE JOURNAL TEMPLATE

For each trade record:
```
Date: 2025-01-13
Time In: 09:30 | Time Out: 10:15

Setup: MA Crossover + RSI 35 + Volume 1.5x
Entry: 100.50
Stop Loss: 99.00
Take Profit: 102.50
Position Size: 50 units
Risk: $75

Exit: Take Profit (102.50)
P&L: +$100 (1.33%)

Market Condition: Uptrend, good volume
Confidence: 7/10
Reason: Classic MA crossover with confirmation
Mistake: Could have better entry at consolidation
Lesson: Patience sometimes better than speed

Emotional State: 😊 Calm and focused
```

---

## 📱 MONITORING DASHBOARD TEMPLATE

### Daily Dashboard
```
Date: 2025-01-13 | Time: 17:00

TRADES TODAY:
├─ Opened: 4
├─ Closed: 3
├─ P&L: +$150
└─ Win Rate: 2/3 = 66%

POSITIONS:
├─ BTC/USD: +50 units, +$200 unrealized
├─ ETH/USD: -30 units, -$50 unrealized
└─ Open P&L: +$150

ACCOUNT:
├─ Balance: $10,150
├─ Today P&L: +$150 (1.5%)
├─ Drawdown: -2% from peak
└─ Risk Used: 2% (at limit!)

ALERTS:
⚠️ Daily loss limit approaching
✅ All systems operational
✅ No technical errors
```

### Weekly Dashboard
```
Week of: 2025-01-13

PERFORMANCE:
├─ Trades: 20
├─ Winners: 12 (60%)
├─ Losers: 8 (40%)
├─ Profit Factor: 1.85
├─ Weekly P&L: +$800 (8%)
└─ Sharpe Ratio: 1.2

METRICS vs TARGET:
├─ Win Rate: 60% ✅ (target: 50%)
├─ RR Ratio: 2.1 ✅ (target: 2.0)
├─ Max DD: -5% ✅ (target: < 20%)
├─ Consecutive Loss: 2 ✅ (target: < 5)
└─ Daily Avg: $114 ✅ (target: $50+)

ISSUES:
└─ None - week successful!

ACTION ITEMS:
├─ Continue current strategy
├─ Monitor market conditions
└─ Plan next week scaling
```

---

## 🎓 LEARNING PROGRESSION

### Week 1: Fundamentals
```
Day 1: Read TRADING_BOT_GUIDE.md overview
Day 2: Study 1 strategy from SPECIFIC_STRATEGIES.md
Day 3: Learn risk management principles
Day 4: Study technical analysis basics
Day 5: Understand backtesting concept
Day 6-7: Review & summarize
```

### Week 2-3: Strategy Development
```
Week 2:
├─ Pick 1 strategy
├─ Setup backtesting environment
├─ Collect historical data
└─ First backtest run

Week 3:
├─ Parameter optimization
├─ Out-of-sample testing
├─ Edge validation
└─ Decision: accept or reject
```

### Week 4+: Implementation
```
Week 4: Code implementation
Week 5-6: Paper trading (2 weeks minimum)
Week 7: Go live micro
Week 8+: Scaling based on results
```

---

## 🚨 EMERGENCY PROCEDURES

### If Account Down 5% Today
```
1. STOP TRADING immediately
2. Close any open positions (market order)
3. Review today's trades for mistakes
4. Check risk management violation
5. Wait for market close
6. Don't resume until next day
```

### If Losing 5 Consecutive Trades
```
1. PAUSE strategy
2. Check market conditions changed
3. Backtest in current market
4. Verify stops were hit properly
5. Don't trade until manual backtest shows edge
6. Resume carefully with micro sizing
```

### If Technical Error (Missed Trade/Duplicate)
```
1. Stop bot immediately
2. Close any erroneous positions
3. Don't resume until fixed & tested
4. Paper trade 5+ trades to verify fix
5. Run unit tests on code
6. Only resume after verification
```

### If Server Down
```
1. Access VPS immediately (SSH)
2. Check bot process status
3. Manually close open positions if needed
4. Restart monitoring
5. Review missed trades
6. Set manual alerts for critical levels
7. Fix issue before resuming
```

---

## 📈 SCALING DECISION MATRIX

| Condition | Action | Next Step |
|-----------|--------|-----------|
| Win% > 55%, PF > 2.0, DD < 10% | ✅ SCALE UP | Increase 50% position size |
| Win% 50-55%, PF 1.5-2.0, DD 10-15% | ✅ CONTINUE | Maintain current size 2-4 weeks |
| Win% 40-50%, PF 1.0-1.5, DD 15-20% | ⚠️ CAUTION | Don't scale, monitor closely |
| Win% < 40%, PF < 1.0, DD > 20% | ❌ PAUSE | Reduce size 50%, reanalyze |
| Technical errors | ❌ STOP | Fix immediately, paper test |
| Market regime changed | ⚠️ ADAPT | Test strategy in new regime |

---

## 💎 GOLDEN RULES (NEVER BREAK)

1. **ALWAYS use stop losses**
   - On every single trade
   - Set BEFORE entering
   - Use hard stops on exchange

2. **ALWAYS manage position size**
   - 2% risk per trade maximum
   - 5% account maximum per position
   - Reduce when losing

3. **ALWAYS follow your rules**
   - No manual overrides
   - No revenge trading
   - No "just one more trade"

4. **ALWAYS keep a journal**
   - Every trade recorded
   - Every lesson documented
   - Weekly review mandatory

5. **ALWAYS backup your data**
   - Daily automated backups
   - Test restoration monthly
   - Keep offsite copies

6. **ALWAYS have emergency procedures**
   - Kill switch ready
   - Backup connection plan
   - Manual override procedures

---

## 🎯 MONTHLY TARGETS

```
MONTH 1: Learning Phase
Target: Learn strategy inside out
Success: Understand all rules, can trade manually

MONTH 2: Development Phase
Target: Build bot, backtest, paper trade
Success: Results within 10% of backtest

MONTH 3: Micro Live Phase
Target: 1-2% risk sizing
Success: Profitable, no technical errors

MONTH 4+: Building Phase
Target: Scale gradually
Success: Sustainable profitability

Realistic Monthly ROI:
Month 1: -$500 (study/setup)
Month 2: $0 (development costs)
Month 3: +$150 (micro - learning)
Month 4: +$500 (small sizing)
Month 5+: +$1,000+ (building)
```

---

## ✅ FINAL VERIFICATION BEFORE GO-LIVE

- [ ] 200+ trades backtested ✓
- [ ] Walk-forward tested ✓
- [ ] Out-of-sample verified ✓
- [ ] Paper traded 4 weeks ✓
- [ ] Results within 10% of backtest ✓
- [ ] Code tested (unit + integration) ✓
- [ ] Infrastructure ready (VPS, monitoring, backups) ✓
- [ ] API keys secured (encrypted, IP whitelist) ✓
- [ ] Emergency procedures documented & tested ✓
- [ ] Risk management hardcoded ✓
- [ ] Trading journal prepared ✓
- [ ] Emotional readiness confirmed ✓
- [ ] Ready for losses without panic ✓
- [ ] First week plan: micro sizing only ✓
- [ ] 6-month runway capital available ✓

---

**Remember: The goal is consistency, not home runs. Slow money is the best money! 🚀**

