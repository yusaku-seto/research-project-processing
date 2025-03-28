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

# # アノテーション項目の選択
# with st.expander("アノテーション設定"):
#     annotation_options = config.experiment.simout_columns_jp.values()
#     annotations: list[str] = st.multiselect(
#         label="アノテーション項目を選択してください",
#         options=annotation_options,
#         default=[],
#     )

x_column = options_dict[x]
fig = px.scatter()

for y_value in y:
    y_column = options_dict[y_value]
    fig.add_scatter(
        x=df_plot[x_column], y=df_plot[y_column], mode="markers", name=y_value
    )
# st.write(config.experiment.simout_columns.items())
# # アノテーション追加
# for annotation_column_jp in annotations:
#     annotation_column_en = [
#         k
#         for k, v in config.experiment.simout_columns_jp.items()
#         if v == annotation_column_jp
#     ][0]
#     annotation_column = config.experiment.simout_columns[annotation_column_en]
#     for i in range(len(df_plot)):
#         fig.add_annotation(
#             x=df_plot[x_column][i],
#             y=df_plot[y_column][0],  # 最初のy軸の値を使用
#             text=f"{annotation_column_jp}: {df_plot[annotation_column][i]}",
#             showarrow=True,
#             arrowhead=1,
#         )

st.plotly_chart(fig)
st.write(f"60km/h: {60/3.6:.2f}m/s")
st.write(f"50km/h: {50/3.6:.2f}m/s")
st.write(f"40km/h: {40/3.6:.2f}m/s")
