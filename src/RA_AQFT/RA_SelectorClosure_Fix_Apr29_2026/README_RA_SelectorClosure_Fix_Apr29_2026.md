# RA Selector Closure Lean fix — Apr29 2026

This packet fixes the first generated `RA_ActualizationSelector_v1.lean` scaffold.

## Problem

The earlier scaffold used the Unicode identifier `Π` as a Lean term variable for structured potentia. Lean parses uppercase pi as binder syntax, so it reports errors such as:

```text
unexpected token 'Π'; expected '_' or identifier
```

## Fix

The corrected file renames the term variable from `Π` to `Pot` everywhere. No theorem content is changed.

## Install

From the repository root:

```bash
cp RA_SelectorClosure_Fix_Apr29_2026/lean/RA_ActualizationSelector_v1.lean \
   src/RA_AQFT/RA_ActualizationSelector_v1.lean

cd src/RA_AQFT
lake env lean RA_ActualizationSelector_v1.lean
```

Keep this file out of active Lake roots until it compiles locally and we decide to integrate it.
