import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df=pd.read_csv('D:/mariam main/GUC/project/final project/Nike_Sales_Cleaned.csv')


# KPI Cards
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_units = df["Units_Sold"].sum()

df['years']=pd.to_datetime (df['Order_Date']).dt.year
df['month']=pd.to_datetime (df['Order_Date']).dt.month


# best oroduct ineach region 

best_products = (
    df.groupby(["Region", "Product_Name"])["Revenue"].sum().reset_index()
)

best_products = best_products.loc[
    best_products.groupby("Region")["Revenue"].idxmax()
]


# discount inoact on the revenu 
discount_impact = (
    df.groupby("Discount_Applied")["Revenue"].mean().reset_index()
)


# profit  with product line  
profit_line = (
    df.groupby("Product_Line")["Profit"].sum().reset_index()
)

# most popular shoe size
shoe = (
    df.groupby("Shoe_Size")["Units_Sold"].sum().reset_index()
)

# most popular clothing size 
clothes = (
    df.groupby("clothing_sizes")["Units_Sold"].sum().reset_index()
)

# graohs for discount and best product in each region 

fig_best = px.bar(
    best_products,
    x="Region",
    y="Revenue",
    color="Product_Name",
    text="Product_Name",
    title="Best Product in Every Region",
    template="plotly_dark"
)

fig_discount = px.bar(
    discount_impact,
    x="Discount_Applied",
    y="Revenue",
    color="Revenue",
    title="Average Revenue by Discount",
    template="plotly_dark"
)
# graph for profit and product line 
fig_profit_line = px.bar(
    profit_line,
    x="Profit",
    y="Product_Line",
    orientation="h",
    color="Profit",
    color_continuous_scale="Viridis",
    title="Profit by Product Line",
    template="plotly_dark"
)

fig_profit_line.update_layout(title_x=0.5)

#most popular shoe line 

fig_shoe = px.bar(
    shoe,
    x="Shoe_Size",
    y="Units_Sold",
    color="Units_Sold",
    color_continuous_scale="Blues",
    title="Most Popular Shoe Size",
    template="plotly_dark"
)

fig_shoe.update_layout(title_x=0.5)


# most popular cloth size 
fig_clothes = px.pie(
    clothes,
    names="clothing_sizes",
    values="Units_Sold",
    title="Clothing Size Distribution",
    template="plotly_dark"
)


app = Dash(__name__)

