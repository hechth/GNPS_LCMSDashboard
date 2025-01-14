# Dash imports

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_daq as daq

# Plotly Imports
import plotly.express as px
import plotly.graph_objects as go

OVERLAY_PANEL = [
    dbc.CardHeader(html.H5("LCMS Overlay Options")),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay UDI", addon_type="prepend"),
                            dbc.Input(id='overlay_usi', placeholder="Enter Overlay File UDI for GNPS"),
                        ],
                        className="mb-3",
                    ),
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay m/z", addon_type="prepend", style={"margin-right":"20px"}),
                            #dbc.Input(id='overlay_mz', placeholder="Enter Overlay mz column", value="row m/z"),
                            dcc.Dropdown(
                                id='overlay_mz',
                                options=[
                                    {'label': 'None', 'value': ''},
                                ],
                                searchable=False,
                                clearable=False,
                                value="row m/z",
                                style={
                                    "width":"60%"
                                }
                            )
                        ],
                        className="mb-3",
                    ),
                ),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay RT", addon_type="prepend", style={"margin-right":"20px"}),
                            #dbc.Input(id='overlay_rt', placeholder="Enter Overlay rt column", value="row retention time"),
                            dcc.Dropdown(
                                id='overlay_rt',
                                options=[
                                    {'label': 'None', 'value': ''},
                                ],
                                searchable=False,
                                clearable=False,
                                value="row retention time",
                                style={
                                    "width":"60%"
                                }
                            )
                        ],
                        className="mb-3",
                    ),
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay color", addon_type="prepend", style={"margin-right":"20px"}),
                            #dbc.Input(id='overlay_color', placeholder="Enter Overlay color column", value=""),
                            dcc.Dropdown(
                                id='overlay_color',
                                options=[
                                    {'label': 'None', 'value': ''},
                                ],
                                searchable=False,
                                clearable=False,
                                value="",
                                style={
                                    "width":"60%"
                                }
                            )
                        ],
                        className="mb-3",
                    ),
                ),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay size", addon_type="prepend", style={"margin-right":"20px"}),
                            #dbc.Input(id='overlay_size', placeholder="Enter Overlay size column", value=""),
                            dcc.Dropdown(
                                id='overlay_size',
                                options=[
                                    {'label': 'None', 'value': ''},
                                ],
                                searchable=False,
                                clearable=False,
                                value="",
                                style={
                                    "width":"60%"
                                }
                            )
                        ],
                        className="mb-3",
                    ),
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay Label Column", addon_type="prepend", style={"margin-right":"20px"}),
                            dcc.Dropdown(
                                id='overlay_hover',
                                options=[
                                    {'label': 'None', 'value': ''},
                                ],
                                searchable=False,
                                clearable=False,
                                value="",
                                style={
                                    "width":"60%"
                                }
                            )
                        ],
                        className="mb-3",
                    ),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay Filter Column", addon_type="prepend"),
                            dbc.Input(id='overlay_filter_column', placeholder="Enter Overlay filter column", value=""),
                        ],
                        className="mb-3",
                    ),
                ),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay Filter Value", addon_type="prepend"),
                            dbc.Input(id='overlay_filter_value', placeholder="Enter Overlay size column", value=""),
                        ],
                        className="mb-3",
                    ),
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Overlay Raw Tabular Data (if no UDI)", addon_type="prepend"),
                            dbc.Textarea(id='overlay_tabular_data', placeholder="Enter Overlay tabular data", rows="20", value=""),
                        ],
                        className="mb-3",
                    ),
                )
            ])
        ]
    )

]