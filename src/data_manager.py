import logging

import pandas as pd

from config import Config
from src.master_data_manager import MasterDataManager
from src.subject_processor import SubjectProcessor


class DataManager:
    """
    全被験者のデータを管理し、最終的なCSV出力を行う
    Attributes:
        config (Config): 設定オブジェクト
        logger (logging.Logge): ロガー
    """

    def __init__(self, config: Config, logger: logging.Logger):
        self.config: Config = config
        self.logger: logging.Logger = logger
        master_file_path: str = self.config.paths.file_path_model.subjects_master
        self.master_data_manager: MasterDataManager = MasterDataManager(
            master_file_path, logger
        )
        self.subject_processors: list[SubjectProcessor] = []

    def load_data(self) -> list[dict]:
        """
        マスターファイルを基に被験者ごとのデータを読み込み、リストとして返す。

        Returns:
            subjects (list[dict]): 被験者情報リスト
        """
        try:
            self.logger.debug("マスターデータから被験者情報を取得します")
            subjects = self.master_data_manager.get_subjects()
            self.logger.debug(f"{len(subjects)} 件の被験者データを処理します")
            return subjects
        except Exception:
            self.logger.exception("マスターデータの読み込み中にエラーが発生しました")
            raise

    def process_all(self, subjects_data: list[dict]) -> pd.DataFrame:
        """
        全被験者のデータ処理を行う。

        Args:
            subjects (list[dict]): 被験者情報リスト
        Returns:
            df_index_all_subjects (pd.DataFrame): 全被験者の結果
        """
        df_index_all_subjects = None
        try:
            self.logger.debug("全被験者のデータ処理を開始します")
            for subject in subjects_data:
                subject_id = subject.get("subject_id")
                if not subject_id:
                    self.logger.warning("被験者IDが存在しないレコードをスキップします")
                    continue
                subject_processor = SubjectProcessor(
                    subject_info=subject, config=self.config, logger=self.logger
                )
                df_index_subject = subject_processor.process()
                subject_processor.save_metrics(df_index_subject)
                self.subject_processors.append(subject_processor)
                if df_index_all_subjects is not None:
                    df_index_all_subjects = pd.concat(
                        [df_index_all_subjects, df_index_subject], ignore_index=True
                    )
                else:
                    df_index_all_subjects = df_index_subject
                self.logger.debug(f"被験者 '{subject_id}' の指標を追加しました")
            self.logger.debug("全被験者のデータ処理が完了しました")
            self.df_index_all_subjects = df_index_all_subjects
            return df_index_all_subjects
        except Exception as e:
            self.logger.exception("全被験者のデータ処理中にエラーが発生しました")
            raise

    def save_metrics(self, df: pd.DataFrame):
        """
        全被験者の指標データをcsv出力。

        Args:
            df (pd.DataFrame): 全被験者の結果
        """
        try:
            self.logger.debug("指標データを保存します")
            df.to_csv(
                self.config.paths.file_path_model.all_subjects_results, index=False
            )
            self.logger.debug("指標データの保存が完了しました")
        except Exception as e:
            self.logger.exception(f"指標データの保存中にエラーが発生しました: {e}")
            raise

    # def get_output_path(self, file_name: str) -> str:
    #     """
    #     指定されたファイル名に対応する出力ファイルのパスを生成する。
    #     """
    #     return self.path_manager.get_output_path(file_name)
