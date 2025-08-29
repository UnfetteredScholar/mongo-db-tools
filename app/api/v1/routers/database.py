import json
from logging import getLogger

from bson import ObjectId
from core.authentication.subscription import validate_subscription
from core.platfom_integration_client import (
    PlatformIntegrationClient,
    get_platform_client,
)
from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient
from schemas.database import (
    DeleteQueryInput,
    DeleteQueryResult,
    FindQueryInput,
    InsertQueryInput,
    InsertQueryResult,
    UpdateQueryInput,
    UpdateQueryResult,
)

router = APIRouter(dependencies=[Depends(validate_subscription)])


@router.get(
    path="/databases",
    operation_id="list_databases",
    response_model=list[str],
)
def list_databases(
    mongo_project: str,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> list[str]:
    """
    List all databases in the MongoDB instance.
    """

    logger = getLogger(__name__ + ".query_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")
        client = MongoClient(connection_string)

        db_names = client.list_database_names()

        return db_names
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not query documents: {ex}")
    finally:
        if client:
            client.close()


@router.get(
    path="/databases/{db_name}/collections",
    operation_id="list_collections",
    response_model=list[str],
)
def list_collections(
    mongo_project: str,
    db_name: str,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> list[str]:
    """
    List all collections in the specified database.
    """

    logger = getLogger(__name__ + ".query_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")

        client = MongoClient(connection_string)

        collections = client[db_name].list_collection_names()

        return collections
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not query documents: {ex}")
    finally:
        if client:
            client.close()


@router.post(
    path="/databases/{db_name}/collections/{collection_name}/documents/insert",
    operation_id="insert_documents",
    response_model=InsertQueryResult,
)
def insert_documents(
    mongo_project: str,
    db_name: str,
    collection_name: str,
    query: InsertQueryInput,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> InsertQueryResult:
    """
    Insert documents into the specified collection.
    """

    logger = getLogger(__name__ + ".insert_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")

        client = MongoClient(connection_string)

        collection = client[db_name][collection_name]

        res = collection.insert_many(documents=query.documents)
        inserted_ids = [str(id) for id in res.inserted_ids]

        return InsertQueryResult(inserted_ids=inserted_ids)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not insert documents: {ex}")
    finally:
        if client:
            client.close()


@router.post(
    path="/databases/{db_name}/collections/{collection_name}/documents/find",
    operation_id="query_documents",
    response_model=list[dict],
)
def query_documents(
    mongo_project: str,
    db_name: str,
    collection_name: str,
    query: FindQueryInput,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> list[dict]:
    """
    Query documents in the specified collection.
    """

    logger = getLogger(__name__ + ".query_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")

        client = MongoClient(connection_string)
        collection = client[db_name][collection_name]

        filter = query.filter

        if "_id" in filter:
            try:
                filter["_id"] = ObjectId(filter["_id"])
            except:
                pass

        documents = collection.find(filter=filter).limit(query.limit).skip(query.skip).sort(query.sort)

        res = [json.loads(json.dumps(document, default=str)) for document in documents]

        return res
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not query documents: {ex}")
    finally:
        if client:
            client.close()


@router.patch(
    path="/databases/{db_name}/collections/{collection_name}/documents",
    response_model=UpdateQueryResult,
    operation_id="update_documents",
)
def update_documents(
    mongo_project: str,
    db_name: str,
    collection_name: str,
    query: UpdateQueryInput,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> UpdateQueryResult:
    """
    Update document(s) in the specified collection.
    """

    logger = getLogger(__name__ + ".query_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")

        client = MongoClient(connection_string)
        collection = client[db_name][collection_name]

        filter = query.filter

        if "_id" in filter:
            try:
                filter["_id"] = ObjectId(filter["_id"])
            except:
                pass

        if query.multi:
            res = collection.update_many(filter=filter, update=query.update, upsert=query.upsert)
        else:
            res = collection.update_one(filter=filter, update=query.update, upsert=query.upsert)

        return UpdateQueryResult(matched_count=res.matched_count, modified_count=res.modified_count)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not update documents: {ex}")
    finally:
        if client:
            client.close()


@router.delete(
    path="/databases/{db_name}/collections/{collection_name}/documents",
    response_model=DeleteQueryResult,
    operation_id="delete_documents",
)
def delete_documents(
    mongo_project: str,
    db_name: str,
    collection_name: str,
    query: DeleteQueryInput,
    platform_client: PlatformIntegrationClient = Depends(get_platform_client),
) -> DeleteQueryResult:
    """
    Delete document(s) in the specified collection.
    """

    logger = getLogger(__name__ + ".query_documents")
    client: MongoClient | None = None
    try:
        mongo_details = platform_client.get_mongodb_details(mongo_project)
        connection_string = mongo_details.get("connection_string")

        client = MongoClient(connection_string)
        collection = client[db_name][collection_name]

        filter = query.filter

        if "_id" in filter:
            try:
                filter["_id"] = ObjectId(filter["_id"])
            except:
                pass

        if query.multi:
            res = collection.delete_many(filter=filter)
        else:
            res = collection.delete_one(filter=filter)

        return DeleteQueryResult(deleted_count=res.deleted_count)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail=f"Could not delete documents: {ex}")
    finally:
        if client:
            client.close()
