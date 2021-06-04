
import pandas as pd
import ipywidgets
import plotly.express as px
import ipywidgets as widgets

df = pd.read_csv('/Users/suhairkilliyath/Downloads/floods.csv')
df['Year'] = pd.to_datetime(df['Began']).dt.year
df.head()

year_widget1 = widgets.IntRangeSlider(value=[2015, 2020], min=1985,
        max=2020, step=1, description='Years:')

@ipywidgets.interact(year =year_widget1)
def geo_plot(year):
    fig = px.scatter_mapbox(
        df[df['Year'].between(year[0], year[1])],
        lat='lat',
        lon='long',
        hover_name='Country',
        size='Dead',
        )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

year_widget2 = widgets.IntRangeSlider(value=[2015, 2020], min=1985,
 max=2020, step=1, description= 'Years:')
l = widgets.link((year_widget1, 'value'), (year_widget2, 'value'))


@ipywidgets.interact(year=year_widget2)
def bar_plot_causes(year):
    causes = df[df['Year'].between(year[0],
                year[1])].groupby(by=['Main cause'      ]).size().reset_index(name='counts')
    causes = causes.sort_values(['counts'], ascending=False)[:10]
    fig = px.bar(data_frame=causes, y= 'Main cause', x='counts')
    year_widget2.layout.display = 'none'
    fig.show()

@ipywidgets.interact(year=year_widget2)
def bar_plot_causes(year):
    countries = df[df["Year"].between(year[0], year[1])].groupby(by=["Country"])["Dead"].sum().reset_index(name="counts")
    countries = countries.sort_values(['counts'],ascending=False)[:10]
    fig = px.bar(data_frame=countries, x="Country", y="counts")
    year_widget2.layout.display = 'none'
    fig.show()

# <center style=”color:blue”> World Wide Floods Dashboard </center> <center><img src=”flood_logo.png”/></center> <center> <b> Global Active Archive of Large Flood Events, 1985-Present. Dartmouth Flood Observatory, University of Colorado, USA.</b></center>

from IPython.display import display, HTML
CSS = """
.output {
    align-items: center;
}
"""
HTML('<style>{}</style>'.format(CSS))

@ipywidgets.interact(year=year_widget2)
def calculate_period_death(year):
    return display(widgets.HTML(value='<h3>Flooding Caused {size} Total <i>Death</i> for the selected Period</{size}></h3>'.format(size=df[df["Year"].between(year[0], year[1])]["Dead"].sum())))
