import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
#from scipy import integrate
import numpy as np
import datetime as dt
import collections
import csv

with open('acc_predict_dict.csv', mode='rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader)[2:]
    dict1 = collections.defaultdict(dict)
    for row in reader:
        dict1[row[0]][row[1]] = {key: float(value) for key, value in zip(headers, row[2:])}

df = pd.read_csv('male_change_final.csv')


# def func(row, slope, y_int, lb, ub):
#     return integrate.quad(lambda x: (dict1[row['event']][row['Year']][slope]*x+dict1[row['event']][row['Year']][y_int])*
#     (np.exp(-0.5*((x-row['predict_mean'])/row['predict_std'])**2)/(row['predict_std']*(2*np.pi)**(0.5))),
#     dict1[row['event']][row['Year']][lb], dict1[row['event']][row['Year']][ub])[0]

# def func2(row, ub):
#     return integrate.quad(lambda x: 32*(np.exp(-0.5*((x-row['predict_mean'])/row['predict_std'])**2)/(row['predict_std']*(2*np.pi)**(0.5))), -np.inf, dict1[row['event']][row['Year']][ub])[0]

def score_lookup(c):
  if c['predict_mean'] <= dict1[c['event']][c['Year']]['top_1']:
    return 32
  elif c['predict_mean'] <= dict1[c['event']][c['Year']]['top_8']:
    return int(round(dict1[c['event']][c['Year']]['a_slope']*c['predict_mean']+dict1[c['event']][c['Year']]['a_int']))
  elif c['predict_mean'] <= dict1[c['event']][c['Year']]['top_16']:
    return int(round(dict1[c['event']][c['Year']]['b_slope']*c['predict_mean']+dict1[c['event']][c['Year']]['b_int']))
  elif c['predict_mean'] <= dict1[c['event']][c['Year']]['top_24']:
    return int(round(dict1[c['event']][c['Year']]['c_slope']*c['predict_mean']+dict1[c['event']][c['Year']]['c_int']))
  else:
    return 0
    
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children="GTSD Men's Swimming Time Predictions"),

    html.Div(
        [html.Label('Name'),
        dcc.Input(id='name', type='text'
        )],

        style={'width': '200px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Current Age'),
        dcc.Dropdown(id='age',
            options=[
                {'label': '15', 'value': 15},
                {'label': '16', 'value': 16},
                {'label': '17', 'value': 17},
                {'label': '18', 'value': 18},
                {'label': '19', 'value': 19},
                {'label': '20', 'value': 20},
                {'label': '21', 'value': 21}
            ],
            value=16
        )],

        style={'width': '100px', 'display': 'inline-block'}),

    html.Div(
        [html.Label('Start Year'),
        dcc.Input(id='year', value=2021, type='number', min=2020, max=2023, step=1
        )],

        style={'width': '5px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Delayed enrollment'),
        dcc.Dropdown(id='start',
            options=[
                {'label': 'No', 'value': 0},
                {'label': '1 year', 'value': 1},
                {'label': '2 years', 'value': 2},
                {'label': '3 years', 'value': 3},
            ],
            value=0
        )],

        style={'width': '100px', 'display': 'inline-block'}),

    html.Div(style={'height': '40px', 'display': 'block'}),

    html.Div(
        [html.Label('ACC Team Goal'),
        dcc.Dropdown(id='team_place',
            options=[
                {'label': '1st Place', 'value': 1},
                {'label': '2nd Place', 'value': 2},
                {'label': '3rd Place', 'value': 3},
                {'label': '4th Place', 'value': 4},
                {'label': '5th Place', 'value': 5},

            ],
            value=1)], style={'width': '130px', 'display': 'inline-table'}),

    html.Div(
        [
            html.Label('Event 1 Points/Year'),
            html.Div(id='event1-points-year')
        ], 
        style={'width': '100px', 'display': 'inline-table', 'text-align': 'center'}),
        
    html.Div(
        [
            html.Label('Event 2 Points/Year'),
            html.Div(id='event2-points-year')
        ], 
        style={'width': '100px', 'display': 'inline-table', 'text-align': 'center'}),

    html.Div(
        [
            html.Label('Event 3 Points/Year'),
            html.Div(id='event3-points-year')
        ], 
        style={'width': '100px', 'display': 'inline-table', 'text-align': 'center'}),

    html.Div(
        [
            html.Label('Total Points/Year'),
            html.Div(id='all-event-points-year')
        ], 
        style={'width': '100px', 'display': 'inline-table', 'text-align': 'center'}),

    html.Div(
        [
            html.Label('Scholarship'),
            html.Div(id='schol')
        ], 
        style={'width': '100px', 'display': 'inline-table', 'text-align': 'center', 'font-weight': 'bolder', 'font-size': 'x-large', 'border': '5px solid blue'}),


    html.Div(style={'height': '40px', 'display': 'block'}),

    html.Div(
        [html.Label('Event 1'),
        dcc.Dropdown(id='event1',
            options=[
                {'label': '50 Free', 'value': '50 FR'},
                {'label': '100 Free', 'value': '100 FR'},
                {'label': '200 Free', 'value': '200 FR'},
                {'label': '400/500 Free', 'value': '500 FR'},
                {'label': '800/1000 Free', 'value': '1000 FR'},
                {'label': '1500/1650 Free', 'value': '1650 FR'},
                {'label': '100 Back', 'value': '100 BK'},
                {'label': '200 Back', 'value': '200 BK'},
                {'label': '100 Breast', 'value': '100 BR'},
                {'label': '200 Breast', 'value': '200 BR'},
                {'label': '100 Fly', 'value': '100 FL'},
                {'label': '200 Fly', 'value': '200 FL'},
                {'label': '200 IM', 'value': '200 IM'},
                {'label': '400 IM', 'value': '400 IM'},

            ],
            value='50 FR'
        )],

        style={'width': '165px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Course'),
        dcc.Dropdown(id='course1',
            options=[
                {'label': 'SCY', 'value': 'SCY'},
                {'label': 'SCM', 'value': 'SCM'},
                {'label': 'LCM', 'value': 'LCM'}
            ],
            value='SCY'
        )],

        style={'width': '90px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Min'),
        dcc.Input(id='min1', value=0, type='number', min=0, max=20, step=1
        )],

        style={'width': '5px', 'display': 'inline-table'}),
    
    html.Div(
        [html.Label('Sec'),
        dcc.Input(id='sec1', value=21.05, type='number', min=0.00, max=59.99, step=0.01
        )],

        style={'width': '7px', 'display': 'inline-table'}),

    html.Div(id='datatable-event1-container'),

    html.Br(),

    html.Div(
        [html.Label('Event 2'),
        dcc.Dropdown(id='event2',
            options=[
                {'label': '50 Free', 'value': '50 FR'},
                {'label': '100 Free', 'value': '100 FR'},
                {'label': '200 Free', 'value': '200 FR'},
                {'label': '400/500 Free', 'value': '500 FR'},
                {'label': '800/1000 Free', 'value': '1000 FR'},
                {'label': '1500/1650 Free', 'value': '1650 FR'},
                {'label': '100 Back', 'value': '100 BK'},
                {'label': '200 Back', 'value': '200 BK'},
                {'label': '100 Breast', 'value': '100 BR'},
                {'label': '200 Breast', 'value': '200 BR'},
                {'label': '100 Fly', 'value': '100 FL'},
                {'label': '200 Fly', 'value': '200 FL'},
                {'label': '200 IM', 'value': '200 IM'},
                {'label': '400 IM', 'value': '400 IM'},

            ],
            value='100 FR'
        )],

        style={'width': '165px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Course'),
        dcc.Dropdown(id='course2',
            options=[
                {'label': 'SCY', 'value': 'SCY'},
                {'label': 'SCM', 'value': 'SCM'},
                {'label': 'LCM', 'value': 'LCM'}
            ],
            value='SCY'
        )],

        style={'width': '90px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Min'),
        dcc.Input(id='min2', value=0, type='number', min=0, max=20, step=1
        )],

        style={'width': '5px', 'display': 'inline-table'}),
    
    html.Div(
        [html.Label('Sec'),
        dcc.Input(id='sec2', value=45.95, type='number', min=0.00, max=59.99, step=0.01
        )],

        style={'width': '7px', 'display': 'inline-table'}),

    html.Div(id='datatable-event2-container'),

    html.Br(),

    html.Div(
        [html.Label('Event 3'),
        dcc.Dropdown(id='event3',
            options=[
                {'label': '50 Free', 'value': '50 FR'},
                {'label': '100 Free', 'value': '100 FR'},
                {'label': '200 Free', 'value': '200 FR'},
                {'label': '400/500 Free', 'value': '500 FR'},
                {'label': '800/1000 Free', 'value': '1000 FR'},
                {'label': '1500/1650 Free', 'value': '1650 FR'},
                {'label': '100 Back', 'value': '100 BK'},
                {'label': '200 Back', 'value': '200 BK'},
                {'label': '100 Breast', 'value': '100 BR'},
                {'label': '200 Breast', 'value': '200 BR'},
                {'label': '100 Fly', 'value': '100 FL'},
                {'label': '200 Fly', 'value': '200 FL'},
                {'label': '200 IM', 'value': '200 IM'},
                {'label': '400 IM', 'value': '400 IM'},

            ],
            value='200 FR'
        )],

        style={'width': '165px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Course'),
        dcc.Dropdown(id='course3',
            options=[
                {'label': 'SCY', 'value': 'SCY'},
                {'label': 'SCM', 'value': 'SCM'},
                {'label': 'LCM', 'value': 'LCM'}
            ],
            value='SCY'
        )],

        style={'width': '90px', 'display': 'inline-table'}),

    html.Div(
        [html.Label('Min'),
        dcc.Input(id='min3', value=1, type='number', min=0, max=20, step=1
        )],

        style={'width': '5px', 'display': 'inline-table'}),
    
    html.Div(
        [html.Label('Sec'),
        dcc.Input(id='sec3', value=40.45, type='number', min=0.00, max=59.99, step=0.01
        )],

        style={'width': '7px', 'display': 'inline-table'}),

    html.Div(id='datatable-event3-container'),
])

