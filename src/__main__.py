#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/21 10:51:39 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/29 14:09:55 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model
from .vocab import id_to_str
# from .json_fsm import force_literal, legal_choice_tokens, choose_from
# from .schema_constraints import (
#     legal_number_tokens, generate_number, legal_string_tokens,
#     generate_string)
from .io_utils import load_function_definitions, load_prompts
from .generator import process_prompt
# from .generator import build_context
from .cli import parse_args
import json
import pathlib

result = []
model = Small_LLM_Model()
args = parse_args()

vocab_path = model.get_path_to_vocab_file()
with open(vocab_path) as f:
    vocab = json.load(f)
print(len(vocab), list(vocab.items())[:5])

id_to_str_map = id_to_str(vocab)

functions = load_function_definitions(args.functions_definition)
prompts = load_prompts(args.input)

for prompt in prompts:
    generated = process_prompt(prompt, model, id_to_str_map, functions)
    result.append(generated)

output_path = pathlib.Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(args.output, "w") as g:
    json.dump(result, g, indent=2)
