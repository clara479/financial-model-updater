import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Financial Model Updater – Analyst Copilot™", layout="wide")

st.title("📊 Financial Model Updater – Analyst Copilot™")
st.markdown("Automate your comparable company and financial model updates using live data from Yahoo Finance.")

tickers_input = st.text_input("Enter stock tickers (separated by commas):", "AAPL, MSFT, TSLA")

if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
    results = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            data = {
                "Ticker": ticker,
                "Company Name": info.get("shortName", "N/A"),
                "Revenue (TTM)": info.get("totalRevenue", "N/A"),
                "Net Income (TTM)": info.get("netIncomeToCommon", "N/A"),
                "EPS (Trailing)": info.get("trailingEps", "N/A"),
                "P/E Ratio": info.get("trailingPE", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A")
            }
            results.append(data)
        except Exception as e:
            st.warning(f"⚠️ Error fetching data for {ticker}: {e}")

    if results:
        df = pd.DataFrame(results)

        # Format large numbers for readability
        df["Revenue (TTM)"] = pd.to_numeric(df["Revenue (TTM)"], errors='coerce') / 1e9
        df["Net Income (TTM)"] = pd.to_numeric(df["Net Income (TTM)"], errors='coerce') / 1e9
        df.rename(columns={
            "Revenue (TTM)": "Revenue (B USD)",
            "Net Income (TTM)": "Net Income (B USD)"
        }, inplace=True)

        st.subheader("📈 Financial Summary")
        st.dataframe(df.style.format({
            "Revenue (B USD)": "{:.2f}",
            "Net Income (B USD)": "{:.2f}",
            "EPS (Trailing)": "{:.2f}",
            "P/E Ratio": "{:.2f}"
        }))

        # Download button
        from io import BytesIO

# Convert dataframe to Excel in memory
buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
buffer.seek(0)

# Show download button
st.download_button(
    label="⬇ Download as Excel",
    data=buffer,
    file_name="financial_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

