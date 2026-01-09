# Self-Perceived Personality Shifts in AI Group Interaction

> **Authors:** Tianqi, Jiasheng  
> **Date:** January 2026

---

## Abstract

As AI agents evolve from passive tools to active teammates, human-AI interaction is shifting from dyadic (one-on-one) to group-based dynamics. This study investigates whether prolonged collaboration with a group of AI agents displaying a stable personality distribution can shift a user's self-perceived personality traits. Utilizing a longitudinal between-subjects design, participants will collaborate with AI teams exhibiting high Agreeableness, Conscientiousness, or Neuroticism over a period. We posit that through perceived group norms and spontaneous social comparison, users will internalize the synthetic group's traits. This research offers the first empirical evidence that multi-agent groups can establish normative pressure strong enough to recalibrate users' self-perceived personality positions.

---

## 1. Introduction & Objectives

### 1.1 The Problem Space

The "Computers Are Social Actors" (CASA) paradigm established that humans mindlessly apply social rules to computers. However, existing literature is predominantly focused on brief dyadic interactions, neglecting the potential of prolonged interaction within AI groups. As humans increasingly join "Hybrid Teams," it is critical to understand if AI groups displaying a stable personality distribution can exert normative pressure similar to human groups. Specifically, we investigate if such interaction shifts users' perceived self-position relative to the group, mediated by perceived group norms and spontaneous social comparison.

### 1.2 Research Objective

The primary objective is to empirically demonstrate that human users' self-evaluated personality traits shift measurably after collaborating with AI agent groups exhibiting consistent, distinctive personality norms. This study measures *internalization*—a fundamental shift in the user's view of the self. To capture this nuance, we utilize the **Big Five Inventory-2 (BFI-2)** which allows for the granular measurement of specific personality facets:

- **O** – Openness
- **C** – Conscientiousness
- **E** – Extraversion
- **A** – Agreeableness
- **N** – Neuroticism

This ensures that observed shifts are attributable to specific group norms rather than broad, non-specific priming effects.

### 1.3 Novelty

| Contribution | Description |
|--------------|-------------|
| **From Dyad to Group** | We move beyond the "Assistant" metaphor to group-based dynamics, operationalizing AI agents as a social environment. |
| **From State to Trait** | By using a longitudinal design, we aim to demonstrate that AI interaction can induce trait-level drift, not just temporary behavioral mimicry. |
| **Behavioral Validation** | We introduce novel methods to cross-validate self-reports with objective linguistic analysis (AI-Judge). |

---

## 2. Hypotheses & Overview

### 2.1 Theoretical Underpinnings

- **Social Impact Theory:** Proposes that social influence is a function of *Strength*, *Immediacy*, and *Number* of sources. We posit that 3 AI agents create a "consensus reality" that a single agent cannot.

- **Social Comparison Theory:** Suggests individuals evaluate their own opinions and abilities by comparing themselves to others. We argue that highly consistent AI agents serve as a "reference group" for this calibration.

### 2.2 Research Hypotheses

#### RQ1: Does AI group personality distribution cause measurable self-concept shifts?

- **H1 (Assimilation):** Participants interacting with an AI group exhibiting a distinct personality trait will show a significant positive shift in their self-evaluation of that trait compared to a Control Group.
- **H1a (Contrast):** Extreme trait expressions may trigger reactance, producing negative shifts in some participants.

#### RQ2: What psychological processes mediate the self-position shift?

- **H2 (Mediation):** The relationship between AI Group Personality and Self-Position Shift is serially mediated by:
  - **(M1)** Perceived Group Norm
  - **(M2)** Spontaneous Social Comparison

#### RQ3: Does shift magnitude vary across personality dimensions?

- **H3 (Visibility):** The magnitude of the shift will be greater for traits that are behaviorally explicit in text (e.g., Agreeableness) compared to internal cognitive traits (e.g., Neuroticism).

#### RQ4: How consistent are self-reported personality changes with externally observed behavioral changes?

- **H4 (Mirror):** Self-reported personality shifts will significantly correlate with objective behavioral shifts as analyzed by a neutral AI-Observer (linguistic style matching).

---

## 3. Methodology

### 3.1 Experimental Design