@app.callback(
    [Output('datatable-event1-container', 'children'), Output('event1-points-year', 'children')],
    [Input('age', 'value'), Input('start', 'value'), Input('year','value'), Input('event1', 'value'), Input('course1', 'value'), Input('min1', 'value'), Input('sec1', 'value')])
def update_output_div(input_age, input_start, input_year, input_event1, input_course1, input_min1, input_sec1):
    input_start += 19
    if input_event1=='500 FR' and (input_course1 in ['LCM','SCM']):
        input_event1='400 FR'
    if input_event1=='1000 FR' and (input_course1 in ['LCM','SCM']):
        input_event1='800 FR'
    if input_event1=='1650 FR' and (input_course1 in ['LCM','SCM']):
        input_event1='1500 FR'

    filtered_df = df[(df.age_end < (input_start+4)) & (df.age_end >= input_start) & (df.age_start == input_age) & (df.event == input_event1) & (df.course == input_course1)]
    years = [str(input_year+1), str(input_year+2), str(input_year+3), str(input_year+4)]
    classes = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    filtered_df['Class'] = classes[0:(filtered_df.shape[0])]
    filtered_df['Year'] = years[0:(filtered_df.shape[0])]
    filtered_df['Predicted Time'] = pd.to_datetime((input_min1*60 + input_sec1) * filtered_df['mean'], unit='s')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].dt.strftime('%M:%S.%f')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].apply(lambda x: x[:-4])
    filtered_df['predict_mean'] = (input_min1*60 + input_sec1)*filtered_df['mean']
    filtered_df['ACC Points'] = filtered_df.apply(score_lookup,axis=1)
    filtered_df = filtered_df.drop(columns=['event','course','age_start','age_end','mean','std', 'predict_mean'])
    points = filtered_df['ACC Points'].mean()
    return generate_table(filtered_df), points

