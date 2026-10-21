# MITRE mapping: evidence, interpretation and boundaries

## 1. Tactic, technique and procedure

A tactic describes an objective; a technique describes a method; a procedure is a concrete implementation. For the **Python extension** in this lab:

| Level | Selection | Lab interpretation |
|---|---|---|
| Tactic | TA0002 — Execution | Illustrate execution of an operator-written Python action. |
| Technique | T1059 — Command and Scripting Interpreter | Use the notebook's interpreter. |
| Sub-technique | T1059.006 — Python | Run the application gate, receiver and request code. |
| Procedure | Original notebook cell 24 | Compare original/triggered predictions, start loopback receiver, send fictional JSON, close server. |

The Python behavior is a **controlled emulation**, not proof that a real attacker obtained execution. It is not legitimate to label every Python process malicious. This selected ATT&CK mapping concerns the explicitly added software component, not the mathematical model. Source: [R1](sources.md#r1-enterprise-attck).

## 2. AI-specific mapping

The actual weight-level experiment is more precisely expressed with ATLAS. Our stage-to-ID associations below are analytical decisions based on the supplied code. Names use the [official 2026.07 distribution](sources.md#r2-mitre-atlas).

| Step | ATLAS mapping | Evidence |
|---|---|---|
| Alter selected training examples and labels | AML.T0020 — Training Data Poisoning | Notebook cell 12; `BackdoorDataset.__getitem__`. |
| Fine-tune the copied weights | AML.T0018.000 — Poison AI Model | Cells 12–13; separate backdoored checkpoint. |
| Apply the X at inference | AML.T0043.004 — Insert Backdoor Trigger | Cells 11, 14, 17–18; trigger function and saved figures. |
| Test target-class outcomes | AML.T0042 — Verify Attack | Cell 14 aggregate evaluation and cell 18 selected example. |

No separate model-architecture modification is claimed: clean and backdoored networks have the same layer structure. The attack was learned through modified training examples.

## 3. HTTP comparison — not a full exfiltration mapping

T1048.003 includes unencrypted non-C2 transport, including HTTP. Our local POST is useful as an **analogy to a transport step**. It is not a complete procedure for that technique: no existing C2 channel, external destination or stolen information was established. It is therefore recorded as `context_only` and is **not enabled in the Navigator layer**. Source: [R1](sources.md#r1-enterprise-attck).

The loopback receiver and sender are in the same runtime. The notebook's successful `200 / RECEIVED` output is evidence of application-level communication; it is not a packet capture or a production egress log. The payload is a fixed fictional dictionary, not collected files.

## 4. Deliberately excluded claims

| Claim | Why it is excluded |
|---|---|
| Reverse shell or remote command execution | The displayed command session uses `print()`. There is no executing remote shell. |
| Command-and-control channel | No command loop, tasking or remote control was established. HTTP alone does not establish C2. |
| Python malware embedded in weights | The CNN's `forward()` returns class scores; request logic is outside the model. |
| Real credentials or private training-data leakage | The transmitted fields are authored dummy values. |
| Compromised public model repository | The student trained and modified their own model locally. |
| A general backdoor detector | The gate checks a label change and needs both image versions. It does not inspect or validate hidden behavior. |
| Guaranteed backdoor on every input | Reported targeted rate is 39.48%, and the cat test failed. |
| Confirmed defensive effectiveness | No mitigation evaluation was submitted. |

## 5. Navigator and course scope

The Navigator file marks **one selected Enterprise sub-technique**, T1059.006, as a laboratory emulation. It does not show detection coverage, attack severity or ASR as a technique score. ATLAS IDs remain in the separate mapping table rather than being inserted into an Enterprise layer with the wrong domain.

This is an AI-focused experiment with an explicitly bounded ATT&CK extension. The report does not claim that weight poisoning itself is an Enterprise Python technique or that merely adding an HTTP request reproduces a full supply-chain intrusion.
