from enum import Enum


class DailySummaryStatus(str, Enum):
    WITHIN_TARGET = "within_target"
    OVER_TARGET = "over_target"
    UNDER_TARGET = "under_target"
