\# Prioritization Loop



Status: AGENT LAYER

Parent: .agent/kernel/STATE\_CLASSIFICATION.md



\## Purpose



Determine the next highest-value repository action.



The loop must recommend work using repository evidence.



The loop may not recommend work based on assumptions, preferences, habits, or undocumented opinions.



\## Inputs



Required:



\- Bootstrap Output

\- Orientation Output

\- State Classification Output



\## Core Principle



Not all unfinished work has equal value.



Priority must be determined by:



\- constitutional impact

\- architectural impact

\- trust impact

\- governance impact

\- dependency impact

\- implementation readiness

\- risk reduction

\- roadmap progression



\## Priority Categories



\### P0



Repository cannot safely advance.



Examples:



\- constitutional violation

\- broken governance chain

\- failing tests

\- repository corruption

\- unrecoverable ambiguity



\### P1



Required prerequisite work.



Examples:



\- missing authoritative model

\- missing contract

\- missing schema

\- missing dependency phase



\### P2



Direct roadmap advancement.



Examples:



\- next planned implementation phase

\- implementation required by roadmap



\### P3



Optimization.



Examples:



\- cleanup

\- refactoring

\- convenience tooling



\## Dependency Rules



A recommendation must identify:



\- what depends on it

\- what it depends on



The loop may not recommend implementation that violates dependency order.



\## Roadmap Rules



If roadmap phases exist:



The loop must determine:



\- current phase

\- next phase

\- blocked phases

\- future phases



The loop should prefer advancing the next unfinished roadmap phase.



\## Required Outputs



Current Priority



Priority Classification



Reason



Supporting Evidence



Blocking Dependencies



Affected Components



Expected Outcome



Confidence Score



\## Recommendation Scoring



Each candidate action should be scored using:



Constitutional Value



Governance Value



Architectural Value



Trust Value



Roadmap Value



Risk Reduction



Implementation Readiness



Total Score



\## Example



Current Priority:

Implement Reconciliation Engine



Classification:

P2



Reason:

Phase 5 exists in roadmap.

Specifications exist.

Implementation does not exist.



Supporting Evidence:

docs/roadmap/IMPLEMENTATION\_PHASES.md

docs/specifications/RECONCILIATION\_SPECIFICATION.md



Confidence:

95%

