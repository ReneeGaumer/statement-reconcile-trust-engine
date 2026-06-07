\# Evidence Loop



Status: AGENT LAYER

Parent: .agent/kernel/KERNEL.md



\## Purpose



Collect repository evidence before interpretation, prioritization, or recommendation.



The Evidence Loop prevents conclusions from being formed from chat memory, assumptions, or partial inspection.



\## Inputs



Required:



\- Git repository

\- Tracked file inventory

\- Commit history

\- Roadmap

\- Constitution

\- Specifications

\- Contracts

\- Schemas

\- Source files

\- Tests



\## Required Evidence Categories



1\. Git state

2\. Commit history

3\. Repository structure

4\. Roadmap evidence

5\. Governing authority evidence

6\. Specification evidence

7\. Implementation evidence

8\. Test evidence

9\. Drift evidence

10\. Unknowns



\## Rules



Evidence must be collected before conclusions.



Every later loop must cite evidence from this loop.



Missing evidence must be recorded as UNKNOWN.



Unknown does not mean failed.



Incomplete does not mean drift.



\## Required Outputs



Evidence Inventory



Known Facts



Known Unknowns



Repository Signals



Evidence Gaps



Confidence Level

