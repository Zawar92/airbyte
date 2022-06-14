from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.models.airbyte_protocol import DestinationSyncMode
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator
from airbyte_cdk.models import AdvancedAuth, AuthFlowType, ConnectorSpecification, OAuthConfigSpecification, SyncMode

from .json_restructured import (
    helper_getinductries_restructured
)

DEFAULT_START_DATE = "2016-09-01"
DEFAULT_END_DATE = "2016-12-01"


# Basic full refresh stream
class AdscannerTvStream(HttpStream, ABC):

    url_base = "https://api.uat.adscanner.tv/"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        return {}

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield {}


# class that contains main source germany | full-refresh
class Helper(AdscannerTvStream):
    """Docs: https://api.uat.adscanner.tv/helper"""

    primary_key = None

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "helper/"


class HelperGetIndustries(Helper):
    """Docs: https://api.uat.adscanner.tv/helper/getIndustries"""

    def __init__(self, args, **kwargs):
        super().__init__(**kwargs)
        self.params = args

    primary_key = None

    @property
    def http_method(self) -> str:
        return "POST"

    def request_headers(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return self.params

    def request_body_json(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> Optional[Mapping]:
        return {"filter": ""}

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield helper_getinductries_restructured(response.json())

    def path(
            self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "helper/getIndustries/"
