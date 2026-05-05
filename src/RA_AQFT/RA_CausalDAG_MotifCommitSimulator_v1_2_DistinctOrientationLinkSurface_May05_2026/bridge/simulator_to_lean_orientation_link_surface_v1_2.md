# Simulator-to-Lean Bridge: v1.2 Distinct Orientation-Link Surface

The v1.1 audit showed that the v0.9/v1.0 component proxy did not independently
resolve orientation overlap.  The v1.2 analysis introduces a separate simulator
column:

```text
orientation_link_overlap
```

The Lean bridge `RA_MotifOrientationLinkSurface.lean` mirrors this at the
qualitative level by defining:

```text
DAGOrientationLinkSurfaceContext
GraphOrientationLinkSurfaceContext
DAGHasOrientationLinkSurface
GraphHasOrientationLinkSurface
DAGOrientationLinkOverlapProfile
GraphOrientationLinkOverlapProfile
```

It proves only refinement-style facts: orientation-link evidence can supply the
older generic orientation component evidence.  It does not prove or state a
numerical rescue law.