app.layout = html.Div(

    [

        html.H1(
            "Nike Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "white",
                "fontSize": "40px",
                "marginBottom": "30px"
            }
        ),


# coomon questions
        html.Div([

        html.Div([

                html.H3(
                    "💰 Total Revenue",
                    style={"color":"white"}
                ),

                html.H2(
                    f"${total_revenue:,.0f}",
                    style={"color":"#00FF7F"}
                )

            ],

            style={
                "backgroundColor":"#1E1E1E",
                "padding":"20px",
                "borderRadius":"12px",
                "width":"30%",
                "textAlign":"center",
                "boxShadow":"0px 0px 10px gray"
            }

        ),

        html.Div([
                html.H3(
                    "📈 Total Profit",
                    style={"color":"white"}
                ),

                html.H2(
                    f"${total_profit:,.0f}",
                    style={"color":"#00BFFF"}
                )
            ],

            style={
                "backgroundColor":"#1E1E1E",
                "padding":"20px",
                "borderRadius":"12px",
                "width":"30%",
                "textAlign":"center",
                "boxShadow":"0px 0px 10px gray"
            }

        ),

        html.Div([
                html.H3(
                    "👟 Units Sold",
                    style={"color":"white"}
                ),

                html.H2(
                    f"{total_units:,}",
                    style={"color":"#FFA500"}
                )
            ],

            style={
                "backgroundColor":"#1E1E1E",
                "padding":"20px",
                "borderRadius":"12px",
                "width":"30%",
                "textAlign":"center",
                "boxShadow":"0px 0px 10px gray"
            }
            )
    ],

    style={
        "display":"flex",
        "justifyContent":"space-between",
        "marginBottom":"30px"
    }

),


# DROP DOWN
        html.Div(

            [

                # Compare By
                html.Div([

                    html.Label(
                        "Compare By",
                        style={
                            "color":"white",
                            "fontWeight":"bold",
                            "marginBottom":"8px"
                        }
                    ),

                    dcc.Dropdown(

                        id="compare",

                        options=[
                            {"label":"Region","value":"Region"},
                            {"label":"Gender","value":"Gender_Category"},
                            {"label":"Product Name","value":"Product_Name"},
                            {"label":"Product Line","value":"Product_Line"},
                            {"label":"Sales Channel","value":"Sales_Channel"},
                            {"label":"Year","value":"years"},
                            {"label":"Month","value":"month"},
                        ],

                        value="Region",

                        clearable=False

                    )

                ], style={"width":"32%"}),

                # Metric
                html.Div([

                    html.Label(
                        "Metric",
                        style={
                            "color":"white",
                            "fontWeight":"bold",
                            "marginBottom":"8px"
                        }
                    ),

                    dcc.Dropdown(

                        id="metric",

                        options=[
                            {"label":"Revenue","value":"Revenue"},
                            {"label":"Profit","value":"Profit"},
                            {"label":"Units Sold","value":"Units_Sold"}
                        ],

                        value="Revenue",

                        clearable=False

                    )

                ], style={"width":"32%"}),

                # Chart Type
                html.Div([

                    html.Label(
                        "Chart Type",
                        style={
                            "color":"white",
                            "fontWeight":"bold",
                            "marginBottom":"8px"
                        }
                    ),

                    dcc.Dropdown(

                        id="chart_type",

                        options=[
                            {"label":"Bar Chart","value":"bar"},
                            {"label":"Pie Chart","value":"pie"},
                            {"label":"Line Chart","value":"line"},
                            {"label":"Scatter Plot","value":"scatter"}
                        ],

                        value="bar",

                        clearable=False

                    )

                ], style={"width":"32%"})

            ],

            style={
                "display":"flex",
                "justifyContent":"space-between",
                "alignItems":"flex-start",
                "gap":"20px",
                "backgroundColor":"#1E1E1E",
                "padding":"20px",
                "borderRadius":"12px",
                "marginBottom":"25px"
            }

        ),

        dcc.Graph(
            id="compare_graph"
        ),


    # graphs for discount and best product in each region 

        html.Div(

            [

                dcc.Graph(
                    figure=fig_best,
                    style={"width":"49%"}
                ),

                dcc.Graph(
                    figure=fig_discount,
                    style={"width":"49%"}
                )

            ],
            style={
                "display":"flex",
                "justifyContent":"space-between",
                "justifyContent":"center",

            }

        ),

# profit&product line , most clothing size and shoe size sold


html.Div([
        dcc.Graph(
            figure=fig_profit_line,
            style={"width":"49%"}
        ),

        dcc.Graph(
            figure=fig_shoe,
            style={"width":"49%"}
        )

],

    style={
        "display":"flex",
        "justifyContent":"space-between",
        "justifyContent":"center",
        "marginTop":"20px"
    }

),


html.Div(
    [
        dcc.Graph(
            figure=fig_clothes,
            style={"width":"49%"}
        )
    ],

    style={
        "display":"flex",
        "justifyContent":"center",
        "marginTop":"20px"
    }
),

],


# full page style
    style={
        "backgroundColor":"#111111",
        "padding":"30px",
        "minHeight":"100vh"
    }  
)








@app.callback(
    Output("compare_graph","figure"),
    Input("compare","value"),
    Input("metric","value"),
    Input("chart_type", "value")
)

def update_graph(compare_by, metric , chart_type):

    data = (
        df.groupby(compare_by)[metric].sum().reset_index()
    )

    if chart_type=="bar":
        fig = px.bar(
            data,
            x=compare_by,
            y=metric,
            color=metric,
            color_continuous_scale="Blues",
            template="plotly_dark",
            title=f"{metric} by {compare_by}"
        )
    elif chart_type=="pie":
          fig = px.pie(
            data,
            names=compare_by,
            values=metric,
            template="plotly_dark"
        )
    elif chart_type == "line":
            fig = px.line(
            data,
            x=compare_by,
            y=metric,
            markers=True,
            template="plotly_dark"
        )
    elif chart_type == "scatter":
            fig = px.scatter(
            data,
            x=compare_by,
            y=metric,
            color=metric,
            template="plotly_dark"
        )

    return fig


# ==========================
# Run App
# ==========================

if __name__ == "__main__":
    app.run(debug=True)

