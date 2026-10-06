*This project has been created as part of the 42 curriculum by jkrishna.*

# call_me_maybe

An LLM function-calling tool powered by constrained decoding.

## Description

Small language models are unreliable at producing structured output on request. Asked to
return JSON, a model like Qwen3-0.6B might add commentary, break syntax, invent keys, or
simply guess wrong on the format — even when the prompt explains exactly what's wanted.

`call_me_maybe` solves this without trusting the model's formatting at all. Given a natural
language prompt (e.g. *"What is the sum of 2 and 3?"*) and a set of available functions, it
does not ask the model to compute an answer or to freely write JSON. Instead it forces the
model, token by token, to produce **only** a valid function call: a function name chosen from
the real set of available functions, and arguments whose types match that function's schema.
The model never sees the possibility of producing anything else, because every illegal next
token is masked out before it can be chosen — this is **constrained decoding**.

The output is never `5`; it is:

```json
{"prompt": "What is the sum of 2 and 3?", "name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

Computing the actual answer is deliberately out of scope — this project decides *what to
call and with what arguments*, the same way real tool-calling/function-calling systems in
production LLM APIs work: the model chooses, a separate trusted system executes.

## Instructions

### Prerequisites

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) for package and environment management

### Installation

```bash
make install
```

This installs the project's own dependencies (`numpy`, `pydantic`) as well as `llm_sdk`,
which is wired in as a `uv` workspace member and pulls in `torch`, `transformers`, and
`huggingface-hub` to load and run the model. On 42 campus machines the Makefile
automatically redirects `uv`'s cache, the Hugging Face model cache, and the virtual
environment itself to `/goinfre`, since home directory quotas are too small for the
downloaded model weights; on any other machine it falls back to normal defaults.

### Running

```bash
make run python -m src [--functions_definition <path>] [--input <path>] [--output <path>]
```

By default the program reads from `data/input/functions_definition.json` and
`data/input/function_calling_tests.json`, and writes to
`data/output/function_calling_results.json`. Example:

```bash
make run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

or simply:

```bash
make run
```

### Other Makefile targets

- `make lint` / `make lint-strict` — flake8 + mypy (own code only; `llm_sdk`'s internals
  are excluded, since they are provided, not authored, and not to be modified)
- `make clean` / `make fclean` / `make purge` — remove build artifacts, the virtual
  environment, and (for `purge`) the downloaded model/uv caches

## Algorithm Explanation

The core idea: a language model produces one probability score (a **logit**) per possible
next token at every step. Normally you'd pick the highest-scoring token and move on. Constrained
decoding intervenes *before* that pick: at every step, a legality check computes which tokens
are even allowed given the JSON structure and schema so far, sets every other token's score to
`-infinity`, and only then takes the best-scoring token among what's left. The model can
never produce an illegal token, because it is never given the option.

The output for one prompt is built as a fixed sequence of phases, alternating between text
the program forces outright and text the model genuinely chooses:

1. **Force** the literal prefix `{"name":"`.
2. **Choose**: the model selects one function name from the real, loaded set of function
   names — never a hardcoded list, since the function set can change between runs. This is
   a choice-set constraint: at each step, only tokens that keep the generated text a prefix
   of *at least one* remaining candidate name are legal.
3. **Force** the literal bridge `","parameters":{`.
4. **For each parameter of the chosen function, in schema order:**
   - **Force** the parameter's key and colon (`"a":`), and, for a string parameter, the
     opening quote.
   - **Generate** the value, using a type-specific legality check:
     - *number*: only digits, at most one `.`, and `-` only at the very start are legal.
       Generation stops once a comma or closing brace outranks any legal digit continuation.
     - *string*: any character is legal except an unescaped `"` or an invalid backslash
       escape (checked with proper odd/even backslash-parity counting, so `\"` inside a
       string is correctly treated as an escaped quote, not a terminator). Since the closing
       quote itself is never a "legal" token under this rule, the tokens that would close the
       string are tracked separately and allowed to compete against the best legal
       continuation on every round; generation stops the moment a closing token outscores it.
   - **Force** the closing punctuation: `,` if more parameters follow, or the closing braces
     `}}` if this was the last one.
