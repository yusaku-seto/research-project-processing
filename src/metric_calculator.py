import logging

import pandas as pd

from config import Config
from schemas.df_processed_schema import DfProcessedSchema
from schemas.df_result_schema import DfResultSchema
from schemas.df_simout_schema import DfSimoutSchema


class MetricCalculator:
    """
    指標の計算を行う。
    """

    def __init__(self, config: Config, logger: logging.Logger):
        """
        指標計算クラス
        Args:
            config (Config): 諸設定
            logger (logging.Logger): logger
        """

        self.config = config
        self.logger = logger

        self.df_processed_columns = DfProcessedSchema()
        self.df_result_columns = DfResultSchema()
        self.df_simout_columns = DfSimoutSchema()

    def filtering_df_time(
        self, df: pd.DataFrame, start_time: float, end_time: float
    ) -> pd.DataFrame:
        """
        dfの時刻を抽出

        Parameters:
            start_time (float): dfの最初の行の時刻
            end_time (float): dfの最後の行の時刻
        Returns:
            filtered_df (pd.Dataframe): 時刻抽出されたdf
        """
        filtered_df = df[df[self.df_simout_columns.time] >= start_time]
        filtered_df = filtered_df[filtered_df[self.df_simout_columns.time] <= end_time]

        return filtered_df

    def calculate_average_velocity(self, df: pd.DataFrame) -> float:
        """
        平均速度を計算

        Attributes (Input)
        ------------------
        df (pd.Dataframe): simulinkから取得したcsvファイルのdf

        Attributes (Output)
        -------------------
        Average_velocity (float): 平均速度
        """
        average_velocity = df[self.df_simout_columns.ego_v].mean()
        return average_velocity

    def add_mileage_column(self, dt: float, df: pd.DataFrame) -> pd.DataFrame:
        """
        走行距離列を追加

        Attributes (Input)
        ------------------
        df (pd.Dataframe): simulinkから取得したcsvファイルのdf

        Attributes (Output)
        -------------------
        Average_velocity (float): 平均速度
        """
        # 速度のステップ積分値
        df[self.df_processed_columns.Velocity_times_dt] = abs(
            df[self.df_simout_columns.ego_v] * dt
        )
        return df

    def calculate_total_mileage(self, dt: float, df: pd.DataFrame) -> float:
        """
        走行距離を計算

        Attributes (Input)
        ------------------
        df (pd.Dataframe): simulinkから取得したcsvファイルのdf

        Attributes (Output)
        -------------------
        Average_velocity (float): 平均速度
        """
        # 速度のステップ積分値
        df = self.add_mileage_column(dt=dt, df=df)
        total_mileage = df[self.df_processed_columns.Velocity_times_dt].sum()
        return total_mileage

    def sum_brake_and_gas(self, dt: float, df: pd.DataFrame) -> dict:
        """
        ブレーキ、アクセル踏み込み量の積分を計算

        Attributes (Input)
        ------------------
        df (pd.Dataframe): simulinkから取得したcsvファイルのdf

        Attributes (Output)
        -------------------
        self.Brake_Out_sum (float): シミュレーション全期間のブレーキ量の積分
        self.Gas_Out_sum (float): シミュレーション全期間のアクセル量の積分
        """
        # ペダル量のステップ積分値
        df[self.df_processed_columns.Brake_Out_times_dt] = (
            df[self.df_simout_columns.Brake_Out] * dt
        )
        df[self.df_processed_columns.Gas_Out_times_dt] = (
            df[self.df_simout_columns.Gas_Out] * dt
        )

        # 積分値を合計
        Brake_Out_sum = df[self.df_processed_columns.Brake_Out_times_dt].sum()
        Gas_Out_sum = df[self.df_processed_columns.Gas_Out_times_dt].sum()

        brake_and_gas_dict = {
            self.df_result_columns.Brake_Out_sum: Brake_Out_sum,
            self.df_result_columns.Gas_Out_sum: Gas_Out_sum,
        }

        return brake_and_gas_dict
        return brake_and_gas_dict
