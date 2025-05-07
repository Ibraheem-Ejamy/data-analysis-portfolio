from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio
pio.templates.default = "ggplot2"
import pandas as pd

df = pd.read_csv(r'C:\Users\ibrah\Downloads\workspace (4)\workspace\survey_data_cleaned.csv')
df["size_metric"] = df["size_metric"].clip(lower=0) * 3
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Expected Employee vs Revenue Growth'),
    html.P("Adjust figure width:", style={'fontSize': '30px'}),
    dcc.Slider(id='slider', min=800, max=2400, step=10, value=1200,
               marks={x: {'label': str(x), 'style': {'fontSize': '18px'}} for x in [800, 1200, 1600, 2000, 2400]},
               tooltip={"placement": "bottom", "always_visible": False}),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input('slider', 'value'))
def update_scatter(width):

    fig = px.scatter(df,
                     x="question_2_row_1_transformed",
                     y="question_2_row_2_transformed",
                     size="size_metric",
                     color="Growth_Firm",
                     size_max =100,
                     color_discrete_sequence=["#483D8B", "#ff7f0e", "#ffbb78"]
                     )
    fig.update_layout(
        height=800,
        width=int(width),
        margin=dict(l=20, r=20, t=40, b=40),
        paper_bgcolor="LightSteelBlue",
        font=dict(
            size=18,  # 👈 Change this value for larger or smaller fonts
            color="black",  # Optional: change font color
            family="Nunito"  # Optional: change font family
        )
    )
    fig.update_layout(width=int(width))
    return fig

app.run(debug=True)