#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   io_utils.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/26 12:55:28 by jay-k               #+#    #+#            #
#   Updated: 2026/09/26 19:33:49 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from .models import Parameter, FunctionDefinition, ValidationError


def load_function_definitions(path: str) -> list[FunctionDefinition]:
    """Load and validate function definitions from JSON file."""
    function_list: list[FunctionDefinition] = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for function in data:
            function_object = FunctionDefinition(**function)
            function_list.append(function_object)
    except FileNotFoundError:
        raise ValueError("input file not found")
    except json.JSONDecodeError:
        raise ValueError("Error while decoding")
    except ValidationError:
        raise ValueError("Error while validating")
    return function_list


def load_prompts(path: str) -> list[str]:
    """Load the list of test prompts from a JSON file."""
    prompt_list: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for entry in data:
            prompt_list.append(entry["prompt"])
    except FileNotFoundError:
        raise ValueError("input file not found")
    except json.JSONDecodeError:
        raise ValueError("Error while decoding")
    except KeyError:
        raise ValueError("Malformed file: missing 'prompt' key")
    return prompt_list
