import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# 1. Load the processed data
# Ensure you run data_processor.py first to generate this file
df = pd.read_csv('formatted_data.csv')
df = df.sort_values(by="date")

# 2. Initialize the Dash app
app = Dash(__name__)

# 3. Define the Layout
app.layout = html.Div(style={'fontFamily': 'sans-serif', 'padding': '40px'}, children=[
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Region Picker
    html.Div([
        html.Label("Filter by Region: ", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True
        )
    ], style={'textAlign': 'center', 'margin': '20px', 'padding': '15px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),

    # The Graph
    dcc.Graph(id='sales-graph')
])

# 4. Callback to update graph based on region selection
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Data: {selected_region.capitalize()} Region"
    )
    
    # Add vertical line for price increase on Jan 15, 2021
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="red", 
        annotation_text="Price Increase")
    
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run(debug=True)