from pathlib import Path
from typing import NamedTuple

import tomli

DEFAULT_CONFIG_DIR = "/etc/simple-web-counter"
CONFIG_FILENAME = "config.toml"


class ConfigImagesSection(NamedTuple):
    base_dir: str
    filename: str


class ConfigDataSection(NamedTuple):
    out_dir: str


class Config(NamedTuple):
    images: ConfigImagesSection
    data: ConfigDataSection


def load(config_dir: str = DEFAULT_CONFIG_DIR) -> Config:
    config_path = Path(config_dir) / CONFIG_FILENAME

    with open(config_path, "rb") as fp:
        config = tomli.load(fp)

        return Config(
            images=ConfigImagesSection(
                base_dir=config["images"]["base_dir"],
                filename=config["images"]["filename"],
            ),
            data=ConfigDataSection(out_dir=config["data"]["out_dir"]),
        )
