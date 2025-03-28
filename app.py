import datetime
import logging
import re

import pandas as pd
import plotly.express as px
import streamlit as st

from config import Config
from src.metric_calculator import MetricCalculator
from src.subject_processor import SubjectProcessor


def setting_log(config: Config, log_file_name=None, to_file=True):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 既存のハンドラをクリア
    if logger.hasHandlers():
        logger.handlers.clear()

    # ログハンドラをファイルに出力する場合
    if to_file:
        # 現在の時刻を取得し、ファイル名に使用
        if not log_file_name:
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file_name = f"{current_time}.txt"

        log_file_path = config.paths.get_log_path(log_file_name)

        # ログハンドラを作成し、UTF-8 エンコーディングを指定
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
        file_handler.setFormatter(formatter)

        # ロガーにハンドラを追加
        logger.addHandler(file_handler)

    # コンソールに出力するハンドラを常に追加
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


config = Config()

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f"{current_time}.txt"
log_file_path = config.paths.file_manager.get_log_path(log_file_name)

logger = config.logging.setting_log(log_file_path)
print(f"Base directory: {config.paths.folder_path_model.base_dir}")

# Title of the app
st.title("MASTERファイルを生成します")

need_master_file = st.radio(
    label="masterファイルを出力しますか",
    options=("Yes", "No"),
    index=0,
    horizontal=True,
)

experiment_condition = st.radio(
    label="道路のタイプを選択してください",
    options=("A", "B"),
    index=0,
    horizontal=True,
)

subject_id = st.text_input("被験者IDを入力してください")
date = st.text_input("日付を入力してください")

st.text(f"道路のタイプは{experiment_condition}です")

# simoutのファイルを格納するフォルダ名を取得
# date_list = config.get_simout_file_names("")
# # 8桁の数字のみを残す
# date_list = [item for item in date_list if re.fullmatch(r"\d{8}", item)]
# # simoutのファイルを格納するフォルダ名の一覧を選択肢として与える
# simout_date = st.radio(
#     label="simoutのフォルダ名（YYYYMMDD）を選択してください",
#     options=date_list,
#     index=0,
#     horizontal=True,
# )

# フォルダ名選択後に、フォルダ内のファイル名を選択肢として与える
# if simout_date:
simout_list = config.paths.file_manager.get_simout_file_names()
file60 = st.radio(
    label="60km/hのファイルを選択してください",
    options=simout_list,
    index=0,
    horizontal=True,
)
file50 = st.radio(
    label="50km/hのファイルを選択してください",
    options=simout_list,
    index=0,
    horizontal=True,
)
file40 = st.radio(
    label="40km/hのファイルを選択してください",
    options=simout_list,
    index=0,
    horizontal=True,
)


files = {
    "file60": file60,
    "file50": file50,
    "file40": file40,
}

experiment_numbers = [40, 50, 60]
experiment_1 = st.radio(
    label="1番目の実験条件を選択してください",
    options=experiment_numbers,
    index=0,
    horizontal=False,
)
experiment_2 = st.radio(
    label="2番目の実験条件を選択してください",
    options=experiment_numbers,
    index=1,
    horizontal=False,
)
experiment_3 = st.radio(
    label="3番目の実験条件を選択してください",
    options=experiment_numbers,
    index=2,
    horizontal=False,
)

experiments = {
    "experiment_1": experiment_1,
    "experiment_2": experiment_2,
    "experiment_3": experiment_3,
}


# 重複チェック
if len(set(files.values())) < len(files):
    st.error(
        "エラー: 複数の速度で同じファイルが選択されています。別のファイルを選んでください。"
    )

if len(set(experiments.values())) < len(experiments):
    st.error("エラー: 実験順が重複しています。")

if not subject_id:
    st.error("エラー: 被験者IDを入力してください。")

# st.write(master_file)

if simout_list:
    fileplot: str = st.radio(
        label="可視化するファイルを選択してください",
        options=simout_list,
        index=0,
        horizontal=True,
    )
    df_plot = pd.read_csv(config.paths.file_manager.get_simout_path(fileplot))
    x: str = st.radio(
        label="xを選択してください",
        options=df_plot.columns,
        index=0,
        horizontal=True,
    )
    y: str = st.radio(
        label="yを選択してください",
        options=df_plot.columns,
        index=0,
        horizontal=True,
    )
    if st.button("生データを可視化する"):
        fig = px.scatter(df_plot, x=x, y=y)
        st.plotly_chart(fig)

subject_results_str = f"{date}_{subject_id}.xlsx"

# 初期化
if "subject_results_new" not in st.session_state:
    st.session_state.subject_results_new = None
if st.button("MASTERファイルを作成する") and need_master_file:
    st.session_state.subject_results_new = subject_results_str
    st.session_state.experiment_condition = experiment_condition
    subject = {
        "subject_id": subject_id,
        "experiment_date": date,
        "file_name_60": file60,
        "file_name_50": file50,
        "file_name_40": file40,
        "experiment_1": experiment_1,
        "experiment_2": experiment_2,
        "experiment_3": experiment_3,
        "experiment_condition": experiment_condition,
    }
    subject_processor = SubjectProcessor(subject, config, logger)
    df_index_subject = subject_processor.process()
    subject_processor.save_metrics(df_index_subject)
    st.write("ファイルを出力しました")


if st.button("subject_resultsフォルダ内のMASTERファイルを結合する"):
    # simoutのファイルを格納するフォルダ名を取得
    index_files = config.paths.file_manager.get_subject_results_file_names()
    # 8桁の数字のみを残す
    index_files = [item for item in index_files if ".xlsx" in item]
    st.write(index_files)
    df_all = None
    for index_file in index_files:
        index_file_path = config.paths.file_manager.get_subject_results_path(index_file)
        df = pd.read_excel(index_file_path)
        if df_all is not None:
            df_all = pd.concat([df_all, df], axis=0, ignore_index=True)
        else:
            df_all = df
    df_all.to_csv(config.paths.file_manager.all_subjects_results, index=False)
    st.write("all_subjects_resultsファイルを出力しました")

# for uploaded_file in uploaded_files:
#     st.write(uploaded_file.name)
# # Load and display data
# df = pd.read_csv(
#     config.get_simout_path("output_20240719_180031.csv")
# )  # Replace with your actual file
# st.write("Data Preview:", df.head())

# # Create a simple plot
# st.line_chart(df)
