# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                {'label': 'All Sites','value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                ],
                                                value='ALL',
                                                placeholder="All launchsites",
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
                                                min=0,max=10000,step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value'))

def get_scatter_plot(entered_site,entered_payload):
    min_payload,max_payload = entered_payload

    if entered_site == 'ALL':
        payload_df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_payload,max_payload)]
        fig = px.scatter(payload_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation payload and success')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_payload_df = filtered_df[filtered_df['Payload Mass (kg)'].between(min_payload,max_payload)]
        fig = px.scatter(filtered_payload_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation payload and success')
        return fig
                               
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        successdf = spacex_df[spacex_df['class']==1].groupby('Launch Site').size().reset_index(name='count')
        fig = px.pie(successdf, values='count', 
        names='Launch Site', 
        title='Succesful launches by site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        successfiltered = filtered_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(successfiltered, values='count',
        names='class', 
        title= entered_site)
        return fig
        # return the outcomes piechart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()

