from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import psycopg2
import datetime
import os

#TODO Move year_built bar graph into main method and use if statement to change y range
#TODO Create tabs to sort location data by categories (TAB INSIDE TAB)
#TODO Add relationship for database for chloropleth maps.

def postgres_connect():
    """Creates postgresql connection to RF_PG_DB

    Returns:
        con : Connection to postgres db
    """
    con = psycopg2.connect(host=os.environ.get('PG_RF_HOST'),
                            port=os.environ.get('PG_RF_PORT'),
                            user=os.environ.get('PG_RF_USER'),
                            password=os.environ.get('PG_RF_PASS'),
                            dbname=os.environ.get('PG_RF_DB'),
                            sslmode='require')
    con.autocommit = True
    return con

#This dictionary is used to clean up graph titles and labels for columns so labels can be variables
GRAPH_FORMAT_MAP = {'sqft' : 'Square Feet',
                    'lot_size' : 'Lot Size',
                    'price_per_sqft' : 'Price Per Square Foot',
                    'price' : 'Price',
                    'year_built' : 'Year Built',
                    'beds' : 'Bedrooms',
                    'baths' : 'Bathrooms',
                    'property_type' : 'Property Type'}

#Auto populates graph-ids for use in callbacks for each tab, could these be moved into tabs?
GRAPHS = 12
CITY_GRAPHS = [f"city-graph-{num}" for num in range(0,GRAPHS)]
STATE_GRAPHS = [f"state-graph-{num}" for num in range(0,GRAPHS)]
ZIP_GRAPHS = [f"zip-graph-{num}" for num in range(0,GRAPHS)]
LOCATION_GRAPHS = [f"location-graph-{num}" for num in range(0, GRAPHS)]

def create_dashboard(server=False):
    """Creates a dash dashboard application and adds it to a flask server. If no flask server is passed,
    returns Dash instance's server.

    Args:
        server (Flask server): Flask server to add the dashboard application to.

    Returns:
        Flask server: Returns flask server after dashboard app has been created and
        layout has been set and callbacks initialized.
    """
    css_path = [dbc.themes.BOOTSTRAP]
    scripts_path = [os.getcwd() + "/static/assets/js/scripts.js"]
    assets_path = os.getcwd() + "/static/assets"
    if server:
        app = Dash(__name__, suppress_callback_exceptions=True, server=server, url_base_pathname="/rf_dashboard/", assets_folder=assets_path, external_scripts=scripts_path, external_stylesheets=css_path)
    else:
        app = Dash(__name__, suppress_callback_exceptions=True, assets_folder=assets_path, external_scripts=scripts_path, external_stylesheets=css_path)
    
    app.title = "Redfin Data Dashboard"
    app.layout = html.Div([
        (html.H1(dbc.Row(f'Data from: {datetime.date.today()}', justify='center', class_name='text-dark bg-light'))),
        dbc.Tabs(id='tabs-example-1', active_tab='tab-1', children=[
            dbc.Tab(label='City', tab_id='tab-1', label_class_name='text-secondary', activeLabelClassName = 'fw-bold fst-italic text-dark'),
            dbc.Tab(label='State', tab_id='tab-2', label_class_name='text-secondary', activeLabelClassName = 'fw-bold fst-italic text-dark'),
            dbc.Tab(label='Postal code', tab_id='tab-3', label_class_name='text-secondary', activeLabelClassName = 'fw-bold fst-italic text-dark'),
            dbc.Tab(label='Market', tab_id='tab-4',  label_class_name='text-secondary', activeLabelClassName = 'fw-bold fst-italic text-dark')
        ]),
        html.Div(id='tabs-example-content-1')
    ])
    init_callbacks(app)
    return app.server


