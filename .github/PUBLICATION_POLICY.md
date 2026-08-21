# Public publication policy

This public repository is limited to material that is intentionally ready for public release.

## Allowed by default

- Search and screening protocols
- Verified bibliographic metadata and citations
- Taxonomy coding and research-gap analysis
- Reproducible experiments and results approved for release
- General contribution and resource-management documentation

## Approval required

The following must remain in a private research or manuscript repository unless a repository maintainer explicitly approves publication:

- Unverified hypotheses and unpublished contributions
- Detailed threat models, experiment plans, or internal experiment notes
- Paper or submission roadmaps
- Manuscript drafts, response letters, and pre-submission analysis
- Topic-specific design tracks under restricted research paths

The required **build** check inspects pull requests. When restricted paths or sensitive research-design content are introduced, the check fails until a maintainer adds the `publication-approved` label. Deletions are not blocked.

The label means that the maintainer has confirmed both of the following:

1. The content is intentionally public.
2. Its release does not conflict with an active submission or private research plan.
