# Domain Ontology — Chess

**Stratum:** 1 (Ontology)
**Domain:** Chess
**Source study:** Hokage Chess (Rob Bonavoglia)
**Created:** 2026-04-25

## Question

What is the domain made of?

## Entities

| Canonical name | Variants | Definition | Boundary case |
|---|---|---|---|
| Position | board state, FEN | A configuration of pieces + side-to-move + castling rights + en passant + halfmove counter | NOT just piece arrangement; clock state and game continuation are separate |
| Move | turn, ply | Legal transformation of a position | A "move" in casual usage = full move (both sides); "ply" = single side's move |
| Game | match | Sequence of positions connected by moves until terminal state | Single game ≠ tournament; tournament has separate ontology (pairings, swiss, round-robin) |
| Opening | repertoire | Documented sequence of typical first ~10 moves | Opening ≠ playing chess; it's a study category |
| Middlegame | tactical phase | Phase after opening exits theory, before pawn-thinning into endgame | Boundary fuzzy — depends on piece count, not move number |
| Endgame | endgame study | Phase where typically ≤6 pieces remain; tablebase-solvable | NOT just "end of the game" — has structural distinctness |
| Tactical motif | combination, pattern | Recurring tactical pattern (pin, fork, skewer, discovered attack, etc.) | Singular tactic vs combination (which is sequence of tactics) |
| Strategic principle | positional principle | Long-term guideline (e.g., "knights before bishops in opening") | Heuristic, not absolute rule; principle-bound creativity |
| Rating | ELO, FIDE, USCF, online | Numerical skill measurement | Multiple incompatible scales (FIDE ≠ chess.com ≠ Lichess); not portable |
| Coaching session | lesson, study | Pedagogical encounter between coach and student | Distinct from puzzle-rush, game-review, theory-study (different pedagogical units) |

## Relations

| Relation | Source → Target | Semantics | Cardinality |
|---|---|---|---|
| applies-to | Tactical motif → Position | Pattern is realizable in this position | N:M |
| transitions | Position → Position (via Move) | One move advances one position to the next | 1:1 per move |
| classifies | Opening → Game | Opening label assigned to game's first phase | 1:N (one opening, many games) |
| derives-from | Strategic principle → Tactical motif | Principles abstract over specific patterns | 1:N |
| ranks | Rating → Player | Player's rating represents skill in a system | 1:1 per system |

## Primitives

- **Square** — atomic unit of the board (a1 through h8)
- **Piece** — pawn / knight / bishop / rook / queen / king × white / black
- **Side-to-move** — binary state (white / black)
- **Half-move counter** — integer for 50-move rule
- **Castling rights** — 4-bit state (white kingside / white queenside / black kingside / black queenside)
- **En passant target** — optional square

## Canonical vocabulary

- **Position** (lowercase as concept; "the position" with article when discussing a specific one)
- **FEN** (always uppercase — Forsyth-Edwards Notation)
- **PGN** (always uppercase — Portable Game Notation)
- **ELO** (uppercase — named after Arpad Elo, but conventionally all-caps)
- **Rapid / Blitz / Bullet** (capitalized as time-control category names)
- **Genin / Chunin / Jonin** (Hokage Chess tier system, capitalized — Naruto-derived)

## Boundary cases — what's NOT chess

- **Chess variants** (Chess960, Bughouse, Atomic) — adjacent domains; share primitives but diverge at higher levels
- **Computer chess theory** (engine architecture, NNUE evaluation, etc.) — adjacent technical domain; engines USE chess but engineering them is software architecture
- **Chess history as broad cultural study** — adjacent humanistic domain; relevant context but not "doing chess"

## Authoritative sources

- *My System* (Aron Nimzowitsch, 1925) — foundational positional theory
- FIDE Laws of Chess (current edition) — rule canon
- *Dvoretsky's Endgame Manual* (Mark Dvoretsky) — endgame canon
- chess.com / Lichess move databases — live opening theory canon
- Saint Louis Chess Club video archives — current pedagogy canon

## Validation gate

A fresh agent reading this file alone can answer "what is X in this chess domain?" for any term used in subsequent strata without external lookups.

## Changelog

- 2026-04-25 — initial fill (proof-instance for DIWS skill)
