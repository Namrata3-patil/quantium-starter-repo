from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash application
app = Dash(__name__)

# 1. Load and clean the data generated in Task 2
df = pd.read_csv("./formatted_output.csv")

# Ensure the date column is in datetime format and sort chronologically
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 2. Create the line chart visualization using Plotly Express
fig = px.line(
    df, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales Performance (Over Time)",
    labels={"date": "Date of Sale", "sales": "Total Sales ($)"}
)

# Customize the chart layout for better presentation
fig.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Date",
    yaxis_title="Total Sales ($)"
)

# 3. Define the layout of the Dash application
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    
    # Header element
    html.H1(
        children="Soul Foods Sales Visualizer",
        style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}
    ),
    
    # Subheading giving context to the business question
    html.P(
        children="Analyzing Pink Morsel sales data before and after the January 15, 2021 price increase.",
        style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '16px'}
    ),
    
    # Graph component rendering our line chart
    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# Run the server locally
if __name__ == "__main__":
    app.run(debug=True)