5. **Force** the final `}`.

Every forced and generated token is appended to the model's running context (`input_ids`),
so by the time the model has to produce a value, it is looking at syntactically valid JSON
built so far — it is continuing correct JSON, not inventing structure from nothing.

A separate piece of context, built fresh from the loaded function definitions on every run,
lists the available functions and their descriptions before the actual question. Without
this, the model has no way to know which functions exist and defaults to picking one
function for every prompt regardless of content; with it, function selection becomes
reliable across all provided test prompts.

## Design Decisions

- **Two legality primitives underlie everything.** `legal_next_tokens` (does a candidate
  token keep the generated text a prefix of one known target?) and its choice-set
  counterpart, `legal_choice_tokens` (a prefix of *any* remaining candidate?) are used for
  forced literals and function-name selection respectively. `legal_number_tokens` and
  `legal_string_tokens` are the same idea applied to type semantics instead of an exact
  target. All four return the same shape (a list of legal token IDs), which is why the
  four generation loops built on top of them (`force_literal`, `choose_from`,
  `generate_number`, `generate_string`) share the same structure: compute legal tokens,
  get real logits, pick the best legal one, append, repeat.
- **Values are tracked as real Python types, not re-parsed from text.** Each parameter's
  generated value is converted (`float(...)` for numbers) and stored directly into the
  result dictionary as it is produced, rather than assembling one long string and parsing
  it back into JSON afterward.
- **Output keys follow the subject document and the moulinette's own grading script**
  (`prompt`, `name`, `parameters`). The evaluation scale's manual checklist independently 
  lists `fn_name`/`args` instead — this is a real discrepancy between the subject and the
  scale, documented here rather than left for the evaluator to discover. The subject's
  worked example (V.4.1) and the moulinette's `grade_student_answers` (which reads
  `student_answer.get("name")` / `student_answer.get("parameters", {})`) both use
  `name`/`parameters`, and the moulinette is the actual automated scoring mechanism, so
  this implementation follows that rather than the scale's checklist wording.
- **`llm_sdk` is treated as read-only, external code.** It is wired in as its own `uv`
  workspace member rather than modified or flattened into this project's own source, and
  it is excluded from this project's own lint/type checks, since it is provided rather
  than authored and no private methods or attributes of `Small_LLM_Model` are used.
- **A round cap (40 tokens) backstops string generation** as a last resort against a
  genuinely stuck generation loop. In practice it is rarely if ever reached once the
  closing-token competition (described above) is in place; it exists purely for safety,
  not as the primary stopping mechanism.
- **Pydantic validates the function-definition schema on load**, including restricting a
  parameter's `type` to the literal values `"number"`, `"string"`, `"boolean"` — an
  unexpected type fails loudly and clearly at load time rather than causing a confusing
  failure deep inside generation.

## Performance Analysis

On the provided 11-prompt test set, constrained decoding guarantees syntactically valid,
schema-compliant JSON for every output by construction — the model is structurally
incapable of producing anything else. Function selection and argument extraction were
verified correct across all 11 provided prompts, including the three-string-parameter
`fn_substitute_string_with_regex` case, and additionally stress-tested against a hand-built
set of adversarial prompts (unanswerable questions, empty/whitespace-only prompts, extreme
and negative numbers, apostrophes and escape sequences inside names and strings) with no
crashes. The full provided test set runs well within the required 5-minute budget.

## Challenges Faced

- **Escaped quotes inside JSON strings.** Detecting whether a `"` inside a generated string
  is a real terminator or an escaped literal character (`\"`) required counting the parity
  of the run of backslashes immediately preceding it, not just checking the previous
  character — a naive one-character look-back misclassifies `\\"` (an escaped backslash
  followed by a real closing quote).
