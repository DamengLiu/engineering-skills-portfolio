---
name: database-schema-design
description: Design or review a consequential relational schema change, including field semantics, constraints, indexes, compatibility, and migration or rollback. Use for new tables or changed data meaning, not routine query edits.
---

# Database Schema Design

## 1. Gather the data contract

Confirm the entity's meaning, lifecycle, write and read patterns, uniqueness, allowed values, nullability, expected volume, and retention. Inspect the actual database engine and existing schema conventions. Treat similar tables as compatibility evidence, not as authority for a new business rule.

## 2. Produce a reviewable design

Specify columns with types, lengths, defaults, nullability, and comments. Explain keys, foreign keys where appropriate, unique constraints, and indexes against actual predicates and sort order. Trace the change into models, queries, API fields, UI values, and historical data. For an existing table, include a bounded migration and rollback plan.

Do not manufacture code lists, values, or a retention period. If a domain dictionary exists, read its complete relevant value set and record the source. Present unresolved semantics as questions before applying them to stored data.

## 3. Verify at the right level

Review SQL syntax for the actual engine, data compatibility, null and duplicate cases, and affected ORM mappings. Use an execution plan on representative queries when authorized and available; explain its limits. Preparing SQL does not authorize DDL or production changes. Report the design, evidence, checks performed, and pending decisions.