@app.callback(
    [Output('datatable-event2-container', 'children'), Output('event2-points-year', 'children')],
    [Input('age', 'value'), Input('start', 'value'), Input('year','value'), Input('event2', 'value'), Input('course2', 'value'), Input('min2', 'value'), Input('sec2', 'value')])
def update_output_div(input_age, input_start, input_year, input_event2, input_course2, input_min2, input_sec2):
    input_start += 19
    if input_event2=='500 FR' and (input_course2 in ['LCM','SCM']):
        input_event2='400 FR'
    if input_event2=='1000 FR' and (input_course2 in ['LCM','SCM']):
        input_event2='800 FR'
    if input_event2=='1650 FR' and (input_course2 in ['LCM','SCM']):
        input_event2='1500 FR'

    filtered_df = df[(df.age_end < (input_start+4)) & (df.age_end >= input_start) & (df.age_start == input_age) & (df.event == input_event2) & (df.course == input_course2)]
    years = [str(input_year+1), str(input_year+2), str(input_year+3), str(input_year+4)]
    classes = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    filtered_df['Class'] = classes[0:(filtered_df.shape[0])]
    filtered_df['Year'] = years[0:(filtered_df.shape[0])]
    filtered_df['Predicted Time'] = pd.to_datetime((input_min2*60 + input_sec2) * filtered_df['mean'], unit='s')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].dt.strftime('%M:%S.%f')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].apply(lambda x: x[:-4])
    filtered_df['predict_mean'] = (input_min2*60 + input_sec2)*filtered_df['mean']
    filtered_df['ACC Points'] = filtered_df.apply(score_lookup,axis=1)
    filtered_df = filtered_df.drop(columns=['event','course','age_start','age_end','mean','std', 'predict_mean'])
    points = filtered_df['ACC Points'].mean()
    return generate_table(filtered_df), points

