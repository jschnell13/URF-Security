# Import libraries
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Create the Dash app
app = dash.Dash(__name__)
app.css.append_css({'external_url': '/assets/style.css'})

# Variables
toolCheck = ""
sensCheck = ""
sensCheck2 = ""
authCheck = ""
f1Check = ""
l1Check = ""
f2Check = ""
l2Check = ""
ptDropCheck = ""
rwDropCheck = ""
passDropCheck = ""
otpDropCheck = ""
clearCheck = 0
results_displayed = 0

# Definitions
cDef = "Confidentiality: A measure indicating to which degree sensitive information may be known by entities who are" \
       "not the owner of the given data"
iDef = "Integrity: A measure of the accuracy and completeness of data"
aDef = "Authentication: The process of verifying the identity of a user"

# Terms
cTerm = "C = I: Entity Claiming to be the correct Identity is the owner of a given set of data", html.Br(), \
        "C ≠ I: Entity Claiming to be the correct Identity is NOT the owner of a given set of data", html.Br(), \
        "𝑷_𝑻 = Known: The Plain Text is known"
iTerm = "C = I: Entity Claiming to be the correct Identity is the owner of a given set of data", html.Br(), \
        "C ≠ I: Entity Claiming to be the correct Identity is NOT the owner of a given set of data"
aTerm = "C = I: Entity Claiming to be the correct Identity is the owner of a given set of data", html.Br(), \
        "C ≠ I: Entity Claiming to be the correct Identity is NOT the owner of a given set of data", html.Br(), \
        "One-factor: Correct username and password required for successful authentication", html.Br(), \
        "Two-factor: Correct username, password, and OTP required for successful authentication", html.Br(), \
        "𝑷_𝑰 = 𝑷_𝑪: The Password Inserted is the Correct password", html.Br(), \
        "OTP:  One-time password used in two-factor authentication"

# Attack Definitions
cAttack = "The information has been accessed by the attacker. It is no longer confidential."
cNoAttack = "The information is not currently being accessed by anyone."
cOwner = "The owner can successfully see their information."
iAttack = "The information has been tampered with by the attacker. It is no longer accurate."
iNoAttack = "The owner does not have read / write access to their information.", html.Br(), \
            "However, their information is accurate and complete."
iOwner = "The owner has read / write access to their information. Their information is accurate and complete."
aAttack1 = "The attacker entered the correct password and has compromised the identity of the user.", html.Br(), \
           "Try using two-factor authentication to make the user's account more secure."
aOwner1 = "The owner has entered the correct password.", html.Br(), \
          "Authentication has been granted since only one-factor is necessary."
aNoAttack1 = "The owner has entered the incorrect password.", html.Br(), \
             "Thus, authentication has NOT been granted."
aAttack2 = "The attacker entered the correct password but failed to enter the correct OTP.", html.Br(), \
           "Due to two-factor authentication, the user's account is secure."
aOwner2 = "The owner has entered the correct password, but not the correct OTP.", html.Br(), \
          "Authentication has NOT been granted due to the incorrect OTP."
aAttack3 = "The attacker entered the correct password and the correct OTP.", html.Br(), \
           "The attacker has compromised both layers of authentication and the identity of the user."
aOwner3 = "The owner has entered the correct password and the correct OTP.", html.Br(), \
          "Authentication has been granted both factors are correct."

