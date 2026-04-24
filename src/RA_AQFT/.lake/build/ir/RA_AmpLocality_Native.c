// Lean compiler output
// Module: RA_AmpLocality_Native
// Imports: public import Init public import RA_AmpLocality
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
lean_object* lp_RelationalActualism_causal__past___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_RelationalActualism_causal__interval___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_RelationalActualism_causal__past___redArg(x_1, x_2, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_RelationalActualism_causal__past___redArg(x_2, x_4, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_realized__past___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_RelationalActualism_realized__past(x_1, x_2, x_3, x_4, x_5);
lean_dec_ref(x_3);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_RelationalActualism_causal__interval___redArg(x_1, x_2, x_3, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
lean_object* x_8; 
x_8 = lp_RelationalActualism_causal__interval___redArg(x_4, x_5, x_6, x_7);
return x_8;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_local__interval___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
lean_object* x_8; 
x_8 = lp_RelationalActualism_local__interval(x_1, x_2, x_3, x_4, x_5, x_6, x_7);
lean_dec_ref(x_3);
lean_dec(x_2);
return x_8;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_RelationalActualism_RA__AmpLocality(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__AmpLocality__Native(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_RelationalActualism_RA__AmpLocality(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
