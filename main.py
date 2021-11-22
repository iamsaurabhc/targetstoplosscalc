from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='.')

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

class Output:
    call_target = 0
    call_stoploss = 0
    put_target = 0
    put_stoploss = 0

class NameForm(FlaskForm):
    call_ltp = StringField('Call Strike LTP', validators=[DataRequired()])
    put_ltp = StringField('Put Strike LTP', validators=[DataRequired()])
    target = StringField('Target (in rs)', validators=[DataRequired()])
    stoploss = StringField('Stoploss (in rs)', validators=[DataRequired()])
    
    lot_size = SelectField('Lot Size', choices=['x25', 'x50'])
    type_ = SelectField('Type of Strategy', choices=['SELL', 'BUY'])
    
    submit = SubmitField('Submit')
    
def calculator(call_ltp=1, put_ltp=1, target=1, stoploss=1, lot_size=1, type_=None):
    target_val = target / lot_size
    stoploss_val = stoploss / lot_size
    
    output = Output()
    
    if type_ == 'SELL':
        output.call_target = call_ltp-target_val
        output.call_stoploss = call_ltp+stoploss_val
        
        output.put_target = put_ltp-target_val
        output.put_stoploss = put_ltp+stoploss_val
    
    else:
        output.call_target = call_ltp+target_val
        output.call_stoploss = call_ltp-stoploss_val
        
        output.put_target = put_ltp+target_val
        output.put_stoploss = put_ltp-stoploss_val
        
    return output
    
@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    
    output = Output()
    
    if form.validate_on_submit():
        output = calculator(
            float(form.call_ltp.data),
            float(form.put_ltp.data),
            int(form.target.data),
            int(form.stoploss.data),
            int(form.lot_size.data.replace('x','')),
            form.type_.data
        )
        
    return render_template('index.html', form= form, output = output)

# main driver function
if __name__ == '__main__':
    app.run()