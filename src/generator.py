#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   generator.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/28 09:33:17 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/29 11:17:27 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .json_fsm import force_literal, choose_from
from .schema_constraints import generate_number, generate_string
from .models import FunctionDefinition
from llm_sdk import Small_LLM_Model


def build_context(prompt: str, functions: list[FunctionDefinition]) -> str:
    """Build the text, the model reads before it starts generating."""
    lines = ["Available functions:"]
    for f in functions:
        params = ", ".join(f.parameters.keys())
        lines.append(f"- {f.name}({params}): {f.description}")
    lines.append("")
    lines.append(f"Request: {prompt}")
    lines.append("Function call as JSON:")
    return "\n".join(lines) + "\n"


def process_prompt(
    prompt: str, model: Small_LLM_Model,
    id_to_str: dict[int, str],
    functions: list[FunctionDefinition],
) -> dict[str, object]:
    """Run one prompt through the model and
    return its function call as a dict"""
    parameters: dict[str, str | float] = {}
    input_ids_so_far = model.encode(
        build_context(prompt, functions))[0].tolist()

    force_literal('{"name":"', model, id_to_str, input_ids_so_far)
    chosen_name = choose_from(
        [f.name for f in functions], model, id_to_str, input_ids_so_far)

    for f in functions:
        if f.name == chosen_name:
            function = f
            break
    force_literal('","parameters":{', model, id_to_str, input_ids_so_far)
    total = len(function.parameters)
    for index, (param_name, param) in enumerate(function.parameters.items()):
        if index == total - 1:
            is_last = True
        else:
            is_last = False

        if param.type == "number":
            force_literal(
                f'"{param_name}":', model, id_to_str, input_ids_so_far)
            parameters[param_name] = float(
                generate_number(model, id_to_str, input_ids_so_far))
            after = "}}" if is_last else ","

        elif param.type == "string":
            force_literal(
                f'"{param_name}":"', model, id_to_str, input_ids_so_far)
            parameters[param_name] = generate_string(
                model, id_to_str, input_ids_so_far)
            after = '"}}' if is_last else '",'

        else:
            raise ValueError(f"Unsupported parameter type: {param.type}")

        force_literal(after, model, id_to_str, input_ids_so_far)

    return {"prompt": prompt, "name": function.name, "parameters": parameters}
