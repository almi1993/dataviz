import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import hvplot.pandas
import panel as pn
import holoviews as hv
import bokeh.models
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20
from bokeh.io import show
import pandas as pd
import panel as pn
import holoviews as hv
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
#hv.extension('bokeh')
data = pd.read_csv('StudentsPerformance.csv')
data2 = pd.read_csv('StudentsPerformance.csv')
data3 = pd.read_csv('StudentsPerformance.csv')

hv.extension('bokeh')
attr_options2 = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

# Define attribute selection widget
attr_select2 = pn.widgets.Select(name='Select attribute', options=attr_options2)
viz3 = pn.Column(attr_select2)

@pn.depends(attr_select2.param.value)

def create_barplot_dashboard(attr_select):
    # Group data by attribute and calculate mean math, reading, and writing scores
    grouped_data = data.groupby(attr_select)[['math score', 'reading score', 'writing score']].mean().reset_index()

    # Sort data by math score in ascending order
    grouped_data = grouped_data.sort_values(by='math score', ascending=True)

    # Define the plot figure
    p = figure(y_range=grouped_data[attr_select], plot_width=800, plot_height=400, toolbar_location=None)

    # Add horizontal bars to the plot
    p.hbar_stack(['math score', 'reading score', 'writing score'], y=attr_select, height=0.8, color=( 'blue'), source=grouped_data)

    # Set plot options
    p.title.text = f'Mean scores by {attr_select}'
    p.xaxis.axis_label = 'Mean score'
    p.yaxis.axis_label = attr_select

    return p
viz3.append(create_barplot_dashboard)

viz2 = pn.Column(attr_select2)

    # Define callback function to update dashboard
@pn.depends(attr_select2.param.value)
def create_countplot_dashboard(attr):
        # Calculate count of unique values in selected column
        value_counts = data3[attr].value_counts()

        # Create bar chart using HoloViews
        bars = hv.Bars(value_counts).opts(width=600, height=350, xrotation=90, show_grid=True, 
                                           color=hv.Cycle('Category20'), title=f"Countplot for {attr}")

        return bars

    # Combine widgets and plot into a dashboard using Panel

# Define attribute options
#viz2 = create_countplot_dashboard(data3, attr_options2)
viz2.append(create_countplot_dashboard)

attr_options = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

# Create a selection widget using a Dropdown
#attr_select = pn.widgets.Select(name='Select attribute', options=attr_options)

# Combine into dashboard
#viz1 = pn.Column(attr_select)
viz1 = pn.Column()

# Define callback to update the dashboard when selection changes
@pn.depends(attr_select2.param.value)
def update_dashboard(attr):
    # Group data by attribute and calculate mean math scores
    grouped_data = data2.groupby(attr)['math score'].mean().reset_index()

    # Sort data by math score in ascending order
    grouped_data = grouped_data.sort_values(by='math score', ascending=True)

    # Create a ColumnDataSource object
    source = ColumnDataSource(grouped_data)

    # Define the plot figure
    p = figure(x_range=grouped_data[attr], plot_width=500, plot_height=300)

  # Define color mapper based on math score values
    color_mapper = linear_cmap(field_name='math score', palette=Viridis256, low=min(grouped_data['math score']), high=max(grouped_data['math score']))

    # Add vertical bars to the plot with colormap
    p.vbar(x=attr, top='math score', width=0.8, source=source, line_color='white', color=color_mapper)

    # Set plot options
    p.title.text = f'Mean math score by {attr}'
    p.xaxis.axis_label = attr
    p.yaxis.axis_label = 'Mean math score'
    p.yaxis.formatter = bokeh.models.PrintfTickFormatter(format='%.2f')
    p.legend.visible = False

    return p


# Add callback output to dashboard
viz1.append(update_dashboard)

# First dashboard with the four plots
plots = pn.Column( pn.Row(viz3),
     pn.Row(viz2),
    pn.Row(viz1)
    #pn.Row(data.hvplot.bar('gender', 'math score', groupby='test preparation course', height=100)),
    #pn.Row(data.hvplot.bar('race/ethnicity', 'math score', groupby='test preparation course', height=100)),
    #pn.Row(data.hvplot.bar('gender', 'reading score', groupby='test preparation course', height=100)),
   # pn.Row  (data.hvplot.bar('race/ethnicity', 'reading score', groupby='test preparation course', height=100)),
)

# Set the switch button for the first dashboard
analysis_button = pn.widgets.Button(name='Data Analysis', button_type='primary')
def switch_to_plots(event):
    dashboard[:] = [plots]
analysis_button.on_click(switch_to_plots)

# Second dashboard with machine learning algorithm results
X = data[['math score', 'reading score']].values
y = data['writing score'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
score = regressor.score(X_test, y_test)

results = pn.Column(
    pn.Row(pn.panel("Machine Learning Algorithm Results", align="center", width=800)),
    pn.Row(pn.panel(f"R-squared score: {score}", align="center", width=800))
)

# Set the switch button for the second dashboard
ml_button = pn.widgets.Button(name='Machine Learning', button_type='primary')
def switch_to_results(event):
    dashboard[:] = [results]
ml_button.on_click(switch_to_results)

# Initial dashboard
welcome = pn.pane.Markdown("# Bienvenue Projet Data Visualisation",width=800)

# Load DataFrame
df = pd.read_csv('StudentsPerformance.csv')

# Create DataFrame preview
df_preview = pn.pane.DataFrame(df.head() ,width=800)


# Add the button widget to the dashboard
#dashboard = pn.Column(refresh_button, pn.Row(attr_select, plot))
# Combine into dashboard
dashboard = pn.Column(pn.Row(welcome),pn.Row( df_preview))
dashboard.insert(0, pn.Row(analysis_button, ml_button))

# Add the switch buttons to each dashboard separately
plots.insert(0, pn.Row(analysis_button, ml_button))
results.insert(0, pn.Row(analysis_button, ml_button))

# Convert the dashboard to a Bokeh layout
bokeh_layout = pn.Row(pn.Column(dashboard), sizing_mode='stretch_both')


# Display the dashboard
pn.serve(bokeh_layout)
