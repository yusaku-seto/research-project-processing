import logging
from typing import Dict, List

import pandas as pd


class MasterDataManager:
    """
    マスターファイルを管理し、被験者ごとの情報を提供するクラス。
    """

    def __init__(self, master_file_path: str, logger: logging.Logger):
        self.master_file_path = master_file_path
        self.logger = logger
        self.data = self.load_master_file()

    def load_master_file(self) -> pd.DataFrame:
        """
        マスターファイルを読み込み、DataFrameとして保持する。
        """
        try:
            self.logger.debug(
                f"マスターファイル '{self.master_file_path}' を読み込みます"
            )
            df = pd.read_excel(self.master_file_path)
            # df = pd.read_csv(self.master_file_path, encoding="cp932")
            df = df[df["file_name_60"].notna()]
            self.logger.debug("マスターファイルの読み込みが成功しました")
            return df
        except FileNotFoundError:
            self.logger.error(
                f"マスターファイル '{self.master_file_path}' が見つかりません"
            )
            raise
        except pd.errors.EmptyDataError:
            self.logger.error(f"マスターファイル '{self.master_file_path}' が空です")
            raise
        except pd.errors.ParserError as e:
            self.logger.error(
                f"マスターファイル '{self.master_file_path}' のパース中にエラーが発生しました: {e}"
            )
            raise
        except Exception as e:
            self.logger.exception(
                f"マスターファイル '{self.master_file_path}' の読み込み中にエラーが発生しました: {e}"
            )
            raise

    def get_subjects(self) -> List[Dict]:
        """
        マスターファイルからすべての被験者情報を取得する。
        """
        try:
            subjects = self.data.to_dict(orient="records")
            self.logger.debug(f"{len(subjects)} 件の被験者情報を取得しました")
            return subjects
        except Exception as e:
            self.logger.exception("被験者情報の取得中にエラーが発生しました")
            raise
