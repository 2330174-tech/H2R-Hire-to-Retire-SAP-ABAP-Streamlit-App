CLASS zcl_h2r_employee_lifecycle DEFINITION
  PUBLIC
  FINAL
  CREATE PUBLIC.

  PUBLIC SECTION.
    INTERFACES zif_h2r_constants.

    TYPES:
      BEGIN OF ty_action_input,
        pernr         TYPE pernr_d,
        action_code   TYPE c LENGTH 4,
        action_reason TYPE c LENGTH 4,
        begda         TYPE begda,
        endda         TYPE endda,
        plans         TYPE plans,
        orgeh         TYPE orgeh,
        werks         TYPE werks_d,
        btrtl         TYPE btrtl,
        persg         TYPE persg,
        persk         TYPE persk,
        abkrs         TYPE abkrs,
        trfar         TYPE trfar,
        trfgb         TYPE trfgb,
        trfgr         TYPE trfgr,
        trfst         TYPE trfst,
        lgart         TYPE lgart,
        betrg         TYPE betrg,
        awart         TYPE awart,
      END OF ty_action_input.

    TYPES ty_return_tab TYPE STANDARD TABLE OF bapiret2 WITH DEFAULT KEY.

    METHODS validate_action_input
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

    METHODS hire_employee
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

    METHODS process_org_change
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

    METHODS process_leave
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

    METHODS separate_employee
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

    METHODS retire_employee
      IMPORTING
        is_input         TYPE ty_action_input
      CHANGING
        ct_return        TYPE ty_return_tab.

  PRIVATE SECTION.
    METHODS add_message
      IMPORTING
        iv_type          TYPE bapi_mtype
        iv_id            TYPE symsgid
        iv_number        TYPE symsgno
        iv_message       TYPE bapi_msg
      CHANGING
        ct_return        TYPE ty_return_tab.

ENDCLASS.

CLASS zcl_h2r_employee_lifecycle IMPLEMENTATION.

  METHOD add_message.
    APPEND VALUE bapiret2(
      type       = iv_type
      id         = iv_id
      number     = iv_number
      message    = iv_message
    ) TO ct_return.
  ENDMETHOD.

  METHOD validate_action_input.
    IF is_input.begda IS INITIAL.
      add_message(
        EXPORTING
          iv_type    = 'E'
          iv_id      = 'ZHR_H2R'
          iv_number  = '001'
          iv_message = 'Effective start date is mandatory'
        CHANGING
          ct_return  = ct_return ).
    ENDIF.

    CASE is_input.action_code.
      WHEN zif_h2r_constants~gc_action_hire
        OR zif_h2r_constants~gc_action_transfer
        OR zif_h2r_constants~gc_action_retire
        OR zif_h2r_constants~gc_action_separate.
        IF is_input.plans IS INITIAL OR is_input.orgeh IS INITIAL.
          add_message(
            EXPORTING
              iv_type    = 'E'
              iv_id      = 'ZHR_H2R'
              iv_number  = '002'
              iv_message = 'Position and org unit are mandatory for this action'
            CHANGING
              ct_return  = ct_return ).
        ENDIF.
      WHEN OTHERS.
    ENDCASE.
  ENDMETHOD.

  METHOD hire_employee.
    validate_action_input(
      EXPORTING
        is_input  = is_input
      CHANGING
        ct_return = ct_return ).

    IF line_exists( ct_return[ type = 'E' ] ).
      RETURN.
    ENDIF.

    " Template only: replace with project-specific HR action wrapper.
    add_message(
      EXPORTING
        iv_type    = 'S'
        iv_id      = 'ZHR_H2R'
        iv_number  = '010'
        iv_message = |Hire process prepared for employee { is_input-pernr }|
      CHANGING
        ct_return  = ct_return ).
  ENDMETHOD.

  METHOD process_org_change.
    validate_action_input(
      EXPORTING
        is_input  = is_input
      CHANGING
        ct_return = ct_return ).

    IF line_exists( ct_return[ type = 'E' ] ).
      RETURN.
    ENDIF.

    add_message(
      EXPORTING
        iv_type    = 'S'
        iv_id      = 'ZHR_H2R'
        iv_number  = '020'
        iv_message = |Organizational change prepared for employee { is_input-pernr }|
      CHANGING
        ct_return  = ct_return ).
  ENDMETHOD.

  METHOD process_leave.
    validate_action_input(
      EXPORTING
        is_input  = is_input
      CHANGING
        ct_return = ct_return ).

    IF line_exists( ct_return[ type = 'E' ] ).
      RETURN.
    ENDIF.

    IF is_input.awart IS INITIAL.
      add_message(
        EXPORTING
          iv_type    = 'E'
          iv_id      = 'ZHR_H2R'
          iv_number  = '030'
          iv_message = 'Leave type is mandatory for leave processing'
        CHANGING
          ct_return  = ct_return ).
      RETURN.
    ENDIF.

    add_message(
      EXPORTING
        iv_type    = 'S'
        iv_id      = 'ZHR_H2R'
        iv_number  = '031'
        iv_message = |Leave action prepared for employee { is_input-pernr }|
      CHANGING
        ct_return  = ct_return ).
  ENDMETHOD.

  METHOD separate_employee.
    validate_action_input(
      EXPORTING
        is_input  = is_input
      CHANGING
        ct_return = ct_return ).

    IF line_exists( ct_return[ type = 'E' ] ).
      RETURN.
    ENDIF.

    add_message(
      EXPORTING
        iv_type    = 'S'
        iv_id      = 'ZHR_H2R'
        iv_number  = '040'
        iv_message = |Separation process prepared for employee { is_input-pernr }|
      CHANGING
        ct_return  = ct_return ).
  ENDMETHOD.

  METHOD retire_employee.
    validate_action_input(
      EXPORTING
        is_input  = is_input
      CHANGING
        ct_return = ct_return ).

    IF line_exists( ct_return[ type = 'E' ] ).
      RETURN.
    ENDIF.

    add_message(
      EXPORTING
        iv_type    = 'S'
        iv_id      = 'ZHR_H2R'
        iv_number  = '050'
        iv_message = |Retirement process prepared for employee { is_input-pernr }|
      CHANGING
        ct_return  = ct_return ).
  ENDMETHOD.

ENDCLASS.
