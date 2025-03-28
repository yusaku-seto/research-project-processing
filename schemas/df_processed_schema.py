import pandas as pd
from pydantic import BaseModel


class DfProcessedSchema(BaseModel):
    Ego_front_left_x: str = "Ego_front_left_x"
    Ego_front_left_y: str = "Ego_front_left_y"
    Velocity_times_dt: str = "Velocity_times_dt"
    Brake_Out_times_dt: str = "Brake_Out_times_dt"  # ブレーキ積分
    Gas_Out_times_dt: str = "Gas_Out_times_dt"  # アクセル積分

    @classmethod
    def get_column_map(cls) -> dict:
        """変数名 → 実際のカラム名 のマッピングを取得"""
        return cls().dict()

    @classmethod
    def rename_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """DataFrameの列名をスキーマに基づいてリネーム"""
        return df.rename(columns=cls.get_column_map())

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> bool:
        """DataFrame のカラム名がスキーマと一致しているかチェック"""
        expected_columns = set(cls.get_column_map().values())  # 実際のカラム名
        return set(df.columns) == expected_columns
