\# Kernel Check Contract



Status: TOOLING CONTRACT



Purpose:

Produce a factual repository snapshot to reduce repeated CURRENT STATE reconstruction.



This tool is not Trust Engine logic.

This tool is not runtime code.

This tool does not determine truth, trust, reconciliation, export eligibility, or audit validity.



\## Input



A local Git repository.



\## Output



.agent/kernel/state/kernel\_state.json



\## Required Facts



The tool may collect only factual repository evidence:



\- git status

\- current branch

\- remote sync state

\- recent commits

\- tracked file inventory

\- top-level repository inventory

\- source tree summary

\- test tree summary

\- roadmap file presence

\- constitution file presence

\- pytest execution result



\## Forbidden



The tool must not:



\- recommend next work

\- prioritize objectives

\- classify trust

\- classify export readiness

\- modify engine logic

\- modify source files

\- modify tests

\- create audit conclusions

\- replace human approval

\- become part of runtime



\## Failure Behavior



If evidence cannot be collected, the tool must report:



\- missing evidence

\- failed command

\- blocked capability



Unknown is preferable to unsupported certainty.

