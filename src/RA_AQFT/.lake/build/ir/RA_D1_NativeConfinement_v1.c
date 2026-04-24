// Lean compiler output
// Module: RA_D1_NativeConfinement_v1
// Imports: public import Init public import RA_D1_NativeKernel_v1
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
LEAN_EXPORT lean_object* lp_RelationalActualism_closure__length__symmetric;
LEAN_EXPORT lean_object* lp_RelationalActualism_closure__length__asymmetric;
static lean_object* _init_lp_RelationalActualism_closure__length__symmetric(void) {
_start:
{
lean_object* x_1; 
x_1 = lean_unsigned_to_nat(3u);
return x_1;
}
}
static lean_object* _init_lp_RelationalActualism_closure__length__asymmetric(void) {
_start:
{
lean_object* x_1; 
x_1 = lean_unsigned_to_nat(4u);
return x_1;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_RelationalActualism_RA__D1__NativeKernel__v1(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__D1__NativeConfinement__v1(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_RelationalActualism_RA__D1__NativeKernel__v1(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_RelationalActualism_closure__length__symmetric = _init_lp_RelationalActualism_closure__length__symmetric();
lean_mark_persistent(lp_RelationalActualism_closure__length__symmetric);
lp_RelationalActualism_closure__length__asymmetric = _init_lp_RelationalActualism_closure__length__asymmetric();
lean_mark_persistent(lp_RelationalActualism_closure__length__asymmetric);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
