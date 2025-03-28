import datetime
import os
import warnings

import pandas as pd
import streamlit as st

from config import Config
from src.plots.plot_t_v_a_gas_distance import plot_t_v_a_gas_distance_individual
from src.subject_manager import SubjectManager

warnings.simplefilter("ignore")

config = Config()

simout_list = config.paths.file_manager.get_simout_file_names()
simout_list = [file for file in simout_list if ".csv" in file]

all_subject_results_path = config.paths.file_path_model.all_subjects_results
if os.path.exists(all_subject_results_path):
    df_all_subject_results = pd.read_csv(all_subject_results_path)
else:
    st.error(f"error：処理済ファイル '{all_subject_results_path}' は存在しません。")
    st.stop()

with st.sidebar:
    to_log_file = st.radio(
        label="ログファイルを出力しますか",
        options=("はい", "いいえ"),
        index=1,
        horizontal=True,
    )
    ids_options = list(range(1, 11))
    ids = st.multiselect(
        label="IDを選択してください", options=ids_options, default=ids_options
    )
subject_managers = {}
for id in ids:
    st.write(f"{id}")
    subject_i = SubjectManager(id, simout_list)
    subject_i.load_raw_data(config=config)
    subject_managers[id] = subject_i
    fig = plot_t_v_a_gas_distance_individual(
        config,
        subject_i.df_dict,
        id,
        subject_i.experiment_type,
        df_all_subject_results=df_all_subject_results,
    )
    st.pyplot(fig)

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

log_file_name = f"{current_time}_raw_multi_plot.txt"
log_file_path = (
    config.paths.get_log_path(log_file_name) if to_log_file == "はい" else None
)

logger = config.logging.setting_log(log_file_path)
