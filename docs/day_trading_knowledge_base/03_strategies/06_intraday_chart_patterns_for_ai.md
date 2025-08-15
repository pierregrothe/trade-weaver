# [CONCEPT: Chart_Patterns] Algorithmic Guide to Intraday Chart Patterns

This document translates classic visual chart patterns into quantifiable characteristics and pseudocode that an AI agent can use for detection. These patterns represent periods of consolidation that often precede a significant price move.

### [PATTERN: Bull_Flag] Bull Flag / Bear Flag

- **[WHAT]** A powerful **continuation pattern**. A "flagpole" is a strong, high-volume directional move. The "flag" is a subsequent period of brief, low-volume consolidation with a slight counter-trend drift.
- **[WHY]** It represents a brief pause where the market digests the initial, impulsive move. The low volume in the flag confirms that there is little conviction in the counter-trend drift, suggesting the original trend is likely to resume.
- **[HOW] AI Detection Logic (Bull Flag):**
    1. **Detect Flagpole:** `price_change_percent > (3 * ATR_percent)` over the last `N` bars (e.g., N=5 to 10) AND `average_volume` during this move is `> 1.5 * moving_average_volume(50)`.
    2. **Detect Flag:** The subsequent `M` bars (e.g., M=5 to 15) form a downward sloping channel (a series of lower highs and lower lows) with low volume (`< 0.8 * moving_average_volume(50)`).
- **[TRADE_EXECUTION]**
  - **Entry:** Buy on a high-volume (`> 2.0 * moving_average_volume`) breakout and close above the flag's upper trendline.
  - **Stop-Loss:** Place the stop-loss just below the low of the flag pattern.
  - **Profit Target:** The "measured move" is the height of the flagpole (in dollars) added to the breakout price.

### [PATTERN: Triangle] Triangles (Symmetrical, Ascending, Descending)

- **[WHAT]** A pattern showing a tightening of the price range and contracting volatility as buyers and sellers reach an equilibrium.
  - **Ascending:** A flat upper trendline (resistance) and a rising lower trendline (support). A bullish pattern.
  - **Descending:** A flat lower trendline (support) and a falling upper trendline (resistance). A bearish pattern.
- **[WHY]** Represents a "coiling spring" of energy. The decreasing volatility often precedes a significant volatility expansion (the breakout). The pattern of highs and lows reveals which side is more aggressive (e.g., in an ascending triangle, buyers are making higher lows, showing increasing aggression).
- **[HOW] AI Detection Logic (Ascending Triangle):**
    1. Identify a series of at least two swing highs at a near-identical price level (`resistance_level`), allowing for minor deviation.
    2. Identify a series of at least two consecutive higher swing lows, forming a rising `support_trendline`.
    3. Confirm that volume tends to diminish as the pattern progresses towards its apex.
- **[TRADE_EXECUTION]**
  - **Entry:** Buy on a high-volume breakout and close above the flat `resistance_level`.
  - **Stop-Loss:** Place the stop-loss just below the rising `support_trendline`.
  - **Profit Target:** The height of the triangle at its widest point (the "base"), added to the breakout price.

### [PATTERN: Head_and_Shoulders] Head and Shoulders / Inverse Head and Shoulders

- **[WHAT]** A major **reversal pattern**. A standard Head and Shoulders (H&S) signals a potential top and a shift from a bullish to a bearish trend. It consists of a `Left Shoulder`, a higher `Head`, and a lower `Right Shoulder`. The `Neckline` connects the lows between the peaks. An Inverse H&S is the bullish equivalent at a market bottom.
- **[WHY]** Represents a waning of buying pressure in an uptrend. The failure to make a new high after the "Head" and the subsequent lower high of the "Right Shoulder" signals that buyers are exhausted and sellers are beginning to take control. The break of the Neckline is the confirmation of this power shift.
- **[HOW] AI Detection Logic (Standard H&S):**
    1. Identify three consecutive peaks in an established uptrend: `peak_2 (Head) > peak_1 (Left Shoulder)` AND `peak_2 > peak_3 (Right Shoulder)`.
    2. Identify the two troughs between these peaks and algorithmically fit the `neckline` connecting them.
    3. Confirm that volume is generally highest on the Left Shoulder and diminishes on the Head and Right Shoulder, indicating fading buying conviction. The breakout below the neckline should ideally occur on expanding volume.
- **[TRADE_EXECUTION]**
  - **Entry:** Sell short on a high-volume breakdown and close below the `neckline`.
  - **Stop-Loss:** Place the stop-loss just above the high of the Right Shoulder.
  - **Profit Target:** The distance from the top of the Head to the Neckline, subtracted from the breakdown price.

[SOURCE_ID: Day Trading AI Agent Build, Section 3.2]