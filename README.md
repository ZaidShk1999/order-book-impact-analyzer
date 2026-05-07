

# L2 Execution Engine & Liquidity Monitor ⚡

A high-performance, real-time Python engine designed to "walk" the Binance L2 Order Book. This tool simulates institutional-scale execution by calculating the true market impact and implementation shortfall of large block trades (e.g., 20 BTC) in real-time.

## 🚀 The Core Problem
In high-frequency trading, the "Mid-Price" is a vanity metric. If you need to execute a **$1.8M (20 BTC) order**, the top-of-book liquidity is insufficient. This engine bridges the gap between raw exchange data and actionable execution logic by calculating the **Volume Weighted Average Price (VWAP)** across multiple depth levels.

## 🛠️ Technical Architecture
* **Asynchronous Data Pipeline:** Built with `asyncio` and `WebSockets` to consume and process 100ms L2 depth updates from Binance without blocking the UI thread.
* **Liquidity Pathfinding:** Implements a "Book Walking" algorithm that traverses the bid/ask stacks to determine exactly where a specified volume would clear.
* **Real-time Analytics:** Calculates **Slippage** and **Market Impact %** dynamically as the order book fluctuates.
* **High-Density CLI:** Utilizes the `Rich` library for a low-overhead, high-throughput terminal dashboard, prioritizing data density over GUI latency.

## 📊 Key Metrics Tracked
* **VWAP (Buy/Sell):** The actual price you would pay/receive for the total volume.
* **Implementation Shortfall:** The delta between the theoretical Mid-Price and the actual execution price.
* **L2 Depth Map:** Visual representation of volume distribution across the top 20 levels of the book.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Concurrency:** AsyncIO
* **Data Handling:** Pandas / NumPy
* **Interface:** Rich (Terminal UI)
* **Source:** Binance Spot WebSockets

## 🛤️ Roadmap: Phase 2 (In Development)
* **Order Book Imbalance (OBI):** Integrating a predictive signal based on the volume ratio between Bids and Asks.
* **Micro-Price Calculation:** Implementing a weighted mid-price to predict short-term price movements.
* **Market Making Module:** A simulated automated strategy to manage bid/ask spreads based on real-time volatility.

---

### **Quick Setup**
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/l2-execution-engine`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the engine: `python main.py`
