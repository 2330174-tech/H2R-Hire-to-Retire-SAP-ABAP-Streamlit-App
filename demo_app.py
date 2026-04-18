from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_FILE = DATA_DIR / "employees.json"


@dataclass
class Employee:
    employee_id: str
    full_name: str
    gender: str
    date_of_birth: str
    date_of_joining: str
    department: str
    designation: str
    location: str
    manager_name: str
    email: str
    phone: str
    basic_salary: float
    status: str
    leave_balance: int
    last_action: str
    updated_at: str


def ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        return

    seed_employees = [
        Employee(
            employee_id="EMP1001",
            full_name="Aarav Sharma",
            gender="Male",
            date_of_birth="2000-04-12",
            date_of_joining="2025-07-01",
            department="Human Resources",
            designation="HR Executive",
            location="Mumbai",
            manager_name="Priya Nair",
            email="aarav.sharma@example.com",
            phone="9876543210",
            basic_salary=35000,
            status="Active",
            leave_balance=18,
            last_action="Hire",
            updated_at=current_timestamp(),
        ),
        Employee(
            employee_id="EMP1002",
            full_name="Meera Patel",
            gender="Female",
            date_of_birth="1998-09-21",
            date_of_joining="2024-11-15",
            department="Finance",
            designation="Analyst",
            location="Pune",
            manager_name="Rohan Desai",
            email="meera.patel@example.com",
            phone="9988776655",
            basic_salary=42000,
            status="Active",
            leave_balance=12,
            last_action="Hire",
            updated_at=current_timestamp(),
        ),
    ]
    save_employees([asdict(employee) for employee in seed_employees])


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_employees() -> list[dict[str, Any]]:
    ensure_data_file()
    return json.loads(DATA_FILE.read_text())


def save_employees(employees: list[dict[str, Any]]) -> None:
    DATA_FILE.write_text(json.dumps(employees, indent=2))


def generate_employee_id(employees: list[dict[str, Any]]) -> str:
    if not employees:
        return "EMP1001"
    numbers = []
    for employee in employees:
        try:
            numbers.append(int(employee["employee_id"].replace("EMP", "")))
        except (KeyError, ValueError):
            continue
    next_number = max(numbers, default=1000) + 1
    return f"EMP{next_number}"


def find_employee(employees: list[dict[str, Any]], employee_id: str) -> dict[str, Any] | None:
    for employee in employees:
        if employee["employee_id"] == employee_id:
            return employee
    return None


