from pathlib import Path
from datetime import datetime


class Logs:
    def __init__(self):
        self._logs_path = Path("data/logs")
        self._log_file = None

    def _generate_log_filename(self) -> Path:
        """
        Creates a timestamped log filename and increments a counter
        if a file with the same name already exists.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_name = f"pyssh_{timestamp}"
        counter = 0

        while True:
            if counter == 0:
                filename = f"{base_name}.log"
            else:
                filename = f"{base_name}_{counter}.log"

            file_path = self._logs_path / filename

            if not file_path.exists():
                return file_path

            counter += 1

    @property
    def log_file(self) -> Path:
        """
        Lazily creates and returns the final log file path.
        """
        if self._log_file is None:
            self._log_file = self._generate_log_filename()

        return self._log_file

