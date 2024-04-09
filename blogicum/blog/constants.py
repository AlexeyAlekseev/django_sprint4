"""Constants for blog app."""


class Config:
    """Class for storing configuration values."""

    TRUNCATION_LENGTH = 30
    ORDER_BY_DATE_DESC = '-pub_date'
    POST_PER_PAGE = 10
