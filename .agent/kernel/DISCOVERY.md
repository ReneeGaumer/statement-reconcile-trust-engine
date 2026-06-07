\# KERNEL Discovery Contract



\## Purpose



This file exists to allow a newly initialized LLM session to discover, locate, and execute KERNEL without requiring prior conversation history.



KERNEL is the repository operational intelligence loop for the Statement Reconcile Trust Engine.



KERNEL is not a trust decision engine.



KERNEL is not a reconciliation engine.



KERNEL is not a runtime component.



KERNEL is a repository governance and execution coordinator.



Its purpose is to determine:



\- Current repository state

\- Current implementation phase

\- Current risk profile

\- Current gaps

\- Current priorities

\- Recommended next action



\---



\## Discovery Rule



If a user requests:



Run KERNEL



the model must attempt repository discovery before requesting additional information.



Discovery order:



1\. Search for:



.agent/kernel/KERNEL.md



2\. If KERNEL.md exists:



Execute KERNEL.



3\. If KERNEL.md does not exist:



Report:



KERNEL\_NOT\_FOUND



and stop.



\---



\## Required Execution Chain



Execution order is mandatory.



KERNEL

↓

BOOTSTRAP

↓

ORIENTATION

↓

STATE\_CLASSIFICATION

↓

PRIORITIZATION

↓

RECOMMENDATION

↓

EXECUTION

↓

VERIFICATION



\---



\## Required Files



Mandatory:



.agent/kernel/KERNEL.md

.agent/kernel/BOOTSTRAP.md

.agent/kernel/ORIENTATION.md

.agent/kernel/STATE\_CLASSIFICATION.md

.agent/kernel/PRIORITIZATION.md

.agent/kernel/RECOMMENDATION.md

.agent/kernel/EXECUTION.md

.agent/kernel/VERIFICATION.md



Supporting:



.agent/kernel/EVIDENCE.md

.agent/kernel/GAP\_RISK.md



\---



\## Required Output



KERNEL must produce:



CURRENT STATE



including:



\- Project Structure

\- Verified Existing

\- Incomplete Components

\- Missing Components

\- Current Implementation Phase

\- Highest Priority Gap

\- Recommended Next Step

\- Known Risks

\- Technical Debt

\- Git Hygiene Status



\---



\## Failure Conditions



Stop execution if:



\- repository cannot be inspected

\- evidence is insufficient

\- implementation phase cannot be determined

\- confidence falls below 80%



Report:



INSUFFICIENT\_EVIDENCE



and stop.



\---



\## Success Criteria



A successful KERNEL execution allows a newly initialized LLM session to orient itself within the repository and recommend the next highest-value action without requiring reconstruction of prior conversation history.