def init_callbacks(app):
    """Initializes callbacks for dash application.

    Args:
        app (Dash application): Dash application to initialized the callbacks to.
    """

    @callback(
        Output('tabs-example-content-1', 'children'),
        Input('tabs-example-1', 'active_tab')
    )
    def render_content(tab):
        """Renders dash tabs based on which tab id is active.

        Args:
            tab (String): ID of tab to render in Dash app

        Returns:
            Dash html.Div: Returns html.Div object containing the data to be loaded into the tab.
        """
        if tab == 'tab-1':
            return html.Div([
                dbc.Row([html.H2('City Analysis')],
                        class_name='text-center'),
                dbc.Row([dbc.Col(html.H3('City Data: '), width=2, class_name='text-end'),
                             dbc.Col(dbc.Input(id="city-name", type='text', placeholder="City Name", value="Glassell Park", debounce=True), width=2),
                             dbc.Col(dbc.Input(id="state-abbreviation-city", type='text', placeholder="State Abbreviation", value="CA", debounce=True), width=2),],
                             class_name='justify-content-md-center g-3',
                             align='center'),
                             
                             dbc.Spinner(children=[dbc.Accordion([dbc.AccordionItem(id=f'{id}-text', children=[html.Div([dcc.Graph(id)])]) for id in CITY_GRAPHS])],
                                         id="loading-1",
                                         type="grow",
                                         spinner_class_name='position-absolute top-0')
                                         ]),
        elif tab == 'tab-2':
            return html.Div([
                dbc.Row([html.H2('State Analysis')],
                        class_name='text-center'),
                dbc.Row(children=[
                                    dbc.Col(html.H3('State: '), width=2, class_name='text-end'),
                                    dbc.Col(dbc.Input(id="state-name", type='text', placeholder="State Abbreviation", value="WA", debounce=True), width=2),
                                    ],
                                    class_name='justify-content-md-center g-3',
                                    align='center'),
                dbc.Spinner(children=[html.Div([dcc.Graph(id) for id in STATE_GRAPHS])],
                            id="loading-2",
                            type="grow",
                            spinner_class_name='position-absolute top-0')
                            ])
        
        elif tab == 'tab-3':
            return html.Div([
                dbc.Row([html.H2('Postal Code Analysis')],
                         class_name='text-center'),
                dbc.Row([dbc.Col(html.H3('Postal Code: '), 
                                 width=2, 
                                 class_name='text-end'),
                         dbc.Col(dbc.Input(id="postal-code", type='number', placeholder="Postal code", value=2128, debounce=True),width=2)],
                         class_name='justify-content-md-center g-3',
                         align='center'),
                            
                dbc.Spinner(children=[html.Div([dcc.Graph(id) for id in ZIP_GRAPHS]),
                                    html.Div([dcc.Dropdown(id='prop-year',
                                                                options=[2023, 2022, 2021, 2020, 2019, 2018],
                                                                value=2023),
                                                #These graphs still need to be added into other locations and their own method to generate                                                
                                                dcc.Graph(id='zip-sales-by-year'),
                                                dcc.Graph(id='zip-prop-type-sold-per-year'),
                                                dcc.Graph(id='zip-prop-price-by-year')]
                                                )],    
                            id="loading-3",
                            type="grow",
                            spinner_class_name='position-absolute top-0')
                ])
        
        elif tab == "tab-4":
            return html.Div([
                dbc.Row(html.H2('Market Analysis'),class_name='text-center'),
                dbc.Row([
                    dbc.Col(html.H3('Market: '),width=2,class_name='text-end'),
                    dbc.Col(dbc.Input(id="location-name", type='text', placeholder="Market", value="North Tacoma", debounce=True), width=2)],
                    class_name='justify-content-md-center g-3',
                    align='center'),
                dbc.Spinner(children=[html.Div([dcc.Graph(id) for id in LOCATION_GRAPHS])],
                            id="loading-4",
                            type="grow",
                            spinner_class_name='position-absolute top-0')
                            ])

    @callback([Output(id, 'figure') for id in ZIP_GRAPHS],
        Output('zip-sales-by-year', 'figure'),
        Output('zip-prop-type-sold-per-year', 'figure'),
        Output('zip-prop-price-by-year', 'figure'),
        Input('postal-code', 'value'),
        Input('prop-year', 'value')
    )
    def zip_div(postal_code, prop_year):
        """Loads data from database into dataframe to use for creating graphs and
        html for the zip tab based on data from Input callbacks.
        graphs is converted to a tuple in order to be correctly passed as parameters.

        Args:
            postal_code (Int): Postal code to query from databse
            prop_year (Int): Year of property sold to query

        Returns:
            Tuple(figures): Returns a tuple of plotly graphs to send to Output callbacks
        """
        con = postgres_connect()
        zip_df = pd.read_sql(("SELECT *  FROM sold_properties WHERE postal_code LIKE (%s) AND property_type != 'Other' and property_type != 'Unknown'"), con, params=(str(postal_code) + '%',))
        con.close()
        graphs = compile_graphs(zip_df, postal_code)

        #TODO Create methods and clean this up in order to use for other locations
        data_by_year = zip_df.query('sold_year == @prop_year')
        prop_price_by_year = data_by_year[['property_type', 'price']].groupby('property_type', as_index=False).mean(True)
        zip_prop_price_by_year_bar = px.bar(prop_price_by_year, x=prop_price_by_year.get('property_type'), y=prop_price_by_year.get('price'))
        prop_to_year = data_by_year['property_type'].value_counts()
        zip_prop_type_sold_by_year = px.bar(prop_to_year, x=prop_to_year.get('property_type'), y=prop_to_year.get('count'))
        zip_count_by_year = zip_df['sold_year'].value_counts()
        zip_sales_by_year = px.bar(zip_count_by_year, x=zip_count_by_year.get('year'), y=zip_count_by_year.get('count'))
        graphs = graphs + [zip_sales_by_year, zip_prop_type_sold_by_year, zip_prop_price_by_year_bar]
        return tuple(graphs)

    @callback(
        [Output(id, 'figure') for id in STATE_GRAPHS],
        Input('state-name', 'value')
    )
    def state_div(state_name):
        """Loads data from database into dataframe to use for creating graphs and
        html for the state tab based on data from Input callbacks.
        graphs is converted to a tuple in order to be correctly passed as parameters.

        Args:
            state_name (String): State or province abbreviation as two letters. Ex: WA

        Returns:
            Tuple(figures): Returns a tuple of plotly graphs to send to Output callbacks        """
        
        con = postgres_connect()
        state_df = pd.read_sql(("SELECT *  FROM sold_properties WHERE state_prov = (%s) AND property_type != 'Other' and property_type != 'Unknown'"), con, params=(state_name,))
        con.close()
        graphs = compile_graphs(state_df, state_name)
        return tuple(graphs)

    @callback([Output(id, 'figure') for id in CITY_GRAPHS],
              [Output(f'{id}-text', 'title') for id in CITY_GRAPHS],
        Input('city-name', 'value'),
        Input('state-abbreviation-city', 'value')
    )
    def city_div(city_name, state_name):
        """Loads data from database into dataframe to use for creating graphs and
        html for the city tab based on data from Input callbacks._summary_
        graphs is converted to a tuple in order to be correctly passed as parameters.

        Args:
            city_name (String): The city name to search for in the database
            state_name (String): State or province abbreviation as two letters. Ex: WA. 
            This state should contain the city to be searched

        Returns:
            Tuple(figures): Returns a tuple of plotly graphs to send to Output callbacks
        """

        con = postgres_connect()
        city_df = pd.read_sql(("SELECT *  FROM sold_properties WHERE state_prov = (%s) AND city = (%s) AND property_type != 'Other' and property_type != 'Unknown'"), con, params=(state_name, city_name))
        con.close()
        graphs = compile_graphs(city_df, city_name)
        titles = [graph.layout.title.text for graph in graphs]
        return tuple(graphs + titles)


    @callback(
        [Output(id, 'figure') for id in LOCATION_GRAPHS],
        Input('location-name', 'value')
    )
    def market_div(market_name):
        """Loads data from database into dataframe to use for creating graphs and
        html for the market tab based on data from Input callbacks.
        graphs is converted to a tuple in order to be correctly passed as parameters.

        Args:
            market_name (String): Market to search for properties in

        Returns:
            Tuple(figures): Returns a tuple of plotly graphs to send to Output callbacks
        """

        con = postgres_connect()
        market_df = pd.read_sql(("SELECT *  FROM sold_properties WHERE location = (%s) AND property_type != 'Other' and property_type != 'Unknown'"), con, params=(market_name,))
        con.close()
        graphs = compile_graphs(market_df, market_name)
        return tuple(graphs)

    def prop_type_bar_graphs(dataframe, location):
        """Creates a list of bar graphs using data from dataframe, with location being passed
        to populate labels in the graphs. Creates a graph for each Dataframe column name in column_list

        Args:
            dataframe (Dataframe): Dataframe containing data to be passed into bar creation methods
            location (String): location String to be passed as labels into graphs. 

        Returns:
            List: List of plotly bar graphs
        """
        column_list = ['price', 'beds', 'baths', 'sqft', 'lot_size', 'price_per_sqft']
        bar_figure_list = [bar_property_price_v_avg_var(dataframe, location, column) for column in column_list]
        bar_figure_list.append(bar_average_year_built_by_prop_type(dataframe, location))
        return bar_figure_list

    def prop_type_scatter_graphs(dataframe, location):
        """Creates a list of scatter graphs using data from dataframe, with location being passed
        to populate labels in the graphs. Creates a graph for each Dataframe column name in column_list

        Args:
            dataframe (Dataframe): Dataframe containing data to be passed into scatter creation methods
            location (String): location String to be passed as labels into graphs. 

        Returns:
            List: List of plotly scatter graphs
        """
        column_list = ["sqft", "lot_size"]
        scatter_figure_list = [scatter_price_v_var_by_prop_type(dataframe, location, column) for column in column_list]
        return scatter_figure_list

    def prop_type_line_graphs(dataframe, location):
        """Creates a list of line graphs using data from dataframe, with location being passed
        to populate labels in the graphs. Creates a graph for each Dataframe column name in column_list

        Args:
            dataframe (Dataframe): Dataframe containing data to be passed into line creation methods
            location (String): location String to be passed as labels into graphs. 

        Returns:
            List: List of plotly line graphs
        """
        column_list = ["price", "price_per_sqft"]
        line_figure_list = [line_avg_var_by_prop_type_by_year(dataframe, location, column) for column in column_list]
        return line_figure_list

    def compile_graphs(dataframe, location):
        """Compiles a list of various graph types.

        Args:
            dataframe (Dataframe): Dataframe containing data to send to creation methods
            location (String): String to send to graph creation methods

        Returns:
            List: List of various plotly graph types
        """
        prop_type_pie_list = [pie_property_data(dataframe, location)]
        bar_figure_list = prop_type_bar_graphs(dataframe, location)
        scatter_figure_list = prop_type_scatter_graphs(dataframe, location)
        line_figure_list = prop_type_line_graphs(dataframe, location)
        graphs = prop_type_pie_list + bar_figure_list + scatter_figure_list + line_figure_list
        return graphs

    def pie_property_data(dataframe, location):
        """Takes dataframe and creates pie chart based 
        on property_type distribution

        Args:
            dataframe (dataframe): Dataframe with property_type data to chart.

        Returns:
            figure: Plotly express pie chart
        """
        if dataframe.shape[0] == 0:
            return None
        else:
            graph = px.pie(dataframe.dropna(), 
                        names=dataframe['property_type'],
                        title=f"Property Type Breakdown for {location}")
            graph.update_layout(title={
                               'xanchor' : 'center',
                               'x' : .5})
            return graph


    def line_avg_var_by_prop_type_by_year(dataframe, location, secondary_column):
        """Creates a plotly line figure to show secondary_column over year 
        by property_type. Removes Unknown, Other, and Timeshare property types from dataframe
        before creating figure. If empty dataframe returns None.

        Args:
            dataframe (Dataframe): Dataframe containing data to create plotly graph.
            location (String): String to populate graph labels with
            secondary_column (String): Name of dataframe secondary column to plot

        Returns:
            Figure: Returns plotly line graph based on data or None

        """
        dataframe = dataframe[~dataframe['property_type'].isin(['Unknown', 'Other', 'Timeshare'])]
        df = dataframe[['property_type', secondary_column, 'sold_year']]
        if df.shape[0] == 0:
            return None
        else: 
            df = df.groupby(['sold_year', 'property_type'], as_index=False).mean(True)  
            graph = px.line(df,
                        x=df.get('sold_year'),
                        y=df.get(secondary_column),
                        color="property_type",
                        title=(f"Average {GRAPH_FORMAT_MAP[secondary_column]} by Property Type Per Year for {location}"),
                        labels={secondary_column : (f"{GRAPH_FORMAT_MAP[secondary_column]}"),
                                "sold_year" : "Year",
                                "property_type" : "Property Type"})
            graph.update_layout(title={
                               'xanchor' : 'center',
                               'x' : .5})
            return graph

    def scatter_price_v_var_by_prop_type(dataframe, location, secondary_column):
        """Creates a plotly scatter figure to show price and secondary_column correlation
        by property_type. Removes Unknown, Other, and Timeshare property types from dataframe
        before creating figure. If empty dataframe returns None.

        Args:
            dataframe (Dataframe): Dataframe containing data to create plotly graph.
            location (String): String to populate graph labels with
            secondary_column (String): Name of dataframe secondary column to plot

        Returns:
            Figure: Returns plotly scatter graph based on data or None

        """
        dataframe = dataframe[~dataframe['property_type'].isin(['Unknown', 'Other', 'Timeshare'])]
        df = dataframe[['property_type', secondary_column, 'price']]
        if df.shape[0] == 0:
            return None
        else:    
            graph = px.scatter(df,
                        x=df.get(secondary_column),
                        y=df.get('price'),
                        color="property_type",
                        trendline='ols',
                        title=f"Price vs {GRAPH_FORMAT_MAP[secondary_column]} by Property Type for {location}",
                        labels={secondary_column : f"{GRAPH_FORMAT_MAP[secondary_column]}",
                                "Price" : "Price"})
            
            graph.update_layout(title={
                    'xanchor' : 'center',
                    'x' : .5})
            return graph

    def bar_property_price_v_avg_var(dataframe, location, secondary_column):
        """Takes dataframe and creates bar chart based on property_type distribution and 
        average of secondary_column. Removes Unknown, Other, and Timeshare property types from dataframe
        before creating figure. If empty dataframe returns None.

        Args:
            dataframe (Dataframe): Dataframe with property_type and price data to chart.
            location (String): location for population of graph labels
            secondary_column (String): Name of column in Dataframe to plot as y axis
        Returns:
            figure: Plotly express bar chart
        """
        dataframe[~dataframe['property_type'].isin(['Unknown', 'Other', 'Timeshare'])]
        avg_price = dataframe[['property_type', secondary_column]]
        if avg_price.shape[0] == 0:
            return None
        else:
            avg_price = avg_price.groupby('property_type', as_index=False).mean(True)
            graph = px.bar(avg_price,
                        x=avg_price.get('property_type'),
                        y=avg_price.get(secondary_column),
                        color="property_type",
                        title=f"Average {GRAPH_FORMAT_MAP[secondary_column]} by property type {location}",
                        labels={secondary_column : f"Average {GRAPH_FORMAT_MAP[secondary_column]}",
                                "property_type" : "Property Type"})
            
            graph.update_layout(title={
                    'xanchor' : 'center',
                    'x' : .5})
            return graph

    def bar_average_year_built_by_prop_type(dataframe, location):
        #TODO Create if statement from other bar chart method to set range
        #if secondary_column is year_built instead of seperate method
        secondary_column = 'year_built'
        """Takes dataframe and creates bar chart based on property_type distribution and 
        average of secondary_column. Changes y axis range to better show years. Removes Unknown, Other, and Timeshare property types from dataframe
        before creating figure. If empty dataframe returns None.

        Args:
            dataframe (Dataframe): Dataframe with property_type and price data to chart.
            location (String): location for population of graph labels
            secondary_column (String): Name of column in Dataframe to plot as y axis
        Returns:
            figure: Plotly express bar chart
        """
        dataframe[~dataframe['property_type'].isin(['Unknown', 'Other', 'Timeshare'])]

        avg = dataframe[['property_type', secondary_column]].groupby('property_type', as_index=False).mean(True).dropna()
        if avg.shape[0] == 0:
            return None
        else:    
            graph = px.bar(avg,
                        x=avg.get('property_type'),
                        y=avg.get(secondary_column),
                        color="property_type",
                        title=f"Average year built by property type for {location}",
                        range_y=[1900, datetime.date.today().year],
                        labels={secondary_column : GRAPH_FORMAT_MAP[secondary_column],
                                "property_type" : "Property Type"})

            graph.update_layout(title={
                               'xanchor' : 'center',
                               'x' : .5})
            return graph
        
if __name__ == '__main__':
    app = create_dashboard()
    app.run()