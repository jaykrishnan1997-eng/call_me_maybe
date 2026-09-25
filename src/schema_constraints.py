#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   schema_constraints.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/24 17:01:58 by jay-k               #+#    #+#            #
#   Updated: 2026/09/25 20:47:09 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def legal_number_tokens(generated_so_far: str, id_to_str: dict[int, str]) -> list[int]:
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
    model, id_to_str: dict[int, str], input_ids_so_far: list[int]
) -> str:
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


def count_trailing_backslashes(candidate: str, j: int) -> bool:
    count_slash = 0
    while j > 0:
        j -= 1
        if candidate[j] == '\\':
            count_slash += 1
        else:
            break
    if count_slash % 2 == 0:
        return True
    else:
        return False


def legal_string_tokens(generated_so_far, id_to_str):
    """Which tokens keep the next a legal, still-open JSON string body?"""
    i: int
    legal_token_id: list[int] = []
    for token_id, token_string in id_to_str.items():
        found_illegal = False
        candidate = generated_so_far + token_string
        i = 0
        for i in range(0, len(candidate)):
            if (
                candidate[i] == '\\'
                and i + 1 != len(candidate)
                and candidate[i + 1] not in ('"','\\','/','n','t','r','b','f')
            ):
                found_illegal = True
                break
            if (
                candidate[i] == '"'
                and count_trailing_backslashes(candidate, i)
            ):
                found_illegal = True
                break
        if not found_illegal:
            legal_token_id.append(token_id)
    return legal_token_id


def generate_string(
    model, id_to_str: dict[int, str], input_ids_so_far: list[int]
) -> str:
    rounds = 0
    generated_so_far = ""
    quote_id = -1
    for token_id, token_string in id_to_str.items():
        if token_string == '"':
            quote_id = token_id
    while True:
        rounds += 1
        max_token_id = -1
        max_token_logits = float("-inf")
        legal_ids = legal_string_tokens(generated_so_far, id_to_str)
        logits = model.get_logits_from_input_ids(input_ids_so_far)
        for token_id in legal_ids:
            if logits[token_id] >= max_token_logits:
                max_token_id = token_id
                max_token_logits = logits[token_id]
        if (
            (max_token_id == quote_id
            and len(generated_so_far) > 0)
            or rounds > 40
        ):
            break
        generated_so_far += id_to_str[max_token_id]
        input_ids_so_far.append(max_token_id)
        print(repr(generated_so_far))
    return generated_so_far
