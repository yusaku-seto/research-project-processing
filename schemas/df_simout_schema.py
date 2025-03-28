from datetime import datetime
from typing import ClassVar

import pandas as pd
from pydantic import BaseModel


class DfSimoutSchema(BaseModel):
    time: str = "simout1"
    ego_a: str = "simout2"
    ego_v: str = "simout3"
    ego_x: str = "simout4"
    ego_y: str = "simout5"
    psi: str = "simout6"
    Gas_Out: str = "simout7"
    Brake_Out: str = "simout8"

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
