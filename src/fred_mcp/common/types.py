from typing import Literal, TypeAlias

__all__ = [
    "FredUnit",
    "FredSortOrder",
    "FredFrequency",
    "FredAggregationMethod",
    "FredOutput",
    "FredSearch",
    "FredSeriesSearchOrderBy",
    "FredTagGroup",
    "FredTagOrderBy",
    "FredSeriesUpdateFilter",
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
FredOutput: TypeAlias = Literal[1, 2, 3, 4]
FredSearch: TypeAlias = Literal["full_text", "series_id"]
FredSeriesSearchOrderBy: TypeAlias = Literal[
    "search_rank",
    "series_id",
    "title",
    "units",
    "frequency",
    "seasonal_adjustment",
    "realtime_start",
    "realtime_end",
    "last_updated",
    "observation_start",
    "observation_end",
    "popularity",
    "group_popularity",
]
FredTagGroup: TypeAlias = Literal[
    "freq",
    "gen",
    "geo",
    "geot",
    "rls",
    "seas",
    "src",
]
FredTagOrderBy: TypeAlias = Literal[
    "series_count",
    "popularity",
    "created",
    "name",
    "group_id",
]
FredSeriesUpdateFilter: TypeAlias = Literal[
    "all",
    "macro",
    "regional",
]
