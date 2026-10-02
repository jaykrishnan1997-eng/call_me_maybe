#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   schema_constraints.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/24 17:01:58 by jay-k               #+#    #+#            #
#   Updated: 2026/10/02 12:19:29 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model


def legal_number_tokens(
    generated_so_far: str, id_to_str: dict[int, str]
) -> list[int]:
    """ legal checker for JSON number values"""

    legal_token_id: list[int] = []
    for token_id, token_string in id_to_str.items():
        candidate = generated_so_far + token_string
        count_minus = 0
        count_punkt = 0
        count_digits = 0
        if "-" in candidate:
            if not candidate.startswith("-"):
                continue
        dot = candidate.find(".")
        if dot != -1 and (dot == 0 or candidate[dot - 1] not in "0123456789"):
            continue
        for character in candidate:
            if character == "-":
                count_minus += 1
            elif character == ".":
                count_punkt += 1
            elif character in "0123456789":
                count_digits += 1
            else:
                break
        total_count = count_punkt + count_minus + count_digits
        if (
            count_minus < 2 and count_punkt < 2
            and total_count == len(candidate)
            and len(candidate) > 0
        ):
            legal_token_id.append(token_id)
    return legal_token_id


def generate_number(
    model: Small_LLM_Model, id_to_str: dict[int, str],
    input_ids_so_far: list[int]
) -> str:
    """Generate the digits of a JSON number
     value, stopping before a seperator"""
    generated_so_far = ""
    comma_id = -1
    for token_id, token_string in id_to_str.items():
        if token_string == ",":
            comma_id = token_id
    while True:
        max_token_id = -1
        max_token_logits = float("-inf")
        legal_ids = legal_number_tokens(generated_so_far, id_to_str)
        logits = model.get_logits_from_input_ids(input_ids_so_far)
        for token_id in legal_ids:
            if logits[token_id] >= max_token_logits:
                max_token_id = token_id
                max_token_logits = logits[token_id]
        can_stop = (
            generated_so_far != ""
            and generated_so_far != "-"
            and not generated_so_far.endswith(".")
        )
        if can_stop and logits[comma_id] > max_token_logits:
            break
        generated_so_far += id_to_str[max_token_id]
        input_ids_so_far.append(max_token_id)
    return generated_so_far


def legal_string_tokens(
    generated_so_far: str, id_to_str: dict[int, str]
) -> list[int]:
    """Which tokens keep the body free of a literal quote character?
    Backslashes are ordinary text, except right before a quote, where
    \\" is allowed as a way to embed a literal quote in the value"""
    legal_token_id: list[int] = []
    for token_id, token_string in id_to_str.items():
        candidate = generated_so_far + token_string
        temp = candidate.replace('\\"', "")  # drops escape quotes
        if '"' not in temp:
            legal_token_id.append(token_id)
    return legal_token_id


def generate_string(
    model: Small_LLM_Model, id_to_str: dict[int, str],
    input_ids_so_far: list[int]
) -> str:
    """Generate the body of a JSON string value (without the quotes)."""
    closing_ids = [i for i, s in id_to_str.items() if s.startswith('"')]
    generated_so_far = ""
    generated_ids: list[int] = []

    for _ in range(40):
        logits = model.get_logits_from_input_ids(input_ids_so_far)
        legal_ids = legal_string_tokens(generated_so_far, id_to_str)
        if not legal_ids:
            break
        best_id = max(legal_ids, key=lambda i: logits[i])

        can_close = generated_so_far != ""
        if can_close:
            best_close = max(closing_ids, key=lambda i: logits[i])
            if logits[best_close] > logits[best_id]:
                break

        generated_so_far += id_to_str[best_id]
        generated_ids.append(best_id)
        input_ids_so_far.append(best_id)

    text = model.decode(generated_ids)
    text = text.replace('\\"', '"')
    text = text.replace("\\\\", "\\")
    return text
