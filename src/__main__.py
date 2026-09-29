#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/21 10:51:39 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/29 15:06:05 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import json
import pathlib
import traceback

from llm_sdk import Small_LLM_Model
from .vocab import id_to_str
from .io_utils import load_function_definitions, load_prompts
from .generator import process_prompt
from .cli import parse_args


def main() -> None:

    result = []
    model = Small_LLM_Model()
    args = parse_args()

    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path) as f:
        vocab = json.load(f)

    id_to_str_map = id_to_str(vocab)

    functions = load_function_definitions(args.functions_definition)
    prompts = load_prompts(args.input)

    for prompt in prompts:
        generated = process_prompt(prompt, model, id_to_str_map, functions)
        result.append(generated)
        print(f"\n{generated}")

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput JSON file in: {args.output}\n")
    with open(args.output, "w") as g:
        json.dump(result, g, indent=2)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
