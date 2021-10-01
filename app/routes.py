from flask import render_template, flash, redirect, url_for, request, make_response, send_file
from app import app, db
from app.forms import AttachmentForm, DownloadForm
from app.models import Run, Error, Panel
from app.plotly_plots import plot_errors, plot_panels

from io import StringIO, BytesIO
import csv
import zipfile

from datetime import date

#for trending page
import pandas as pd
import numpy as np




@app.route('/')
@app.route('/view_records')
def view_records():
    flash(message='If you would like to report an error, please email chilker@luminexcorp.com and include the Run ID, Error ID (if applicable) and associated corrections. Thank You!', category='warning')
    page = request.args.get('page', 1, type=int)

    # lists past runs in chronological order
    runs = Run.query.order_by(Run.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('view_records', page=runs.next_num) \
        if runs.has_next else None
    prev_url = url_for('view_records', page=runs.prev_num) \
        if runs.has_prev else None
    return render_template('view_records.html', title='Previous Records', runs=runs.items,
                           next_url=next_url, prev_url=prev_url)


# Callback that commits entries into db once "submit" is clicked
@app.route('/enter_record', methods=['GET', 'POST'])
def enter_record():
    form = AttachmentForm()
    if form.validate_on_submit():
        run = Run(
            operator_1=form.operator_1.data, 
            operator_2=form.operator_2.data, 
            date_begin=form.date_begin.data, 
            date_end=form.date_end.data, 
            final_dis=form.final_dis.data,
            lot_nc=form.lot_nc.data,
            e_dat_nc=form.e_dat_nc.data,
            lot_vii=form.lot_vii.data,
            e_dat_vii=form.e_dat_vii.data,

            bsc_id=form.bsc_id.data,
            bsc_cdd=form.bsc_cdd_mo.data + '-' + form.bsc_cdd_yr.data,
            pip_id=form.pip_id.data,
            pip_cdd=form.pip_cdd_mo.data + '-' + form.bsc_cdd_yr.data,

            #error entry
            is_ie=form.is_ie.data
            )
        db.session.add(run)

        # this is so we can grab run ID
        db.session.flush()

        for ind, lot_dat in enumerate([(form.lot_p1.data, form.e_dat_p1.data), (form.lot_p2.data, form.e_dat_p2.data), (form.lot_p3.data, form.e_dat_p3.data), (form.lot_p4.data, form.e_dat_p4.data), (form.lot_p5.data, form.e_dat_p5.data), (form.lot_p6.data, form.e_dat_p6.data)]):
            if len(lot_dat[0]) > 0 and lot_dat[1] != None:
                panel = Panel(
                    panel_type=ind+1,
                    panel_lot=lot_dat[0],
                    panel_e_dat=lot_dat[1],
                    run_entry=run
                    )
                db.session.add(panel)


        # conditional to only add entries to the Error table where data was filled in
        for ind, id_type in enumerate([(form.ie1_id.data, form.ie1_type.data), (form.ie2_id.data, form.ie2_type.data), (form.ie3_id.data, form.ie3_type.data), (form.ie4_id.data, form.ie4_type.data), (form.ie5_id.data, form.ie5_type.data)]):
            if form.is_ie.data == 'True' and len(id_type[0]) > 0 and len(id_type[1]) > 0:
                error = Error(
                    cart_id=id_type[0],
                    error_type=id_type[1],
                    vii_lot=form.lot_vii.data,
                    run_entry=run
                    )
                db.session.add(error)

        db.session.commit()
        flash(message='Your record submission was successful', category='info')
        return redirect(url_for('view_records'))
    return render_template('enter_record.html',  title='Enter Record', form=form)


@app.route('/download_csv', methods=['GET', 'POST'])
def download_csv():
    form = DownloadForm()
    if form.validate_on_submit():
        
        query_1 = Run.query.filter(Run.timestamp >= str(form.start_date.data) + ' 00:00:00', Run.timestamp < str(form.end_date.data) + ' 00:00:00').all()
        query_2 = [item for sublist in [row.errors.all() for row in query_1] for item in sublist]
        query_3 = [item for sublist in [row.panels.all() for row in query_1] for item in sublist]

        try:
            test_query = [col for col in query_1[0].__dict__]

        except:
            flash(message='Invalid Date Range', category='danger')
            return render_template('download_csv.html',  title='Retrieve Data as CSV', form=form)


        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            queries = [(query_1, 'run_table.csv'), (query_2, 'error_table.csv'), (query_3, 'panel_table.csv')]
            for query, filename in queries:

                si = StringIO()
                cw = csv.writer(si)

                column_names = [col for col in query[0].__dict__]
                column_names.pop(column_names.index('_sa_instance_state'))

                column_names.sort()
                cw.writerow(column_names)

                for row in query:
                    csv_list = list()
                    for column_name in column_names:
                        col = ""
                        if column_name != '_sa_instance_state':
                            data = str(row.__dict__[column_name])
                            col = col.join(data)
                        csv_list.append(col)
                    cw.writerow(csv_list)


                data = zipfile.ZipInfo(filename)
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, si.getvalue())
        memory_file.seek(0)
        
        return send_file(memory_file, attachment_filename='QCSTM_data-pull.zip', as_attachment=True)
    
    return render_template('download_csv.html',  title='Retrieve Data as CSV', form=form)


@app.route('/trending')
def trending():
    
    run_df = pd.read_sql(Run.query.all(), db.session.bind)
    error_df = pd.read_sql(Error.query.all(), db.session.bind)
    panel_df = pd.read_sql(Panel.query.all(), db.session.bind)

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
    
    panel_viz = plot_panels(panel_df)
    error_viz = plot_errors(error_df)
    
    context = {'panel_viz': panel_viz, 'error_viz': error_viz}
    return render_template('trending.html', title='QCSTM-124 Data Trending', context=context)
    
