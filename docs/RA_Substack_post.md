# The Moment Time Was Born

## Twenty-three years to one insight — and what a computer did with it

---

In 2003 I was reading Brian Greene's *The Fabric of the Cosmos* on a lunch break. I was not a physicist. I was working in computational neuroscience, between careers, paying the bills. But something in the book stopped me.

The double-slit experiment. The delayed-choice experiment. The quantum eraser. Greene describes these carefully, with the full weight of their strangeness. A particle seems to "know" whether it's being watched. A measurement made in the present seems to reach back and alter the past. The universe appears to withhold commitment about what is real until the last possible moment.

And then, reading through these experiments, something clicked. Not an answer — not yet. A question, sharply focused for the first time.

*When does possible become actual?*

Not "how does the wave function collapse" in the mathematical sense. Not "which interpretation of quantum mechanics is correct." Something more primitive. The universe seems to make a decision — irreversible, permanent, factual — at certain moments and not others. What is that decision? What is that moment? Is it the same kind of thing everywhere, for all particles, at all scales?

I thought: it has to be. One nature of Nature. Not a quantum rule that mysteriously hands off to a classical rule at some Heisenberg cut that nobody can precisely define. One thing, all the way down.

That was 2003. For the next twenty-three years, I carried the question.

---

## Carried, not pursued

I want to be honest about what those twenty-three years looked like, because it affects how you should evaluate what I'm about to tell you.

I did not have a PhD programme, a research group, a grant, or a supervisor. I worked — through Silicon Valley, through medicine, currently as a Family Nurse Practitioner in Salem, Oregon. I read voraciously and privately, through hundreds of books and papers and podcasts, because the question didn't fit anywhere institutional. A brief encounter with a PhD programme made that clear. Academic disciplines have boundaries. Nature does not.

The question was the constant. Not a career. A question, carried through every other career, because I couldn't put it down.

What changed recently was the tools. When AI systems became powerful enough to serve as genuine research collaborators — not just autocomplete, but something that could hold a formalism in mind, check calculations, push back on arguments, and draft at professional quality — I could finally pursue the question at the level it required. Over the past several months, working intensively with Claude, the question that started on a lunch break in 2003 has become eleven formal papers, 101 machine-verified mathematical results, and a framework with testable predictions.

I am telling you this not to be dramatic, but because it is true and because the honesty matters. This could be wrong. I'm not a professional physicist. The framework has genuine open problems. It has critics that I take seriously. But it has also survived every red-team attack I've been able to throw at it, made predictions that are falsifiable right now, and produced mathematical results that a computer has verified with zero errors.

---

## What the framework actually claims

Relational Actualism starts with one ontological commitment:

*Actualization events are the primitive fact of reality.*

An actualization event is an irreversible physical interaction — a moment when possibility becomes actuality, when a quantum state becomes a classical fact, when an edge is permanently written into the causal history of the universe. Not a subjective observation. Not a measurement by a conscious observer. A physical process with a precise criterion: an irreversible increase in quantum relative entropy with respect to the vacuum.

From this single commitment, everything else follows.

**Time** is not a background dimension through which events move. Time is the process of the graph growing. The arrow of time — why the past is fixed and the future is open — is not something that needs to be explained by the framework. It is encoded in the framework's most primitive commitment. Actualization is by definition irreversible. The graph only grows. That is the arrow of time.

**Quantum mechanics** is exact at the discrete level. The superposition is the space of possible next steps in the graph. The measurement problem — why observation seems to collapse the wave function — is dissolved: actualization is what collapse is, physically. It happens when the relative entropy threshold is crossed, not when a conscious observer looks.

**General relativity** is what the graph looks like from the outside at high density. The Einstein field equations are not an input to Relational Actualism. They are an output — proved as a theorem, with no free parameters, by combining the Lean-verified Local Ledger Condition with Lovelock's uniqueness theorem and a vacuum energy suppression result. GR is the unique macroscopic description of the actualization graph. Where GR fails — galactic rotation curves, the Hubble tension — is precisely where the graph is sparse enough that the departures from the dense-limit approximation matter.

**The Standard Model** emerges from counting. The Benincasa-Dowker integers that define the local curvature of a 4D causal graph are (1, −1, 9, −16, 8). These five integers have exactly the right structure to produce three non-gravitational gauge interactions in four spacetime dimensions. The particle types — leptons, quarks, gauge bosons — correspond to different local topological structures of the causal graph. Quarks and gluons are confined because their causal topology cannot survive more than 3-4 actualization steps before it dissolves into the standard sequential structure. This is a theorem. A computer verified it.

