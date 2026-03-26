# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

We designed a modular system using four main classes: Owner, Pet, Task, and Scheduler. The Owner class manages multiple pets, each Pet maintains its own list of tasks, and the Task class represents individual activities with attributes like description, time, duration, priority, frequency, and completion status. The Scheduler acts as the central logic component that retrieves tasks, sorts them, filters them, detects conflicts, generates daily plans, and explains them. Copilot AI reviewed the system and confirmed that class initialization, type hints, and relationships are coherent with our UML design.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After AI review, we refined the design to address potential bottlenecks. Notable considerations include:

- get_all_tasks exists in both Owner and Scheduler, which could duplicate logic; careful delegation is needed.

- filter_tasks currently uses free strings for status, which may lead to typos; a constrained type could improve reliability.

- time is stored as a string, so strict formatting is necessary for sorting and conflict detection.

- Methods like get_tasks and get_all_tasks expose internal lists; future improvements could include remove_task, remove_pet, or update_time to manage data safely.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

At this stage, the scheduler is designed to consider key constraints such as task time, duration, and priority level. Priority helps determine which tasks are more important, while time ensures tasks are organized chronologically. These constraints were chosen because they are the most essential factors for building a clear and practical daily schedule for a pet owner.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One planned tradeoff is simplifying conflict detection by checking for tasks scheduled at the same exact time rather than handling overlapping durations. This approach is easier to implement and sufficient for the scope of this project, even though it does not capture more complex scheduling conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools such as Copilot to help brainstorm the system design, generate the initial UML diagram, and refine the class structure. The most helpful prompts were those that clearly defined constraints, such as asking the AI to simplify the design and avoid unnecessary complexity. This allowed me to quickly generate a strong starting point and then iteratively improve it.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One instance where I did not accept the AI’s suggestion as-is was when it generated a UML design with extra attributes (such as IDs and contact details) and overly complex methods. I evaluated the design against the project requirements and removed anything that was not necessary. This helped keep the system focused, simpler to implement, and aligned with the assignment goals.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- **Behaviors tested:**
  - Task completion (`mark_complete`) updates the task status correctly and is idempotent.
  - Adding tasks to a pet updates the pet’s task list.
  - `get_tasks` returns a copy of the list, preventing external mutation of internal data.
  - Adding multiple tasks to a pet works as expected.
- **Why important:** These tests verify the integrity of the core data structures and ensure that the fundamental operations of the system—tracking tasks and pets—behave correctly before integrating more complex scheduling logic or UI components.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- **Confidence level:** High. The scheduler correctly retrieves, sorts, filters, detects conflicts, and generates daily plans in all tested scenarios.
- **Next edge cases to test:**
  - Tasks with identical start times or overlapping durations across multiple pets.
  - Tasks with invalid or malformed time strings.
  - Tasks with unusual priorities or frequencies.
  - Scheduler behavior with no pets, no tasks, or extremely large task lists.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- The modular design of the core classes (Owner, Pet, Task, Scheduler) allowed rapid development and testing.
- Using AI to generate and refine the UML, skeletons, and test scaffolds accelerated the implementation while keeping the design consistent.
- The CLI demo and automated tests gave immediate feedback, confirming that tasks, pets, and scheduling logic work together correctly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- Introduce stricter type checks and enums for task status and priority to reduce potential errors.
- Expand Scheduler capabilities to handle more complex rules, such as recurring tasks, multi-pet coordination, and dynamic rescheduling.
- Improve the user-facing output formatting for clarity and include pet names consistently in all views.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- Clear system decomposition into modular classes makes it easier to implement, test, and extend functionality.
- AI can accelerate design and implementation, but human judgment is crucial for verifying logic, enforcing best practices, and maintaining consistency.
