\# Bootstrap Loop



Status: AGENT LAYER

Parent: .agent/kernel/KERNEL.md



\## Purpose



Reconstruct repository state at the beginning of a session from repository evidence.



The Bootstrap Loop replaces long session-start prompts and prevents reliance on chat memory.



\## Required Evidence



The loop must inspect:



1\. Git status

2\. Current branch

3\. Remote synchronization state

4\. Recent commit history

5\. Tracked repository inventory

6\. Repository roadmap

7\. Constitution and governing specifications

8\. Source implementation structure

9\. Test structure

10\. Current test result



\## Required Classifications



The loop must classify repository state as:



\* CLEAN\_AND\_SYNCED

\* CLEAN\_AHEAD

\* DIRTY\_WORKTREE

\* TESTS\_PASSING

\* TESTS\_FAILING

\* VERIFICATION\_BLOCKED

\* ROADMAP\_ALIGNED

\* ROADMAP\_UNCLEAR

\* DRIFT\_CANDIDATE



\## Stop Conditions



Stop if:



\* Git state cannot be determined

\* Repository is dirty and the change source is unknown

\* Tests cannot be executed

\* Roadmap or governing documents cannot be found

\* Confidence is below 80%



\## Output



The Bootstrap Loop must produce:



\* verified repository status

\* verified test status

\* available roadmap evidence

\* known incomplete or undefined areas

\* next loop to run