---

## What can falsify it

I want to be specific about this, because vague "this might be wrong" disclaimers are easy. Relational Actualism makes predictions that are testable now, or within the next decade. Here are the ones I care most about:

**The WIMP prohibition.** Whatever dark matter is, it must actualize — it must interact, leave causal marks, participate in the graph. WIMPs (Weakly Interacting Massive Particles), axions, and sterile neutrinos that never interact electromagnetically or strongly are categorically excluded. Not because we searched for them and didn't find them. Because within this framework, a particle that doesn't interact doesn't gravitate, and something that doesn't gravitate isn't dark matter. If LZ or another underground detector finds a WIMP above the neutrino floor, the framework is falsified. The current experimental null results are consistent with the prediction.

**The Hubble tension.** The discrepancy between the early-universe and late-universe measurements of the expansion rate of the universe is not a measurement error. It is a real physical effect caused by the fact that the actualization density — how fast the graph is growing — varies from place to place. Dense regions expand more slowly. Void regions expand faster. A specific prediction: the Eridanus supervoid, one of the largest known cosmic underdensities, should give a locally measured Hubble constant of approximately 75.9 km/s/Mpc. This is falsifiable with current and near-future survey data.

**The BMV null result.** A set of experiments currently underway (Bose-Marletto-Vedral protocol) is trying to detect whether gravity can mediate quantum entanglement. Standard quantum gravity approaches predict yes. Relational Actualism predicts a strict null result: because the spacetime metric is updated only from actualized vertices, quantum superpositions cannot source a superposed gravitational field. If the BMV experiment detects gravity-mediated entanglement, the framework is falsified.

**The quantum computing bound.** Quantum computers scale badly for a structural reason: electrons propagate at the minimum BDG stability that the causal graph permits — the lowest positive score in the stable spectrum — which means they are maximally vulnerable to actualization-induced decoherence. A specific prediction: there is a maximum fault-tolerant array size N_max = η × p_th, where η is the single-qubit quality factor. Unlimited scaling without improving single-qubit quality will hit this wall regardless of error correction. The observation that large superconducting arrays require continual improvement of qubit quality alongside qubit count is consistent with this prediction.

---

## What a computer verified

One of the stranger aspects of this project is the machine verification.

Over the past few months, I have worked with Claude to produce formal proofs of 101 mathematical results in Lean 4 — the same proof-checking system used to verify Fermat's Last Theorem. These proofs compile with zero errors and zero axioms beyond the standard mathematical library.

What does that mean? It means a computer has checked that certain mathematical claims follow necessarily from their stated premises, with no logical gaps. Not "this argument is plausible" — "this conclusion follows, definitionally, from these definitions."

The verified results include the Local Ledger Condition (charge conservation at every actualization vertex), the Graph Cut Theorem (conservation holds independently on each side of a causal boundary — relevant to the black hole information paradox), the frame-independence of the actualization criterion (two observers in different frames agree about whether an actualization event occurred), the BDG particle topology classification (quarks and gluons have topologically distinct causal pasts from leptons and photons, and this is provably stable under all possible single-step graph extensions), and — most recently — the P_act conservation theorem, which is the key step in proving that the Einstein field equations are the unique macroscopic field equation of the actualization graph.

I am not claiming the framework is right. I am claiming that these specific mathematical results are correct, and that I can tell you precisely where the remaining gaps are and what it would take to close them.

---

## The open problems

Honest frameworks have honest open problems. Here are the three I most want help with:

**The Wyler formula.** The fine structure constant α ≈ 1/137 appears in the framework through the optical theorem: the fraction of electromagnetic interaction candidates that become actualization events equals α. Two of three conditions needed to derive α from the BDG integers alone are now established. The remaining step is a computation in the geometry of the SU(3) coherent state space. If it works, the fine structure constant becomes a prediction of the framework rather than an input. If anyone works in symmetric space geometry or the Wyler programme, this is a specific, well-defined calculation.

**The continuum limit.** The Einstein field equations are proved from the framework's discrete structure. The remaining gap is showing that the discrete conservation law converges correctly to the continuum conservation equation as the vertex density increases. This is a mathematical analysis problem — a law of large numbers for a specific Poisson graph measure. It is the kind of problem that interests people in causal set theory and ergodic theory.

