import json
from typing import Optional
from collections import OrderedDict
from error_correction.data_dirs import ErrorCorrectionDirs
from datetime import datetime as dt
from pathlib import Path

class StatusDecodingPerformance:
    def __init__(
        self, channel, code, decoder, max_iter, data_dirs: ErrorCorrectionDirs
    ):
        self.channel = channel
        self.code = code
        self.decoder = decoder
        self.max_iter = max_iter
        self.data_dirs = data_dirs

        self.tot = OrderedDict()
        self.bec = OrderedDict()
        self.ber = OrderedDict()
        self.fec = OrderedDict()
        self.fer = OrderedDict()

    def _file_name(self, timestamp) -> str:
        """
        Infer the file name from the key attributes.
        For example, a file name can be "channel_code_decoder_max_iter.json".
        """
        if not timestamp:
            timestamp = dt.now().strftime("%Y%m%d-%H%M%S")
        return f"{self.channel}_{self.decoder}_{self.max_iter}_{self.code}_{timestamp}.json"

    def _file_path(self, timestamp: Optional[dt.timestamp]=None) -> Path:
        """
        Combine the directory and file name.
        """
        return self.data_dirs.output_path(self._file_name(timestamp))

    @classmethod
    def read_from_json(cls, filename: str, data_dirs: Path) -> None:
        """
        Read the JSON file (whose name is inferred from the instance attributes)
        and update the instance attributes accordingly.
        """
        path = data_dirs.output_path(filename)
        if path.exists():
            with open(path, "r") as f:
                data = json.load(f)
            obj = cls(
                channel=data.get("channel"),
                code=data.get("code"),
                decoder=data.get("decoder"),
                max_iter=data.get("max_iter"),
                data_dirs=data_dirs
            )

            obj.tot = data.get("tot")
            obj.bec = data.get("bec")
            obj.ber = data.get("ber")
            obj.fec = data.get("fec")
            obj.fer = data.get("fer")
            return obj
        else:
            print(f"File {path} does not exist.")

    def update_metrics(self, channel_parameter: float, metrics: dict) -> None:
        """
        Update the metrics from the provided dictionary.
        The expected structure for metrics is a dict with keys corresponding
        to metric names (e.g. "tot", "bec", etc.) and whose values are dictionaries
        with key/value pairs of current channel parameter and value to update. For example:
            {
                "tot": {"0.5": 100.0, 0.45: 150.0},
                "bec": {"0.5": 51289.0},
                ...
            }
        This method updates each metric individually.
        """
        valid = ["tot", "bec", "ber", "fec", "fer"]
        for metric_name, metric_value in metrics.items():
            if metric_name not in valid:
                raise ValueError(f"Metric {metric_name} not valid")
            metric_to_update = getattr(self, metric_name)
            metric_to_update[channel_parameter] = metric_value

    def save_json(self) -> None:
        """
        Save the current state of the object to a JSON file.
        The file name is inferred from the instance’s key attributes.
        """
        data = {
            "channel": self.channel,
            "code": self.code,
            "decoder": self.decoder,
            "max_iter": self.max_iter,
            "tot": self.tot,
            "bec": self.bec,
            "ber": self.ber,
            "fec": self.fec,
            "fer": self.fer,
        }
        path = self._file_path()
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def get_status_dict(self):
        return {
            "channel": self.channel,
            "code": self.code,
            "decoder": self.decoder,
            "max_iter": self.max_iter,
            "tot": self.tot,
            "bec": self.bec,
            "ber": self.ber,
            "fec": self.fec,
            "fer": self.fer,
        }

