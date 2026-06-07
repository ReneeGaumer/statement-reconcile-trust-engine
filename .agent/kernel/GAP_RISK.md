\# Gap / Risk Loop



Status: AGENT LAYER

Parent: .agent/kernel/STATE\_CLASSIFICATION.md



\## Purpose



Identify repository gaps and risks from evidence before any objective is selected.



The loop distinguishes incomplete work from drift.



\## Inputs



Required:



\* Evidence Loop Output

\* Orientation Loop Output

\* State Classification Output

\* Roadmap

\* Constitution

\* Specifications

\* Source structure

\* Test structure



\## Gap Classifications



Each gap must be classified as exactly one:



\* NOT\_STARTED

\* SPECIFIED\_ONLY

\* PARTIALLY\_IMPLEMENTED

\* IMPLEMENTED\_UNTESTED

\* IMPLEMENTED\_TESTED

\* VERIFIED\_COMPLETE

\* UNDEFINED\_PHASE

\* DRIFT\_CANDIDATE

\* CONFLICT



\## Rules



Incomplete does not mean drift.



Missing implementation does not mean failure if the roadmap phase has not been reached.



A drift candidate requires evidence that repository reality conflicts with roadmap, constitution, specification, or tests.



Unknowns must be recorded as UNKNOWN.



\## Risk Categories



\* Repository Health Risk

\* Architectural Risk

\* Governance Risk

\* Trust Risk

\* Auditability Risk

\* Reconstructibility Risk

\* Verification Risk

\* Scope Risk



\## Required Outputs



Gap Inventory



Risk Inventory



Drift Candidates



Unknowns



Blocked Areas



Highest-Risk Area



Confidence Score



\## Stop Conditions



Stop if:



\* gap cannot be classified

\* risk source is unknown

\* evidence is insufficient

\* confidence is below 80%



