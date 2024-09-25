import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

spacex_df = pd.read_csv(r'./spacex.csv')

app = dash.Dash(__name__)

options = [{'label':x, 'value':x} for x in spacex_df['Launch Site'].unique().tolist()]
options.insert(0,{'label':'All Sites','value':'ALL'})
app.layout = html.Div(children=[
        html.H1("SpaceX Launch Records Dashboard",
                style={'textAlign':'center','color':'#503D36','font-size':26}),
        html.Div([
            dcc.Dropdown(id='site-dropdown',
                        options=options,
                        value='ALL',
                        placeholder='Select a Launch Site here',
                        searchable=True
                        ),
        ]),
        html.Div([
            html.Div(dcc.Graph(id='success-pie-chart'))
        ]),

        html.Div([
            dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()])
        ]),

        html.Div([
            html.Div(dcc.Graph(id='success-payload-scatter-chart'))
        ])
])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']
        fig = px.pie(class_counts, values='count',
        names='class',
        title=f'Total Success Launches for Site {entered_site}')
        return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")
              ])

def get_scatter_plot(entered_site,payload_range):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version',
        title='Payload Success Rate for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        new_df = filtered_df[filtered_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
        fig = px.scatter(new_df, x='Payload Mass (kg)', y='class',
        color='Booster Version',
        title=f'Payload Success Rate for Site {entered_site}')
        return fig

if __name__ == '__main__':
    app.run_server(debug=True,port='8090')
        
        
