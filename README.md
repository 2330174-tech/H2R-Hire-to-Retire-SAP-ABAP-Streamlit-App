# SAP H2R Employee Lifecycle Project

This project now includes both:

- an end-to-end `Hire to Retire (H2R)` implementation blueprint for `SAP HCM / SAP HR`
- a simple runnable `college project demo app` built with `Streamlit`
- a practical `SAP ABAP in VS Code` setup reference

It is designed to help you start faster with:

- process scope definition
- SAP HR infotype mapping
- technical design and object naming
- ABAP starter templates
- a runnable local H2R prototype
- test scenarios
- VS Code configuration for ABAP-oriented work

## Run The Demo App

This is the fastest way to execute and show the project during a demo or viva.

### Command
```bash
.venv/bin/streamlit run sap-h2r-hcm-project/demo_app.py
```
```bash
streamlit run sap-h2r-hcm-project/demo_app.py
```

### What the app shows

- `Dashboard` with employee register and metrics
- `Hire` employee form
- `Transfer / Promotion` form
- `Leave Management` form
- `Separation` form
- `Retirement` form
- local JSON-based data persistence for simple demo use

### Demo data

The app auto-creates sample employee data in:

```text
sap-h2r-hcm-project/data/employees.json
```

You can reset the demo data from the app sidebar.

## 1. Project Scope

The H2R lifecycle in this starter covers the full employee journey:

1. Requisition handoff to HR administration
2. Pre-hiring checks and employee creation
3. Hiring action execution in SAP HR
4. Organizational assignment and position alignment
5. Compensation and benefits enrollment
6. Time management and leave processing
7. Employee self-service and manager self-service touchpoints
8. Transfers, promotions, and organizational changes
9. Separation processing
10. Retirement processing and post-retirement closure

## 2. Key SAP HR Areas Included

- `PA` Personnel Administration
- `OM` Organizational Management
- `TM` Time Management
- `Payroll` integration checkpoints
- `Benefits` integration checkpoints
- `Workflow / approvals`
- `Interfaces` to downstream systems

## 3. Suggested Infotype Coverage

| Process | Example Infotypes |
|---|---|
| Hire | `0000`, `0001`, `0002`, `0006`, `0007`, `0008`, `0009` |
| Job change | `0000`, `0001`, `0007`, `0008` |
| Leave | `2001`, `2002`, `0007` |
| Separation | `0000`, `0001`, `0041` |
| Retirement | `0000`, `0001`, `0041`, `0008` |

## 4. Folder Structure

```text
sap-h2r-hcm-project/
  README.md
  demo_app.py
  abaplint.jsonc
  data/
    employees.json
  config/
    project-setup.md
  docs/
    h2r-lifecycle-overview.md
    h2r-technical-design.md
    h2r-test-scenarios.md
  abap/
    src/
      zif_h2r_constants.intf.abap
      zcl_h2r_employee_lifecycle.clas.abap
      zhr_h2r_employee_lifecycle_demo.prog.abap
```

## 5. VS Code Setup For SAP ABAP

Use VS Code for local editing, linting, repository work, and optional SAP connection workflows.

Recommended extensions in this workspace:

- `larshp.vscode-abap`
- `larshp.vscode-abaplint`
- `murbani.vscode-abap-remote-fs`
- `larshp.vscode-abap-artifacts`

### Practical Setup Steps

1. Open this workspace in VS Code.
2. Install the recommended extensions.
3. Open `Settings` and confirm the workspace settings from `.vscode/settings.json`.
4. Configure your SAP system connection for `ABAP FS`.
5. Open the `abap/` folder files and verify ABAP syntax highlighting.
6. Run `abaplint` from the extension to catch naming and syntax issues early.
7. Move finalized objects into your SAP system transport workflow.

### Example ABAP FS Connection Snippet

Add the connection in your VS Code settings when your SAP landscape is ready:

```json
{
  "abapfs.remote": {
    "DEV_HR": {
      "url": "https://your-sap-host:44300",
      "username": "YOUR_USER",
      "password": "YOUR_PASSWORD",
      "client": "100",
      "language": "EN",
      "allowSelfSigned": false
    }
  }
}
```

## 6. Delivery Approach

Suggested implementation phases:

1. `Foundation`
Define enterprise structure, number ranges, actions, reasons, feature switches, and security roles.

2. `Hire`
Build hiring action templates, validations, approvals, and master data defaulting.

3. `Manage`
Enable transfers, promotions, leave, position updates, payroll-impacting changes, and workflow notifications.

4. `Separate and Retire`
Standardize termination reasons, final payroll controls, clearance steps, and retirement-specific actions.

5. `Reporting and Audit`
Add HR operational reports, reconciliation jobs, and audit logs.

## 7. Important Design Note

For productive enterprise ABAP development, many SAP customers still use `ABAP Development Tools (ADT) in Eclipse` as the primary SAP-supported ABAP IDE. VS Code is still very useful for local source management, linting, documentation, Fiori/UI work, and community-based ABAP workflows.

Read the detailed design next:

- [Lifecycle overview](/Users/as-mac-1316/Documents/New%20project/sap-h2r-hcm-project/docs/h2r-lifecycle-overview.md)
- [Technical design](/Users/as-mac-1316/Documents/New%20project/sap-h2r-hcm-project/docs/h2r-technical-design.md)
- [Test scenarios](/Users/as-mac-1316/Documents/New%20project/sap-h2r-hcm-project/docs/h2r-test-scenarios.md)
- [Project setup checklist](/Users/as-mac-1316/Documents/New%20project/sap-h2r-hcm-project/config/project-setup.md)
