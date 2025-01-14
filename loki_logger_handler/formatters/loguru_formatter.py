import traceback
import sys


class LoguruFormatter:
    """
    A custom formatter for log records generated by Loguru, formatting the record into a structured dictionary.
    """
    def __init__(self):
        pass

    def format(self, record):
        """
        Format a Loguru log record into a structured dictionary.

        Args:
            record (dict): The Loguru log record to format.

        Returns:
            dict: A dictionary representation of the log record.
        """
        # Convert timestamp to a standard format across Python versions
        timestamp = record.get("time")
        if hasattr(timestamp, "timestamp"):
            # Python 3.x
            timestamp = timestamp.timestamp()
        else:
            # Python 2.7: Convert datetime to a Unix timestamp
            timestamp = (timestamp - timestamp.utcoffset()).total_seconds()

        formatted = {
            "message": record.get("message"),
            "timestamp": timestamp,
            "process": record.get("process").id,
            "thread": record.get("thread").id,
            "function": record.get("function"),
            "module": record.get("module"),
            "name": record.get("name"),
            "level": record.get("level").name.upper(),
        }

        # Update with extra fields if available
        extra = record.get("extra", {})
        if isinstance(extra, dict):
            # Handle the nested "extra" key correctly
            if "extra" in extra and isinstance(extra["extra"], dict):
                formatted.update(extra["extra"])
            else:
                formatted.update(extra)

        # Check if the log level indicates an error (case-insensitive and can be partial)
        if formatted["level"].startswith("ER"):
            formatted["file"] = record.get("file").name
            formatted["path"] = record.get("file").path
            formatted["line"] = record.get("line")

            if record.get("exception"):
                exc_type, exc_value, exc_traceback = record.get("exception")
                if sys.version_info[0] == 2:
                    # Python 2.7: Use the older method for formatting exceptions
                    formatted_traceback = traceback.format_exception(
                        exc_type, exc_value, exc_traceback
                    )
                else:
                    # Python 3.x: This is the same
                    formatted_traceback = traceback.format_exception(
                        exc_type, exc_value, exc_traceback
                    )
                formatted["stacktrace"] = "".join(formatted_traceback)

        return formatted
