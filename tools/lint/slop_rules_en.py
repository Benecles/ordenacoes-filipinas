"""English rule tables for slop_lint (CEO, 16/10). Same engine, same bands as the Portuguese set.

HARD: any hit is a review prompt. RATE: (pattern, limit per 1,000 words, fix); limits are set from the English
backtest (work/slop-bench/en/BACKTEST.md): the smallest value at which ≤10% of human documents alarm, on both the
informal (the chairman's own messages) and the formal (English legal scholarship) human corpora.
The prose this guards is the backstage: the blog, course twins, notes, the CEO's own pages (Writing Standard Part H).
"""
import re

HARD = {
    'puffery': (r"\b(?:plays? an? (?:crucial|pivotal|key|vital|central|important|significant) role|cornerstone of|game[- ]changer|paradigm shift|watershed moment|(?:stands|serves) as an? (?:testament|reminder|beacon)|is a testament to|speaks volumes|sets? the stage for|a new era)\b", 'Say what the thing does, with the fact that makes it matter.'),
    'significance-gerund': (r",\s*(?:highlighting|underscoring|showcasing|reflecting|emphasi[sz]ing|demonstrating|cementing|reinforcing|signaling|illustrating)\s+(?:the|its|their|our|his|her|a)\s+(?:\w+\s+)?(?:importance|significance|role|commitment|power|value|need|depth|strength|potential)\b", 'Delete the evaluative tail; let the fact stand.'),
    'formulaic-metatext': (r"\b(?:it(?:'s| is) worth (?:noting|mentioning|pointing out)|it(?:'s| is) important to (?:note|remember|understand)|(?:it )?bears mentioning|as (?:we've|we have|I've|I have) (?:seen|discussed|mentioned)|in this (?:post|article|section),? (?:we|I)(?:'ll| will)|let(?:'s| us) (?:dive|delve|take a (?:closer )?look|explore|unpack|break (?:it|this) down)|without further ado)\b", 'Cut the announcement; start with the thing.'),
    'vague-attribution': (r"\b(?:experts (?:say|agree|believe|note)|many (?:people|experts|critics) (?:believe|say|argue)|some (?:say|argue|believe)|studies (?:show|suggest)|critics (?:say|argue)|it is (?:widely|generally) (?:believed|accepted))\b", 'Name who, or drop it.'),
    'reader-address': (r"\b(?:you (?:might|may) be wondering|don't worry|let that sink in|you(?:'ll| will) (?:notice|see) that|here's the kicker|buckle up|trust me)\b", 'State the point; the reader will notice by themselves.'),
    'AI-calque': (r"\b(?:delv(?:e|es|ed|ing)|tapestry|in today's (?:fast[- ]paced|digital|ever[- ]changing|modern) (?:world|landscape|age)|ever[- ](?:evolving|changing) (?:landscape|world)|navigat(?:e|es|ing) the (?:complexities|landscape|intricacies|nuances)|(?:in|into) the realm of|embark(?:s|ed|ing)? on|unlock(?:s|ing)? (?:the )?(?:full )?(?:power|potential)|harness(?:es|ing)? the power|elevate(?:s|d)? (?:your|the|our) |symphony of|intricate dance|a dance of|rich (?:tapestry|history of)|holistic(?:ally)?|seamless(?:ly)?|testament)\b", 'Replace the stock phrase with the plain word or the actual detail.'),
    'teaser-hook': (r"(?:^|(?<=[.!?]\s))(?:Here's (?:the thing|why|what|how|the catch|the kicker|the twist)|The (?:result|catch|kicker|answer|twist|verdict|punchline|best part)\?|Spoiler(?: alert)?:|Plot twist:|But here's (?:the thing|where)|Enter:?\s|The short version\?)", 'Lead with the answer; drop the drumroll.'),
    'self-labeling': (r"\b(?:this (?:isn't|is not) just (?:a|an|about)|this is where (?:it|things) get(?:s)? interesting|make no mistake|let me be (?:clear|honest)|to be (?:clear|honest|fair),|in other words,|simply put,|put simply,)\b", 'Delete the label; if the sentence needs it, it needs rewriting.'),
    'hedge-stack': (r"\b(?:may potentially|could possibly|might possibly|might perhaps|may perhaps|could potentially|arguably,? perhaps|somewhat arguably|potentially (?:could|might|may))\b", 'One hedge at most, where the uncertainty is real.'),
    'false-concession': (r"\b(?:while (?:it|this|that) (?:may|might|can) (?:seem|appear|look)[^.]{0,80}, (?:it|this|that) (?:is|actually)|at first glance,[^.]{0,80}(?:but|however|actually))", 'State what is true; skip the strawman first impression.'),
    'staged-objection': (r"\b(?:some (?:might|may|would) (?:say|argue|object)|you (?:might|may) (?:think|say|object)|one (?:could|might) (?:argue|object|say)|a skeptic (?:might|would))\b", 'Answer a real objection if one exists; do not invent one to knock down.'),
    'reader-steer-question': (r"(?:^|(?<=[.!?]\s))(?:Why does (?:this|that|it) matter\?|So what does (?:this|that|it) mean\?|What does (?:this|that) mean for\b[^?]{0,60}\?|Why\? Because|How\? By|The question is:? )", 'Say the answer.'),
    'circular-because': (r"\bbecause (?:it|they|we) (?:needed|had) to\b|\bbecause (?:it|this) (?:was|is) (?:necessary|needed|important)\b", 'Give the actual reason.'),
    'tool-artifact': (r"(?:oaicite|contentReference|turn\d+(?:search|view)\d+|\[citation needed\]|\bAs of my (?:last|knowledge) (?:update|cutoff)\b)", 'Remove the tool artifact.'),
    'placeholder': (r"(?:\[(?:insert|add|TODO|TBD|placeholder)[^\]]*\]|\bTODO\b|\bTBD\b|\blorem ipsum\b|\{\{[^}]+\}\})", 'Fill or cut the placeholder.'),
    'chat-scaffolding': (r"\b(?:I hope this helps|let me know if (?:you|there)|feel free to|happy to help|great question|certainly!|absolutely!|of course!|here(?:'s| is) (?:a|an|the) (?:quick |brief |short )?(?:summary|overview|breakdown|rundown))\b", 'Chat scaffolding: delete it.'),
    'ai-self-reference': (r"\b(?:as an AI(?: language model)?|as a (?:large )?language model|I(?:'m| am) (?:just )?an AI)\b", 'Delete.'),
    'ritual-conclusion': (r"(?:^|(?<=[.!?]\s))(?:In conclusion|In summary|To sum up|To summari[sz]e|All in all|At the end of the day|Ultimately|The bottom line(?: is)?|In the end|Overall),", 'End on the last real point, not a recap.'),
    'challenges-future': (r"\b(?:despite (?:these|its|the|some) challenges|the future (?:looks|is) (?:bright|promising)|only time will tell|remains to be seen|looking ahead,|paves? the way for|the road ahead|exciting times)\b", 'Name the next concrete step, or stop.'),
    'evaluative-tail': (r",\s*(?:and )?(?:which|that)(?:'s| is) (?:exactly|precisely|the whole) (?:the )?(?:point|what|why|idea)\b|,\s*a (?:testament|reminder|sign|nod) (?:to|of|that)\b", 'Cut the tail that tells the reader how to feel.'),
    'count-announce': (r"\b(?:here are (?:the )?(?:two|three|four|five|six|seven|\d+) (?:ways|things|reasons|lessons|takeaways|steps|key)|(?:^|(?<=[.!?]\s))(?:Two|Three|Four|Five) (?:things|lessons|reasons|takeaways)(?: stand out)?:)", 'List them; the count shows itself.'),
    'analogy-coach': (r"(?:^|(?<=[.!?]\s))(?:Think of (?:it|this|that) (?:like|as)|Imagine (?:a|an|you|if)|Picture (?:a|this|an))\b", 'Use the real case instead of an analogy, or let the drawing do it.'),
    'where-it-lives': (r"\b(?:this|that) is where [\w\s]{1,40} comes? in\b|\b(?:that|this)'s where [\w\s]{1,40} comes? in\b", 'Say what it does, directly.'),
    'invented-label': (r"\b(?:what I (?:like to )?call|I(?:'d| would)? like to call (?:it|this)|let's call (?:it|this)|call it the)\b", 'Use the house\'s existing name, or describe the thing.'),
    'stakes-inflation': (r"\b(?:changes everything|everything changes|fundamentally (?:changes|transforms|reshapes|alters)|revolutioni[sz](?:e|es|ed|ing)|unprecedented|groundbreaking|transformative|redefin(?:e|es|ed|ing) what)\b", 'Size the claim to the evidence.'),
    'rhetorical-triad': (r"(?:^|(?<=[.!?]\s))[A-Z][a-z]+\. [A-Z][a-z]+\. (?:And )?[A-Z][a-z]+\.", 'Three one-word beats: say it as one sentence.'),
    'offer-closer': (r"(?:^|(?<=[.!?]\s))(?:Want me to|Should I|Shall I|Would you like me to|Do you want me to)\b[^?]{0,160}\?", 'Chat closer: on a page, end on the last fact.'),
    'stock-metaphor': (r"\b(?:where (?:it|they|this|that) (?:lives|live|belongs|belong|lands|land)|earn(?:s|ed)? (?:its|their) (?:keep|place|stripes)|in the wild|the hard way|put (?:it|them|this) to the test|(?:came|come|comes|coming) full circle|(?:the|do(?:es)? the|did the) heavy lifting|where the rubber meets the road|st(?:and|ood|ands) on nothing|the (\w+) of the \\1|(?:a|the) (?:north star|secret sauce|silver bullet)|move the needle|at the end of the road|tells? (?:the|a) story)\b", 'Stock metaphor standing in for a fact (chairman 16/10: "tested where it lives"): say what happened.'),
    'personified-thing': (r"\b(?:the )?(?:books?|data|numbers|pages?|code|figures?|drawings?|site|day|night|run|pipeline|linter|gate) (?:speaks?|spoke|sings?|whispers?|breathes?|lives?|ran on|tells? (?:us|you)|wants?|knows?|remembers?|earns?)\b", 'A thing doing a person\'s act: name who did what, or state the fact.'),
    'manner-tag-en': (r",\s+(?:done (?:right|well|carefully|properly)|one (?:\w+) at a time|quietly|carefully|deliberately|gently|properly|cleanly)[.!?](?=\s|$)", 'Tacked-on manner tag (D11): delete it; if the manner matters, show it.'),
}

