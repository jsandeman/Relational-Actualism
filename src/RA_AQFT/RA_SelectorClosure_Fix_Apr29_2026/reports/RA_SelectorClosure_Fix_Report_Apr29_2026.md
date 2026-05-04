# RA Selector Closure Lean fix report — Apr29 2026

## Issue

The generated Lean scaffold used `Π` as a term-level identifier. Lean 4 parses this token as binder syntax, so it cannot be used as a normal variable name.

## Change

Renamed the term variable `Π` to `Pot` throughout `RA_ActualizationSelector_v1.lean`.

## Expected result

The original parse errors of the form:

```text
unexpected token 'Π'; expected '_' or identifier
```

should disappear.

## Caveat

This environment does not have Lean/Lake installed, so this correction is syntax-reasoned but not locally compiled here. Please run:

```bash
lake env lean RA_ActualizationSelector_v1.lean
```

in your local Lean 4.29.0 environment.
