import pandas as pd
import plotly.express as px
import streamlit as st

from config import Config
from schemas.df_simout_schema import DfSimoutSchema

config = Config()

simout_list = config.paths.file_manager.get_simout_file_names()
simout_list = [file for file in simout_list if ".csv" in file]

df_simout_columns = DfSimoutSchema()


with st.expander("ファイルを選択"):
    fileplot: str = st.radio(
        label="可視化するファイルを選択してください",
        options=simout_list,
        index=0,
        horizontal=True,
    )

df_plot = pd.read_csv(config.paths.file_manager.get_simout_path(fileplot))

options_dict = df_simout_columns.get_column_map()
options = list(options_dict.keys())
x: str = st.radio(
    label="xを選択してください",
    options=options,
    index=0,
    horizontal=True,
)
y: list[str] = st.multiselect(
    label="yを選択してください", options=options, default=options[2]
)

x_column = options_dict[x]
fig = px.scatter()

for y_value in y:
    y_column = options_dict[y_value]
    fig.add_scatter(
        x=df_plot[x_column], y=df_plot[y_column], mode="markers", name=y_value
    )

st.plotly_chart(fig)
