// Lean compiler output
// Module: RA_Alpha_EM_Proof
// Imports: public import Init public import Mathlib public import Mathlib.Tactic
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
static const lean_string_object lp_RelationalActualism_tacticPush__neg_____00__closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "tacticPush_neg__"};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__0 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__0_value;
lean_object* l_Lean_Name_mkStr1(lean_object*);
static const lean_ctor_object lp_RelationalActualism_tacticPush__neg_____00__closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__0_value),LEAN_SCALAR_PTR_LITERAL(70, 56, 73, 223, 241, 255, 116, 146)}};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__1 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__1_value;
static const lean_string_object lp_RelationalActualism_tacticPush__neg_____00__closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "andthen"};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__2 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__2_value;
static const lean_ctor_object lp_RelationalActualism_tacticPush__neg_____00__closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__2_value),LEAN_SCALAR_PTR_LITERAL(40, 255, 78, 30, 143, 119, 117, 174)}};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__3 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__3_value;
static const lean_string_object lp_RelationalActualism_tacticPush__neg_____00__closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "push_neg"};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__4 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__4_value;
static const lean_ctor_object lp_RelationalActualism_tacticPush__neg_____00__closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 8, .m_other = 1, .m_tag = 6}, .m_objs = {((lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__4_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__5 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__5_value;
extern lean_object* l_Lean_Parser_Tactic_optConfig;
static lean_once_cell_t lp_RelationalActualism_tacticPush__neg_____00__closed__6_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__6;
static const lean_string_object lp_RelationalActualism_tacticPush__neg_____00__closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "optional"};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__7 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__7_value;
static const lean_ctor_object lp_RelationalActualism_tacticPush__neg_____00__closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__7_value),LEAN_SCALAR_PTR_LITERAL(233, 141, 154, 50, 143, 135, 42, 252)}};
static const lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__8 = (const lean_object*)&lp_RelationalActualism_tacticPush__neg_____00__closed__8_value;
extern lean_object* l_Lean_Parser_Tactic_location;
static lean_once_cell_t lp_RelationalActualism_tacticPush__neg_____00__closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__9;
static lean_once_cell_t lp_RelationalActualism_tacticPush__neg_____00__closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__10;
static lean_once_cell_t lp_RelationalActualism_tacticPush__neg_____00__closed__11_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_tacticPush__neg_____00__closed__11;
LEAN_EXPORT lean_object* lp_RelationalActualism_tacticPush__neg____;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "Tactic"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__0 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__0_value;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "Mathlib"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__1 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__1_value;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "Push"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__2 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__2_value;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "pushStx"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__3 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__3_value;
lean_object* l_Lean_Name_mkStr4(lean_object*, lean_object*, lean_object*, lean_object*);
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_0 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__1_value),LEAN_SCALAR_PTR_LITERAL(118, 213, 161, 2, 73, 184, 31, 228)}};
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_1 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_0),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__0_value),LEAN_SCALAR_PTR_LITERAL(139, 222, 98, 232, 116, 132, 69, 249)}};
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_2 = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_1),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__2_value),LEAN_SCALAR_PTR_LITERAL(179, 237, 76, 44, 143, 69, 172, 56)}};
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value_aux_2),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__3_value),LEAN_SCALAR_PTR_LITERAL(191, 92, 154, 179, 191, 15, 216, 138)}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4_value;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "push"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__5 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__5_value;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = "null"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__6 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__6_value;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__6_value),LEAN_SCALAR_PTR_LITERAL(24, 58, 49, 223, 146, 207, 197, 136)}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__7 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__7_value;
lean_object* l_Array_mkArray0(lean_object*);
static lean_once_cell_t lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8;
static const lean_string_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "Not"};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__9 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__9_value;
lean_object* l_String_toRawSubstring_x27(lean_object*);
static lean_once_cell_t lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__9_value),LEAN_SCALAR_PTR_LITERAL(185, 11, 203, 55, 27, 192, 137, 230)}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11_value;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__12 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__12_value;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 0}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11_value)}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__13 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__13_value;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__13_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__14 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__14_value;
static const lean_ctor_object lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__12_value),((lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__14_value)}};
static const lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__15 = (const lean_object*)&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__15_value;
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
static lean_once_cell_t lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16;
uint8_t l_Lean_Syntax_isOfKind(lean_object*, lean_object*);
lean_object* l_Lean_Syntax_getArg(lean_object*, lean_object*);
lean_object* l_Array_append___redArg(lean_object*, lean_object*);
lean_object* l_Lean_Syntax_node5(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_SourceInfo_fromRef(lean_object*, uint8_t);
lean_object* l_Lean_addMacroScope(lean_object*, lean_object*, lean_object*);
lean_object* l_Array_mkArray1___redArg(lean_object*);
lean_object* l_Lean_Syntax_getOptional_x3f(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1(lean_object*, lean_object*, lean_object*);
lean_object* lean_nat_to_int(lean_object*);
static lean_once_cell_t lp_RelationalActualism_c___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__0;
lean_object* lean_int_neg(lean_object*);
static lean_once_cell_t lp_RelationalActualism_c___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__1;
static lean_once_cell_t lp_RelationalActualism_c___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__2;
static lean_once_cell_t lp_RelationalActualism_c___closed__3_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__3;
static lean_once_cell_t lp_RelationalActualism_c___closed__4_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__4;
static lean_once_cell_t lp_RelationalActualism_c___closed__5_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_RelationalActualism_c___closed__5;
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_c(lean_object*);
LEAN_EXPORT lean_object* lp_RelationalActualism_c___boxed(lean_object*);
static lean_object* _init_lp_RelationalActualism_tacticPush__neg_____00__closed__6(void) {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = l_Lean_Parser_Tactic_optConfig;
x_2 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__5));
x_3 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__3));
x_4 = lean_alloc_ctor(2, 3, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_2);
lean_ctor_set(x_4, 2, x_1);
return x_4;
}
}
static lean_object* _init_lp_RelationalActualism_tacticPush__neg_____00__closed__9(void) {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_Lean_Parser_Tactic_location;
x_2 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__8));
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_lp_RelationalActualism_tacticPush__neg_____00__closed__10(void) {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = lean_obj_once(&lp_RelationalActualism_tacticPush__neg_____00__closed__9, &lp_RelationalActualism_tacticPush__neg_____00__closed__9_once, _init_lp_RelationalActualism_tacticPush__neg_____00__closed__9);
x_2 = lean_obj_once(&lp_RelationalActualism_tacticPush__neg_____00__closed__6, &lp_RelationalActualism_tacticPush__neg_____00__closed__6_once, _init_lp_RelationalActualism_tacticPush__neg_____00__closed__6);
x_3 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__3));
x_4 = lean_alloc_ctor(2, 3, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_2);
lean_ctor_set(x_4, 2, x_1);
return x_4;
}
}
static lean_object* _init_lp_RelationalActualism_tacticPush__neg_____00__closed__11(void) {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = lean_obj_once(&lp_RelationalActualism_tacticPush__neg_____00__closed__10, &lp_RelationalActualism_tacticPush__neg_____00__closed__10_once, _init_lp_RelationalActualism_tacticPush__neg_____00__closed__10);
x_2 = lean_unsigned_to_nat(1022u);
x_3 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__1));
x_4 = lean_alloc_ctor(3, 3, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_2);
lean_ctor_set(x_4, 2, x_1);
return x_4;
}
}
static lean_object* _init_lp_RelationalActualism_tacticPush__neg____(void) {
_start:
{
lean_object* x_1; 
x_1 = lean_obj_once(&lp_RelationalActualism_tacticPush__neg_____00__closed__11, &lp_RelationalActualism_tacticPush__neg_____00__closed__11_once, _init_lp_RelationalActualism_tacticPush__neg_____00__closed__11);
return x_1;
}
}
static lean_object* _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8(void) {
_start:
{
lean_object* x_1; 
x_1 = l_Array_mkArray0(lean_box(0));
return x_1;
}
}
static lean_object* _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__9));
x_2 = l_String_toRawSubstring_x27(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; uint8_t x_5; 
x_4 = ((lean_object*)(lp_RelationalActualism_tacticPush__neg_____00__closed__1));
lean_inc(x_1);
x_5 = l_Lean_Syntax_isOfKind(x_1, x_4);
if (x_5 == 0)
{
lean_object* x_6; lean_object* x_7; 
lean_dec_ref(x_2);
lean_dec(x_1);
x_6 = lean_box(1);
x_7 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_7, 0, x_6);
lean_ctor_set(x_7, 1, x_3);
return x_7;
}
else
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_23; lean_object* x_44; lean_object* x_45; lean_object* x_46; 
x_8 = lean_unsigned_to_nat(1u);
x_9 = l_Lean_Syntax_getArg(x_1, x_8);
x_44 = lean_unsigned_to_nat(2u);
x_45 = l_Lean_Syntax_getArg(x_1, x_44);
lean_dec(x_1);
x_46 = l_Lean_Syntax_getOptional_x3f(x_45);
lean_dec(x_45);
if (lean_obj_tag(x_46) == 0)
{
lean_object* x_47; 
x_47 = lean_box(0);
x_23 = x_47;
goto block_43;
}
else
{
uint8_t x_48; 
x_48 = !lean_is_exclusive(x_46);
if (x_48 == 0)
{
x_23 = x_46;
goto block_43;
}
else
{
lean_object* x_49; lean_object* x_50; 
x_49 = lean_ctor_get(x_46, 0);
lean_inc(x_49);
lean_dec(x_46);
x_50 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_50, 0, x_49);
x_23 = x_50;
goto block_43;
}
}
block_22:
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; 
x_18 = l_Array_append___redArg(x_10, x_17);
lean_dec_ref(x_17);
lean_inc(x_16);
x_19 = lean_alloc_ctor(1, 3, 0);
lean_ctor_set(x_19, 0, x_16);
lean_ctor_set(x_19, 1, x_14);
lean_ctor_set(x_19, 2, x_18);
x_20 = l_Lean_Syntax_node5(x_16, x_11, x_13, x_9, x_15, x_12, x_19);
x_21 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_21, 0, x_20);
lean_ctor_set(x_21, 1, x_3);
return x_21;
}
block_43:
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; uint8_t x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; 
x_24 = lean_ctor_get(x_2, 1);
lean_inc(x_24);
x_25 = lean_ctor_get(x_2, 2);
lean_inc(x_25);
x_26 = lean_ctor_get(x_2, 5);
lean_inc(x_26);
lean_dec_ref(x_2);
x_27 = 0;
x_28 = l_Lean_SourceInfo_fromRef(x_26, x_27);
lean_dec(x_26);
x_29 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__4));
x_30 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__5));
lean_inc(x_28);
x_31 = lean_alloc_ctor(2, 2, 0);
lean_ctor_set(x_31, 0, x_28);
lean_ctor_set(x_31, 1, x_30);
x_32 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__7));
x_33 = lean_obj_once(&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8, &lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8_once, _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__8);
lean_inc(x_28);
x_34 = lean_alloc_ctor(1, 3, 0);
lean_ctor_set(x_34, 0, x_28);
lean_ctor_set(x_34, 1, x_32);
lean_ctor_set(x_34, 2, x_33);
x_35 = lean_obj_once(&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10, &lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10_once, _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__10);
x_36 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__11));
x_37 = l_Lean_addMacroScope(x_24, x_36, x_25);
x_38 = ((lean_object*)(lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__15));
lean_inc(x_28);
x_39 = lean_alloc_ctor(3, 4, 0);
lean_ctor_set(x_39, 0, x_28);
lean_ctor_set(x_39, 1, x_35);
lean_ctor_set(x_39, 2, x_37);
lean_ctor_set(x_39, 3, x_38);
if (lean_obj_tag(x_23) == 1)
{
lean_object* x_40; lean_object* x_41; 
x_40 = lean_ctor_get(x_23, 0);
lean_inc(x_40);
lean_dec_ref(x_23);
x_41 = l_Array_mkArray1___redArg(x_40);
x_10 = x_33;
x_11 = x_29;
x_12 = x_39;
x_13 = x_31;
x_14 = x_32;
x_15 = x_34;
x_16 = x_28;
x_17 = x_41;
goto block_22;
}
else
{
lean_object* x_42; 
lean_dec(x_23);
x_42 = lean_obj_once(&lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16, &lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16_once, _init_lp_RelationalActualism___aux__RA__Alpha__EM__Proof______macroRules__tacticPush__neg______1___closed__16);
x_10 = x_33;
x_11 = x_29;
x_12 = x_39;
x_13 = x_31;
x_14 = x_32;
x_15 = x_34;
x_16 = x_28;
x_17 = x_42;
goto block_22;
}
}
}
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__0(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(1u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__1(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_obj_once(&lp_RelationalActualism_c___closed__0, &lp_RelationalActualism_c___closed__0_once, _init_lp_RelationalActualism_c___closed__0);
x_2 = lean_int_neg(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__2(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(9u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__3(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(16u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__4(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_obj_once(&lp_RelationalActualism_c___closed__3, &lp_RelationalActualism_c___closed__3_once, _init_lp_RelationalActualism_c___closed__3);
x_2 = lean_int_neg(x_1);
return x_2;
}
}
static lean_object* _init_lp_RelationalActualism_c___closed__5(void) {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(8u);
x_2 = lean_nat_to_int(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_c(lean_object* x_1) {
_start:
{
lean_object* x_2; uint8_t x_3; 
x_2 = lean_unsigned_to_nat(0u);
x_3 = lean_nat_dec_eq(x_1, x_2);
if (x_3 == 1)
{
lean_object* x_4; 
x_4 = lean_obj_once(&lp_RelationalActualism_c___closed__0, &lp_RelationalActualism_c___closed__0_once, _init_lp_RelationalActualism_c___closed__0);
return x_4;
}
else
{
lean_object* x_5; lean_object* x_6; uint8_t x_7; 
x_5 = lean_unsigned_to_nat(1u);
x_6 = lean_nat_sub(x_1, x_5);
x_7 = lean_nat_dec_eq(x_6, x_2);
if (x_7 == 1)
{
lean_object* x_8; 
lean_dec(x_6);
x_8 = lean_obj_once(&lp_RelationalActualism_c___closed__1, &lp_RelationalActualism_c___closed__1_once, _init_lp_RelationalActualism_c___closed__1);
return x_8;
}
else
{
lean_object* x_9; uint8_t x_10; 
x_9 = lean_nat_sub(x_6, x_5);
lean_dec(x_6);
x_10 = lean_nat_dec_eq(x_9, x_2);
if (x_10 == 1)
{
lean_object* x_11; 
lean_dec(x_9);
x_11 = lean_obj_once(&lp_RelationalActualism_c___closed__2, &lp_RelationalActualism_c___closed__2_once, _init_lp_RelationalActualism_c___closed__2);
return x_11;
}
else
{
lean_object* x_12; uint8_t x_13; 
x_12 = lean_nat_sub(x_9, x_5);
lean_dec(x_9);
x_13 = lean_nat_dec_eq(x_12, x_2);
if (x_13 == 1)
{
lean_object* x_14; 
lean_dec(x_12);
x_14 = lean_obj_once(&lp_RelationalActualism_c___closed__4, &lp_RelationalActualism_c___closed__4_once, _init_lp_RelationalActualism_c___closed__4);
return x_14;
}
else
{
lean_object* x_15; uint8_t x_16; lean_object* x_17; 
x_15 = lean_nat_sub(x_12, x_5);
lean_dec(x_12);
x_16 = lean_nat_dec_eq(x_15, x_2);
lean_dec(x_15);
x_17 = lean_obj_once(&lp_RelationalActualism_c___closed__5, &lp_RelationalActualism_c___closed__5_once, _init_lp_RelationalActualism_c___closed__5);
return x_17;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_RelationalActualism_c___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_RelationalActualism_c(x_1);
lean_dec(x_1);
return x_2;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_RelationalActualism_RA__Alpha__EM__Proof(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_RelationalActualism_tacticPush__neg____ = _init_lp_RelationalActualism_tacticPush__neg____();
lean_mark_persistent(lp_RelationalActualism_tacticPush__neg____);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
