import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Create a Dash app
app = dash.Dash(__name__)

# Load a sample dataset
df = px.data.iris()     # Iris dataset

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Iris Data Visualization Dashboard"),

    html.Div("Choose X-axis"),
    dcc.Dropdown(
        id='x-axis',
        options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
        value='sepal_width'
    ),

    html.Div("Choose Y-axis"),
    dcc.Dropdown(
        id='y-axis',
        options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
        value='sepal_length'
    ),

    dcc.Graph(id='scatter-plot'),

    html.Div("Select a Species:"),
    dcc.Checklist(
        id='species-selector',
        options=[{'label': species, 'value': species} for species in df['species'].unique()],
        value=df['species'].unique(),
        inline=True
    ),

    dcc.Graph(id='box-plot')
])

# Callback to update scatter plot based on user selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis', 'value'), Input('y-axis', 'value'), Input('species-selector', 'value')]
)
def update_scatter_plot(x_axis, y_axis, selected_species):
    filtered_df = df[df['species'].isin(selected_species)]
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color='species', title=f"Scatter Plot: {x_axis} vs {y_axis}")
    return fig


# Callback to update box plot based on selected species
@app.callback(
    Output('box-plot', 'figure'),
    [Input('species-selector', 'value')]
)
def update_box_plot(selected_species):
    filtered_df = df[df['species'].isin(selected_species)]
    fig = px.box(filtered_df, x='species', y='sepal_width', title='Box Plot of Sepal Width by Species')
    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
