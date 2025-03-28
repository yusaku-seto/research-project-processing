from datetime import datetime
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel


class DfSubjectMasterSchema(BaseModel):
    index: str = "index"
    subject_id: str = "subject_id"
    subject_name: str = "subject_name"
    experiment_date: str = "experiment_date"
    file_name_60: str = "file_name_60"
    file_name_50: str = "file_name_50"
    file_name_40: str = "file_name_40"
    experiment_condition: str = "experiment_condition"
    experiment_1: str = "experiment_1"
    experiment_2: str = "experiment_2"
    experiment_3: str = "experiment_3"

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
