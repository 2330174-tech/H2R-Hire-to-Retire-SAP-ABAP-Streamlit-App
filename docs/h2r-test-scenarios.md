# H2R Test Scenarios

## Hire

1. Hire a new employee with complete mandatory data and verify infotypes `0000`, `0001`, `0002`, `0007`, `0008`, and `0009`.
2. Attempt hire without position and confirm validation failure.
3. Attempt hire with invalid payroll area and confirm message handling.

## Organization Change

1. Transfer employee to a new org unit and verify `0001`.
2. Promote employee with salary increase and verify `0008`.
3. Backdate organizational change and verify effective-date handling.

## Leave

1. Create approved annual leave and verify `2001`.
2. Create overlapping leave and verify rejection.
3. Create attendance adjustment and verify `2002`.

## Separation

1. Process voluntary resignation with future last working day.
2. Process involuntary termination and verify downstream workflow trigger.
3. Attempt separation when payroll lock prevents update and verify error handling.

## Retirement

1. Retire employee on superannuation date.
2. Retire employee with pending leave balances and verify exception message.
3. Verify retired employee is excluded from active workforce reporting after closure.

## Audit and Reporting

1. Confirm each successful action writes an audit entry.
2. Confirm failed validations are visible in the return message set.
3. Confirm report output can be filtered by effective date and action type.
