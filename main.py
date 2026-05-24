import yfinance as yf
import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import warnings

# Suppress annoying pandas warnings
warnings.filterwarnings('ignore')

def get_stock_data(ticker_symbol, period="1mo"):
    """Fetch historical stock price data."""
    print(f"Fetching {period} of stock data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    # Ensure timezone-naive for merging later
    hist.index = hist.index.tz_localize(None)
    return hist

def get_financial_news(ticker_symbol):
    """Fetch recent news articles for the stock and run sentiment analysis."""
    print(f"Fetching recent news for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news
    
    news_data = []
    
    for article in news:
        # Sometimes yfinance news items don't have a publisher or title
        title = article.get('title', '')
        publisher = article.get('publisher', 'Unknown')
        link = article.get('link', '')
        
        # yfinance news timestamps are standard unix epoch
        timestamp = article.get('providerPublishTime')
        if not timestamp:
            continue
            
        date = datetime.datetime.fromtimestamp(timestamp)
        
        # Run AI Sentiment Analysis on the Headline
        analysis = TextBlob(title)
        sentiment_score = analysis.sentiment.polarity
        
        if sentiment_score > 0.05:
            sentiment_label = 'Bullish'
            marker_color = 'green'
        elif sentiment_score < -0.05:
            sentiment_label = 'Bearish'
            marker_color = 'red'
        else:
            sentiment_label = 'Neutral'
            marker_color = 'gray'
            
        news_data.append({
            'Date': pd.to_datetime(date.date()), # Group by day for the chart
            'Title': title,
            'Publisher': publisher,
            'Sentiment_Score': sentiment_score,
            'Sentiment': sentiment_label,
            'Color': marker_color,
            'Link': link
        })
        
    df = pd.DataFrame(news_data)
    print(f"Analyzed {len(df)} news articles.")
    return df

def generate_financial_dashboard(stock_df, news_df, ticker_symbol):
    """Generate an interactive chart overlaying stock price with news sentiment."""
    print("Generating interactive dashboard...")
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Plot the Stock Price (Candlestick or Line)
    fig.add_trace(
        go.Scatter(
            x=stock_df.index, 
            y=stock_df['Close'], 
            name="Closing Price",
            line=dict(color='#1f77b4', width=2)
        ),
        secondary_y=False,
    )

    # 2. Overlay the News Sentiment as Markers
    if not news_df.empty:
        # Merge news dates with stock prices to plot markers at the right height
        # We find the closing price on the day the news was published
        merged = pd.merge(news_df, stock_df['Close'].reset_index(), left_on='Date', right_on='Date', how='inner')
        
        # Add hover text with the actual news headline
        hover_text = merged['Publisher'] + ":<br><i>" + merged['Title'] + "</i><br>Sentiment: " + merged['Sentiment']

        fig.add_trace(
            go.Scatter(
                x=merged['Date'],
                y=merged['Close'],
                mode='markers',
                name='News Events',
                marker=dict(
                    color=merged['Color'],
                    size=12,
                    line=dict(width=2, color='white'),
                    symbol='star'
                ),
                text=hover_text,
                hoverinfo='text'
            ),
            secondary_y=False,
        )

    # Clean up the layout to look like a Bloomberg Terminal
    fig.update_layout(
        title_text=f"<b>{ticker_symbol}</b>: Price Action vs. AI News Sentiment",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=False)

    # Save to HTML file
    output_file = f'{ticker_symbol}_sentiment_dashboard.html'
    fig.write_html(output_file)
    print(f"\n✅ SUCCESS! Dashboard generated: {output_file}")
    print("You can open this file in any web browser to see the interactive chart.")

if __name__ == "__main__":
    # Choose a volatile stock (like NVDA, TSLA, or AAPL)
    TICKER = "NVDA"
    
    try:
        # 1. Get 1 month of stock price data
        stock_df = get_stock_data(TICKER, period="1mo")
        
        # 2. Get recent news and run NLP sentiment analysis
        news_df = get_financial_news(TICKER)
        
        # 3. Build the dashboard
        generate_financial_dashboard(stock_df, news_df, TICKER)
        
    except Exception as e:
        print(f"An error occurred: {e}")