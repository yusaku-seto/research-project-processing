import datetime
import logging
import os
import warnings

from config import Config
from src.data_manager import DataManager

# warnings.simplefilter("ignore")


def setting_log(config: Config, log_file_name=None):
    if not log_file_name:
        # 現在の時刻を取得し、ファイル名に使用
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"{current_time}.txt"
    log_file_path = config.paths.get_log_path(log_file_name)
    # ログの設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 既存のハンドラをクリア
    if logger.hasHandlers():
        logger.handlers.clear()

    # ログハンドラを作成し、UTF-8 エンコーディングを指定
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
    file_handler.setFormatter(formatter)

    # ロガーにハンドラを追加
    logger.addHandler(file_handler)
    return logger


def main():
    config = Config()
    config.paths.file_manager.print_base_dir()

    os.makedirs(config.paths.folder_path_model.path_folder_output, exist_ok=True)

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"{current_time}.txt"
    log_file_path = config.paths.file_manager.get_log_path(log_file_name)
    logger = config.logging.setting_log(log_file_path)

    # データマネージャの初期化
    data_manager = DataManager(config, logger=logger)

    # データの読み込み
    subjects_data = data_manager.load_data()

    # 全データの処理
    df = data_manager.process_all(subjects_data)

    # 指標の保存
    data_manager.save_metrics(df)

    config.logging.clear_logging()
    return df


if __name__ == "__main__":
    main()
