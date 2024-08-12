import plotly.express as px
import plotly.io as pio
import webview

# Sample data
df = px.data.iris()

# Create a Plotly figure
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species', title='Iris Data Scatter Plot')

# Save the figure as an HTML file
html_file = 'plotly_chart.html'
pio.write_html(fig, html_file)

# Create a PyWebView window and display the HTML file
webview.create_window('Plotly Chart', html_file)
webview.start()
