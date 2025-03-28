import os
from pathlib import Path

from pydantic import BaseModel


class FolderPathModel(BaseModel):
    """フォルダのパス"""

    base_dir: Path = Path(".")
    path_folder_config: Path = base_dir / "config"
    path_folder_output: Path = base_dir / "output"
    path_folder_simout: Path = base_dir / "simout"

    path_folder_subject_results: Path = path_folder_output / "subject_results"
    path_folder_log: Path = path_folder_output / "log"


class FilePathModel(BaseModel):
    """ファイルのパス"""

    folder_path_model: FolderPathModel = FolderPathModel()

    subjects_master: Path = (
        folder_path_model.path_folder_config / "Subjects_MASTER.xlsx"
    )
    all_subjects_results: Path = (
        folder_path_model.path_folder_output / "all_subjects_results.csv"
    )


class FileManager:
    """ファイル操作に関するクラス"""

    def __init__(self):
        self.folder_path_model = FolderPathModel()

    def get_simout_file_names(self):
        file_names = os.listdir(self.folder_path_model.path_folder_simout)
        file_names = [
            file for file in file_names if file.endswith((".xlsx", ".xls", ".csv"))
        ]
        file_names = sorted(file_names, reverse=False)
        return file_names

    def get_subject_results_file_names(self):
        file_names = os.listdir(self.folder_path_model.path_folder_subject_results)
        file_names = [
            file for file in file_names if file.endswith((".xlsx", ".xls", ".csv"))
        ]
        file_names = sorted(file_names, reverse=False)
        return file_names

    def get_simout_path(self, file_name):
        return self.folder_path_model.path_folder_simout / file_name

    def get_subject_results_path(self, file_name):
        return self.folder_path_model.path_folder_subject_results / file_name

    def get_output_path(self, file_name):
        return self.folder_path_model.path_folder_output / file_name

    def get_log_path(self, file_name):
        return self.folder_path_model.path_folder_log / file_name

    def print_base_dir(self):
        print(f"Base directory: {self.folder_path_model.base_dir}")


class PathConfig:
    def __init__(self):
        self.folder_path_model = FolderPathModel()
        self.file_path_model = FilePathModel()
        self.file_manager = FileManager()
