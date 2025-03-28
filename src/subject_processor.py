import logging

import numpy as np
import pandas as pd

from config import Config
from schemas.df_result_schema import DfResultSchema
from schemas.df_subject_master import DfSubjectMasterSchema
from src.experiment_processor import ExperimentProcessor
from src.metric_calculator import MetricCalculator


class SubjectProcessor:
    """
    被験者ごとの全実験（3回）のデータ処理を行う。
    Attributes:
        subject_info (dict): 被験者情報
        config (Config): 設定オブジェクト
        logger (logging.Logge): ロガー
    """

    def __init__(self, subject_info: dict, config: Config, logger: logging.Logger):
        self.df_result_columns = DfResultSchema()
        self.df_subject_master = DfSubjectMasterSchema()

        self.subject_id: str = subject_info.get(
            self.df_subject_master.subject_id, "None"
        )
        self.subject_name: str = subject_info.get(
            self.df_subject_master.subject_name, "None"
        )
        self.experiment_date: str = subject_info.get(
            self.df_subject_master.experiment_date, "None"
        )
        self.file_name_60: str = subject_info.get(
            self.df_subject_master.file_name_60, "None"
        )
        self.file_name_50: str = subject_info.get(
            self.df_subject_master.file_name_50, "None"
        )
        self.file_name_40: str = subject_info.get(
            self.df_subject_master.file_name_40, "None"
        )
        self.experiment_1: str = subject_info.get(
            self.df_subject_master.experiment_1, "None"
        )
        self.experiment_2: str = subject_info.get(
            self.df_subject_master.experiment_2, "None"
        )
        self.experiment_3: str = subject_info.get(
            self.df_subject_master.experiment_3, "None"
        )
        self.experiment_condition: str = subject_info.get(
            self.df_subject_master.experiment_condition, "None"
        )
        self.experiments = {
            1: self.experiment_1,
            2: self.experiment_2,
            3: self.experiment_3,
        }
        self.experiments = {
            key: value
            for key, value in self.experiments.items()
            if not (value == "None" or pd.isnull(value))
        }

        subject_info_dict = {
            self.df_subject_master.subject_id: self.subject_id,
            self.df_subject_master.file_name_60: self.file_name_60,
            self.df_subject_master.file_name_50: self.file_name_50,
            self.df_subject_master.file_name_40: self.file_name_40,
            self.df_subject_master.experiment_condition: self.experiment_condition,
        }
        for var_name, value in subject_info_dict.items():
            if value == "None" or pd.isnull(value):
                logging.warning(f"{var_name} が欠損しています。")

        self.config: Config = config
        self.logger = logger

        self.metric_calculator = MetricCalculator(config, logger)

        self.experiment_processors = [
            ExperimentProcessor(
                config=config,
                metric_calculator=self.metric_calculator,
                file_name=self.file_name_60,
                experiment_type=experiment,
                experiment_condition=self.experiment_condition,
                logger=self.logger,
            )
            for experiment in self.experiments.values()
        ]

    # 特定の値からexperiment番号を取得する関数
    def get_experiment_number(self, value):
        for key, val in self.experiments.items():
            if int(val) == int(value):
                return key
        return None

    def process(self) -> pd.DataFrame:
        """
        被験者の全実験（3回）のデータ処理を行う。

        Returns:
            df_index_subject (pd.DataFrame): 被験者の全実験（3回）の結果
        """
        try:
            self.logger.debug(f"被験者 '{self.subject_id}' のデータ処理を開始します")
            df_index_subject = None
            for processor in self.experiment_processors:
                df_index_experiment = processor.process()
                df_index_experiment[self.df_result_columns.experiment_number] = (
                    self.get_experiment_number(processor.experiment_type)
                )
                self.logger.debug(
                    f"被験者 '{self.subject_id}' の {processor.experiment_type} のデータ処理が完了しました"
                )
                if df_index_subject is not None:
                    df_index_subject = pd.concat(
                        [df_index_subject, df_index_experiment], ignore_index=True
                    )
                else:
                    df_index_subject = df_index_experiment
            df_index_subject[self.df_result_columns.subject_id] = self.subject_id
            df_index_subject[self.df_result_columns.experiment_date] = (
                self.experiment_date
            )
            self.logger.debug(f"被験者 '{self.subject_id}' のデータ処理が完了しました")
            return df_index_subject
        except Exception as e:
            self.logger.exception(
                f"被験者 '{self.subject_id}' のデータ処理中にエラーが発生しました"
            )
            raise

    def save_metrics(self, df: pd.DataFrame):
        """
        被験者の指標データをcsv出力。

        Args:
            df (pd.DataFrame): 全被験者の結果
        """
        try:
            self.logger.debug("指標データを保存します")
            file_name = f"{str(int(self.experiment_date))}_{self.subject_id :02}.csv"
            df.to_csv(
                self.config.paths.file_manager.get_subject_results_path(file_name),
                index=False,
            )
            self.logger.debug("指標データの保存が完了しました")
        except Exception as e:
            self.logger.exception(f"指標データの保存中にエラーが発生しました: {e}")
            raise
            raise
