#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/21 10:51:39 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/26 19:46:20 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model
from .vocab import id_to_str
from .json_fsm import force_literal, legal_choice_tokens, choose_from
from .schema_constraints import (
    legal_number_tokens, generate_number, legal_string_tokens,
    generate_string)
from .io_utils import load_function_definitions, load_prompts
import json

model = Small_LLM_Model()
ids = model.encode("Hello")[0].tolist()
print(ids)

logits = model.get_logits_from_input_ids(ids)
print(len(logits), max(logits))

vocab_path = model.get_path_to_vocab_file()
with open(vocab_path) as f:
    vocab = json.load(f)
print(len(vocab), list(vocab.items())[:5])

result = id_to_str(vocab)
print(list(result.items())[:10])

print("======================")

input_ids_so_far = model.encode("some starting text")[0].tolist()
print(force_literal('{"name":"', model, result, input_ids_so_far))

print("==========================")

candidates = ["cat", "car", "cap"]

for token_id in legal_choice_tokens(
    candidates, "ca", result
):
    print(token_id, result[token_id])

print("=========================")

candidates = [
    "fn_add_numbers", "fn_greet", "fn_reverse_string", "fn_get_square_root",
    "fn_substitute_string_with_regex"]
input_ids_so_far = model.encode("What is the sum of 2 and 3? Function to call: ")[0].tolist()
print(choose_from(candidates, model, result, input_ids_so_far))

# input_ids_so_far = model.encode("add 2 and 3?")[0].tolist()
# print(choose_from(candidates, model, result, input_ids_so_far))

# print("===========================")

# ids = legal_number_tokens("1", result)
# print([result[i] for i in ids][:30])

# ids = legal_number_tokens("1.5", result)
# print([result[i] for i in ids][:30])

# print("============================")
# input_ids_so_far = model.encode(
#     "What is the sum of 2 and 3? Functions: fn_add_numbers. Parameter a: "
# )[0].tolist()
# print(generate_number(model, result, input_ids_so_far))

# input_ids_so_far = model.encode(
#     "What is the sum of 2 and 3? Functions: fn_add_numbers. Parameter b: "
# )[0].tolist()
# print(generate_number(model, result, input_ids_so_far))

# print("===========================")
# quote_id = None
# backlash_id = None
# for token_id, token_string in result.items():
#     if token_string == '"':
#         quote_id = token_id
#     if token_string == '\\':
#         backlash_id = token_id

# print(quote_id in legal_string_tokens("hel", result))
# print(backlash_id in legal_string_tokens("hel", result))
# print(quote_id in legal_string_tokens("hel\\", result))

print("=======================")
print("generate_string fun check")

input_ids_so_far = model.encode(
    'fn_greet(name:"Bob")\n'
    'fn_greet(name:"'
)[0].tolist()
print(generate_string(model, result, input_ids_so_far))

print("=======================")
print("real file loading check")

functions = load_function_definitions("data/input/fuunctions_definitions.json")
prompts = load_prompts("data/input/fuunction_calling_tests.json")

print(f"loaded {len(functions)} functions")
for f in functions:
    print(" -", f.name)

print(f"loaded {len(prompts)} prompts")
for p in prompts:
    print(" -", p)
