// Lean compiler output
// Module: RA_AQFT_Proofs_v10
// Imports: public import Init public import Mathlib
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
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
lean_object* lp_mathlib_Complex_ofReal(lean_object*);
static lean_once_cell_t lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0;
extern lean_object* lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
static lean_once_cell_t lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1;
lean_object* lean_nat_mod(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
extern lean_object* lp_mathlib_Complex_instZero;
lean_object* lp_mathlib_Matrix_diagonal(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1850581184____hygCtx___hyg_8_;
x_2 = lp_mathlib_Complex_ofReal(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_mathlib_Real_definition_00___x40_Mathlib_Data_Real_Basic_1279875089____hygCtx___hyg_8_;
x_2 = lp_mathlib_Complex_ofReal(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; uint8_t x_7; 
x_4 = lean_unsigned_to_nat(0u);
x_5 = lean_nat_mod(x_4, x_1);
x_6 = lean_apply_2(x_2, x_3, x_5);
x_7 = lean_unbox(x_6);
if (x_7 == 0)
{
lean_object* x_8; 
x_8 = lean_obj_once(&lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0, &lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0_once, _init_lp_RelationalActualism_vacuumState___redArg___lam__0___closed__0);
return x_8;
}
else
{
lean_object* x_9; 
x_9 = lean_obj_once(&lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1, &lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1_once, _init_lp_RelationalActualism_vacuumState___redArg___lam__0___closed__1);
return x_9;
}
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_RelationalActualism_vacuumState___redArg___lam__0(x_1, x_2, x_3);
lean_dec(x_1);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; 
lean_inc_ref(x_2);
x_3 = lean_alloc_closure((void*)(lp_RelationalActualism_vacuumState___redArg___lam__0___boxed), 3, 2);
lean_closure_set(x_3, 0, x_1);
lean_closure_set(x_3, 1, x_2);
x_4 = lp_mathlib_Complex_instZero;
x_5 = lean_alloc_closure((void*)(lp_mathlib_Matrix_diagonal), 7, 5);
lean_closure_set(x_5, 0, lean_box(0));
lean_closure_set(x_5, 1, lean_box(0));
lean_closure_set(x_5, 2, x_2);
lean_closure_set(x_5, 3, x_4);
lean_closure_set(x_5, 4, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_RelationalActualism_vacuumState___redArg(x_1, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_vacuumState___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_RelationalActualism_vacuumState(x_1, x_2, x_3, x_4);
lean_dec(x_3);
return x_5;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__AQFT__Proofs__v10(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
