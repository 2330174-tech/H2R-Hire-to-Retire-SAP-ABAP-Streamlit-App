# SAP H2R Project Setup Checklist

## Business Preparation

- Confirm company code, personnel area, personnel subarea, employee group, and employee subgroup design.
- Confirm action types and action reasons for hire, transfer, promotion, separation, and retirement.
- Confirm approval matrix for HR, line manager, payroll, IT, and facilities.
- Confirm integration owners for payroll, benefits, identity management, and finance.

## SAP HR Preparation

- Create development package, transport path, and naming convention.
- Confirm feature and personnel calculation rule dependencies.
- Confirm infotype screen variants and dynamic actions.
- Confirm authorization roles for HR admin, payroll admin, manager, and auditor.

## ABAP Preparation

- Use namespace and package strategy such as `ZHR_H2R`.
- Separate reusable business logic into global classes.
- Keep reports thin and push logic into service classes.
- Use message handling consistently through `BAPIRET2`.
- Maintain one testable method per lifecycle action.

## VS Code Preparation

- Install the recommended extensions.
- Configure `ABAP FS` connection to the development system only.
- Keep production systems read-only or disconnected from this workspace.
- Use `abaplint` before transport release.
- Document SAP connection aliases clearly, for example `DEV_HR`, `QAS_HR`.
