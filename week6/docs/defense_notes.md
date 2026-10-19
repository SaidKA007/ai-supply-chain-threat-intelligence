# Week 6 — defense notes

## A short explanation

Week 6 focuses on one ATT&CK sub-technique: T1059.006, Python, under the Execution tactic. It continues the project's model-processing topic with a small, benign experiment.

The lab uses a toy object, not a real trained model. During loading, that object can call a fixed Python function. The function only creates a text marker, so we can check whether it ran.

There are four scenarios. The baseline loads normal data without a marker. The second scenario runs the callback and completes loading. The third runs the callback but then reports an EOFError. Its marker is important because it shows that a final error does not remove an earlier side effect. The fourth rejects Pickle before loading and accepts separate JSON metadata without running the callback.

The reference run contains 24 application events and two marker files. All four scenario expectations and 15 separate code tests passed. Two scenarios demonstrate the same sub-technique, so the Navigator layer highlights only one entry.

The main limitations are the small authored examples and application-level logging. This is not a real malicious-model incident or a test of a production detection product. The supplied reference evidence was collected in the preparation environment. A personal local demonstration needs its own run.

## Questions to prepare for

**What is the difference between a tactic and a technique?**  
A tactic is the objective. A technique is the method. Here, Execution is the objective and Python is the selected method. The fixed marker callback is our concrete procedure. See README Section 2 and its MITRE sources.

**Why is S01 not mapped as an attack just because Python runs?**  
Python is also used for normal work. We map the extra callback that the lab deliberately places in S02 and S03, and label it as benign emulation.

**Does `__reduce__()` itself create the marker?**  
No. It returns the callback reference while the fixture is built. The unpickler later calls that function. The code and generated disassembly show this separation.

**Why does S03 pass even though it reports an error?**  
The expected result is a callback and marker followed by EOFError. The check passes when this exact sequence occurs.

**Did the experiment launch a reverse shell?**  
No. The callback stays inside the existing Python process. It only creates the marker file.

**What did the policy detect?**  
It did not detect malware. It rejected the Pickle format before deserialization and then accepted a different JSON fixture.

**Are these real logs or synthetic logs?**  
The scenario is authored, but these application records were emitted during actual execution. They are not fabricated victim events or independent endpoint telemetry.

**Does the result prove the Week 5 Splunk search is ineffective?**  
No. This implementation lacks the child-shell and network observations that the Week 5 correlation required. That is a coverage question for a future experiment, not a measured detection result.

**Why is the model small?**  
The question concerns when code executes, not model quality or inference speed. A tiny controlled object lets us inspect the mechanism without loading unknown models.

**Where is the evidence?**  
See `evidence/reference_run/`, the two rows of `data/attack_mapping.csv`, and `evidence/test_results.txt`. The main README links them directly and explains provenance.
