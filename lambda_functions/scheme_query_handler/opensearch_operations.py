"""
OpenSearch operations for index management and vector search.
"""
import logging
from config import INDEX_NAME, EMBEDDING_DIMENSION, SEARCH_RESULTS_SIZE, KNN_K_VALUE

logger = logging.getLogger(__name__)


def create_index_if_not_exists(client):
    """
    Create OpenSearch index if it doesn't already exist.
    
    Args:
        client: OpenSearch client instance
    """
    if not client.indices.exists(index=INDEX_NAME):
        logger.info(f"Creating index: {INDEX_NAME}")
        
        index_body = {
            "settings": {
                "index.knn": True
            },
            "mappings": {
                "properties": {
                    "content": {
                        "type": "text"
                    },
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": EMBEDDING_DIMENSION
                    }
                }
            }
        }
        
        client.indices.create(
            index=INDEX_NAME,
            body=index_body
        )
        logger.info(f"Index created successfully: {INDEX_NAME}")
    else:
        logger.info(f"Index already exists: {INDEX_NAME}")


def search_opensearch(client, query_embedding):
    """
    Search OpenSearch using KNN vector similarity.
    
    Args:
        client: OpenSearch client instance
        query_embedding: Query embedding vector
        
    Returns:
        list: List of relevant content strings
    """
    query = {
        "size": SEARCH_RESULTS_SIZE,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": KNN_K_VALUE
                }
            }
        }
    }
    
    response = client.search(
        index=INDEX_NAME,
        body=query
    )
    
    results = []
    for hit in response["hits"]["hits"]:
        results.append(hit["_source"]["content"])
    
    logger.info(f"OpenSearch returned {len(results)} results")
    logger.debug(f"Search results: {results[:100]}...")  # Log first 100 chars
    return results
