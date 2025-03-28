import logging

import numpy as np
import pandas as pd

from config import Config
from schemas.df_processed_schema import DfProcessedSchema
from schemas.df_result_schema import DfResultSchema
from schemas.df_simout_schema import DfSimoutSchema
from src.metric_calculator import MetricCalculator


class ExperimentProcessor:
    """
    各実験のデータ処理を行う。
    Attributes:
        config (Config): 設定オブジェクト
        metric_calculator (MetricCalculator): 指標計算
        file_name (str): 実験データのファイル名
        experiment_type (str): 実験条件（タイプ）
        experiment_condition (str): 実験条件（コース）
        logger (logging.Logge): ロガー
    """

    def __init__(
        self,
        config: Config,
        metric_calculator: MetricCalculator,
        file_name: str,
        experiment_type: str,
        experiment_condition: str,
        logger: logging.Logger,
    ):
        self.config: Config = config
        self.df_processed_columns = DfProcessedSchema()
        self.df_result_columns = DfResultSchema()
        self.df_simout_columns = DfSimoutSchema()
        self.metric_calculator: MetricCalculator = metric_calculator
        self.logger: logging.Logger = logger

        self.file_name: str = file_name
        self.experiment_type: str = experiment_type
        self.experiment_condition: str = experiment_condition
        df = pd.read_csv(
            self.config.paths.file_manager.get_simout_path(file_name=file_name)
        )
        self.df = self._add_ego_edge_coordinates(df)

        self.dt = (
            self.df[self.df_simout_columns.time].iloc[1]
            - self.df[self.df_simout_columns.time].iloc[0]
        )

    def process(self) -> pd.DataFrame:
        """
        核実験で様々な指標を計算(今回は単純に平均速度、総走行距離、ペダル量積分値にする)

        Returns:
            df_index_experiment (pd.DataFrame): 実験の結果
        """
        dt = self.dt
        df = self.df

        average_velocity = self.metric_calculator.calculate_average_velocity(df=df)
        total_mileage = self.metric_calculator.calculate_total_mileage(dt=dt, df=df)
        index_dict = {
            self.df_result_columns.simout_file: self.file_name,
            self.df_result_columns.experiment_condition: self.experiment_condition,
            self.df_result_columns.average_velocity: average_velocity,
            self.df_result_columns.total_mileage: total_mileage,
        }

        brake_and_gas_dict = self.metric_calculator.sum_brake_and_gas(dt=dt, df=df)
        index_dict = dict(**index_dict, **brake_and_gas_dict)

        df_index_experiment = pd.DataFrame({k: [v] for k, v in index_dict.items()})
        return df_index_experiment

    def _add_ego_edge_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        dfに自車直進車両左前端の座標の列を追加

        Args:
            df (pd.Dataframe): 生データ

        Returns:
            df (pd.Dataframe): 新しい座標の列が追加されたdf
        """

        # 自車直進車両左前端の座標
        Ego_front_left_x = (
            df[self.df_simout_columns.ego_x]
            + (self.config.experiment.Ego_l - self.config.experiment.PoI_y)
            * np.cos(df[self.df_simout_columns.psi])
            - self.config.experiment.Ego_w / 2 * np.sin(df[self.df_simout_columns.psi])
        )
        Ego_front_left_y = (
            df[self.df_simout_columns.ego_y]
            + (self.config.experiment.Ego_l - self.config.experiment.PoI_y)
            * np.sin(df[self.df_simout_columns.psi])
            + self.config.experiment.Ego_w / 2 * np.cos(df[self.df_simout_columns.psi])
        )

        df[self.df_processed_columns.Ego_front_left_x] = Ego_front_left_x
        df[self.df_processed_columns.Ego_front_left_y] = Ego_front_left_y

        return df
