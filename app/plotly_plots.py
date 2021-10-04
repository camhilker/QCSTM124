import pandas as pd
import numpy as np

import plotly.express as px
import plotly
import json


def plot_panels(final_df):
    fig = px.strip(final_df, x='vii_lot', y='panel_type',
                 width=1750, height=390,
                 title="Panels", template='simple_white',
                 color='final_dis', color_discrete_map={'fail':'red', 'pass':'lime'}, 
                 hover_name='panel_type', 
                 hover_data={'date_begin':True, 
                             'is_ie':True, 
                             'panel_lot':True, 
                             'operator_1':True, 
                             'operator_2':True,
                             'final_dis':False,
                             'vii_lot':False,
                             'panel_type':False}, 
                 labels={'vii_lot':'Verigene II RSP Lot',
                         'is_ie':'Instrument Errors',
                         'final_dis':'Final Disposition',
                         'panel_lot': 'Panel Lot',
                         'panel_type': 'RSP Panel Number',
                         'operator_1': 'Operator 1',
                         'operator_2': 'Operator 2',
                         'date_begin': 'Run Date'},)
    
    fig.update_xaxes(categoryorder='category ascending')
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                            color='DarkSlateGrey')))

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
    
    
    
def plot_errors(final_df):
    fig= px.strip(final_df, x='vii_lot', y='error_type',
                 width=1750, height=390,
                 title="Instrument Errors", template='simple_white',
                 color='final_dis', color_discrete_map={'fail':'red', 'pass':'lime'}, 
                 hover_name='cart_id', 
                 hover_data={'date_begin':True, 
                             'operator_1':True, 
                             'operator_2':True,
                             'error_type':True,
                             'cart_id':True,
                             'vii_lot':False,
                             'final_dis':False}, 
                 labels={'vii_lot':'Verigene II RSP Lot',
                         'error_type':'Instrument Error',
                         'final_dis':'Final Disposition',
                         'cart_id': 'Cartridge ID',
                         'operator_1': 'Operator 1',
                         'operator_2': 'Operator 2',
                         'date_begin': 'Run Date'})
    
    fig.update_xaxes(categoryorder='category ascending')
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                            color='DarkSlateGrey')))
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