**The particle classification completeness.** We have proved that the known particle types (electrons, quarks, gluons, W/Z bosons) form a closed set under all possible single-step causal graph extensions. We have verified this exhaustively for graphs up to size 7. Proving it for arbitrary size requires a well-founded induction argument in ordered combinatorics. This is a finite, tractable problem.

---

## Why now

The honest answer is: because the tools exist now that didn't exist before.

Twenty-three years ago, pursuing this properly would have required either a full academic research career or collaboration with people who already had one. The problem is that the framework doesn't fit neatly into any existing discipline. It is simultaneously foundational quantum mechanics, general relativity, particle physics, and formal mathematics. No existing research group is set up to pursue all of those simultaneously. Independent researchers are not set up to pursue any of them at professional depth.

What changed is that an AI can hold all of those contexts at once, check calculations in real time, spot errors, suggest literature, draft at professional quality, and run proof checkers. This doesn't replace expertise — the framework needed deep engagement with QFT, causal set theory, Lean 4 proof tactics, and cosmological data. But it made it possible for someone with the right question and twenty-three years of thinking to actually pursue it to the level it required.

I don't know if that's a good thing for physics in general. I think it probably is. The ideas that fall between disciplines, carried by people who can't afford to have careers in any one of them — those ideas have traditionally been filtered out. That filter is changing.

---

## The papers

The framework is laid out in eleven papers, all available on Zenodo with permanent DOIs. The foundational paper (RAQM) is currently under review at *Foundations of Physics*. The papers are:

**RAQM** — The ontological commitment and the quantum mechanics. The measurement problem dissolved, the arrow of time explained, the Unruh effect resolved.

**RAGC** — Gravity and cosmology. The Hubble tension mechanism, the vacuum energy suppression, the speed of light as a causal bandwidth rate.

**RACL** — The proof that the Einstein field equations are the unique macroscopic limit of the actualization graph, with Λ = 0 and no free parameters.

**RAEB** — The Engine of Becoming. The five-step algorithm that generates spacetime from nothing but actualization events.

**RASM** — The Standard Model. Where electrons, quarks, and gauge bosons come from.

**RATM** — The Topology of Matter. Lean-verified proof that the particle catalogue is closed — no new particle types can emerge from any local causal move.

**RADM** — Dark matter. Why WIMPs can't exist. Why rotation curves are flat. The Bullet Cluster.

**RAQI** — Quantum information. Why quantum computers are structurally limited. The Kinematic Coherence Bound.

**RAHC** — Emergence and complexity. The hierarchy from particles to cells to minds.

**RACI** — Life, complexity, and intelligence as causal graph properties.

**Foundation** — The map of the whole territory.

All of them, with the Lean 4 proof files and the Python verification scripts, are at [github.com/jsandeman/Relational-Actualism](https://github.com/jsandeman/Relational-Actualism).

---

## If it's wrong

Then it's wrong, and the search continues.

That is not a performed humility. It is the only honest position. The framework makes specific, falsifiable predictions. If the LZ detector finds a WIMP, if the BMV experiment detects gravity-mediated entanglement, if the Eridanus supervoid gives the wrong Hubble constant — any of those would falsify specific claims. The machine verification says the mathematics is internally consistent. It says nothing about whether the mathematics describes the universe.

What I can say is that in twenty-three years of looking, the measurement problem has never been cleanly dissolved by any other approach I've found. Not the Copenhagen interpretation, not Everett, not pilot waves, not relational quantum mechanics in its standard form. The question I started with in 2003 — *when does possible become actual?* — has a precise answer in this framework. An actualization event is when the quantum relative entropy crosses zero in the direction of increasing departure from vacuum. That is a physical fact, not a subjective observation, not a postulate about consciousness. It is what happens when an irreversible causal mark is written into the graph.

Maybe that's the right answer. Maybe it's approximately right in a way that matters. Maybe it's wrong in ways I can't currently see.

Either way, this is where twenty-three years of carrying a question landed. I thought you should know.

---

*All papers: [zenodo.org/communities/relational-actualism](https://zenodo.org/communities/relational-actualism)*  
*Code and proofs: [github.com/jsandeman/Relational-Actualism](https://github.com/jsandeman/Relational-Actualism)*  
*Contact: sansuikyo@gmail.com*
