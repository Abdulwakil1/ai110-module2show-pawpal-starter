import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# ----------------------------
# SESSION STATE (Persistence)
# ----------------------------
if "owner_name" not in st.session_state:
    st.session_state["owner_name"] = "Jordan"

owner_name = st.text_input(
    "Owner name",
    value=st.session_state["owner_name"],
    key="owner_name",
)

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(owner_name)
else:
    st.session_state["owner"].name = owner_name

owner = st.session_state["owner"]

# ----------------------------
# PET SETUP
# ----------------------------
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "pet" not in st.session_state:
    st.session_state["pet"] = Pet(pet_name, species)
    owner.add_pet(st.session_state["pet"])
else:
    st.session_state["pet"].name = pet_name
    st.session_state["pet"].species = species

pet = st.session_state["pet"]

# ----------------------------
# TASK INPUT
# ----------------------------
st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    task_title = st.text_input("Task title", value="Morning walk")

with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

with col4:
    task_time = st.time_input("Task time")

task_time_str = task_time.strftime("%H:%M")

if st.button("Add task"):
    new_task = Task(
        description=task_title,
        time=task_time_str,
        duration=int(duration),
        priority=priority,
        frequency="Daily",
    )
    pet.add_task(new_task)
    st.success(f"Task '{task_title}' added to {pet.name}!")

# ----------------------------
# DISPLAY TASKS
# ----------------------------
tasks = pet.get_tasks()

if tasks:
    st.write("Current Tasks:")
    for t in tasks:
        status = "Done" if t.is_complete else "Pending"
        st.write(f"- {t.description} ({t.duration} min, {t.priority}, {status})")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# # ----------------------------
# # SCHEDULER
# # ----------------------------
# st.subheader("Schedule")

# if st.button("Generate schedule"):
#     scheduler = Scheduler()
#     all_tasks = scheduler.get_all_tasks(owner)
#     plan = scheduler.generate_daily_plan(all_tasks)
#     conflicts = scheduler.detect_conflicts(plan)

#     """Display the backend-sorted daily plan in a table with task completion status."""
#     if plan:
#         st.caption("Tasks sorted by time, priority, and duration")

#         table_lines = [
#             "| Time | Description | Priority | Duration (min) | Status |",
#             "|---|---|---|---:|---|",
#         ]

#         for t in plan:
#             safe_description = t.description.replace("|", r"\|")
#             status_text = "✅ Complete" if t.is_complete else "⏳ Incomplete"
#             table_lines.append(
#                 f"| {t.time} | {safe_description} | {t.priority} | {t.duration} | {status_text} |"
#             )

#         st.markdown("\n".join(table_lines))
#     else:
#         st.warning("No tasks to schedule.")

#     """Show conflict diagnostics after plan generation, or confirm a conflict-free plan."""
#     if conflicts:
#         st.warning("Task conflicts detected:")
#         for first_task, second_task in conflicts:
#             st.write(
#                 f"{first_task.description} ({first_task.time}) conflicts with "
#                 f"{second_task.description} ({second_task.time})"
#             )
#     else:
#         st.success("No conflicts detected.")

#     st.markdown("### Explanation")
#     st.write(scheduler.explain_plan(plan))

# ----------------------------
# SCHEDULER
# ----------------------------
st.subheader("Schedule")

# Initialize session state (safe, no side effects)
st.session_state.setdefault("plan", [])
st.session_state.setdefault("pet", None)

# Button ONLY generates and stores data
if st.button("Generate schedule"):
    scheduler = Scheduler()
    all_tasks = scheduler.get_all_tasks(owner)
    plan = scheduler.generate_daily_plan(all_tasks)

    # Save so it persists after rerun
    st.session_state["plan"] = plan
    st.session_state["pet"] = pet

# Always read from session state
plan = st.session_state["plan"]
pet = st.session_state["pet"]

# ----------------------------
# DISPLAY (outside button)
# ----------------------------
if plan:
    scheduler = Scheduler()
    conflicts = scheduler.detect_conflicts(plan)

    st.caption("Tasks sorted by time, priority, and duration")

    table_lines = [
        "| Time | Description | Priority | Duration (min) | Status |",
        "|---|---|---|---:|---|",
    ]

    for t in plan:
        safe_description = t.description.replace("|", r"\|")
        status_text = "✅ Complete" if t.is_complete else "⏳ Incomplete"
        table_lines.append(
            f"| {t.time} | {safe_description} | {t.priority} | {t.duration} | {status_text} |"
        )

    st.markdown("\n".join(table_lines))

    # ✅ NEW: Task completion UI (safe)
    st.subheader("Mark Tasks Complete")

    for idx, task in enumerate(plan):
        checked = st.checkbox(
            f"{task.time} — {task.description}",
            value=task.is_complete,
            key=f"complete_task_{idx}_{task.time}_{task.description}",
        )

        if checked != task.is_complete:
            if checked:
                if not task.is_complete:
                    task.is_complete = True
                    new_task = task.mark_complete()

                    if new_task:
                        st.success(
                            f"'{task.description}' marked complete. Next occurrence prepared."
                        )
                    else:
                        st.info(f"'{task.description}' marked complete.")
            else:
                task.is_complete = False
                st.info(f"'{task.description}' marked as incomplete.")

            st.session_state["plan"] = plan
            st.rerun()

    # ----------------------------
    # CONFLICTS (unchanged logic)
    # ----------------------------
    if conflicts:
        st.warning("Task conflicts detected:")
        for first_task, second_task in conflicts:
            st.write(
                f"{first_task.description} ({first_task.time}) conflicts with "
                f"{second_task.description} ({second_task.time})"
            )
    else:
        st.success("No conflicts detected.")

    # ----------------------------
    # EXPLANATION (unchanged)
    # ----------------------------
    st.markdown("### Explanation")
    st.write(scheduler.explain_plan(plan))

else:
    st.warning("No tasks to schedule.")