@app.callback(
    [Output('datatable-event3-container', 'children'), Output('event3-points-year', 'children')],
    [Input('age', 'value'), Input('start', 'value'), Input('year','value'), Input('event3', 'value'), Input('course3', 'value'), Input('min3', 'value'), Input('sec3', 'value')])
def update_output_div(input_age, input_start, input_year, input_event3, input_course3, input_min3, input_sec3):
    input_start += 19
    if input_event3=='500 FR' and (input_course3 in ['LCM','SCM']):
        input_event3='400 FR'
    if input_event3=='1000 FR' and (input_course3 in ['LCM','SCM']):
        input_event3='800 FR'
    if input_event3=='1650 FR' and (input_course3 in ['LCM','SCM']):
        input_event3='1500 FR'

    filtered_df = df[(df.age_end < (input_start+4)) & (df.age_end >= input_start) & (df.age_start == input_age) & (df.event == input_event3) & (df.course == input_course3)]
    years = [str(input_year+1), str(input_year+2), str(input_year+3), str(input_year+4)]
    classes = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    filtered_df['Class'] = classes[0:(filtered_df.shape[0])]
    filtered_df['Year'] = years[0:(filtered_df.shape[0])]
    filtered_df['Predicted Time'] = pd.to_datetime((input_min3*60 + input_sec3) * filtered_df['mean'], unit='s')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].dt.strftime('%M:%S.%f')
    filtered_df['Predicted Time'] = filtered_df['Predicted Time'].apply(lambda x: x[:-4])
    filtered_df['predict_mean'] = (input_min3*60 + input_sec3)*filtered_df['mean']
    filtered_df['ACC Points'] = filtered_df.apply(score_lookup,axis=1)
    filtered_df = filtered_df.drop(columns=['event','course','age_start','age_end','mean','std', 'predict_mean'])
    points = filtered_df['ACC Points'].mean()
    return generate_table(filtered_df), points

@app.callback(
    [Output('all-event-points-year', 'children'), Output('schol', 'children')],
    [Input('team_place', 'value'), Input('event1-points-year', 'children'), Input('event2-points-year', 'children'), Input('event3-points-year','children')])
def update_output_div(input_team_place, input_event1_score, input_event2_score, input_event3_score,):
    total = input_event1_score + input_event2_score + input_event3_score
    scholarship_by_acc_place = {1: 9.9/1388.2, 2: 9.9/1137.733, 3: 9.9/1009.733, 4: 9.9/890.0667, 5: 9.9/787.4667}
    schol = round(total * scholarship_by_acc_place[input_team_place] * 100, 0)
    schol = str(schol) + '%'
    return total, schol


if __name__ == '__main__':
    app.run_server(debug=True)