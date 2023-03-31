import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import hvplot.pandas
import panel as pn
import holoviews as hv
# Load the data
import panel as pn
import numpy as np
import holoviews as hv
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

#hv.extension('bokeh')
data = pd.read_csv('StudentsPerformance.csv')

# First dashboard with the four plots
plots = pn.Column(
    pn.Row(data.hvplot.bar('gender', 'math score', groupby='test preparation course', height=300),
           data.hvplot.bar('race/ethnicity', 'math score', groupby='test preparation course', height=300)),
    pn.Row(data.hvplot.bar('gender', 'reading score', groupby='test preparation course', height=300),
           data.hvplot.bar('race/ethnicity', 'reading score', groupby='test preparation course', height=300))
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
dashboard = pn.Column(results)

# Add the switch buttons to each dashboard separately
plots.insert(0, pn.Row(analysis_button, ml_button))
results.insert(0, pn.Row(analysis_button, ml_button))

# Convert the dashboard to a Bokeh layout
bokeh_layout = pn.Row(pn.Column(dashboard), sizing_mode='stretch_both')


# Display the dashboard
pn.serve(bokeh_layout)
