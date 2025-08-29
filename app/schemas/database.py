from typing import Any

from pydantic import BaseModel, Field


class FindQueryInput(BaseModel):
    filter: dict[str, Any] = Field(default={}, description="The filter to apply to the query")
    limit: int = Field(default=10, ge=1, description="The number of documents to return")
    skip: int = Field(default=0, ge=0, description="The number of documents to skip")
    sort: list[tuple[str, int]] = Field(
        default=[("_id", 1)], description="The sort order to apply to the query. Desending order is indicated by -1."
    )


class InsertQueryInput(BaseModel):
    documents: list[dict[str, Any]] = Field(default=[], description="The documents to insert")


class InsertQueryResult(BaseModel):
    inserted_ids: list[str] = Field(default=[], description="The ids of the documents inserted")


class UpdateQueryInput(BaseModel):
    filter: dict[str, Any] = Field(default={}, description="The filter to apply to the query")
    update: dict[str, Any] = Field(default={}, description="The update to apply to the query")
    multi: bool = Field(default=False, description="Whether to update multiple documents")
    upsert: bool = Field(default=False, description="Whether to insert the document if it does not exist")


class UpdateQueryResult(BaseModel):
    matched_count: int = Field(default=0, description="The number of documents matched")
    modified_count: int = Field(default=0, description="The number of documents modified")


class DeleteQueryInput(BaseModel):
    filter: dict[str, Any] = Field(default={}, description="The filter to apply to the query")
    multi: bool = Field(default=False, description="Whether to delete multiple documents")


class DeleteQueryResult(BaseModel):
    deleted_count: int = Field(default=0, description="The number of documents deleted")
