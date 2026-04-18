# Project Roadmap

## Current Status (v1.2.0)

✅ **101 skills** across 12 categories
✅ Multi-agent support (Claude Code, Codex, Gemini CLI)
✅ Comprehensive documentation and categorization
✅ GitHub workflows for validation
✅ Issue and PR templates
✅ Semantic frontmatter fields (inputs, outputs, side_effects, triggers, complements, includes, tier)
✅ Federation schema for third-party skill repos (v1.1)
✅ Activation conditions specification (5 trigger types)
✅ Machine-readable skills registry (`distributions/skills-registry.json`)
✅ Skill bundles/packs (includes field)
✅ MCP skill server with 7 tools
✅ PR validation bot (auto-comments on PRs)
✅ Skill health checks (scripts, references, size metrics)
✅ Skill override system (`SKILLS_CUSTOM_DIR`)
✅ Lockfile for reproducibility (`distributions/skills-lock.json`)
✅ Core vs community quality tiers
✅ AI-driven skill planner (input/output dependency chains)
✅ Troubleshooting guide

## Short-term (Q1 2026)

### Documentation Improvements
- [ ] Add video tutorials for common skills
- [ ] Create skill showcase with screenshots
- [ ] Write blog post series on skill patterns
- [x] Add troubleshooting guide

### Quality Enhancements
- [x] Add automated testing for skills with scripts (health checks)
- [ ] Implement skill rating/feedback system
- [x] Create skill dependency graph (inputs/outputs in registry)
- [ ] Add performance benchmarks for code-quality skills

### New Skills
- [ ] Database migration patterns (5 requested)
- [ ] API documentation generator (8 requested)
- [ ] Infrastructure as Code patterns (3 requested)
- [ ] CI/CD pipeline templates (6 requested)

## Mid-term (Q2-Q3 2026)

### Platform Expansion
- [ ] Add VS Code extension integration
- [ ] Create web-based skill browser (registry JSON provides data layer)
- [ ] Implement skill marketplace
- [ ] Add skill analytics dashboard

### Skill Improvements
- [ ] Add interactive examples to skills
- [x] Create skill composition patterns (skill planner + chain prompts)
- [x] Implement skill versioning system (lockfile)
- [x] Add skill compatibility matrix (complements, inputs/outputs)

### Community Features
- [ ] Monthly skill contributor highlights
- [ ] Skill creation workshops
- [ ] Community skill showcase
- [ ] Skill certification program

## Long-term (Q4 2026+)

### Advanced Features
- [x] AI-powered skill recommendation (context-aware suggestions)
- [ ] Automatic skill updates
- [ ] Cross-agent skill translation
- [ ] Skill performance optimization

### Enterprise Features
- [x] Private skill repositories (federation schema + overrides)
- [ ] Team skill sharing
- [ ] Skill access controls
- [ ] Usage analytics

### Research & Innovation
- [ ] Study skill effectiveness metrics
- [x] Explore skill composition patterns (planner-driven composition)
- [ ] Investigate skill learning from usage
- [ ] Research skill optimization techniques

## Community Requests

Track community-requested features and skills:

### Most Requested Skills (by votes)
1. **API documentation generator** - 8 votes
2. **CI/CD pipeline templates** - 6 votes
3. **Database migration patterns** - 5 votes
4. **Code review automation** - 4 votes
5. **Infrastructure as Code** - 3 votes

### Most Requested Features
1. ~~**Skill versioning**~~ - 12 votes ✅ (lockfile)
2. ~~**Skill dependencies**~~ - 10 votes ✅ (inputs/outputs/includes)
3. **Interactive examples** - 8 votes
4. **Skill marketplace** - 7 votes (registry JSON provides data layer)
5. **VS Code integration** - 6 votes

## How to Contribute

- **Vote on roadmap items**: Open an issue with 👍 reaction
- **Propose new items**: Use the feature request template
- **Implement features**: Check "good first issue" label
- **Share feedback**: Join discussions on GitHub

---

**Last Updated**: 2026-02-06
**Next Review**: 2026-04-30

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to contribute.
