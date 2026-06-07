\# Recommendation Loop



Status: AGENT LAYER

Parent: .agent/kernel/PRIORITIZATION.md



\## Purpose



Convert the highest-priority objective into the smallest safe executable action.



The loop does not implement work.



The loop produces the implementation plan.



\## Inputs



Required:



\- Bootstrap Output

\- Orientation Output

\- State Classification Output

\- Prioritization Output



\## Core Principle



Large objectives must be decomposed into the smallest verifiable action.



The loop must prefer:



\- small changes

\- isolated changes

\- reversible changes

\- verifiable changes



over:



\- large refactors

\- broad modifications

\- multi-objective changes



\## Required Questions



1\. What is the objective?



2\. What repository evidence supports it?



3\. What files are likely affected?



4\. What dependencies must exist first?



5\. What is the smallest meaningful change?



6\. How will success be verified?



7\. What could go wrong?



8\. What would invalidate the recommendation?



\## Change Scope Classification



Classify recommendation as:



\- DOCUMENTATION

\- GOVERNANCE

\- TEST

\- IMPLEMENTATION

\- ARCHITECTURE

\- REFACTOR

\- INVESTIGATION



Exactly one primary classification is required.



\## Required Outputs



Objective



Reason



Evidence



Affected Files



Recommended Order



Verification Method



Risk Assessment



Expected Outcome



Confidence Score



\## Verification Planning



Every recommendation must define:



Before Change:



\- repository state

\- relevant tests

\- relevant documents



After Change:



\- tests to execute

\- evidence to collect

\- success criteria



\## Stop Conditions



The loop must stop if:



\- objective is ambiguous

\- evidence is insufficient

\- dependencies are missing

\- verification path is unknown

\- confidence is below 80%



\## Example



Objective:

Implement Reconciliation Engine



Classification:

IMPLEMENTATION



Affected Files:

src/trust\_engine/application/reconciliation\_engine.py



Reason:

Phase 5 is specified but not implemented.



Verification:

New reconciliation tests pass.



Confidence:

94%

