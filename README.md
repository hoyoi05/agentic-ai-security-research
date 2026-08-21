# Agentic AI Security Research

A public research portal for surveying, classifying, and experimentally evaluating security risks in agentic AI systems.

The first research track focuses on **self-evolving agents**: systems that learn from trajectories, memories, feedback, or generated skills after deployment. The central question is whether an apparent utility improvement also introduces persistent capability, privilege, or runtime-risk changes.

## Initial direction: Runtime-Verified Secure Skill Evolution

Candidate skills should be promoted only when they improve task utility **and** remain within an approved runtime behavior and privilege envelope. Evaluation therefore correlates semantic intent and tool decisions with observable system effects such as process execution, file access, network connections, identity use, and Kubernetes API activity.

## Initial scope

- Skill optimization and skill-centered assessment: SkillOpt and SkillLens
- Malicious experience, trajectory, memory, and skill poisoning
- Persistent backdoors and unsafe capability acquisition
- Runtime tracing across agent, tool/MCP, host, and cloud boundaries
- Comparative experiments in local-agent and Kubernetes/Knative environments
- Reproducible evidence, limitations, and independent verification status

## Research portal

The documentation site is built with MkDocs and deployed at:

**https://hoyoi05.github.io/agentic-ai-security-research/**

## Evidence policy

Every source is labeled by publication type and verification status. Performance or security claims remain attributed to their authors until independently reproduced. Copyrighted papers, white papers, and news articles are linked and summarized rather than copied.

## License

Documentation and research metadata are licensed under CC BY 4.0. Source code and automation files are licensed under Apache-2.0. See [LICENSE.md](LICENSE.md).
