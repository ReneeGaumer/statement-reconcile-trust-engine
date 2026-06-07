\# Verification Loop



Status: AGENT LAYER

Parent: .agent/kernel/EXECUTION.md



\## Purpose



Verify that conclusions, recommendations, and proposed actions are supported by repository evidence.



Verification is mandatory.



No recommendation becomes trusted without verification.



\## Inputs



Required:



\- Bootstrap Output

\- Orientation Output

\- State Classification Output

\- Gap/Risk Output

\- Prioritization Output

\- Recommendation Output

\- Execution Output



\## Verification Principles



Verify before concluding.



Verify before implementing.



Verify before classifying.



Verify before claiming completion.



Verify before recommending next work.



Unknown is preferable to unsupported certainty.



\## Verification Sources



Repository Evidence:



\- source code

\- tests

\- specifications

\- schemas

\- contracts

\- workflows

\- governance records

\- roadmap records

\- constitution



Git Evidence:



\- commit history

\- branch status

\- repository cleanliness

\- repository structure



\## Verification Levels



Level 0

\- Unverified



Level 1

\- Single-source verified



Level 2

\- Multi-source verified



Level 3

\- Cross-artifact verified



Level 4

\- Courtroom-test verified



\## Required Outputs



Verified Facts



Unverified Assumptions



Conflicts



Evidence References



Confidence Score



Verification Level



Courtroom Test Status



\## Courtroom Test



Can an independent reviewer reconstruct:



\- what was concluded

\- why it was concluded

\- what evidence supports it

\- what remains unknown



If not, verification fails.



\## Stop Conditions



Stop if:



\- evidence conflicts

\- verification fails

\- confidence is below 80%

\- courtroom test cannot be satisfied

