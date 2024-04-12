"""Constants for blog app."""


class Config:
    """Class for storing configuration values."""

    TRUNCATION_LENGTH = 30
    ORDER_BY_DATE_DESC = '-pub_date'
    POST_PER_PAGE = 10
    CLOSE_MATCH_NUM = 1
    CUTOFF_POSSIBLE_SCORE: float = 0.6  # range[0,1]
