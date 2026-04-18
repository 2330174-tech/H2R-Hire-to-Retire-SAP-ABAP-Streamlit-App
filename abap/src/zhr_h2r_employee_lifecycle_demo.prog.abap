REPORT zhr_h2r_employee_lifecycle_demo.

PARAMETERS:
  p_pernr TYPE pernr_d OBLIGATORY,
  p_act   TYPE c LENGTH 4 OBLIGATORY,
  p_begda TYPE begda DEFAULT sy-datum,
  p_plans TYPE plans,
  p_orgeh TYPE orgeh,
  p_awart TYPE awart.

DATA lo_service TYPE REF TO zcl_h2r_employee_lifecycle.
DATA ls_input   TYPE zcl_h2r_employee_lifecycle=>ty_action_input.
DATA lt_return  TYPE zcl_h2r_employee_lifecycle=>ty_return_tab.

START-OF-SELECTION.
  CREATE OBJECT lo_service.

  ls_input-pernr       = p_pernr.
  ls_input-action_code = p_act.
  ls_input-begda       = p_begda.
  ls_input-plans       = p_plans.
  ls_input-orgeh       = p_orgeh.
  ls_input-awart       = p_awart.

  CASE p_act.
    WHEN zif_h2r_constants=>gc_action_hire.
      lo_service->hire_employee(
        EXPORTING
          is_input  = ls_input
        CHANGING
          ct_return = lt_return ).

    WHEN zif_h2r_constants=>gc_action_transfer.
      lo_service->process_org_change(
        EXPORTING
          is_input  = ls_input
        CHANGING
          ct_return = lt_return ).

    WHEN zif_h2r_constants=>gc_action_leave.
      lo_service->process_leave(
        EXPORTING
          is_input  = ls_input
        CHANGING
          ct_return = lt_return ).

    WHEN zif_h2r_constants=>gc_action_separate.
      lo_service->separate_employee(
        EXPORTING
          is_input  = ls_input
        CHANGING
          ct_return = lt_return ).

    WHEN zif_h2r_constants=>gc_action_retire.
      lo_service->retire_employee(
        EXPORTING
          is_input  = ls_input
        CHANGING
          ct_return = lt_return ).

    WHEN OTHERS.
      APPEND VALUE bapiret2(
        type    = 'E'
        id      = 'ZHR_H2R'
        number  = '099'
        message = 'Unsupported action code'
      ) TO lt_return.
  ENDCASE.

  LOOP AT lt_return ASSIGNING FIELD-SYMBOL(<ls_return>).
    WRITE: / <ls_return>-type, <ls_return>-message.
  ENDLOOP.