- **The model would not reliably choose to stop a string on its own.** Investigation showed
  the model's actual preferred next token after a completed value was almost always a
  *merged* token that already included the closing quote plus subsequent punctuation (for
  example `"}}`, `","`), rather than a bare `"`. Since every such merged token contains an
  unescaped quote, the legality check correctly masked all of them — meaning the model's
  real intent to stop was never visible to a stop condition that only checked for the bare
  quote winning. The fix was to let every token that *starts* with an unescaped quote
  compete against the best legal continuation at each step, and to stop as soon as one of
  them wins, without appending it (the surrounding forced literal supplies the real
  ending).
- **Function selection defaulted to one function for every prompt** until the model was
  given a list of the available functions and their descriptions as context before the
  question — without that, it had no basis on which to choose and settled on one answer
  for everything.
- **The subject's worked example and the evaluation scale's checklist disagree** on the
  output field names (`name`/`parameters` vs. `fn_name`/`args`); this was resolved in favor
  of the subject and the moulinette's grading script, documented above under Design
  Decisions.

## Testing Strategy

Each masking/generation primitive was built and verified in isolation before being wired
into the full pipeline: forced-literal generation was tested by forcing a fixed JSON
fragment out of the real model and checking it matched byte-for-byte; choice-set selection
was tested against the real 5 function names with real prompt context; number and string
generation were each tested standalone against representative parameter values before being
combined. The full pipeline was then run against all 11 provided prompts and checked by
hand for correctness, followed by a hand-built adversarial test file covering unanswerable
prompts, empty/whitespace prompts, extreme and negative numbers, and unusual characters, to
probe robustness beyond the happy path. File-loading error handling was verified by
deliberately corrupting copies of the input files (missing file, invalid JSON syntax, a
parameter with an invalid `type`, a prompt entry missing its `prompt` key) and confirming
each produces a single clear message and a clean exit rather than a crash or traceback.

## Example Usage

```bash
make run
cat data/output/function_calling_results.json
```

```json
[
{"prompt": "What is the sum of 2 and 3?", "name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}},
{"prompt": "Greet shrek", "name": "fn_greet", "parameters": {"name": "shrek"}}
]
```

## Resources

- Jurafsky & Martin, *Speech and Language Processing* (3rd ed. draft) — Chapter 2
  (tokenization, byte-pair encoding): https://web.stanford.edu/~jurafsky/slp3/
- Willard & Louf, *Efficient Guided Generation for Large Language Models* (the Outlines
  paper, on FSM-based guided generation): https://arxiv.org/abs/2307.09702
- LMSYS / SGLang blog, *Fast JSON Decoding for Local LLMs with Compressed Finite State
  Machine*: https://lmsys.org/blog/2024-02-05-compressed-fsm
- Andrej Karpathy, *Let's build the GPT Tokenizer* (byte-pair encoding, tokenizer
  internals): https://www.youtube.com/watch?v=zduSFxRajkE
- Python `argparse` documentation, for the CLI: https://docs.python.org/3/library/argparse.html
- [JSONLint](https://jsonlint.com/), used during manual testing to confirm input/output
  file validity
- The provided `llm_sdk` package itself, read directly to understand `encode`,
  `get_logits_from_input_ids`, and `get_path_to_vocab_file`, since it is the only interface
  to the Qwen/Qwen3-0.6B model used throughout
- https://huggingface.co/docs/transformers/index
- https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/vocab.json
 
 
 
**Use of AI:** Use of AI: Used to explain concepts (tokenization, logits, constrained decoding) and to point out bugs in hand-written code for me to fix myself, not to supply fixes directly. All core logic — legality checks, generation loops, state machine, CLI/I/O — was written and debugged by hand. AI help was also used to build the Makefile so the project works consistently on both 42 lab machines and a home PC — specifically, where the virtual environment and caches should be stored (redirected to `/goinfre` on campus machines, default locations elsewhere).