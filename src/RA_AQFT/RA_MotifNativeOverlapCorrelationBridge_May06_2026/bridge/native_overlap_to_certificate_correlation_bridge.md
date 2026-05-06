# Bridge note: native overlap to certificate-fate coupling

The v0.8 simulator used an external certificate-correlation parameter. v0.9 replaced that knob with native witness-overlap proxies. The v0.9.1/v0.9.2 analyses showed qualitative alignment but not absolute calibration.

`RA_MotifNativeOverlapCorrelationBridge.lean` captures the corresponding formal posture:

* low native-overlap evidence may supply member-distinct certificate fate structure;
* high native-overlap endpoint evidence may supply shared-fate structure;
* both low- and high-overlap resilience surfaces refine the already compiled certification-resilience predicates.

The bridge keeps all causal/probabilistic content out of Lean. Numerical monotone decay remains an empirical/simulation signature registered elsewhere in RAKB.
