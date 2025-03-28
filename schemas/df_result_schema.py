import pandas as pd
from pydantic import BaseModel


class DfResultSchema(BaseModel):
    simout_file: str = "simout_file"
    experiment_condition: str = "experiment_condition"
    experiment_type: str = "experiment_type"
    average_velocity: str = "average_velocity"
    total_mileage: str = "total_mileage"
    Brake_Out_sum: str = "Brake_Out_sum"
    Gas_Out_sum: str = "Gas_Out_sum"

    experiment_number: str = "experiment_number"
    subject_id: str = "subject_id"
    experiment_date: str = "experiment_date"

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
