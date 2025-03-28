from .experiment import ExperimentConfig
from .logging_config import LoggingConfig
from .paths import PathConfig


class Config:
    def __init__(self):
        self.paths = PathConfig()
        self.logging = LoggingConfig()
        self.experiment = ExperimentConfig()
