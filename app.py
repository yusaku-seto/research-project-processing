import datetime
import logging

import streamlit as st

from config import Config
from main import main


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

st.title("時系列データから要約ファイルを生成します")


# 初期化
if "subject_results_new" not in st.session_state:
    st.session_state.subject_results_new = None
if st.button("処理を実行する"):
    df = main()
    st.write("ファイルを出力しました")

    st.text("要約テーブル")
    st.dataframe(df)
