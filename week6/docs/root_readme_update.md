# Suggested additions to the repository's root README

These are optional edits for the existing root `README.md`, not a replacement file. The root project page reviewed during preparation listed Weeks 1–4 in its navigation table. Keep the existing introduction, source boundaries, and assistance disclosure.

## Add these rows to the existing “Explore the project” table

Copy them after the Week 4 row in the **root** README. The paths below are relative to the repository root:

```markdown
| [Week 5](week5/README.md) | Hunt with a hypothesis | Executed Splunk searches over synthetic teaching events, candidate review, and limitations. |
| [Week 6](week6/README.md) | Test and map an execution behavior | Benign Python deserialization simulation, baseline and policy comparison, recorded evidence, tests, and an ATT&CK Navigator layer. |
```

## Extend the workflow sentence

```markdown
Workflow: Understand the threat, collect and process evidence, analyze attack stages, build a hunting hypothesis, and test a controlled behavior against ATT&CK.
```

## Add a scope clarification

```markdown
Week 5 uses synthetic teaching events. Week 6 adds actually executed benign local simulations; its bundled reference run was collected in a preparation environment. It does not execute malicious models, compromise a supplier, or evaluate a production detection system.
```

Review the current root README before applying these edits so that a later Week 5 or Week 6 row is not duplicated. None of these suggestions has been pushed to GitHub by the package preparation process.
