# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import accounding

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header_style = {
    'color': '#77a2b6',
    'textAlign': 'center',
}
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#77a2b6',
    'color': 'white',
    'padding': '6px',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
}

app.layout = html.Div(children=[
    html.Div(style=header_style,
             children=html.Div([
                 html.Img(src=app.get_asset_url("logo.png")),
                 html.H3('IT-Маркет Хабр', style={'margin-top': '0rem'}),
             ])),
    html.Div([
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Объем продаж', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Количество клиентов', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Основные показатели', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),
        html.Div(id='tabs-content-inline')
    ])
])


def generate_table(df):
    tbl = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
    return tbl


@app.callback(Output('tabs-content-inline', 'children'), Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(children=[
            html.H6('Распределение суммы продаж по когортам в абсолютном выражении (тыс.усл.ед.)'),
            generate_table(accounding.tbl_revenue()),
            html.H6('Распределение суммы продаж по когортам в относительном выражении (к первому месяцу)'),
            generate_table(accounding.tbl_revenue_percent()),
        ])
    elif tab == 'tab-2':
        return html.Div(children=[
            html.H6('Распределение количества клиентов по когортам в абсолютном выражении'),
            generate_table(accounding.tbl_count_customer()),
            html.H6('Распределение количества клиентов в относительном выражении (к первому месяцу)'),
            generate_table(accounding.tbl_percent_count_customer()),
        ])
    elif tab == 'tab-3':
        return html.Div(children=[
            html.H6('Выручка, средний чек, количество покупок на одного пользователя'),
            generate_table(accounding.tbl_sales_metrics()),
            html.H6('Уровень удержания и оттока клиентов'),
            generate_table(accounding.tbl_crr_churn_rate()),
        ])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True, port=8050)
