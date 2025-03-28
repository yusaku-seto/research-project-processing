from itertools import product

import numpy as np
import plotly.graph_objects as go

from schemas.df_processed_schema import DfProcessedSchema

df_processed_columns = DfProcessedSchema()


# 最短距離を計算する関数
def plot_trajectory(
    df,
    ego_x_column=df_processed_columns.Ego_front_left_x,
    ego_y_column=df_processed_columns.Ego_front_left_y,
):
    """
    軌跡を可視化
    Parameters:
    df (df): df

    Returns:
    fig
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[ego_x_column],
            y=df[ego_y_column],
            mode="markers",
            name="Ego",
            marker=dict(color="blue"),
        )
    )

    # タイトルとラベルを設定
    fig.update_layout(title="走行軌跡", xaxis_title="X", yaxis_title="Y")
    return fig
