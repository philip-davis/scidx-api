from pydantic import BaseModel, Field, root_validator, ValidationError
from typing import Dict, Optional, Union, Any
from enum import Enum

# Define an enumeration for file types
class FileTypeEnum(str, Enum):
    stream = "stream"
    CSV = "CSV"
    TXT = "TXT"
    JSON = "JSON"
    NetCDF = "NetCDF"

# Define processing info models for each file type
class StreamProcessingInfo(BaseModel):
    refresh_rate: Optional[str] = Field(
        None,
        description="The refresh rate for the data stream.",
        json_schema_extra={"example": "5 seconds"},
    )
    data_key: Optional[str] = Field(
        None,
        description="The key for the response data in the JSON file.",
        json_schema_extra={"example": "results"},
    )

class CSVProcessingInfo(BaseModel):
    delimiter: str = Field(
        ...,
        description="The delimiter used in the CSV file.",
        json_schema_extra={"example": ","},
    )
    header_line: int = Field(
        ...,
        description="The line number of the header in the CSV file.",
        json_schema_extra={"example": 1},
    )
    start_line: int = Field(
        ...,
        description="The line number where the data starts in the CSV file.",
        json_schema_extra={"example": 2},
    )
    comment_char: Optional[str] = Field(
        None,
        description="The character used for comments in the CSV file.",
        json_schema_extra={"example": "#"},
    )

class TXTProcessingInfo(BaseModel):
    delimiter: str = Field(
        ...,
        description="The delimiter used in the TXT file.",
        json_schema_extra={"example": "\t"},
    )
    header_line: int = Field(
        ...,
        description="The line number of the header in the TXT file.",
        json_schema_extra={"example": 1},
    )
    start_line: int = Field(
        ...,
        description="The line number where the data starts in the TXT file.",
        json_schema_extra={"example": 2},
    )

class JSONProcessingInfo(BaseModel):
    info_key: Optional[str] = Field(
        None,
        description="The key for additional information in the JSON file.",
        json_schema_extra={"example": "count"},
    )
    additional_key: Optional[str] = Field(
        None,
        description="An additional key in the JSON file.",
        json_schema_extra={"example": ""},
    )
    data_key: Optional[str] = Field(
        None,
        description="The key for the response data in the JSON file.",
        json_schema_extra={"example": "results"},
    )

class NetCDFProcessingInfo(BaseModel):
    group: Optional[str] = Field(
        None,
        description="The group within the NetCDF file.",
        json_schema_extra={"example": "group_name"},
    )

# Define the main request model
class URLRequest(BaseModel):
    resource_name: str = Field(
        ...,
        description="The unique name of the resource to be created.",
        json_schema_extra={"example": "example_resource_name"},
    )
    resource_title: str = Field(
        ...,
        description="The title of the resource to be created.",
        json_schema_extra={"example": "Example Resource Title"},
    )
    owner_org: str = Field(
        ...,
        description="The ID of the organization to which the resource belongs.",
        json_schema_extra={"example": "example_org_id"},
    )
    resource_url: str = Field(
        ...,
        description="The URL of the resource to be added.",
        json_schema_extra={"example": "http://example.com/resource"},
    )
    file_type: Optional[FileTypeEnum] = Field(
        ...,
        description="The type of the file (e.g., stream, CSV, TXT, JSON, NetCDF).",
        json_schema_extra={"example": "CSV"},
    )
    notes: str = Field(
        "",
        description="Additional notes about the resource.",
        json_schema_extra={"example": "Additional notes about the resource."},
    )
    extras: Optional[Dict[str, str]] = Field(
        None,
        description="Additional metadata to be added to the resource package as extras.",
        json_schema_extra={"example": {"key1": "value1", "key2": "value2"}},
    )
    mapping: Optional[Dict[str, str]] = Field(
        None,
        description="Mapping information for the dataset.",
        json_schema_extra={"example": {"field1": "mapping1", "field2": "mapping2"}},
    )
    processing: Optional[Dict[str, Any]] = Field(
        None,
        description="Processing information for the dataset.",
        json_schema_extra={"example": {"data_key": "data", "info_key": "info"}},
    )

    @root_validator(pre=True)
    def check_processing(cls, values):
        file_type = values.get('file_type')
        processing = values.get('processing')

        if file_type == "stream":
            try:
                StreamProcessingInfo(**processing)
            except ValidationError as e:
                raise ValueError(
                    f"Invalid processing info for file_type 'stream': {e}"
                )
        elif file_type == "CSV":
            try:
                CSVProcessingInfo(**processing)
            except ValidationError as e:
                raise ValueError(f"Invalid processing info for file_type 'CSV': {e}")
        elif file_type == "TXT":
            try:
                TXTProcessingInfo(**processing)
            except ValidationError as e:
                raise ValueError(f"Invalid processing info for file_type 'TXT': {e}")
        elif file_type == "JSON":
            try:
                JSONProcessingInfo(**processing)
            except ValidationError as e:
                raise ValueError(f"Invalid processing info for file_type 'JSON': {e}")
        elif file_type == "NetCDF":
            try:
                NetCDFProcessingInfo(**processing)
            except ValidationError as e:
                raise ValueError(
                    f"Invalid processing info for file_type 'NetCDF': {e}"
                )
        else:
            raise ValueError(f"Unsupported file_type: {file_type}")

        return values
