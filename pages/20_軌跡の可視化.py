import datetime
import re

import pandas as pd
import streamlit as st

from config import Config
from src.experiment_processor import ExperimentProcessor
from src.metric_calculator import MetricCalculator
from src.plots.plot_trajectory import plot_trajectory

config = Config()


# simoutのファイルを格納するフォルダ名を取得
simout_list = config.paths.file_manager.get_simout_file_names()
simout_list = [file for file in simout_list if ".csv" in file]

with st.sidebar:
    to_log_file = st.radio(
        label="ログファイルを出力しますか",
        options=("はい", "いいえ"),
        index=1,
        horizontal=True,
    )

    fileplot = st.radio(
        label="可視化するファイルを選択してください",
        options=simout_list,
        index=0,
        horizontal=True,
    )
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file_name = f"{current_time}_{fileplot}.txt"
    log_file_path = (
        config.paths.file_manager.get_log_path(log_file_name)
        if to_log_file is "はい"
        else None
    )
    logger = config.logging.setting_log(log_file_path)

    filename_info = fileplot.split("_")

    experiment_condition_from_filename = filename_info[3]
    experiment_type_from_filename = filename_info[2]
    experiment_type_from_filename = (
        "60" if experiment_type_from_filename == "70" else experiment_type_from_filename
    )

    experiment_condition_options = ["A", "B"]
    experiment_type_options = ("60", "50", "40")
    experiment_condition = st.radio(
        label="実験条件（コース）を選択してください",
        options=experiment_condition_options,
        index=experiment_condition_options.index(experiment_condition_from_filename),
        horizontal=True,
    )
    experiment_type = st.radio(
        label="実験条件（タイプ）を選択してください",
        options=experiment_type_options,
        index=experiment_type_options.index(experiment_type_from_filename),
        horizontal=True,
    )

    st.title("軌跡を可視化します")

    st.text(f"道路のタイプは{experiment_condition}です")

metric_calculator = MetricCalculator(config, logger)
experiment_processor = ExperimentProcessor(
    config=config,
    metric_calculator=metric_calculator,
    file_name=fileplot,
    experiment_type=experiment_type,
    experiment_condition=experiment_condition,
    logger=logger,
)
experiment_processor._add_ego_edge_coordinates(experiment_processor.df)
fig = plot_trajectory(df=experiment_processor.df)
st.plotly_chart(fig)
