# Aula 06 · S5 R3 source and check record

## Governing source locations

- CPC arts. 67–69: course source shelf, `CPC.txt`, arts. 67–69. Supports reciprocal cooperation, requests for any procedural act, no specific form, enumerated forms including information, special regime for letters, and cross-branch cooperation. No shelf case or located example presents a court-to-court information request; following CEO ruling #105, art. 69 III remains exposition only and no invented application is used.
- CPC arts. 188, 190, 192–199 and 204–211: course source shelf `CPC.txt`. Supports procedural form, procedural agreements, Portuguese language and translation, restricted access/secrecy, and acts and terms.
- Marinoni & Mitidiero, *Novo Curso de Processo Civil*, vol. 2, §4.3, printed p. 115 (PDF p. 108): source shelf text. Supports the non-electronic petition cutoff at local forum/tribunal hours, and electronic act through 24:00 on the last day in the court's time; the paired near miss is applying the electronic cutoff to paper or the paper-hours cutoff to electronic filing. This pair is grounded in the source's distinction; no dawn-hours option is used.
- 2017/2, Avaliação 1, Q7: course source shelf `50-exercises-and-exams.txt`, p. 2. Prompt and four options are transcribed in the final quiz; the keyed answer is d, with the medium distinction explained from CPC art. 212 §3 and art. 213 plus Marinoni & Mitidiero §4.3 p. 115.
- 2018/1, Avaliação 1, Q9: course source shelf `50-exercises-and-exams.txt`. Used as the opening bet's stated adaptation source; the lesson's answer applies CPC arts. 67–69.
- CPC arts. 267–268: course source shelf `CPC.txt`. Art. 267 is expressly scoped to precatory and arbitral letters. The three grounds, reasoned refusal, and possible referral for material or hierarchical incompetence are stated with that scope.

## §03 allocation

Page-local count: quoted blockquote text = 423 words; explanatory paragraph prose = 453 words. Prose exceeds quotation by 30 words.

## Final check results

- House check: PASS, 0 fails, 0 warnings. Run after the figure changes; subsequent edits moved the bet and recast explanatory clauses without altering source blocks, figures, or marks.
- Quote check: PASS, 80 segments checked, 0 unmatched, 0 warnings. The §204–211 statutory block uses `[...]` between arts. 210 and 211 for the omitted intervening source text.
- Marks lint: PASS, 0 findings. Run after the figure changes; subsequent edits did not alter inline marks.
- Slop gate: initial run reported 4 negated-inference matches / 3,880 words (1.031/1000, above the blocking 0.5 floor). The four exact clauses were recast to direct positive propositions. Post-edit course-floor parsing reports 0 negated-inference matches / 3,861 words. The slop gate was not rerun because it writes to the shared workshop checkout's Aula 06 run files; its initial run modified `work/slop-bench/runs/aula-06/{critic_input.md,lint.json}` there. No blind restore was attempted.
- Integrated `sh tools/check_all.sh`: PASS. Includes current page structure, negated-inference and gap-talk floors, image-floor, S7 idempotence, and site integrated checks.
- Offline build: PASS, 1,008 files / 38.5 MB, manifest version `f68a12c13345`, no script additions.
- Visual figure-sheet / responsive breakscan: not run because the mandated capture destination is the shared workshop QA tree, which is concurrently dirty; captures were not redirected to a different location.
