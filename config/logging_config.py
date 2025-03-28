import logging


class LoggingConfig:
    def __init__(self):
        self.level = logging.DEBUG
        self.format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.max_bytes = 5 * 1024 * 1024  # 5MB
        self.backup_count = 5
        self.log_file = "app.log"  # ログファイル名

    def setting_log(self, log_file_path=None):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # 既存のハンドラをクリア
        if logger.hasHandlers():
            logger.handlers.clear()

        # ログハンドラをファイルに出力する場合
        if log_file_path:
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

    def clear_logging(self):
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
            handler.close()
            handler.close()
