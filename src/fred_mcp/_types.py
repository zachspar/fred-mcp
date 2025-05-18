from typing import Literal, TypeAlias

__all__ = [
    "FredUnit",
    "FredSortOrder",
    "FredFrequency",
    "FredAggregationMethod",
    "FredOutputType",
]

FredSortOrder: TypeAlias = Literal["asc", "desc"]

FredUnit: TypeAlias = Literal[
    "lin", "chg", "ch1", "pch", "pc1", "pca", "cch", "cca", "log"
]
FredFrequency: TypeAlias = Literal[
    "d",
    "w",
    "bw",
    "m",
    "q",
    "sa",
    "a",
    "wef",
    "weth",
    "wew",
    "wetu",
    "wem",
    "wesu",
    "wesa",
    "bwew",
    "bwem",
]
FredAggregationMethod: TypeAlias = Literal["avg", "sum", "eop"]
FredOutputType: TypeAlias = Literal[1, 2, 3, 4]
