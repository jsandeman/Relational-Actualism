// Lean compiler output
// Module: RA_O14_Uniqueness_Core_draft
// Imports: public import Init public import Mathlib.Data.Nat.Choose.Basic public import Mathlib.Data.Int.Basic public import Mathlib.Tactic.NormNum
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lean_nat_div(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_yeats__moment(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_yeats__moment___boxed(lean_object*);
lean_object* lean_nat_to_int(lean_object*);
static lean_once_cell_t lp_RelationalActualism_r___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_r___closed__0;
static lean_once_cell_t lp_RelationalActualism_r___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_r___closed__1;
static lean_once_cell_t lp_RelationalActualism_r___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_r___closed__2;
static lean_once_cell_t lp_RelationalActualism_r___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_r___closed__3;
static lean_once_cell_t lp_RelationalActualism_r___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_r___closed__4;
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_r(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_r___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_yeats__moment(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_2 = lean_unsigned_to_nat(2u);
x_3 = lean_nat_mul(x_2, x_1);
x_4 = lean_unsigned_to_nat(3u);
x_5 = lean_nat_add(x_3, x_4);
x_6 = lean_nat_add(x_3, x_2);
x_7 = lean_nat_mul(x_5, x_6);
lean_dec(x_6);
lean_dec(x_5);
x_8 = lean_unsigned_to_nat(1u);
x_9 = lean_nat_add(x_3, x_8);
lean_dec(x_3);
x_10 = lean_nat_mul(x_7, x_9);
lean_dec(x_9);
lean_dec(x_7);
x_11 = lean_unsigned_to_nat(6u);
x_12 = lean_nat_div(x_10, x_11);
lean_dec(x_10);
return x_12;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_yeats__moment___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_RelationalActualism_yeats__moment(x_1);
lean_dec(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_r___closed__0(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_r___closed__1(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(84u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_r___closed__2(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(35u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_r___closed__3(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(10u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_r___closed__4(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(1u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_r(lean_object* x_1) {
_start:
{
lean_object* x_2; uint8_t x_3; 
x_2 = lean_unsigned_to_nat(0u);
x_3 = lean_nat_dec_eq(x_1, x_2);
if (x_3 == 0)
{
lean_object* x_4; uint8_t x_5; 
x_4 = lean_unsigned_to_nat(1u);
x_5 = lean_nat_dec_eq(x_1, x_4);
if (x_5 == 0)
{
lean_object* x_6; uint8_t x_7; 
x_6 = lean_unsigned_to_nat(2u);
x_7 = lean_nat_dec_eq(x_1, x_6);
if (x_7 == 0)
{
lean_object* x_8; uint8_t x_9; 
x_8 = lean_unsigned_to_nat(3u);
x_9 = lean_nat_dec_eq(x_1, x_8);
if (x_9 == 0)
{
lean_object* x_10; 
x_10 = lean_obj_once(&lp_RelationalActualism_r___closed__0, &lp_RelationalActualism_r___closed__0_once, _init_lp_RelationalActualism_r___closed__0);
return x_10;
}
else
{
lean_object* x_11; 
x_11 = lean_obj_once(&lp_RelationalActualism_r___closed__1, &lp_RelationalActualism_r___closed__1_once, _init_lp_RelationalActualism_r___closed__1);
return x_11;
}
}
else
{
lean_object* x_12; 
x_12 = lean_obj_once(&lp_RelationalActualism_r___closed__2, &lp_RelationalActualism_r___closed__2_once, _init_lp_RelationalActualism_r___closed__2);
return x_12;
}
}
else
{
lean_object* x_13; 
x_13 = lean_obj_once(&lp_RelationalActualism_r___closed__3, &lp_RelationalActualism_r___closed__3_once, _init_lp_RelationalActualism_r___closed__3);
return x_13;
}
}
else
{
lean_object* x_14; 
x_14 = lean_obj_once(&lp_RelationalActualism_r___closed__4, &lp_RelationalActualism_r___closed__4_once, _init_lp_RelationalActualism_r___closed__4);
return x_14;
}
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_r___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_RelationalActualism_r(x_1);
lean_dec(x_1);
return x_2;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Choose_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Int_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic_NormNum(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__O14__Uniqueness__Core__draft(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Nat_Choose_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Int_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic_NormNum(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
