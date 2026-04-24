// Lean compiler output
// Module: RA_GraphCore_Native
// Imports: public import Init public import RA_GraphCore
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
lean_object* lp_RelationalActualism_internal__edges(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_cut__internal__edges(lean_object*, lean_object*);
lean_object* lp_RelationalActualism_boundary__flux(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_cut__flux(lean_object*, lean_object*);
lean_object* lp_RelationalActualism_List_foldrTR___at___00Multiset_ndunion___at___00MarkovBlanket_boundary_spec__0_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_cut__internal__edges(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; 
x_3 = lean_ctor_get(x_2, 0);
lean_inc(x_3);
lean_dec_ref(x_2);
x_4 = lp_RelationalActualism_internal__edges(x_1, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_cut__flux(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RelationalActualism_boundary__flux(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary___redArg(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_2 = lean_ctor_get(x_1, 2);
lean_inc(x_2);
x_3 = lean_ctor_get(x_1, 3);
lean_inc(x_3);
lean_dec_ref(x_1);
x_4 = lp_RelationalActualism_List_foldrTR___at___00Multiset_ndunion___at___00MarkovBlanket_boundary_spec__0_spec__1(x_3, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RelationalActualism_CausalShield_boundary___redArg(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_CausalShield_boundary___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RelationalActualism_CausalShield_boundary(x_1, x_2);
lean_dec_ref(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket___redArg(lean_object* x_1) {
_start:
{
uint8_t x_2; 
x_2 = !lean_is_exclusive(x_1);
if (x_2 == 0)
{
return x_1;
}
else
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_3 = lean_ctor_get(x_1, 0);
x_4 = lean_ctor_get(x_1, 1);
x_5 = lean_ctor_get(x_1, 2);
x_6 = lean_ctor_get(x_1, 3);
lean_inc(x_6);
lean_inc(x_5);
lean_inc(x_4);
lean_inc(x_3);
lean_dec(x_1);
x_7 = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(x_7, 0, x_3);
lean_ctor_set(x_7, 1, x_4);
lean_ctor_set(x_7, 2, x_5);
lean_ctor_set(x_7, 3, x_6);
return x_7;
}
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RelationalActualism_causalShield__of__markovBlanket___redArg(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_causalShield__of__markovBlanket___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_RelationalActualism_causalShield__of__markovBlanket(x_1, x_2);
lean_dec_ref(x_1);
return x_3;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_RelationalActualism_RA__GraphCore(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__GraphCore__Native(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_RelationalActualism_RA__GraphCore(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
