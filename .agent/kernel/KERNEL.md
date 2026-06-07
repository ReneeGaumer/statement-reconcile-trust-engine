\# Repository Kernel



Status: AGENT LAYER

Purpose: Reconstruct repository state from evidence and determine the next safest objective.



This kernel is not product logic.

It must not be imported by runtime code.

If deleted, the Trust Engine must still function unchanged.



\## Kernel Loop Stack



1\. Bootstrap Loop

2\. Evidence Loop

3\. Orientation Loop

4\. State Classification Loop

5\. Gap / Risk Loop

6\. Objective Scoring Loop

7\. Action Recommendation Loop

8\. Verification Loop

9\. Session Ledger Loop



\## Core Rules



No recommendation without evidence.

No action without classification.

No completion without verification.

No repository state may be inferred from chat memory alone.

GitHub repository state is the source of truth.



