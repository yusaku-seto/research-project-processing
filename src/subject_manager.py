import pandas as pd

from config import Config


class SubjectManager:
    def __init__(self, id: int, simout_list: list):
        """
        指定されたIDの被験者実験データを管理するクラス

        Args:
            id (int): Subject ID
            simout_list (list[str]): 生データのファイル名リスト

        Returns:
            tuple: Optimal x threshold and the best score.
        """
        self.id: int = id
        self.experiment_type: str | None = None
        self.raw_df_dict: dict[pd.DataFrame] = pd.DataFrame()
        self.simout_list = simout_list

    def load_raw_data(self, config: Config):
        subject_raw_data_file_dict, experiment_type = (
            self.extract_subject_raw_file_names_and_type(self.simout_list, self.id)
        )
        self.experiment_type = experiment_type
        self.subject_raw_data_file_dict = subject_raw_data_file_dict
        subject_raw_data_path_dict = self.get_raw_data_full_path(
            config, subject_raw_data_file_dict=subject_raw_data_file_dict
        )
        self.subject_raw_data_path_dict = subject_raw_data_path_dict
        raw_df_dict, df_dict = self.get_id_data(
            config, subject_raw_data_path_dict=subject_raw_data_path_dict
        )
        self.raw_df_dict = raw_df_dict
        self.df_dict = df_dict
        return raw_df_dict, experiment_type

    @staticmethod
    def extract_subject_raw_file_names_and_type(subject_data_list, id):
        subject_id_list = [file for file in subject_data_list if "_" in file]
        subject_id_list = [
            file for file in subject_id_list if int(file.split("_")[1]) == id
        ]
        subject_raw_data_file_dict = {
            int(file.split("_")[2]): file for file in subject_id_list
        }
        experiment_type = subject_id_list[0].split("_")[3]
        return subject_raw_data_file_dict, experiment_type

    @staticmethod
    def get_raw_data_full_path(config: Config, subject_raw_data_file_dict: dict):
        subject_raw_data_path_dict = {}
        for velocity, file_name in subject_raw_data_file_dict.items():
            raw_data_full_path_velocity = config.paths.file_manager.get_simout_path(
                file_name=file_name
            )
            subject_raw_data_path_dict[velocity] = raw_data_full_path_velocity
        return subject_raw_data_path_dict

    @staticmethod
    def get_id_data(config, subject_raw_data_path_dict):
        raw_df_dict = {}
        df_dict = {}
        for velocity, raw_data_path in subject_raw_data_path_dict.items():
            df = pd.read_csv(raw_data_path)
            if velocity == 40 or velocity == 50 or velocity == 60:
                raw_df_dict[velocity] = df
                df_dict[velocity] = df
        return raw_df_dict, df_dict