def employee_table_rows(employees: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for employee in employees:
        rows.append(
            {
                "Employee ID": employee["employee_id"],
                "Name": employee["full_name"],
                "Department": employee["department"],
                "Designation": employee["designation"],
                "Location": employee["location"],
                "Salary": f"{employee['basic_salary']:.2f}",
                "Leave Balance": employee["leave_balance"],
                "Status": employee["status"],
                "Last Action": employee["last_action"],
                "Updated At": employee["updated_at"],
            }
        )
    return rows


def add_timeline_event(message: str) -> None:
    st.session_state.setdefault("timeline", [])
    st.session_state.timeline.insert(0, f"{current_timestamp()} - {message}")
    st.session_state.timeline = st.session_state.timeline[:20]


def render_dashboard(employees: list[dict[str, Any]]) -> None:
    active_count = sum(1 for employee in employees if employee["status"] == "Active")
    retired_count = sum(1 for employee in employees if employee["status"] == "Retired")
    separated_count = sum(1 for employee in employees if employee["status"] == "Separated")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", len(employees))
    col2.metric("Active", active_count)
    col3.metric("Retired", retired_count)
    col4.metric("Separated", separated_count)

    st.subheader("Department Distribution")
    department_counts = Counter(employee["department"] for employee in employees)
    if department_counts:
        st.bar_chart(department_counts)
    else:
        st.info("No employee data available yet.")

    st.subheader("Employee Register")
    st.dataframe(employee_table_rows(employees), use_container_width=True, hide_index=True)


def render_hire_form(employees: list[dict[str, Any]]) -> None:
    st.subheader("Hire Employee")
    with st.form("hire_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            date_of_birth = st.date_input("Date of Birth", value=date(2000, 1, 1))
            department = st.selectbox(
                "Department",
                ["Human Resources", "Finance", "IT", "Sales", "Operations", "Marketing"],
            )
            designation = st.text_input("Designation")
            manager_name = st.text_input("Manager Name")
        with col2:
            date_of_joining = st.date_input("Date of Joining", value=date.today())
            location = st.selectbox("Location", ["Mumbai", "Pune", "Bengaluru", "Hyderabad", "Chennai"])
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            basic_salary = st.number_input("Basic Salary", min_value=0.0, value=25000.0, step=1000.0)
            leave_balance = st.number_input("Opening Leave Balance", min_value=0, value=12, step=1)

        submitted = st.form_submit_button("Hire Employee", use_container_width=True)

    if not submitted:
        return
    if not full_name.strip() or not designation.strip() or not email.strip():
        st.error("Full name, designation, and email are mandatory.")
        return

    employee = Employee(
        employee_id=generate_employee_id(employees),
        full_name=full_name.strip(),
        gender=gender,
        date_of_birth=str(date_of_birth),
        date_of_joining=str(date_of_joining),
        department=department,
        designation=designation.strip(),
        location=location,
        manager_name=manager_name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        basic_salary=basic_salary,
        status="Active",
        leave_balance=int(leave_balance),
        last_action="Hire",
        updated_at=current_timestamp(),
    )
    employees.append(asdict(employee))
    save_employees(employees)
    add_timeline_event(f"Hired employee {employee.full_name} ({employee.employee_id})")
    st.success(f"Employee {employee.full_name} hired successfully with ID {employee.employee_id}.")


def render_transfer_form(employees: list[dict[str, Any]]) -> None:
    st.subheader("Transfer / Promotion")
    active_employees = [employee for employee in employees if employee["status"] == "Active"]
    if not active_employees:
        st.info("No active employees available for transfer.")
        return

    with st.form("transfer_form"):
        employee_id = st.selectbox("Employee", [employee["employee_id"] for employee in active_employees])
        new_department = st.selectbox(
            "New Department",
            ["Human Resources", "Finance", "IT", "Sales", "Operations", "Marketing"],
        )
        new_designation = st.text_input("New Designation")
        new_location = st.selectbox("New Location", ["Mumbai", "Pune", "Bengaluru", "Hyderabad", "Chennai"])
        salary_change = st.number_input("Revised Salary", min_value=0.0, value=40000.0, step=1000.0)
        submitted = st.form_submit_button("Process Transfer", use_container_width=True)

    if not submitted:
        return

    employee = find_employee(employees, employee_id)
    if employee is None:
        st.error("Employee not found.")
        return

    employee["department"] = new_department
    employee["designation"] = new_designation.strip() or employee["designation"]
    employee["location"] = new_location
    employee["basic_salary"] = salary_change
    employee["last_action"] = "Transfer / Promotion"
    employee["updated_at"] = current_timestamp()
    save_employees(employees)
    add_timeline_event(f"Transferred employee {employee['full_name']} ({employee_id})")
    st.success(f"Transfer updated successfully for {employee['full_name']}.")


def render_leave_form(employees: list[dict[str, Any]]) -> None:
    st.subheader("Leave Management")
    active_employees = [employee for employee in employees if employee["status"] == "Active"]
    if not active_employees:
        st.info("No active employees available for leave processing.")
        return

    with st.form("leave_form"):
        employee_id = st.selectbox("Employee", [employee["employee_id"] for employee in active_employees])
        leave_type = st.selectbox("Leave Type", ["Casual Leave", "Sick Leave", "Earned Leave", "Maternity Leave"])
        leave_days = st.number_input("Number of Days", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("Apply Leave", use_container_width=True)

    if not submitted:
        return

    employee = find_employee(employees, employee_id)
    if employee is None:
        st.error("Employee not found.")
        return

    if employee["leave_balance"] < leave_days:
        st.error("Leave balance is not sufficient.")
        return

    employee["leave_balance"] -= int(leave_days)
    employee["last_action"] = f"Leave - {leave_type}"
    employee["updated_at"] = current_timestamp()
    save_employees(employees)
    add_timeline_event(
        f"Approved {leave_days} day(s) of {leave_type} for {employee['full_name']} ({employee_id})"
    )
    st.success(f"Leave applied successfully. Remaining balance: {employee['leave_balance']} day(s).")


def render_separation_form(employees: list[dict[str, Any]]) -> None:
    st.subheader("Separation")
    active_employees = [employee for employee in employees if employee["status"] == "Active"]
    if not active_employees:
        st.info("No active employees available for separation.")
        return

    with st.form("separation_form"):
        employee_id = st.selectbox("Employee", [employee["employee_id"] for employee in active_employees])
        reason = st.selectbox("Reason", ["Resignation", "Termination", "Absconding", "Contract End"])
        submitted = st.form_submit_button("Process Separation", use_container_width=True)

    if not submitted:
        return

    employee = find_employee(employees, employee_id)
    if employee is None:
        st.error("Employee not found.")
        return

    employee["status"] = "Separated"
    employee["last_action"] = f"Separation - {reason}"
    employee["updated_at"] = current_timestamp()
    save_employees(employees)
    add_timeline_event(f"Separated employee {employee['full_name']} ({employee_id}) due to {reason}")
    st.success(f"Separation processed successfully for {employee['full_name']}.")


def render_retirement_form(employees: list[dict[str, Any]]) -> None:
    st.subheader("Retirement")
    eligible_employees = [employee for employee in employees if employee["status"] == "Active"]
    if not eligible_employees:
        st.info("No active employees available for retirement.")
        return

    with st.form("retirement_form"):
        employee_id = st.selectbox("Employee", [employee["employee_id"] for employee in eligible_employees])
        retirement_date = st.date_input("Retirement Date", value=date.today())
        submitted = st.form_submit_button("Process Retirement", use_container_width=True)

    if not submitted:
        return

    employee = find_employee(employees, employee_id)
    if employee is None:
        st.error("Employee not found.")
        return

    employee["status"] = "Retired"
    employee["last_action"] = f"Retirement - {retirement_date}"
    employee["updated_at"] = current_timestamp()
    save_employees(employees)
    add_timeline_event(f"Retired employee {employee['full_name']} ({employee_id})")
    st.success(f"Retirement processed successfully for {employee['full_name']}.")


def render_timeline() -> None:
    st.subheader("Recent H2R Activity")
    timeline = st.session_state.get("timeline", [])
    if not timeline:
        st.info("No lifecycle activity recorded in this session yet.")
        return
    for event in timeline:
        st.write(event)


def main() -> None:
    st.set_page_config(
        page_title="SAP H2R Employee Lifecycle Demo",
        page_icon=":office_worker:",
        layout="wide",
    )

    st.title("SAP H2R Employee Lifecycle Demo")
    st.caption(
        "A college-project style local demo for Hire, Transfer, Leave, Separation, and Retirement."
    )

    employees = load_employees()

    with st.sidebar:
        st.header("Modules")
        module = st.radio(
            "Choose a process",
            ["Dashboard", "Hire", "Transfer", "Leave", "Separation", "Retirement", "Project Notes"],
        )
        if st.button("Reset Demo Data", use_container_width=True):
            if DATA_FILE.exists():
                DATA_FILE.unlink()
            ensure_data_file()
            st.session_state.timeline = []
            st.success("Demo data has been reset.")
            st.rerun()

    if module == "Dashboard":
        render_dashboard(employees)
        render_timeline()
    elif module == "Hire":
        render_hire_form(employees)
    elif module == "Transfer":
        render_transfer_form(employees)
    elif module == "Leave":
        render_leave_form(employees)
    elif module == "Separation":
        render_separation_form(employees)
    elif module == "Retirement":
        render_retirement_form(employees)
    else:
        st.subheader("Project Notes")
        st.markdown(
            """
            This demo simulates a simplified SAP HR `Hire to Retire` lifecycle:

            - `Hire`: create a new employee record
            - `Transfer`: update department, designation, location, and salary
            - `Leave`: reduce leave balance with validation
            - `Separation`: mark employee as separated
            - `Retirement`: mark employee as retired

            The records are stored in a local JSON file for demonstration purposes.
            """
        )
        st.code("streamlit run sap-h2r-hcm-project/demo_app.py", language="bash")


if __name__ == "__main__":
    main()