# Set up the app layout
app.layout = html.Div(children=[
    # Used as global variables to control clearing fields
    html.H4(id='toolCheck', children='', style={'display': 'none'}),
    html.H4(id='sensCheck', children='', style={'display': 'none'}),
    html.H4(id='sensCheck2', children='', style={'display': 'none'}),
    html.H4(id='authCheck', children='', style={'display': 'none'}),
    html.H4(id='f1Check', children='', style={'display': 'none'}),
    html.H4(id='l1Check', children='', style={'display': 'none'}),
    html.H4(id='f2Check', children='', style={'display': 'none'}),
    html.H4(id='l2Check', children='', style={'display': 'none'}),
    html.H4(id='ptDropCheck', children='', style={'display': 'none'}),
    html.H4(id='rwDropCheck', children='', style={'display': 'none'}),
    html.H4(id='passDropCheck', children='', style={'display': 'none'}),
    html.H4(id='otpDropCheck', children='', style={'display': 'none'}),
    html.H4(id='clearCheck', children='', style={'display': 'none'}),
    html.H4(id='results_displayed', children='0', style={'display': 'none'}),

    html.Div(id='title-container', children=[  # Title
        html.H1(id='title', children='Cybersecurity Mission')],
             style={'display': 'block', 'border-radius': '5px',
                    'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                    'padding-top': '0.5%', 'padding-bottom': '0.5%', 'padding-right': '1%', 'padding-left': '1%',
                    'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '23%', 'margin-left': '22%',
                    'text-align': 'center', 'verticalAlign': 'top',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                    }),
    html.Div(id='option-container', children=[
        html.Div(id='cia-container', children=[
            html.H2(children='Control Panel'),
            html.H4(children='Select Visualization Tool',
                    id='tool-text', style={'line-height': '.3'}),
            dcc.Dropdown(id='tool-dropdown',
                         placeholder='Select Tool',
                         options=['Confidentiality', 'Integrity', 'Authentication'],
                         value='',
                         clearable=True,
                         style={'cursor': 'pointer'}),
            html.H4(children='Sensitivity of Data',
                    id='sens-text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='sensitivity-dropdown',
                         placeholder='Select Data Sensitivity',
                         options=['Top Secret', 'Secret', 'Confidential', 'Unclassified'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer'}),
            html.H4(children='Authentication Factors',
                    id='auth_text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='authFactor-dropdown',
                         placeholder='Authentication Factor Type',
                         options=['One-Factor', 'Two-Factor'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer'}),
            html.H4(children='Claim',
                    id='claim-text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Input(id='first_1',
                      placeholder='Enter First',
                      type='text',
                      value='',
                      style={'display': 'none', 'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            dcc.Input(id='last_1',
                      placeholder='Enter Last',
                      type='text',
                      value='',
                      style={'display': 'none', 'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            html.H4(children='Identity',
                    id='id-text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Input(id='first_2',
                      placeholder='Enter First',
                      type='text',
                      value='',
                      style={'display': 'none', 'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            dcc.Input(id='last_2',
                      placeholder='Enter Last',
                      type='text',
                      value='',
                      style={'display': 'none', 'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            html.H4(children='PlainText Known',
                    id='pt_text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='plaintext-dropdown',
                         placeholder='PlainText',
                         options=['Known', 'Unknown'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer',
                                'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            html.H4(children='Read/Write Access Granted',
                    id='rwAccess_text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='rwAccess-dropdown',
                         placeholder='Read Write Access',
                         options=['Yes', 'No'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer',
                                'color': 'white', 'background-color': 'rgb(0, 0, 0)'}),
            html.H4(children='Is the Password Correct?',
                    id='pass_text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='password-dropdown',
                         placeholder='Password Inserted',
                         options=['Correct', 'Incorrect'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer'}),
            html.H4(children='Is the OTP Correct?',
                    id='otp_text',
                    style={'display': 'none', 'line-height': '.3'}),
            dcc.Dropdown(id='otp-dropdown',
                         placeholder='OTP',
                         options=['Correct', 'Incorrect'],
                         value='',
                         clearable=True,
                         style={'display': 'none', 'cursor': 'pointer'})],
                 style={'display': 'block', 'border-radius': '5px',
                        'padding-top': '1%', 'padding-bottom': '4%', 'padding-right': '4%', 'padding-left': '4%',
                        'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                        'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                        'text-align': 'center'}),
        html.Div(id='buttonDashDiv', children=[
            html.Div(id='submit_container', children=[
                html.Button(children='Submit', id='submitButton', n_clicks=0)],
                     style={'display': 'inline-block', 'margin-top': '2%', 'margin-left': '2%', 'margin-right': '4%',
                            }),
            html.Div(id='clear_container', children=[
                html.Button(children='Clear', id='clearButton', n_clicks=0)],
                     style={'display': 'inline-block', 'margin-top': '2%', 'margin-left': '4%', 'margin-right': '2%'}),
        ], style={'display': 'block'})],
             style={'display': 'inline-block', 'width': '18%', 'verticalAlign': 'top',
                    'margin-right': '2%', 'margin-left': '2%'}),
    html.Div(id='mid_Screen', children=[
        html.Div(id='cia-image-container', children=[
            html.Img(id='v_img', src='/assets/startMenu.png',
                     style={'width': '100%'})],
                 style={'display': 'block', 'border-radius': '5px',
                        'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                        'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                        'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)'}),
        html.Div(id='buttonDiv', children=[
            html.Div(id='help_container', children=[
                html.Button(children='Help', id='helpButton', n_clicks=0)],
                     style={'display': 'inline-block', 'margin-top': '2%', 'margin-left': '10%', 'margin-right': '7%'}),
            html.Div(id='dataDive_container', children=[
                html.Button(children='Data Dive', id='dataDiveButton', n_clicks=0)],
                     style={'display': 'inline-block', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '7%'}),
            html.Div(id='defButton_container', children=[
                html.Button(children='Definition', id='defButton', n_clicks=0)],
                     style={'display': 'none', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '10%'}),
        ], style={'display': 'block'}),
    ], style={'display': 'inline-block', 'width': '51%', 'verticalAlign': 'top', 'margin-right': '1%'}),
    html.Div(id='dashboard-container', children=[
        html.Div(id='dashboard', children=[
            html.H2(id='status', children='Attack Status')],
                 style={'display': 'block', 'border-radius': '5px',
                        'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                        'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                        'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                        'text-align': 'center',
                        'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                        }),
        html.Div(id='output_cont', children=[
            html.H3(children='', id='output')],
                 style={'display': 'block', 'border-radius': '5px',
                        'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                        'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                        'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                        'text-align': 'center',
                        'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                        }),
        html.Div(id='term_cont', children=[
            html.H3(children='', id='term')],
                 style={'display': 'none', 'border-radius': '5px',
                        'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                        'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                        'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                        'text-align': 'center',
                        'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                        }),
    ], style={'display': 'inline-block', 'width': '20%', 'verticalAlign': 'top', 'padding-right': '2%',
              'padding-left': '1%', })
], style={'color': 'white'}
)


# Set up the callback function
@app.callback([
    Output(component_id='v_img', component_property='src'),
    Output(component_id='cia-image-container', component_property='style'),
    Output(component_id='title-container', component_property='style'),
    Output(component_id='defButton_container', component_property='style'),
    Output(component_id='term_cont', component_property='style'),
    Output(component_id='cia-container', component_property='style'),
    Output(component_id='dashboard', component_property='style'),
    Output(component_id='output_cont', component_property='style'),
    Output(component_id='auth_text', component_property='style'),
    Output(component_id='authFactor-dropdown', component_property='style'),
    Output(component_id='pt_text', component_property='style'),
    Output(component_id='plaintext-dropdown', component_property='style'),
    Output(component_id='rwAccess_text', component_property='style'),
    Output(component_id='rwAccess-dropdown', component_property='style'),
    Output(component_id='pass_text', component_property='style'),
    Output(component_id='password-dropdown', component_property='style'),
    Output(component_id='otp_text', component_property='style'),
    Output(component_id='otp-dropdown', component_property='style'),
    Output(component_id='sens-text', component_property='style'),
    Output(component_id='sensitivity-dropdown', component_property='style'),
    Output(component_id='claim-text', component_property='style'),
    Output(component_id='first_1', component_property='style'),
    Output(component_id='last_1', component_property='style'),
    Output(component_id='id-text', component_property='style'),
    Output(component_id='first_2', component_property='style'),
    Output(component_id='last_2', component_property='style'),
    Output(component_id='output', component_property='children'),
    Output(component_id='term', component_property='children'),
    Output(component_id='helpButton', component_property='children'),
    Output(component_id='helpButton', component_property='n_clicks'),
    Output(component_id='dataDiveButton', component_property='children'),
    Output(component_id='dataDiveButton', component_property='n_clicks'),
    Output(component_id='defButton', component_property='children'),
    Output(component_id='defButton', component_property='n_clicks'),
    Output(component_id='submitButton', component_property='children'),
    Output(component_id='submitButton', component_property='n_clicks'),
    Output(component_id='sensitivity-dropdown', component_property='value'),
    Output(component_id='authFactor-dropdown', component_property='value'),
    Output(component_id='first_1', component_property='value'),
    Output(component_id='last_1', component_property='value'),
    Output(component_id='first_2', component_property='value'),
    Output(component_id='last_2', component_property='value'),
    Output(component_id='plaintext-dropdown', component_property='value'),
    Output(component_id='rwAccess-dropdown', component_property='value'),
    Output(component_id='password-dropdown', component_property='value'),
    Output(component_id='otp-dropdown', component_property='value'),
    Output(component_id='toolCheck', component_property='children'),
    Output(component_id='sensCheck', component_property='children'),
    Output(component_id='sensCheck2', component_property='children'),
    Output(component_id='authCheck', component_property='children'),
    Output(component_id='f1Check', component_property='children'),
    Output(component_id='l1Check', component_property='children'),
    Output(component_id='f2Check', component_property='children'),
    Output(component_id='l2Check', component_property='children'),
    Output(component_id='ptDropCheck', component_property='children'),
    Output(component_id='rwDropCheck', component_property='children'),
    Output(component_id='passDropCheck', component_property='children'),
    Output(component_id='otpDropCheck', component_property='children'),
    Output(component_id='clearCheck', component_property='children'),
    Output(component_id='results_displayed', component_property='children'),
    Output(component_id='title', component_property='className'),
    Output(component_id='title', component_property='children'),
    Output(component_id='status', component_property='className'),
    Output(component_id='submitButton', component_property='className'),
],
    [Input(component_id='tool-dropdown', component_property='value'),
     Input(component_id='toolCheck', component_property='children'),
     Input(component_id='sensCheck', component_property='children'),
     Input(component_id='sensCheck2', component_property='children'),
     Input(component_id='authCheck', component_property='children'),
     Input(component_id='f1Check', component_property='children'),
     Input(component_id='l1Check', component_property='children'),
     Input(component_id='f2Check', component_property='children'),
     Input(component_id='l2Check', component_property='children'),
     Input(component_id='ptDropCheck', component_property='children'),
     Input(component_id='rwDropCheck', component_property='children'),
     Input(component_id='passDropCheck', component_property='children'),
     Input(component_id='otpDropCheck', component_property='children'),
     Input(component_id='clearCheck', component_property='children'),
     Input(component_id='results_displayed', component_property='children'),
     Input(component_id='first_1', component_property='value'),
     Input(component_id='last_1', component_property='value'),
     Input(component_id='first_2', component_property='value'),
     Input(component_id='last_2', component_property='value'),
     Input(component_id='helpButton', component_property='n_clicks'),
     Input(component_id='dataDiveButton', component_property='n_clicks'),
     Input(component_id='defButton', component_property='n_clicks'),
     Input(component_id='submitButton', component_property='n_clicks'),
     Input(component_id='clearButton', component_property='n_clicks'),
     Input(component_id='sensitivity-dropdown', component_property='value'),
     Input(component_id='authFactor-dropdown', component_property='value'),
     Input(component_id='plaintext-dropdown', component_property='value'),
     Input(component_id='rwAccess-dropdown', component_property='value'),
     Input(component_id='password-dropdown', component_property='value'),
     Input(component_id='otp-dropdown', component_property='value'),
     ])
def update_graph(selected_dropdown, tool, sens1, sens2, auth, f1C, l1C, f2C, l2C, ptDC, rwDC, pDC, otpDC,
                 clear_clicks, r_displayed, f1, l1, f2, l2, helpClicks, dataDiveClicks, defClicks,
                 submitClicks, clearClicks, sensitivity_dropdown=None, auth_dropdown=None, pt_dropdown=None,
                 rw_dropdown=None, pass_dropdown=None, otp_dropdown=None):
    a_drop = {'display': 'none'}
    a_text = {'display': 'none'}
    pt_drop = {'display': 'none'}
    pt_text = {'display': 'none'}
    rw_drop = {'display': 'none'}
    rw_text = {'display': 'none'}
    pw_drop = {'display': 'none'}
    pw_text = {'display': 'none'}
    otp_drop = {'display': 'none'}
    otp_text = {'display': 'none'}
    sens_drop = {'display': 'none'}
    sens_text = {'display': 'none'}
    first1_box = {'display': 'none'}
    last1_box = {'display': 'none'}
    first2_box = {'display': 'none'}
    last2_box = {'display': 'none'}
    claim_text = {'display': 'none'}
    id_text = {'display': 'none'}
    img_cont = {'display': 'block', 'border-radius': '5px',
                'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)'}
    output_cont = {'display': 'block', 'border-radius': '5px',
                   'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                   'padding-top': '0.5%', 'padding-bottom': '0.5%', 'padding-right': '1%', 'padding-left': '1%',
                   'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '23%', 'margin-left': '22%',
                   'text-align': 'center', 'verticalAlign': 'top',
                   'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
    attack_cont = {'display': 'none', 'border-radius': '5px',
                   'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                   'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                   'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                   'text-align': 'center',
                   'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
    cia_cont = {'display': 'block', 'border-radius': '5px',
                'padding-top': '1%', 'padding-bottom': '4%', 'padding-right': '4%', 'padding-left': '4%',
                'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                'text-align': 'center'}
    dash_cont = {'display': 'block', 'border-radius': '5px',
                 'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                 'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                 'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                 'text-align': 'center',
                 'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
    out_cont = {'display': 'block', 'border-radius': '5px',
                'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                'text-align': 'center',
                'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
    def_cont = {'display': 'none', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '10%'}
    submit_style = ''
    attack_text = ''
    title_animate = ''
    status_animate = ''
    num_clear = clear_clicks
    title_text = 'Cybersecurity Mission'  # Title only changes in attack instance
    submit_clicks = submitClicks  # fix box outline color, add text, fix right text boxes
    display_menu = 0  # indicates whether to display a menu, and if so which one

    # Used to deduce whether options have changed
    tool_current = ''
    sens_current = ''
    sens_current2 = ''
    auth_current = ''
    f1C_current = ''
    l1C_current = ''
    f2C_current = ''
    l2C_current = ''
    ptDC_current = ''
    rwDC_current = ''
    pDC_current = ''
    otpDC_current = ''
    pt_case = 0
    pass_case = 0
    otp_case = 0
    rw_case = 0
    r_past = r_displayed
    current_changed = 0  # Used to regulate box color

    # Set Variables
    usertrue = 0  # Usertrue defines whether the user is the correct user
    if (f1 == f2) & (l1 == l2) & (f1 != "") & (f2 != "") & (l1 != "") & (l2 != ""):
        usertrue = 1

    case = 1  # case numerically defines the type of attack
    output_case = "No Attack"  # attack_case defines the type of attack
    venn_image = '/assets/startMenu.png'

    if selected_dropdown == 'Confidentiality':
        pt_drop = {'display': 'block', 'cursor': 'pointer'}
        pt_text = {'display': 'block', 'line-height': '.3'}
        sens_drop = {'display': 'block', 'cursor': 'pointer'}
        sens_text = {'display': 'block', 'line-height': '.3'}
        first1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        first2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        claim_text = {'display': 'block', 'line-height': '.3'}
        id_text = {'display': 'block', 'line-height': '.3'}
        def_cont = {'display': 'inline-block', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '10%'}
        tool_current = 1

        # Set sensitivity value
        sens_case = 0  # Unclassified
        if sensitivity_dropdown == 'Top Secret':
            sens_case = 3  # Top Secret
            sens_current = 3
        if sensitivity_dropdown == 'Secret':
            sens_case = 2  # Secret
            sens_current = 2
        if sensitivity_dropdown == 'Confidential':
            sens_case = 1  # Confidential
            sens_current = 1
        if sensitivity_dropdown == 'Unclassified':
            sens_case = 0  # Unclassified
            sens_current = 0

        if (pt_dropdown is None) or (usertrue is None):
            case = 1
        elif pt_dropdown == 'Unknown':
            case = 2
            pt_case = 1
            ptDC_current = 1
            attack_text = cNoAttack
        elif (pt_dropdown == 'Known') & (usertrue == 1):
            case = 3
            pt_case = 2
            ptDC_current = 2
            output_case = "Owner of Data"
            attack_text = cOwner
        elif (pt_dropdown == 'Known') & (usertrue == 0):
            case = 4
            pt_case = 2
            ptDC_current = 2
            output_case = "Confidentiality Attack"
            attack_text = cAttack

        # Defines what happens in each case
        venn_image = '/assets/confidentialityStart.png'
        if case == 1:
            if sens_case == 0:
                venn_image = '/assets/unclassified_base.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_base.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_base.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_base.png'
        elif case == 2:
            if sens_case == 0:
                venn_image = '/assets/unclassified_noAttack.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_noAttack.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_noAttack.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_noAttack.png'
        elif case == 3:
            if sens_case == 0:
                venn_image = '/assets/unclassified_owner.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_owner.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_owner.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_owner.png'
        elif case == 4:
            if sens_case == 0:
                venn_image = '/assets/unclassified_isAttack.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_isAttack.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_isAttack.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_isAttack.png'

        if sensitivity_dropdown is None:  # Shows confidentiality start screen if the sensitivity value is unchosen
            venn_image = '/assets/confidentialityMenu.png'

    if selected_dropdown == 'Authentication':
        a_drop = {'display': 'block', 'cursor': 'pointer'}
        a_text = {'display': 'block', 'line-height': '.3'}
        pw_drop = {'display': 'block', 'cursor': 'pointer'}
        pw_text = {'display': 'block', 'line-height': '.3'}
        first1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        first2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        claim_text = {'display': 'block', 'line-height': '.3'}
        id_text = {'display': 'block', 'line-height': '.3'}
        def_cont = {'display': 'inline-block', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '10%'}
        tool_current = 2
        venn_image = '/assets/authenticationStart.png'

        if auth_dropdown == 'Two-Factor':
            otp_drop = {'display': 'block', 'cursor': 'pointer'}
            otp_text = {'display': 'block', 'line-height': '.3'}

        # Defines what happens in each case
        if auth_dropdown == 'One-Factor':
            auth_current = 1

            pass_case = 0
            if (pass_dropdown is None) or (usertrue is None):
                case = 1
            elif (pass_dropdown == 'Incorrect') & (usertrue == 1):
                case = 2
                pass_case = 1
                pDC_current = 1
                output_case = "Forgotten Password"
                attack_text = aNoAttack1
            elif (pass_dropdown == 'Correct') & (usertrue == 1):
                case = 3
                pass_case = 2
                pDC_current = 2
                output_case = "Correct Authentication"
                attack_text = aOwner1
            elif (pass_dropdown == 'Correct') & (usertrue == 0):
                case = 4
                pass_case = 2
                pDC_current = 2
                output_case = "Authentication Attack"
                attack_text = aAttack1

            if case == 1:
                venn_image = '/assets/secret_base_auth.png'
            elif case == 2:
                venn_image = '/assets/secret_noAttack_auth.png'
            elif case == 3:
                venn_image = '/assets/secret_owner_auth.png'
            elif case == 4:
                venn_image = '/assets/secret_isAttack_auth.png'

        if auth_dropdown == 'Two-Factor':
            auth_current = 2

            if (pass_dropdown is None) or (usertrue is None) or (otp_dropdown is None) or \
                    ((usertrue == 1) & (pass_dropdown == 'Incorrect') & (otp_dropdown == 'Correct')) or \
                    ((usertrue == 0) & (pass_dropdown == 'Incorrect') & (otp_dropdown == 'Correct')) or \
                    ((usertrue == 0) & (pass_dropdown == 'Incorrect') & (otp_dropdown == 'Incorrect')):
                case = 1
            elif (usertrue == 1) & (pass_dropdown == 'Incorrect') & (otp_dropdown == 'Incorrect'):
                case = 2
                pass_case = 1
                pDC_current = 1
                otp_case = 1
                otpDC_current = 1
                output_case = "Forgotten Password"
                attack_text = aNoAttack1
            elif (usertrue == 1) & (pass_dropdown == 'Correct') & (otp_dropdown == 'Correct'):
                case = 3
                pass_case = 2
                pDC_current = 2
                otp_case = 2
                otpDC_current = 2
                output_case = "Correct Authentication"
                attack_text = aOwner3
            elif (usertrue == 0) & (pass_dropdown == 'Correct') & (otp_dropdown == 'Correct'):
                case = 4
                pass_case = 2
                pDC_current = 2
                otp_case = 2
                otpDC_current = 2
                output_case = "Authentication Attack"
                attack_text = aAttack3
            elif (usertrue == 1) & (pass_dropdown == 'Correct') & (otp_dropdown == 'Incorrect'):
                case = 5
                pass_case = 2
                pDC_current = 2
                otp_case = 1
                otpDC_current = 1
                output_case = "Partial Correct Authentication"
                attack_text = aOwner2
            elif (usertrue == 0) & (pass_dropdown == 'Correct') & (otp_dropdown == 'Incorrect'):
                case = 6
                pass_case = 2
                pDC_current = 2
                otp_case = 1
                otpDC_current = 1
                output_case = "Partial Authentication Attack"
                attack_text = aAttack2

            if case == 1:
                venn_image = '/assets/secret_base_auth2.png'
            elif case == 2:
                venn_image = '/assets/secret_noAttack_auth2.png'
            elif case == 3:
                venn_image = '/assets/secret_owner_auth2.png'
            elif case == 4:
                venn_image = '/assets/secret_isAttack_auth2.png'
            elif case == 5:
                venn_image = '/assets/secret_partOwner_auth2.png'
            elif case == 6:
                venn_image = '/assets/secret_isPartAttack_auth2.png'

    if selected_dropdown == 'Integrity':
        rw_drop = {'display': 'block', 'cursor': 'pointer'}
        rw_text = {'display': 'block', 'line-height': '.3'}
        sens_drop = {'display': 'block', 'cursor': 'pointer'}
        sens_text = {'display': 'block', 'line-height': '.3'}
        first1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last1_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        first2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                      'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        last2_box = {'display': 'inline-block', 'color': 'white', 'background-color': 'rgb(0, 0, 0)', 'width': '40%',
                     'font-family': 'Consolas, Times, serif', 'text-align': 'center'}
        claim_text = {'display': 'block', 'line-height': '.3'}
        id_text = {'display': 'block', 'line-height': '.3'}
        def_cont = {'display': 'inline-block', 'margin-top': '2%', 'margin-left': '7%', 'margin-right': '10%'}
        tool_current = 3

        # Set sensitivity value
        sens_case = 0  # Unclassified
        if sensitivity_dropdown == 'Top Secret':
            sens_case = 3  # Top Secret
            sens_current2 = 3
        if sensitivity_dropdown == 'Secret':
            sens_case = 2  # Secret
            sens_current2 = 2
        if sensitivity_dropdown == 'Confidential':
            sens_case = 1  # Confidential
            sens_current2 = 1
        if sensitivity_dropdown == 'Unclassified':
            sens_case = 0  # Unclassified
            sens_current2 = 0

        if (rw_dropdown is None) or (usertrue is None):
            case = 1
        elif rw_dropdown == 'No':
            case = 2
            rw_case = 1
            rwDC_current = 1
            attack_text = iNoAttack
        elif (rw_dropdown == 'Yes') & (usertrue == 1):
            case = 3
            rw_case = 2
            rwDC_current = 2
            output_case = "Owner of Data"
            attack_text = iOwner
        elif (rw_dropdown == 'Yes') & (usertrue == 0):
            case = 4
            rw_case = 2
            rwDC_current = 2
            output_case = "Integrity Attack"
            attack_text = iAttack

        # Defines what happens in each case
        venn_image = '/assets/integrityStart.png'
        if case == 1:
            if sens_case == 0:
                venn_image = '/assets/unclassified_base_integrity.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_base_integrity.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_base_integrity.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_base_integrity.png'
        elif case == 2:
            if sens_case == 0:
                venn_image = '/assets/unclassified_noAttack_integrity.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_noAttack_integrity.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_noAttack_integrity.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_noAttack_integrity.png'
        elif case == 3:
            if sens_case == 0:
                venn_image = '/assets/unclassified_owner_integrity.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_owner_integrity.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_owner_integrity.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_owner_integrity.png'
        elif case == 4:
            if sens_case == 0:
                venn_image = '/assets/unclassified_isAttack_integrity.png'
            elif sens_case == 1:
                venn_image = '/assets/confidential_isAttack_integrity.png'
            elif sens_case == 2:
                venn_image = '/assets/secret_isAttack_integrity.png'
            elif sens_case == 3:
                venn_image = '/assets/topSecret_isAttack_integrity.png'

        if sensitivity_dropdown is None:  # Shows integrity start screen if the sensitivity value is not chosen
            venn_image = '/assets/integrityMenu.png'

    help_button_text = "Help"
    help_clicks = helpClicks
    data_button_text = "Data Dive"
    data_clicks = dataDiveClicks
    def_button_text = "Definition"
    def_clicks = defClicks

    if (help_clicks > 0) and ((help_clicks % 2) == 0):  # exits help menu
        help_button_text = "Help"
        help_clicks = 0

    if (help_clicks > 0) and ((help_clicks % 2) != 0):  # displays help menu
        help_button_text = "Exit"
        display_menu = 1
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0

    if (data_clicks > 0) and ((data_clicks % 2) == 0):  # exits data menu
        data_button_text = "Data Dive"
        data_clicks = 0

    if (data_clicks > 0) and ((data_clicks % 2) != 0):  # displays data menu
        data_button_text = "Exit"
        display_menu = 2
        help_button_text = "Help"
        help_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0

    if (def_clicks > 0) and ((def_clicks % 2) == 0):  # exits definition menu
        def_button_text = "Definition"
        def_clicks = 0

    if (def_clicks > 0) and ((def_clicks % 2) != 0):  # displays definition menu
        def_button_text = "Exit"
        display_menu = 3
        data_button_text = "Data Dive"
        data_clicks = 0
        help_button_text = "Help"
        help_clicks = 0

    # Checks whether to clear fields, set fields equal to themselves if no change
    sensDrop = sensitivity_dropdown
    authDrop = auth_dropdown
    f1_box = f1
    l1_box = l1
    f2_box = f2
    l2_box = l2
    ptDrop = pt_dropdown
    rwDrop = rw_dropdown
    passDrop = pass_dropdown
    otpDrop = otp_dropdown

    # Clear button functionality
    if ((num_clear != clearClicks) and (clearClicks != 0)) and ((sensDrop != '') or (authDrop != '') or (f1_box != '') or (l1_box != '') or
       (f2_box != '') or (l2_box != '') or (ptDrop != '') or (rwDrop != '') or (passDrop != '') or
       (otpDrop != '')):
        num_clear = clearClicks
        sensDrop = ''
        authDrop = ''
        f1_box = ''
        l1_box = ''
        f2_box = ''
        l2_box = ''
        ptDrop = ''
        rwDrop = ''
        passDrop = ''
        otpDrop = ''
        submit_clicks = 0
        submit_button_text = "Submit"

    submit_ok = 1  # indicates submit button is activated
    if tool_current != tool:  # Change in tool selection
        current_changed = 1
        submit_clicks = 0
        submit_ok = 0
        display_menu = 0
        sensDrop = ''
        authDrop = ''
        f1_box = ''
        l1_box = ''
        f2_box = ''
        l2_box = ''
        ptDrop = ''
        rwDrop = ''
        passDrop = ''
        otpDrop = ''
        sens_current = ''
        sens_current2 = ''
        help_button_text = "Help"
        help_clicks = 0
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        display_menu = 0
        if selected_dropdown == 'Confidentiality':
            venn_image = '/assets/confidentialityStart.png'
        if selected_dropdown == 'Authentication':
            venn_image = '/assets/authenticationStart.png'
        if selected_dropdown == 'Integrity':
            venn_image = '/assets/integrityStart.png'

    if sens_current != sens1:  # Change in confidentiality sensitivity
        current_changed = 1
        submit_clicks = 0
        submit_ok = 0
        display_menu = 0
        f1_box = ''
        l1_box = ''
        f2_box = ''
        l2_box = ''
        ptDrop = ''
        help_button_text = "Help"
        help_clicks = 0
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        display_menu = 0
        if sens_current == 0:
            venn_image = '/assets/unclassified_base.png'
        elif sens_current == 1:
            venn_image = '/assets/confidential_base.png'
        elif sens_current == 2:
            venn_image = '/assets/secret_base.png'
        elif sens_current == 3:
            venn_image = '/assets/topSecret_base.png'

    if sens_current2 != sens2:  # Change in integrity sensitivity
        current_changed = 1
        submit_clicks = 0
        submit_ok = 0
        display_menu = 0
        f1_box = ''
        l1_box = ''
        f2_box = ''
        l2_box = ''
        rwDrop = ''
        help_button_text = "Help"
        help_clicks = 0
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        display_menu = 0
        if sens_current2 == 0:
            venn_image = '/assets/unclassified_base_integrity.png'
        elif sens_current2 == 1:
            venn_image = '/assets/confidential_base_integrity.png'
        elif sens_current2 == 2:
            venn_image = '/assets/secret_base_integrity.png'
        elif sens_current2 == 3:
            venn_image = '/assets/topSecret_base_integrity.png'

    if auth_current != auth:  # Change in number of authentication factors
        current_changed = 1
        submit_clicks = 0
        submit_ok = 0
        display_menu = 0
        f1_box = ''
        l1_box = ''
        f2_box = ''
        l2_box = ''
        passDrop = ''
        otpDrop = ''
        help_button_text = "Help"
        help_clicks = 0
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        display_menu = 0
        if auth_current == 1:
            venn_image = '/assets/secret_base_auth.png'
        elif auth_current == 2:
            venn_image = '/assets/secret_base_auth2.png'

    submit_button_text = "Submit"
    if selected_dropdown == 'Confidentiality':
        if (f1_box == '') or (l1_box == '') or (f2_box == '') or (l2_box == '') or (ptDrop == ''):
            submit_ok = 0
    if selected_dropdown == 'Integrity':
        if (f1_box == '') or (l1_box == '') or (f2_box == '') or (l2_box == '') or (rwDrop == ''):
            submit_ok = 0
    if (auth_current == 1) and (selected_dropdown == 'Authentication'):
        if (f1_box == '') or (l1_box == '') or (f2_box == '') or (l2_box == '') or (passDrop == ''):
            submit_ok = 0
    if (auth_current == 2) and (selected_dropdown == 'Authentication'):
        if ((f1_box == '') or (l1_box == '') or (f2_box == '') or (l2_box == '') or
                (passDrop == '') or (otpDrop == '')):
            submit_ok = 0

    time_to_go = 1  # indicates whether box color should change; 1=true, 0=false
    if ((submit_clicks >= 0) and (submit_clicks % 2) == 0) or (submit_ok == 0):  # instructions currently displayed
        time_to_go = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        attack_text = ''
        output_case = "No Attack"
        if display_menu == 0:
            if selected_dropdown == 'Confidentiality':  # used to show correct definition
                venn_image = '/assets/confidentialityStart.png'
            elif selected_dropdown == 'Authentication':
                venn_image = '/assets/authenticationStart.png'
            elif selected_dropdown == 'Integrity':
                venn_image = '/assets/integrityStart.png'

    r_displayed = 0
    if (submit_clicks > 0) and ((submit_clicks % 2) != 0):  # results currently displayed
        submit_button_text = "Back"
        help_button_text = "Help"
        help_clicks = 0
        data_button_text = "Data Dive"
        data_clicks = 0
        def_button_text = "Definition"
        def_clicks = 0
        display_menu = 0
        r_displayed = 1

    if ((f1 != f1Check) or (l1 != l1Check) or  # used if results are displayed and something changes
        (f2 != f2Check) or (l2 != l2Check) or (pt_case != ptDC_current) or (rw_case != rwDC_current) or
        (pass_case != pDC_current) or (otp_case != otpDC_current)) and ((r_displayed == 1) and (r_past == 1)):
        r_displayed = 0
        time_to_go = 0
        submit_clicks = 0
        submit_button_text = "Submit"
        if display_menu == 0:
            if selected_dropdown == 'Confidentiality':  # used to show correct definition
                venn_image = '/assets/confidentialityStart.png'
            elif selected_dropdown == 'Authentication':
                venn_image = '/assets/authenticationStart.png'
            elif selected_dropdown == 'Integrity':
                venn_image = '/assets/integrityStart.png'

    if display_menu != 0:  # Displays menu options
        time_to_go = 0
        if display_menu == 1:
            venn_image = '/assets/helpMenu.png'
        if display_menu == 2:
            venn_image = '/assets/dataMenu.png'
        if display_menu == 3:
            if selected_dropdown == 'Confidentiality':  # used to show correct definition
                venn_image = '/assets/confidentialityMenu.png'
            elif selected_dropdown == 'Authentication':
                venn_image = '/assets/authenticationMenu.png'
            elif selected_dropdown == 'Integrity':
                venn_image = '/assets/integrityMenu.png'

    if submit_ok == 0:
        submit_style = 'clickDis'

    if (case != 1) & (current_changed == 0) & (
            time_to_go == 1):  # Will show attack definition if options have been chosen
        attack_cont = {'display': 'block', 'border-radius': '5px',
                       'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                       'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                       'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                       'text-align': 'center',
                       'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                       }

    if (case == 4) & (current_changed == 0) & (time_to_go == 1):  # indicates attack, will make picture outline red
        img_cont = {'display': 'block', 'border-radius': '5px',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                    'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                    'box-shadow': '10px 10px 5px rgba(255, 0, 0, 0.5)'}
        output_cont = {'display': 'block', 'border-radius': '5px',
                       'box-shadow': '10px 10px 5px rgba(255, 0, 0, 0.5)',
                       'padding-top': '0.5%', 'padding-bottom': '0.5%', 'padding-right': '1%', 'padding-left': '1%',
                       'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '23%', 'margin-left': '22%',
                       'text-align': 'center', 'verticalAlign': 'top',
                       'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        attack_cont = {'display': 'block', 'border-radius': '5px',
                       'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                       'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                       'box-shadow': '10px 10px 5px rgba(255, 0, 0, 0.5)',
                       'text-align': 'center',
                       'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        cia_cont = {'display': 'block', 'border-radius': '5px',
                    'padding-top': '1%', 'padding-bottom': '4%', 'padding-right': '4%', 'padding-left': '4%',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                    'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                    'text-align': 'center'}
        dash_cont = {'display': 'block', 'border-radius': '5px',
                     'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                     'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                     'box-shadow': '10px 10px 5px rgba(255, 0, 0, 0.5)',
                     'text-align': 'center',
                     'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        out_cont = {'display': 'block', 'border-radius': '5px',
                    'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                    'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                    'box-shadow': '10px 10px 5px rgba(255, 0, 0, 0.5)',
                    'text-align': 'center',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        title_animate = 'red-pop'
        status_animate = 'turn-red'
        if selected_dropdown == 'Confidentiality':
            title_text = 'CONFIDENTIALITY ATTACK'
        if selected_dropdown == 'Integrity':
            title_text = 'INTEGRITY ATTACK'
        if selected_dropdown == 'Authentication':
            title_text = 'AUTHENTICATION ATTACK'

    if (case == 6) & (current_changed == 0) & (
            time_to_go == 1):  # indicates partial attack, will make picture outline yellow
        img_cont = {'display': 'block', 'border-radius': '5px',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                    'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                    'box-shadow': '10px 10px 5px rgba(255, 255, 0, 0.5)'}
        output_cont = {'display': 'block', 'border-radius': '5px',
                       'box-shadow': '10px 10px 5px rgba(255, 255, 0, 0.5)',
                       'padding-top': '0.5%', 'padding-bottom': '0.5%', 'padding-right': '1%', 'padding-left': '1%',
                       'margin-top': '1%', 'margin-bottom': '1%', 'margin-right': '23%', 'margin-left': '22%',
                       'text-align': 'center', 'verticalAlign': 'top',
                       'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        attack_cont = {'display': 'block', 'border-radius': '5px',
                       'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                       'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                       'box-shadow': '10px 10px 5px rgba(255, 255, 0, 0.5)',
                       'text-align': 'center',
                       'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        cia_cont = {'display': 'block', 'border-radius': '5px',
                    'padding-top': '1%', 'padding-bottom': '4%', 'padding-right': '4%', 'padding-left': '4%',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))',
                    'box-shadow': '10px 10px 5px rgba(0, 233, 47, 0.4)',
                    'text-align': 'center'}
        dash_cont = {'display': 'block', 'border-radius': '5px',
                     'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                     'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                     'box-shadow': '10px 10px 5px rgba(255, 255, 0, 0.5)',
                     'text-align': 'center',
                     'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}
        out_cont = {'display': 'block', 'border-radius': '5px',
                    'padding-top': '1%', 'padding-bottom': '1%', 'padding-right': '1%', 'padding-left': '1%',
                    'margin-top': '2%', 'margin-bottom': '1%', 'margin-right': '1%', 'margin-left': '1%',
                    'box-shadow': '10px 10px 5px rgba(255, 255, 0, 0.5)',
                    'text-align': 'center',
                    'background-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 1))'}

    if selected_dropdown is None:  # shows start menu if no tool is chosen
        venn_image = '/assets/startMenu.png'

    return [venn_image, img_cont, output_cont, def_cont, attack_cont, cia_cont, dash_cont, out_cont,
            a_text, a_drop, pt_text, pt_drop, rw_text, rw_drop,
            pw_text, pw_drop, otp_text, otp_drop, sens_text, sens_drop, claim_text, first1_box, last1_box, id_text,
            first2_box, last2_box, output_case, attack_text, help_button_text, help_clicks,
            data_button_text, data_clicks, def_button_text, def_clicks, submit_button_text, submit_clicks,
            sensDrop, authDrop, f1_box, l1_box, f2_box,
            l2_box, ptDrop, rwDrop, passDrop, otpDrop, tool_current, sens_current, sens_current2, auth_current,
            f1C_current, l1C_current, f2C_current, l2C_current, ptDC_current, rwDC_current, pDC_current,
            otpDC_current, num_clear, r_displayed,
            title_animate, title_text, status_animate, submit_style]


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
