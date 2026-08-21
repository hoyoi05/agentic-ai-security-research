# Agentic AI Security Research

A public research portal for systematically mapping, classifying, and experimentally evaluating security risks in agentic AI systems.

The repository hosts a **systematic mapping study (SMS)** of Agentic AI security. It maps the research landscape across goal and context integrity, memory and skills, tools and MCP, identity and delegation, multi-agent propagation, runtime observability and forensics, incident response and recovery, and security evaluation.

## Research workflow

1. Define and version the mapping protocol.
2. Search OpenAlex and arXiv as core open discovery sources, with Semantic Scholar as a secondary source.
3. Normalize DOI and publication metadata through Crossref, DBLP, and official publication pages.
4. Deduplicate and screen records using explicit inclusion and exclusion criteria.
5. Code included studies with a shared taxonomy and evidence scale.
6. Analyze research density, evaluation practice, reproducibility, and gaps.
7. Select high-contribution topics for focused reviews and empirical studies.

Scopus, Web of Science, and IEEE Xplore are not executed without subscription access. This limitation is reported explicitly rather than replacing unavailable result counts with estimates. Google Scholar is used only as a supplementary discovery path.

The initial self-evolving-agent track remains part of the map. It covers experience, trajectory, memory, and skill poisoning; persistent backdoors; unsafe capability acquisition; and runtime-verified skill promotion.

## Focused research track

Agent Forensics and FRIDA are maintained as focused follow-up tracks. The public mapping study identifies their position and evidence gaps. Detailed unpublished design and manuscript work remains in separate private repositories.

## Research portal

The documentation site is built with MkDocs and deployed at:

**https://hoyoi05.github.io/agentic-ai-security-research/**

## Evidence policy

Every source is labeled by publication type, screening state, evidence status, and reproduction status. Performance or security claims remain attributed to their authors until independently reproduced. Copyrighted papers, white papers, and news articles are linked and summarized rather than copied.

## License

Documentation and research metadata are licensed under CC BY 4.0. Source code and automation files are licensed under Apache-2.0. See [LICENSE.md](LICENSE.md).