RATE = {
    'negative-parallelism': (r"\b(?:(?:it|this|that)(?:'s| is| was) not (?:just|only|merely|simply|about)|(?:isn't|wasn't|aren't) (?:just|only|merely|simply|about)|not (?:just|only|merely) (?:a|an|the)\b[^.;]{1,60}\bbut\b|more than (?:just )?(?:a|an)\b)", 1.3, 'Keep only if both sides are a real distinction; otherwise say the affirmative.'),
    'negated-inference': (r"\b(?:(?:is|was|are)n't|(?:is|was|are) not|(?:does|do|did)n't|(?:does|do|did) not|won't|will not|can't|cannot)\s+(?:enough|mean|prove|guarantee|replace|solve|settle|fix|equal|amount to|make it|change the|suffice|do the work|carry)\b", 0.5, 'House tic (EN form of "não basta"): say what does the work instead.'),
    'staged-reveal': (r"\b[^\n.!?]{2,100}:\s+[^\n.!?]{3,160}[.!?]", 11.6, 'If the second half only dramatizes the first, state the fact directly.'),
    'denial-restatement': (r"\bnot\b[^.;:!?]{1,100}[,;]\s*(?:but|rather|instead)\b\s+[^.;:!?]{2,100}", 1.3, 'Delete-the-"not" test: keep both halves only when both carry information.'),
    'rather-than': (r"\b(?:rather than|instead of)\b", 1.3, 'Use the affirmative when the contrast adds nothing.'),
    'triad-density': (r"\b[^,.!?;\n]{1,60},\s*[^,.!?;\n]{1,60},?\s+and\s+[^.!?;\n]{1,60}", 14.4, 'List as many items as there are, not three by habit.'),
    'stance-adverb': (r"\b(?:genuinely|truly|really|simply|merely|actually|literally|quietly|deeply|incredibly|remarkably|fundamentally|essentially|basically)\b", 7.5, 'Delete the intensifier unless it changes the meaning.'),
    'negation-chain': (r"(?:\bNo [^.!?]{1,40}[.!?]\s*){2,}\bNo [^.!?]{1,40}[.!?]|(?:\bwithout\s+[^,.;!?]{1,35},\s*){2,}(?:and\s+)?without\s+[^.;!?]{1,45}", 0.0, 'One negation carries it; three is a drumroll.'),
    'same-opener-run': (r"(?m)(?:^|(?<=[.!?]\s))([A-Z][\w-]{1,18})(?:\b[^.!?]*[.!?]\s+)(?:\1\b[^.!?]*[.!?]\s+){2}", 0.0, 'Vary openings only if the repetition is not doing work.'),
    'semicolon-correction': (r"[^.!?;]{3,100};\s*(?:but|rather|instead|in fact|that is|i\.e\.)\b,?\s+[^.!?]{3,120}[.!?]", 0.5, 'Two sentences, or one plain one.'),
    'colon-appositive': (r"\b(?:is|are|was|were|means|meant)\s*:\s*[^.!?]{3,100}[.!?]", 0.5, 'Drop the colon after a copula; say it.'),
    'stacked-questions': (r"[^.!?\n]{3,140}\?\s+[^.!?\n]{3,140}\?", 0.0, 'Keep at most one question; then answer it.'),
    'transition-opener': (r"(?m)(?:^|(?<=[.!?]\s))(?:Moreover|Furthermore|Additionally|In addition|Notably|Importantly|Crucially|Interestingly|That said|Consequently|Thus|Hence|Indeed),", 1.3, 'Most transitions can go; the order of the sentences carries it.'),
    'uniform-paragraphs': (r'(?!)', 0.0, 'Reshape paragraphs around the argument; never to a length quota.'),
    'ai-vocab-en': (r"\b(?:crucial|pivotal|vital|robust|seamless(?:ly)?|leverag(?:e|es|ed|ing)|foster(?:s|ed|ing)?|nuanc(?:e|ed|es)|intricate|multifaceted|comprehensive|meticulous(?:ly)?|elevat(?:e|es|ed|ing)|empower(?:s|ed|ing)?|vibrant|bustling|showcas(?:e|es|ed|ing)|underscor(?:e|es|ed|ing)|resonat(?:e|es|ed|ing)|captivating|streamlin(?:e|es|ed|ing)|cutting[- ]edge|landscape|realm|journey|unpack(?:s|ed|ing)?|key takeaways?|deep dive|crisp|nuance)\b", 1.3, 'Stock model vocabulary: use the plain word or the specific detail.'),
    'contrast-tail': (r",\s+(?:never|not|always)\s+(?!be\b|been\b|is\b|was\b)[a-z]+(?:\s+[a-z]+){0,3}[.!?](?=\s|$)", 1.2, 'Tacked-on contrast (D11, "X is Y, never Z"): end on Y, or make Z its own sentence if it matters.'),
    'authenticity-intensifier': (r"\b(?:a real|the real|the actual|the exact|exactly (?:the|what|how|why)|is exactly|the very)\b(?! estate| number| world)", 1.3, 'House tic (discovery 16/10: "a real" in 21% of our docs vs 3% human): drop the word; the noun is already real.'),
    'with-no': (r"\bwith no\b", 0.5, 'Often a tacked-on negative: say what it has.'),
    'catalogue-quantifier': (r"\b(?:every|each)\b", 3.7, 'House tic (16/10 distance test: 10 of 10 blog posts over the human range): "every lesson, every page" catalogues; name the count or the case instead.'),
    'em-dash-density': (r"\s?—\s?|\s--\s", 3.9, 'Em dashes are a model tic in English: use a comma, a colon or two sentences.'),
    'paren-scarcity': (r'(?!)', 0.0, 'Consider parenthetical material only when it clarifies.'),
}

