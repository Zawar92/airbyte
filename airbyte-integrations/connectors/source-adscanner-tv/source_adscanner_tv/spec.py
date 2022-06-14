import re
import json
from typing import Union

from pydantic import BaseModel, Field

DEFAULT_START_DATE = "2016-09-01"


class OauthCredSpec(BaseModel):
    class Config:
        title = "Authorization Token"

    authorization: str = Field(title="Authorization", description="Bearer followed by space and session token generated in Login step", airbyte_secret=True)


class SourceAdscannerTvSpec(BaseModel):
    class Config:
        title = "Adscanner Tv Source Spec"

    credentials: Union[OauthCredSpec] = Field(
        title="Authentication Method", description="Authentication method", order=0, default={}, type="object"
    )

    start_date: str = Field(
        title="Replication Start Date *",
        default=DEFAULT_START_DATE,
        pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        description="The Start Date in format: YYYY-MM-DD. Any data before this date will not be replicated. "
        "If this parameter is not set, all data will be replicated.",
        order=1,
    )

    end_date: str = Field(
        None,
        title="End Date",
        pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
        description=(
            "The date until which you'd like to replicate data for all incremental streams, in the format YYYY-MM-DD. "
            "All data generated between start_date and this date will be replicated. "
            "Not setting this option will result in always syncing the data till the current date."
        ),
        order=2,
    )
