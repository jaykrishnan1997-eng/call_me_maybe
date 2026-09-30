#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   io_utils.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/26 12:55:28 by jay-k               #+#    #+#            #
#   Updated: 2026/09/30 09:15:16 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from .models import FunctionDefinition
from pydantic import ValidationError


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
        raise ValueError(f"Function definitions file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
    except ValidationError as e:
        raise ValueError(
            f"Function definitions in {path} do not match"
            f" the expected schema: {e}"
        )
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
        raise ValueError(f"Prompts file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
    except KeyError:
        raise ValueError(
            f"Malformed prompt entry in {path}: "
            "missing 'prompt' key")
    return prompt_list
