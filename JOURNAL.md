## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/6

**Issue title:** Duplicate embeddings generated when re-ingesting the same repository

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The ingestion pipeline currently processes a repository again even when that same repository has already been ingested. This creates duplicate vector embeddings for identical source content, which can cause retrieval results to contain repeated chunks and artificially inflated relevance scores. The problem primarily affects `ingestion/pipeline.py` and the ingested-source tracking model in `core/models/ingested_source.py`. A successful fix would detect an existing ingestion before generating embeddings and prevent duplicate vector entries while preserving legitimate re-ingestion behavior when appropriate.

**Selection notes:**
I reviewed the issue description, relevant files, and estimated effort. The issue requires understanding how the ingestion pipeline checks persisted source records before generating and storing embeddings. The scope is limited to the ingestion workflow and associated tests rather than requiring a major application redesign. I should be able to reproduce the duplicate-ingestion behavior locally and verify that repeated ingestion no longer creates duplicate vector entries.

**Branch name:** fix/6-prevent-duplicate-embeddings

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