# Measured backwards on the 16/10 backtest, off by default, kept with evidence:
# staccato-run: holdout 36% of human docs (PDF headings and footnotes read as fragments), model 0.2%;
# gap-talk: the backstage is meant to talk about its sources (it fired on 9% of the chairman's own messages).
RETIRED = {
    'gap-talk': (r"\b(?:the (?:source|record|text|book|file|data|page|slide)s? (?:doesn't|does not|don't|do not|never) (?:say|name|mention|state|tell|show|give)|there(?:'s| is) no record of|(?:we|I) don't (?:actually )?know (?:whether|if|what|who))\b", 1.2, 'Do not narrate what the source lacks; use what it has.'),
    'staccato-run': (r'(?!)', 0.0, 'Three fragments in a row: fold them into a sentence.'),
}

# Band (16/10 backtest): 'style' = a Part H rule that humans also break as often as our model (ratio < 1.5), so a hit
# is not evidence of model habit; every other rule is a 'tell' (the stock model tells stay tells even where our
# pages are clean: they guard against any model that writes here). rather-than, contrast-tail, authenticity-intensifier,
# staged-reveal, em-dash-density, with-no and negated-inference are the measured tells (Part H, H3).
STYLE = {'ritual-conclusion', 'formulaic-metatext', 'denial-restatement', 'stance-adverb', 'reader-address',
         'analogy-coach', 'transition-opener', 'negative-parallelism', 'triad-density', 'ai-vocab-en',
         'same-opener-run', 'stacked-questions', 'semicolon-correction', 'hedge-stack'}

PAREN = re.compile(r'\([^()\n]{2,100}\)')
# Terms where a flagged word is the right word (legal or house vocabulary).
TERMS = re.compile(r"\b(?:fundamental rights?|essential elements?|key (?:words?|figures?|dates?)|landscape (?:orientation|mode)|journey[- ]map|comprehensive (?:review|exam)|crucial date)\b", re.I)
