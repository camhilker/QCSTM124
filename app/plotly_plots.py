from app import app, db
from app.models import Run, Error, Panel

import pandas as pd
import numpy as np

import plotly.express as px
import plotly
import json


run_df = pd.read_sql(Run.query.statment, db.session.bind)
error_df = pd.read_sql(Error.query.statment, db.session.bind)
panel_df = pd.read_sql(Panel.query.statment, db.session.bind)

m_1 = panel_df.merge(run_df, left_on='run_id', right_on='id')
m_2 = error_df.merge(run_df, left_on='run_id', right_on='id')

panel_df['vii_lot'] = m_1['lot_vii']
panel_df['final_dis'] = m_1['final_dis']
panel_df['date_begin'] = m_1['date_begin']
panel_df['operator_1'] = m_1['operator_1']
panel_df['operator_2'] = m_1['operator_2'].fillna('None')
panel_df['is_ie'] = m_1['is_ie']

error_df['final_dis'] = m_2['final_dis']
error_df['date_begin'] = m_2['date_begin']
error_df['operator_1'] = m_2['operator_1']
error_df['operator_2'] = m_2['operator_2'].fillna('None')

    
    
    
def plot_panels(panel_df):
    fig = px.strip(panel_df, x='vii_lot', y='panel_type',
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
    
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                            color='DarkSlateGrey')))

    plot_json = json.dumps(fig_2, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
    
    
    
def plot_errors(error_df):
    fig= px.strip(error_df, x='vii_lot', y='error_type',
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
    
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                            color='DarkSlateGrey')))
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
