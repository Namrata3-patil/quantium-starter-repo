from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash application
app = Dash(__name__)

# 1. Load data
df = pd.read_csv("./formatted_output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 2. Define the layout with integrated CSS styling
app.layout = html.Div(
    style={
        'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif', 
        'backgroundColor': '#f8f9fa', 
        'padding': '40px 20px',
        'minHeight': '100vh'
    }, 
    children=[
        
        # Centered Container Card
        html.Div(
            style={
                'maxWidth': '1100px',
                'margin': '0 auto',
                'backgroundColor': '#ffffff',
                'padding': '30px',
                'borderRadius': '12px',
                'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.05)'
            },
            children=[
                
                # Header Section (id added for testing)
                html.H1(
                    id="app-header",
                    children="Soul Foods Sales Visualizer",
                    style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px', 'fontWeight': '600'}
                ),
                
                html.P(
                    children="Examine Pink Morsel sales trends across regions to understand the impact of the January 15, 2021 price increase.",
                    style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '16px', 'marginBottom': '35px'}
                ),
                
                # Interactivity Control Section (Radio Buttons)
                html.Div(
                    style={
                        'backgroundColor': '#f1f2f6',
                        'padding': '15px 25px',
                        'borderRadius': '8px',
                        'marginBottom': '30px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'gap': '15px'
                    },
                    children=[
                        html.Span(
                            "Filter by Region:", 
                            style={'fontWeight': 'bold', 'color': '#333', 'marginRight': '10px'}
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {'label': ' All', 'value': 'all'},
                                {'label': ' North', 'value': 'north'},
                                {'label': ' East', 'value': 'east'},
                                {'label': ' South', 'value': 'south'},
                                {'label': ' West', 'value': 'west'}
                            ],
                            value='all',  # Default selection
                            inline=True,
                            style={'display': 'flex', 'gap': '20px'},
                            inputStyle={'marginRight': '5px', 'cursor': 'pointer'},
                            labelStyle={'cursor': 'pointer', 'color': '#2c3e50', 'fontSize': '15px'}
                        )
                    ]
                ),
                
                # Graph Component Placeholder
                html.Div(
                    style={'borderRadius': '8px', 'overflow': 'hidden'},
                    children=[
                        dcc.Graph(id="sales-line-chart")
                    ]
                )
            ]
        )
    ]
)

# 3. Define the Dynamic Callback Function
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    # Filter the dataframe based on user input
    if selected_region == "all":
        filtered_df = df
        chart_title = "Pink Morsel Sales Performance — All Regions"
    else:
        filtered_df = df[df["region"].str.lower() == selected_region]
        chart_title = f"Pink Morsel Sales Performance — {selected_region.capitalize()} Region"
    
    # Generate the dynamic line chart
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=chart_title,
        labels={"date": "Date of Sale", "sales": "Total Sales ($)"},
        color_discrete_sequence=["#e74c3c"]  # Stylish red line
    )
    
    # Apply clean chart presentation styling
    fig.update_layout(
        title_x=0.5,
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        font=dict(family='"Segoe UI", sans-serif', size=13),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

# Run the server locally using the modern .run() syntax
if __name__ == "__main__":
    app.run(debug=True)