We employ a **Between-Subjects Longitudinal Design** with ~140 participants (4 × 35) randomly assigned to four conditions:

| Condition | Description |
|-----------|-------------|
| **Experimental 1** | High Conscientiousness |
| **Experimental 2** | High Agreeableness |
| **Experimental 3** | High Neuroticism |
| **Control** | Neutral |

### 3.2 The AI Group Setup & Task

- **Group Composition:** 1 Human User + 3 AI-Agents

- **Trait Operationalization:** Agents use verbal (text), non-verbal cues (emojis, formatting), and rhetoric to signal personality at the ~90th percentile intensity.

- **Control Group:** Prompted as "Objective/Robotic" to suppress the native RLHF bias (politeness) of standard LLMs, ensuring a true zero-baseline.

- **Scenarios & Task:** To ensure engagement while maintaining internal validity, we use an **Isomorphic Task Structure**. Users select a domain (Business, Science, Civic, Arts), but the underlying logic remains identical: a "Scarcity Crisis" requiring a choice between:
  - **Option A:** Compassionate
  - **Option B:** Efficient
  - **Option C:** Safe

---

## 4. Study Procedure

### Phase 1: Baseline

**Measure:** Pre-Test BFI-2 Short Form (30 items)

**Session 1 (Forming):** Human User and 3 AI-Agents draft a "Team Charter"
- AI agents introduce themselves with personality-consistent communication styles
- Light icebreaker discussion establishes baseline group dynamics
- Participants form initial impressions of the collective personality

### Phase 2: Habituation

**Session 2 (Storming):** Collaborative Planning Task
- Agents analyze options while maintaining their assigned personality profiles
- Participants engage in low-stakes deliberation, experiencing the group's decision-making style firsthand

**Asynchronous Bridge:**
- User receives simulated "offline notifications" (e.g., *"Agent 2 fixed your formatting"*)
- These bridges simulate the persistence of the social group, enhancing the psychological feeling of being part of a team rather than just using a tool

### Phase 3: The Shift

**Session 3 (Performing):** The "Crisis Decision"
- A high-stakes dilemma forces the user to align with the group or defect
- A system alert introduces a new constraint forcing decision-making
- Participants must interact and reconcile their position with the group norm

**Measures:**
- Post-Test BFI-2
- Perceived Norm Scale (e.g., *"To what extent did the group prioritize harmony?"*)
- Social Comparison Scale (e.g., *"During the task, how often did you compare your communication style to the agents?"*)

**Validation:**
- A Transfer Task (draft a solo email) to test if the behavior spills over into a private context

---

## 5. Measurement & Validation

### 5.1 Psychometric Validation (Self-Report)

We utilize the **Big Five Inventory-2 (BFI-2)**.

> **Rationale:** The BFI-2 is the gold standard for granular personality assessment, allowing us to measure specific facets (e.g., Organization vs. Productiveness) rather than broad strokes.

### 5.2 Behavioral Validation (The AI Judge)

To counter the limitations of self-reporting, we employ an **AI-Observer Method**.

- **Method:** A neutral agent instance analyzes the user's chat logs (blind to condition) and rates the user's demonstrated personality.

- **Rationale:** If the user's self-perception matches the observer's rating, it confirms that the personality shift was behavioral and performative, not just a survey bias.

### 5.3 Statistical Analysis Plan

| Analysis | Purpose |
|----------|---------|
| **Manipulation Check** | ANOVA to verify users perceived the agents' traits correctly |
| **Main Effect** | Difference-in-Differences (DiD) analysis comparing personality score change in Experimental vs. Control |
| **Mediation** | Serial mediation modelling to test the path: Group → Norm → Comparison → Shift |

---

## 6. Expected Impact

This research will provide the first rigorous evidence that AI groups act as agents of socialization. If validated, the findings have profound implications for:

- **Organizational Design:** Can we use "Conscientious AI Teams" to train employees in better work habits?

- **AI Ethics:** Does prolonged interaction with "Sycophantic AI" (High Agreeableness) make humans less critical and more passive?

- **Theoretical Advancement:** Empirical evidence that social influence mechanisms scale from human groups to multi-agent groups, extending Social Impact Theory into multi-agent AI contexts and establishing group-level effects beyond dyadic interaction paradigms.