from enum import Enum


class OpenAiRunStatus(Enum):
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
