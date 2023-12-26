import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import us

def convert_state_name_to_abbreviation(state_name):
    state = us.states.lookup(state_name).abbr
    return state

app = dash.Dash(__name__)
app.title = 'Vehicle Registrations in the US'

df = pd.read_excel('data.xlsx')
app.layout = html.Div([

    dcc.Markdown(''' ### Vehicle Registrations in the US '''),

    dcc.Dropdown(id="slct_year",
                        options=[
                        {"label": "2016", "value": 2016},
                        {"label": "2017", "value": 2017},
                        {"label": "2018", "value": 2018},
                        {"label": "2019", "value": 2019},
                        {"label": "2020", "value": 2020},
                        {"label": "2021", "value": 2021},
                        {"label": "2022", "value": 2022}],
                        multi=True,
                        value=[2016],
                        style={'width': "35%"}
                    ),
                    
    dcc.Checklist(id = "slct_mode", 
                   options=[
                        {"label":"Electric", "value": "Electric"}, 
                        {"label":"Alternative", "value": "Alternative"}, 
                        {"label":"Conventional", "value": "Conventional"}], 
                        value = ['Electric'],
                        inline = True
                    ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_auto_map1', figure={}),
    dcc.Graph(id='my_auto_map2', figure={}),
    dcc.Graph(id='my_auto_map3', figure={}),
    dcc.Graph(id='my_auto_map4', figure={})

])

@app.callback(
    [Output(component_id='my_auto_map1', component_property='figure'),
     Output(component_id='my_auto_map2', component_property='figure'),
     Output(component_id='my_auto_map3', component_property='figure'),
     Output(component_id='my_auto_map4', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
    Input(component_id='slct_mode', component_property='value')]
)

def update_graph(option_slctd_year, option_slctd_mode):
    figs = []

    if not isinstance(option_slctd_year, list):
        option_slctd_year = [option_slctd_year]
    if not isinstance(option_slctd_mode, list):
        option_slctd_mode = [option_slctd_mode]

    for year in option_slctd_year:
        for mode in option_slctd_mode:
            df = pd.read_excel('data.xlsx', sheet_name=str(year))
            df['State'] = df['State'].apply(convert_state_name_to_abbreviation)
            mode_column = "Electric" if mode == 'Electric' else 'Alternative' if mode == 'Alternative' else 'Conventional'
    
            min_value = df[mode_column].min()
            mean_value = df[mode_column].mean()
            max_value = df[mode_column].max()


            fig = px.choropleth(
                data_frame = df,
                locationmode ='USA-states',
                locations ='State',
                scope = "usa",
                color = mode_column,
                hover_data = ['State', mode_column],
                color_continuous_scale=px.colors.sequential.YlOrRd,
                labels = {'State', 'Vehicles'},
                template= 'plotly_dark',
                range_color=[min_value, mean_value],
                title='Year:{}, Mode:{}'.format(year, mode)
            )
            figs.append(fig)

    if len(figs) == 1:
        return figs[0], go.Figure(), go.Figure(), go.Figure()
    elif len(figs) == 2:
        return figs[0], figs[1], go.Figure(), go.Figure()
    elif len(figs) == 3:
        return figs[0], figs[1], figs[2], go.Figure()
    elif len(figs) == 4:
        return figs[0], figs[1], figs[2], figs[3]
    else:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure()
    
if __name__ == '__main__':
    app.run_server()

