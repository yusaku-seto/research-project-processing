import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from config import Config
from schemas.df_processed_schema import DfProcessedSchema
from schemas.df_simout_schema import DfSimoutSchema
from src.metric_calculator import MetricCalculator

palette_20 = sns.color_palette("viridis", 20)
palette_20 = sns.color_palette("hls", 20)

config = Config()
metric_calculator: MetricCalculator = MetricCalculator(config=config, logger=None)
df_processed_columns = DfProcessedSchema()
df_simout_columns = DfSimoutSchema()


def plot_t_v_a_gas_distance_by_type(
    config,
    subject_managers,
    velocity: int,
    experiment_type: str,
    df_all_subject_results: pd.DataFrame,
) -> Figure:
    """
    Ego車の速度と加速度をプロットする関数。実験パターンごとに被験者をまとめてプロット

    Args:
        df (pd.DataFrame): データフレーム（時刻、速度、加速度が含まれる）。
        fill_time_range (list, optional): 時間範囲のリスト [開始時刻, 終了時刻]。
        highlight_times (list, optional): 縦線を引く時刻のリスト [時刻1, 時刻2]。

    Returns:
        fig (Figure): プロットした図のオブジェクト。
    """
    label_font_size = 20
    label_font_size_small = label_font_size

    fig, axes = plt.subplots(nrows=3, figsize=(12, 12))
    count = 0
    for id, subject_manager in subject_managers.items():
        if subject_manager.experiment_type != experiment_type:
            continue
        count += 1
        df = subject_manager.df_dict[velocity]
        dt = df[df_simout_columns.time].iloc[1] - df[df_simout_columns.time].iloc[0]
        df = metric_calculator.add_mileage_column(dt=dt, df=df)

        # x column
        distance = df[df_processed_columns.Velocity_times_dt].cumsum()
        # y columns
        ego_velocity = (
            df[df_simout_columns.ego_v] * config.experiment.ms_to_kmh
        )  # km/hに変換
        ego_acceleration = df[df_simout_columns.ego_a]
        Brake_Out = df[df_simout_columns.Brake_Out]

        df_plot = pd.DataFrame()
        df_plot["ego_velocity"] = ego_velocity
        df_plot["ego_acceleration"] = ego_acceleration
        df_plot["Brake_Out"] = Brake_Out
        df_plot.index = distance
        # 各行にプロット
        for i, col in enumerate(df_plot.columns):
            ax = axes[i]
            ax.plot(
                df_plot.index,
                df_plot[col],
                color=palette_20[count],
                label=id,
                linewidth=3,
                alpha=0.7,
            )

            ax.set_xlabel("Distance [m]")
            # ax.set_xticks(np.arange(0, 40000, 5000))
            ax.set_xlim(0, 1)
            # ax.set_yticks(np.arange(0, 70, 10))
            ax.tick_params(
                axis="y", which="both", pad=10
            )  # y軸の目盛ラベルを10ピクセル離す
            # ax.set_ylabel(col)

    # ax.set_ylim(0, int(key)+5)
    # Ego速度のプロット
    axes[0].set_ylabel("Velocity [km/h]", fontsize=label_font_size)
    axes[0].set_yticks(np.arange(0, 3, 1))
    axes[0].set_ylim(0, 3)

    # Ego加速度のプロット
    axes[1].set_ylabel("Acceleration [m/s$^2$]", fontsize=label_font_size)
    axes[1].set_yticks(np.arange(-1, 1, 0.5))
    axes[1].set_ylim(-1, 1)
    # axes[1].minorticks_on()  # サブ目盛りを表示
    # axes[1].grid(which='minor', linestyle='--', linewidth=0.5)

    axes[2].set_ylabel("Amount of Manual Brake[-]", fontsize=label_font_size)
    axes[2].set_yticks(np.arange(0, 1.1, 0.25))
    axes[2].set_ylim(0, 1)

    # 凡例を枠外に1度だけ表示
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        title="Subject ID",
        loc="upper left",
        bbox_to_anchor=(1.0, 0.95),
    )
    # レイアウト調整
    plt.tight_layout()

    return fig


def plot_t_v_a_gas_distance_individual(
    config,
    df_dict: dict[pd.DataFrame],
    subject_id: int,
    experiment_type: str,
    df_all_subject_results: pd.DataFrame,
    fill_time_range: list = None,
    highlight_times: list = None,
    xlim: list = None,
) -> Figure:
    """
    Ego車の速度と加速度をプロットする関数。

    Args:
        df (pd.DataFrame): データフレーム（時刻、速度、加速度が含まれる）。
        fill_time_range (list, optional): 時間範囲のリスト [開始時刻, 終了時刻]。
        highlight_times (list, optional): 縦線を引く時刻のリスト [時刻1, 時刻2]。

    Returns:
        fig (Figure): プロットした図のオブジェクト。
    """
    label_font_size = 18
    label_font_size_small = label_font_size - 1

    fig, axes = plt.subplots(nrows=len(df_dict), figsize=(12, 4 * len(df_dict)))
    for i, (key, df) in enumerate(df_dict.items()):
        dt = df[df_simout_columns.time].iloc[1] - df[df_simout_columns.time].iloc[0]
        df = metric_calculator.add_mileage_column(dt=dt, df=df)
        distance = df[df_processed_columns.Velocity_times_dt].cumsum()
        velocity = df[df_simout_columns.ego_v] * config.experiment.ms_to_kmh
        if len(df_dict) == 1:
            ax = axes
        else:
            ax = axes[i]
        ax.plot(distance, velocity, color="k", linewidth=3)
        ax.set_xlabel("Distance [m]")
        # ax.set_xticks(np.arange(0, 40000, 5000))
        ax.set_xlim(0, 1)
        # ax.set_yticks(np.arange(0, 70, 10))
        # ax.set_ylim(0, int(key)+5)
        ax.set_ylim(0, 3)
        ax.set_ylabel("Velocity [km/h]", fontsize=label_font_size)
        ax.tick_params(
            axis="y", which="both", pad=10
        )  # y軸の目盛ラベルを10ピクセル離す

    plt.tight_layout()
    return fig
