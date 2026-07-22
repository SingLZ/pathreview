from unittest.mock import MagicMock, patch

from ingestion.chunking.base import Chunk
from ingestion.parsers.base import ParseResult
from ingestion.pipeline import IngestionPipeline


def test_reingesting_identical_repository_does_not_generate_embeddings_twice() -> None:
    """Reproduce issue #6: identical repository ingestion is not skipped."""
    pipeline = IngestionPipeline(
        vector_db=MagicMock(),
        db_session=object(),
        embedding_provider=MagicMock(),
    )

    repo_data = {
        "name": "sample-repository",
        "url": "https://github.com/example/sample-repository",
        "description": "Repository used to reproduce duplicate ingestion.",
        "language": "Python",
    }

    with (
        patch.object(
            pipeline.repo_analyzer,
            "parse",
            return_value=ParseResult(
                text="Sample repository metadata",
                metadata={
                    "primary_language": "Python",
                    "tech_stack": ["Python"],
                },
                source_type="repo",
            ),
        ),
        patch.object(
            pipeline.strategy_selector,
            "chunk",
            return_value=[
                Chunk(
                    text="Sample repository metadata",
                    metadata={"chunk_index": 0},
                )
            ],
        ),
        patch.object(
            pipeline.batch_processor,
            "process",
            return_value=[],
        ) as process_mock,
    ):
        pipeline.ingest_repo_metadata(
            "00000000-0000-0000-0000-000000000001",
            repo_data,
        )
        second_result = pipeline.ingest_repo_metadata(
            "00000000-0000-0000-0000-000000000001",
            repo_data,
        )

    assert (
        process_mock.call_count == 1
    ), "Re-ingesting identical repository data generated embeddings twice"
    assert second_result.skipped is True

    pipeline.ingest_repo_metadata("00000000-0000-0000-0000-000000000001", repo_data)
    second_result = pipeline.ingest_repo_metadata(
        "00000000-0000-0000-0000-000000000001",
        repo_data,
    )

    assert (
        process_mock.call_count == 1
    ), "Re-ingesting identical repository data generated embeddings twice"
    assert second_result.skipped is True
