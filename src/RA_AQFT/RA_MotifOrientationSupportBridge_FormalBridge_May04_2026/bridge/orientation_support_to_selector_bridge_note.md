# Bridge Note: Orientation Support to Selector Closure

The bridge intentionally avoids adding another selector policy. Instead it
connects the abstract selector layer to orientation-support evidence already in
the RA Lean corpus.

## Before this packet

```text
RA_MotifCommitProtocol
  -> supports relation is abstract

RA_MotifSelectorClosure
  -> selected commitment assumes certified readiness

RA_GraphOrientationClosure
  -> graph orientation certificates induce deterministic signs and seven-value
     N1 ledger signatures
```

## This packet

```text
GraphOrientedMotifSupport
  -> certifies finite-Hasse-frontier support for a motif
  -> induces deterministic sign source and N1 ledger theorem
  -> feeds GraphCommitContext.supports through GraphOrientationSupports
```

The selector layer now has an RA-native evidence source for `supports` without
making a hard uniqueness claim.

## Still open

The remaining hard theorem is to derive `GraphOrientedMotifSupport.certified`
from primitive RA graph/frontier/orientation/ledger structure, rather than
supplying its frontier sufficiency and local ledger compatibility fields.
