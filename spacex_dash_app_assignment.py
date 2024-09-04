# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
launch_sites = spacex_df['Launch Site'].unique()
launch_sites = np.concatenate((['ALL Sites'],launch_sites))
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': i, 'value': i} for i in launch_sites
                                                ],
                                                value='ALL Sites',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    data_all = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    if entered_site == 'ALL Sites':
        fig = px.pie(data_all, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == entered_site,'class']
        # return the outcomes piechart for a selected site
        fig = px.pie(data, values=data.value_counts().values, 
        names=data.value_counts().index, 
        title='Total Success Launches for site {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload):
    if entered_site == 'ALL Sites':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',
        title='Correlation for Payload and Success for all Sites')
        fig.update_xaxes(range=payload)
        fig.update_yaxes(title='class: 0 failure, 1 success')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        # return the outcomes piechart for a selected site
        fig = px.scatter(data, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',  
        title='Correlation for Payload and Success for Site {}'.format(entered_site))
        fig.update_xaxes(range=payload)
        fig.update_yaxes(title='class: 0 failure, 1 success')        
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
