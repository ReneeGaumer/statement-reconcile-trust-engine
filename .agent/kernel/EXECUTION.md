\# Execution Loop



Status: AGENT LAYER

Parent: .agent/kernel/PRIORITIZATION.md



\## Purpose



Convert recommendations into executable repository actions.



Execution does not modify the repository.



Execution produces a proposed action plan.



Human approval remains required.



\## Inputs



Required:



\- Bootstrap Output

\- Orientation Output

\- State Classification Output

\- Gap/Risk Output

\- Prioritization Output

\- Recommendation Output



\## Execution Rules



The loop may:



\- identify required actions

\- identify verification actions

\- identify repository inspection actions

\- identify governance validation actions

\- identify testing actions



The loop may not:



\- invent repository state

\- assume completion

\- assume implementation success

\- assume test success

\- modify evidence

\- bypass governance

\- bypass verification



\## Action Categories



\- Inspect

\- Verify

\- Test

\- Implement

\- Refactor

\- Govern

\- Document

\- Audit



\## Action Selection Rules



Actions must be:



\- evidence-supported

\- phase-aware

\- roadmap-aligned

\- constitution-compliant



Actions must not:



\- skip unfinished dependencies

\- bypass authoritative specifications

\- violate governance requirements



\## Required Outputs



Current Objective



Recommended Action



Reason



Supporting Evidence



Dependencies



Risks



Verification Required



Expected Outcome



\## Stop Conditions



Stop if:



\- evidence is insufficient

\- roadmap position is unknown

\- dependency chain is incomplete

\- recommendation confidence is below 80%

