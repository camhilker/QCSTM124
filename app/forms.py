from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, InputRequired, Optional, Length, Regexp, ValidationError
from flask_datepicker import datepicker


# custom validator to determine if instrument error dropdown has been filled and/or if Cartridge ID is the correct length
def is_ie_selected(form, field):
    #cart ID is not blank
    if len(field.data) > 0:
        if form.is_ie.data == 'False':
            raise ValidationError('Please select True above (if instrument errors were present), or clear this field')
        else:
            if len(field.data) != 10:
                raise ValidationError('Cartridge ID must be 10-digits')
            else:
                return True
    #cart ID is blank
    else:
        if form.is_ie.data == 'True':
            raise ValidationError('Please enter a valid 10-digit Cartridge ID or select False above')
        else:
            return True


# main form
class AttachmentForm(FlaskForm):
    #header
    operator_1 = StringField('Operator (required)', validators=[DataRequired(message='Please enter an Operator')])
    operator_2 = StringField('Operator 2 (optional)', validators=[Optional()])

    date_begin = DateField('Begin Date (required)', format='%m-%d-%Y', validators=[DataRequired(message='Please enter a start date')])
    date_end = DateField('End Date (optional)', format='%m-%d-%Y', validators=[Optional()])
    def validate_date_end(form, field):
        if form.date_begin.data > field.data:
            raise ValidationError('End Date must be after Start Date')

    final_dis = SelectField('Final Disposition (required)', choices=[('', ''), ('pass', 'Pass'), ('fail','Fail')], default='', validators=[InputRequired(message='Please select a value')])
    #materials
    lot_p1 = StringField('Panel 1 Lot - PN 70-2210', validators=[Optional()])
    e_dat_p1 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    lot_p2 = StringField('Panel 2 Lot - PN 70-2211', validators=[Optional()])
    e_dat_p2 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    lot_p3 = StringField('Panel 3 Lot - PN 70-2212', validators=[Optional()])
    e_dat_p3 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    lot_p4 = StringField('Panel 4 Lot - PN 70-2213', validators=[Optional()])
    e_dat_p4 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    lot_p5 = StringField('Panel 5 Lot - PN 10326', validators=[Optional()])
    e_dat_p5 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    lot_p6 = StringField('Panel 6 Lot - PN 10644', validators=[Optional()])
    e_dat_p6 = DateField('Expiration Date', format='%m-%d-%Y', validators=[Optional()])
    
    lot_nc = StringField('Copan UTM (Negative Control) Lot - PN 80-0280', validators=[DataRequired()])
    e_dat_nc = DateField('Expiration Date', format='%m-%d-%Y', validators=[DataRequired()])
    

    #vii cartridge info
    lot_vii = StringField('VII RSP Flex Assay Lot - PN 20-006-112', validators=[DataRequired(), Regexp('^(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])(1[6-9]|2[0-9])\d\d\d[A-D]((DEV)?(?(1)I|(I|R))(UO))$', message='Invalid Cartridge Lot Format')])
    e_dat_vii = DateField('Date of Manufacture', format='%m-%d-%Y', validators=[DataRequired()])


    #equipment
    bsc_id = StringField('Biosafety Cabinet ID', validators=[DataRequired()])
    bsc_cdd_mo = SelectField('Month', choices=[('', ''), ('01', 'Jan-01'), ('02','Feb-02'), ('03', 'Mar-03'), ('04','Apr-04'), ('05', 'May-05'), ('06','Jun-06'), ('07', 'Jul-07'), ('08','Aug-08'), ('09', 'Sep-09'), ('10','Oct-10'), ('11','Nov-11'), ('12', 'Dec-12')], default='', validators=[InputRequired(message='Please select a value')])
    bsc_cdd_yr = SelectField('Year', choices=[('', ''), ('2021', '2021'), ('2022','2022'), ('2023', '2023'), ('2024', '2024')], default='', validators=[InputRequired(message='Please select a value')])

    pip_id = StringField('Pipette ID', validators=[DataRequired()])
    pip_cdd_mo = SelectField('Month', choices=[('', ''), ('01', 'Jan-01'), ('02','Feb-02'), ('03', 'Mar-03'), ('04','Apr-04'), ('05', 'May-05'), ('06','Jun-06'), ('07', 'Jul-07'), ('08','Aug-08'), ('09', 'Sep-09'), ('10','Oct-10'), ('11','Nov-11'), ('12', 'Dec-12')], default='', validators=[InputRequired(message='Please select a value')])
    pip_cdd_yr = SelectField('Year', choices=[('', ''), ('2021', '2021'), ('2022','2022'), ('2023', '2023'), ('2024', '2024')], default='', validators=[InputRequired(message='Please select a value')])


    #instrument errors
    is_ie = SelectField('There were instrument errors in this run', choices=[('', ''), (True, 'True'), (False,'False')], default='', validators=[DataRequired(message='Please select a value')])
    ie1_id = StringField('Cartridge ID', validators=[is_ie_selected])
    ie1_type = SelectField('Error Type', choices=[('',''), ('hyb-dock-fail', 'Hyb-Dock-Fail'), ('fail-no-tip', 'Fail-no-tip/Tip Clamp Failure'), ('motor-stall','Motor Stall'), ('thermal-control-failure','Thermal Control Failure'), ('imaging-error','Imaging Error'), ('fan-failure','Fan Failure'), ('insufficient-sample','Insufficient Sample (occlusion)'),('magnet-failure','Magnet Failure'), ('led-fail','Slide LED light failure'), ('pressure-fail','High Pressure Failure/Pressure out of range'), ('scan-failure','Cartridge Scan Failure/Invalid Barcode'), ('invalid-parameter','Received Invalid Parameter'), ('invalid-control','Invalid Control Name'), ('chassis-stall','Chassis Freeze/Tray Motor Stall'), ('invalid-assay','Invalid Assay Name'), ('hybridization-error','Hybridization Error'), ('sonic-fail','Ultrasonics Failure/Sonic Horn Failure'), ('motor-deviation','Motor Position Deviation'), ('invalid-crc','Scheme Files Have Invalid CRC'), ('no-tare-pss','Unable to Tare Pressure Sensor'), ('other', 'Other')])
    
    # another custom validator for whether a type has been selected based on whether the Cartridge ID field above it was filled
    def validate_ie1_type(form, field):
        if len(form.ie1_id.data) == 10 and len(field.data) == 0:
            raise ValidationError('Please select an Instrument Error Type')
        elif len(form.ie1_id.data) == 0 and len(field.data) > 0:
            raise ValidationError('Please clear this field if no Cartridge ID was entered')


    ie2_id = StringField('Cartridge ID', validators=[is_ie_selected, Optional()])
    ie2_type = SelectField('Error Type', choices=[('',''), ('hyb-dock-fail', 'Hyb-Dock-Fail'), ('fail-no-tip', 'Fail-no-tip/Tip Clamp Failure'), ('motor-stall','Motor Stall'), ('thermal-control-failure','Thermal Control Failure'), ('imaging-error','Imaging Error'), ('fan-failure','Fan Failure'), ('insufficient-sample','Insufficient Sample (occlusion)'),('magnet-failure','Magnet Failure'), ('led-fail','Slide LED light failure'), ('pressure-fail','High Pressure Failure/Pressure out of range'), ('scan-failure','Cartridge Scan Failure/Invalid Barcode'), ('invalid-parameter','Received Invalid Parameter'), ('invalid-control','Invalid Control Name'), ('chassis-stall','Chassis Freeze/Tray Motor Stall'), ('invalid-assay','Invalid Assay Name'), ('hybridization-error','Hybridization Error'), ('sonic-fail','Ultrasonics Failure/Sonic Horn Failure'), ('motor-deviation','Motor Position Deviation'), ('invalid-crc','Scheme Files Have Invalid CRC'), ('no-tare-pss','Unable to Tare Pressure Sensor'), ('other', 'Other')])
    def validate_ie2_type(form, field):
        if len(form.ie2_id.data) == 10 and len(field.data) == 0:
            raise ValidationError('Please select an Instrument Error Type')
        elif len(form.ie2_id.data) == 0 and len(field.data) > 0:
            raise ValidationError('Please clear this field if no Cartridge ID was entered')


    ie3_id = StringField('Cartridge ID', validators=[is_ie_selected, Optional()])
    ie3_type = SelectField('Error Type', choices=[('',''), ('hyb-dock-fail', 'Hyb-Dock-Fail'), ('fail-no-tip', 'Fail-no-tip/Tip Clamp Failure'), ('motor-stall','Motor Stall'), ('thermal-control-failure','Thermal Control Failure'), ('imaging-error','Imaging Error'), ('fan-failure','Fan Failure'), ('insufficient-sample','Insufficient Sample (occlusion)'),('magnet-failure','Magnet Failure'), ('led-fail','Slide LED light failure'), ('pressure-fail','High Pressure Failure/Pressure out of range'), ('scan-failure','Cartridge Scan Failure/Invalid Barcode'), ('invalid-parameter','Received Invalid Parameter'), ('invalid-control','Invalid Control Name'), ('chassis-stall','Chassis Freeze/Tray Motor Stall'), ('invalid-assay','Invalid Assay Name'), ('hybridization-error','Hybridization Error'), ('sonic-fail','Ultrasonics Failure/Sonic Horn Failure'), ('motor-deviation','Motor Position Deviation'), ('invalid-crc','Scheme Files Have Invalid CRC'), ('no-tare-pss','Unable to Tare Pressure Sensor'), ('other', 'Other')])
    def validate_ie3_type(form, field):
        if len(form.ie3_id.data) == 10 and len(field.data) == 0:
            raise ValidationError('Please select an Instrument Error Type')
        elif len(form.ie3_id.data) == 0 and len(field.data) > 0:
            raise ValidationError('Please clear this field if no Cartridge ID was entered')


    ie4_id = StringField('Cartridge ID', validators=[is_ie_selected, Optional()])
    ie4_type = SelectField('Error Type', choices=[('',''), ('hyb-dock-fail', 'Hyb-Dock-Fail'), ('fail-no-tip', 'Fail-no-tip/Tip Clamp Failure'), ('motor-stall','Motor Stall'), ('thermal-control-failure','Thermal Control Failure'), ('imaging-error','Imaging Error'), ('fan-failure','Fan Failure'), ('insufficient-sample','Insufficient Sample (occlusion)'),('magnet-failure','Magnet Failure'), ('led-fail','Slide LED light failure'), ('pressure-fail','High Pressure Failure/Pressure out of range'), ('scan-failure','Cartridge Scan Failure/Invalid Barcode'), ('invalid-parameter','Received Invalid Parameter'), ('invalid-control','Invalid Control Name'), ('chassis-stall','Chassis Freeze/Tray Motor Stall'), ('invalid-assay','Invalid Assay Name'), ('hybridization-error','Hybridization Error'), ('sonic-fail','Ultrasonics Failure/Sonic Horn Failure'), ('motor-deviation','Motor Position Deviation'), ('invalid-crc','Scheme Files Have Invalid CRC'), ('no-tare-pss','Unable to Tare Pressure Sensor'), ('other', 'Other')])
    def validate_ie4_type(form, field):
        if len(form.ie4_id.data) == 10 and len(field.data) == 0:
            raise ValidationError('Please select an Instrument Error Type')
        elif len(form.ie4_id.data) == 0 and len(field.data) > 0:
            raise ValidationError('Please clear this field if no Cartridge ID was entered')


    ie5_id = StringField('Cartridge ID', validators=[is_ie_selected, Optional()])
    ie5_type = SelectField('Error Type', choices=[('',''), ('hyb-dock-fail', 'Hyb-Dock-Fail'), ('fail-no-tip', 'Fail-no-tip/Tip Clamp Failure'), ('motor-stall','Motor Stall'), ('thermal-control-failure','Thermal Control Failure'), ('imaging-error','Imaging Error'), ('fan-failure','Fan Failure'), ('insufficient-sample','Insufficient Sample (occlusion)'),('magnet-failure','Magnet Failure'), ('led-fail','Slide LED light failure'), ('pressure-fail','High Pressure Failure/Pressure out of range'), ('scan-failure','Cartridge Scan Failure/Invalid Barcode'), ('invalid-parameter','Received Invalid Parameter'), ('invalid-control','Invalid Control Name'), ('chassis-stall','Chassis Freeze/Tray Motor Stall'), ('invalid-assay','Invalid Assay Name'), ('hybridization-error','Hybridization Error'), ('sonic-fail','Ultrasonics Failure/Sonic Horn Failure'), ('motor-deviation','Motor Position Deviation'), ('invalid-crc','Scheme Files Have Invalid CRC'), ('no-tare-pss','Unable to Tare Pressure Sensor'), ('other', 'Other')])
    def validate_ie5_type(form, field):
        if len(form.ie5_id.data) == 10 and len(field.data) == 0:
            raise ValidationError('Please select an Instrument Error Type')
        elif len(form.ie5_id.data) == 0 and len(field.data) > 0:
            raise ValidationError('Please clear this field if no Cartridge ID was entered')

    submit = SubmitField('Submit')


# form to download CSV
class DownloadForm(FlaskForm):
    start_date = DateField('Start:', format='%m-%d-%Y', validators=[DataRequired(message='Please enter a start date')])
    end_date = DateField('End:', format='%m-%d-%Y')
    def validate_end_date(form, field):
        if field.data == None or form.start_date.data > field.data:
            raise ValidationError('End Date must be after Start Date')

    submit = SubmitField('Submit')
