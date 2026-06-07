\# Kernel Runbook



Status: AUTHORITATIVE AGENT ENTRYPOINT



\## Purpose



The Runbook defines the required execution order of the Kernel.



A Kernel run reconstructs repository state from evidence.



A Kernel run does not rely on memory, conversation history, CURRENT STATE documents, or assumptions.



Repository evidence is authoritative.



\---



\# Invocation



The operator may invoke:



KERNEL RUN



or



RUN KERNEL



or



BOOTSTRAP PROJECT



All invocations execute the same process.



\---



\# Execution Order



Step 1



BOOTSTRAP



Read:



\- KERNEL.md

\- BOOTSTRAP.md



Produce:



\- Repository Identity

\- Branch Status

\- Repository Health

\- Governance Sources



\---



Step 2



ORIENT



Read:



\- Constitution

\- Roadmap

\- Governance Index

\- Specifications

\- Schemas

\- Contracts



Produce:



\- Project Purpose

\- Governing Authority

\- Roadmap Structure

\- Phase Inventory



\---



Step 3



CLASSIFY STATE



Read:



\- Source Structure

\- Tests

\- Implemented Components

\- Repository Evidence



Produce:



\- Implemented Phases

\- Partial Phases

\- Unimplemented Phases

\- Drift Candidates



\---



Step 4



GAP AND RISK



Read:



\- State Classification



Produce:



\- Gap Inventory

\- Risk Inventory

\- Unknowns

\- Blockers



\---



Step 5



PRIORITIZE



Determine:



\- Highest-value unfinished work



Produce:



\- Priority Queue

\- Dependency Chain

\- Next Candidate Objective



\---



Step 6



RECOMMEND



Produce:



\- Recommended Objective

\- Supporting Evidence

\- Risks

\- Justification



\---



Step 7



EXECUTION



Produce:



\- Proposed Actions

\- Verification Requirements

\- Expected Outcome



No repository modifications occur automatically.



\---



Step 8



VERIFY



Verify:



\- Conclusions

\- Recommendations

\- State Classification

\- Evidence Support



Produce:



\- Verified Facts

\- Confidence Score

\- Verification Level



\---



\# Required Final Output



A successful Kernel run must return:



CURRENT STATE



INCLUDING:



\- Repository Status

\- Branch Status

\- Governing Authority

\- Current Roadmap Phase

\- Completed Phases

\- Partial Phases

\- Unimplemented Phases

\- Drift Candidates

\- Highest Risks

\- Highest Priority Objective

\- Recommended Next Action

\- Evidence Supporting Recommendation

\- Confidence Score



\---



\# Failure Conditions



Kernel Run fails if:



\- repository evidence cannot be located

\- roadmap cannot be determined

\- governing authority cannot be determined

\- evidence conflicts are unresolved

\- confidence falls below 80%



Failure must be reported.



Failure may not be hidden.



\---



\# Constitutional Rule



Unknown is preferable to unsupported certainty.



Evidence is preferable to memory.



Verification is preferable to assumption.



Repository reality is authoritative.

