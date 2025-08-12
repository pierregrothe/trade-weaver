# [CONCEPT: Order_Flow] Order Flow Analysis and Data Feeds

Order flow analysis provides a real-time, forward-looking view of the raw supply and demand dynamics in the market. Processing this high-frequency data is a significant potential edge for an AI agent.

### [CONCEPT: Data_Hierarchy] Data Hierarchy and AI Implementation

There is a clear hierarchy of data latency and predictive power. A sophisticated AI should fuse these data types, using lagging data for context and real-time data for execution timing.

1. **[DATA: Level_1] (Lagging):** Best Bid/Ask, Last Price. Used for calculating standard technical indicators. Provides **context**.
2. **[DATA: Level_2] (Real-Time Intent):** The full order book. Shows the *intent* to trade. Provides **short-term prediction**.
3. **[DATA: Time_and_Sales] (Real-Time Execution):** The log of executed trades. Shows *actual* transactions as they happen. Provides **immediate confirmation**.

### [DATA: Level_2] Level 2 Data (Market-by-Price, MBP)

- **[DEFINITION:]** The "order book"—a ranked list of all open limit buy and sell orders at various price levels, aggregated by price.
- **[AI_USE_CASE: Liquidity_Analysis]** An AI must parse Level 2 data to gauge market depth and identify large orders ("bid/ask walls") that can act as temporary support or resistance.
- **[LIMITATION:]** Standard Level 2 data is **aggregated**. It shows the total volume at a price level but does not reveal the number or size of individual orders, which is a critical limitation for advanced analysis.

### [DATA: Level_3] Level 3 Data (Market-by-Order, MBO)

- **[DEFINITION:]** The highest possible granularity. It is the raw, un-aggregated feed of every single order and its full lifecycle (add, modify, cancel, execute). Exchange-native feeds like NASDAQ's TotalView-ITCH provide this level of detail.
- **[AI_USE_CASE: Predictive Modeling]** Level 3 data is a **non-negotiable prerequisite** for building a predictive `Order_Imbalance_Score`. It allows the agent to differentiate between institutional and retail order flow, detect spoofing, and analyze the replenishment of iceberg orders.

### [DATA: Time_and_Sales] Time & Sales (The "Tape")

- **[DEFINITION:]** The real-time log of every executed trade, including its price, volume, and time.
- **[AI_USE_CASE: Order_Flow_Analysis]** The AI agent's Order Flow Analysis module must process this stream to identify micro-events that are invisible on a standard price chart.

#### [CONCEPT: Programmable_Tape_Patterns] Programmable Tape Reading Patterns

- **[PATTERN: Absorption]**
  - **[SIGNATURE:]** A large number of aggressive orders are filled at a specific price level, yet the price fails to move. This indicates a large passive participant is absorbing the pressure.
  - **[PROGRAMMABLE_RULE:]**
        `FUNCTION detect_absorption(price_level, time_window):`
        `trades = get_tape(price_level, time_window)`
        `volume_at_ask = sum(trade.volume for trade in trades if trade.price == ask)`
        `price_change = get_price_change(time_window)`
        `IF volume_at_ask > threshold AND price_change < epsilon THEN`
        `RETURN signal(type='SELL_ABSORPTION', price=price_level)`

- **[PATTERN: Iceberg_Orders]**
  - **[SIGNATURE:]** A large institutional order hidden as smaller, visible "child" orders. On Level 2, a small order keeps "refreshing" after being filled. On the Tape, a much larger cumulative volume is seen trading at that exact price.
  - **[PROGRAMMABLE_RULE:]**
        `FUNCTION detect_iceberg(price_level):`
        `level2_size = get_level2_size(price_level)`
        `tape_volume = get_cumulative_tape_volume(price_level, time_window)`
        `IF level2_size > 0 AND tape_volume > (level2_size * 10) THEN`
        `RETURN signal(type='ICEBERG_DETECTED', price=price_level)`

[SOURCE_ID: Day Trading AI Agent Research, Part II, Section 2.1]
