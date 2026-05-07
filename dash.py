import asyncio, json, websockets, pandas as pd
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console

console = Console()
history = []

def get_layout(m):
    layout = Layout()
    layout.split_column(
        Layout(name="head", size=3),
        Layout(name="body", ratio=1),
        Layout(name="foot", size=3)
    )
    layout["body"].split_row(
        Layout(name="stats", ratio=1),
        Layout(name="depth", ratio=1)
    )

    # 1. Header
    layout["head"].update(Panel(f"● [bold green]LIVE[/] | [bold white]BTC-USDT EXECUTION ENGINE[/] | [cyan]TARGET: {m['size']} BTC[/]", border_style="bright_blue"))

    # 2. Execution Stats
    stats = Table(show_header=False, expand=True, box=None)
    stats.add_row("CURRENT MID", f"[bold white]${m['price']:,.2f}[/]")
    stats.add_row("EST. FILL (VWAP)", f"[yellow]${m['fill']:,.2f}[/]")
    stats.add_row("TOTAL SLIPPAGE", f"[bold red]${m['slip']:,.2f}[/]")
    stats.add_row("MARKET IMPACT", f"[bold magenta]{m['impact']:.4f}%[/]")
    layout["stats"].update(Panel(stats, title="[bold]Trade Analytics[/]", border_style="cyan"))

    # 3. L2 Depth Map
    book = Table(show_header=True, header_style="bold magenta", expand=True, box=None)
    book.add_column("Type", width=8)
    book.add_column("Price", justify="right")
    book.add_column("Liquidity Depth", justify="left")

    for p, q in m['asks']:
        book.add_row("ASK", f"${p:,.1f}", "█" * int(min(q*5, 20)), style="red")
    book.add_row("---", "---", "---")
    for p, q in m['bids']:
        book.add_row("BID", f"${p:,.1f}", "█" * int(min(q*5, 20)), style="green")
    
    layout["depth"].update(Panel(book, title="[bold]L2 Order Book[/]", border_style="magenta"))

    # 4. Ticker Tape
    tape = "  |  ".join([f"${p:,.1f}" for p in history[-8:]])
    layout["foot"].update(Panel(f"[dim]{tape}[/]", title="[bold]Recent Ticks[/]", border_style="white"))
    
    return layout

async def run():
    # SET TO 20.0 TO ENSURE VISIBLE SLIPPAGE
    size = 20.0 
    
    uri = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"
    async with websockets.connect(uri) as ws:
        with Live(refresh_per_second=10, screen=True) as live:
            while True:
                data = json.loads(await ws.recv())
                asks = pd.DataFrame(data['asks'], columns=['Price', 'Quantity']).astype(float)
                bids = pd.DataFrame(data['bids'], columns=['Price', 'Quantity']).astype(float)
                
                p = asks['Price'].iloc[0]
                history.append(p)
                if len(history) > 20: history.pop(0)

                # Slippage Logic: Walking the Book
                acc_q, cost = 0, 0
                for ap, aq in zip(asks['Price'], asks['Quantity']):
                    take = min(aq, size - acc_q)
                    cost += take * ap
                    acc_q += take
                    if acc_q >= size: break
                fill = cost / size

                metrics = {
                    "size": size, "price": p, "fill": fill,
                    "slip": fill - p, "impact": ((fill - p)/p)*100,
                    "asks": list(zip(asks['Price'][:3], asks['Quantity'][:3]))[::-1],
                    "bids": list(zip(bids['Price'][:3], bids['Quantity'][:3]))
                }
                live.update(get_layout(metrics))

if __name__ == "__main__":
    asyncio.run(run())
