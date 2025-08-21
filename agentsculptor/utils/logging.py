import logging
import sys

# ANSI color codes
RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",     # cyan
    "INFO": "\033[32m",      # green
    "DIALOG": "\033[33m",    # yellow
    "NOOP": "\033[90m",      # gray
    "ERROR": "\033[31m",     # red
    "FATAL": "\033[41m",     # red background
    "STOP": "\033[35m",      # magenta
    "ITERATION": "\033[34m", # blue
}

# Mapping from our custom tags to logging levels
LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "ERROR": logging.ERROR,
    "FATAL": logging.CRITICAL,
    "STOP": logging.CRITICAL + 1,
    "DIALOG": logging.INFO,
    "NOOP": logging.INFO,
}

logging.addLevelName(LEVELS["STOP"], "STOP")


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        for tag, color in COLORS.items():
            if msg.startswith(f"[{tag}"):
                msg = f"{color}{msg}{RESET}"
                break
        return msg


class CustomLogger(logging.Logger):
    def iteration(self, num: int, msg: str = "") -> None:
        self.info(f"[ITERATION {num}] {msg}")

    def dialog(self, msg: str) -> None:
        self.info(f"[DIALOG] {msg}")

    def noop(self, msg: str) -> None:
        self.info(f"[NOOP] {msg}")

    def fatal(self, msg: str) -> None:
        self.critical(f"[FATAL] {msg}")

    def stop(self, msg: str) -> None:
        self.log(LEVELS["STOP"], f"[STOP] {msg}")


def setup_logging(level: str = "INFO") -> None:
    """Configure logging globally with our custom logger and colors."""
    logging.setLoggerClass(CustomLogger)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter("%(message)s"))

    logging.basicConfig(
        level=LEVELS.get(level.upper(), logging.INFO),
        handlers=[handler],
        force=True,
    )


def get_logger(name: str = "AgentSculptor") -> CustomLogger:
    return logging.getLogger(name)
