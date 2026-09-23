#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   json_fsm.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/22 15:35:14 by jay-k               #+#    #+#            #
#   Updated: 2026/09/23 13:09:27 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #


def legal_next_tokens(
    target: str, generated_so_far: str, id_to_str: dict[int, str]
) -> list[int]:
    """ Give me the legal next tokens for this target
    , generated what i've generated so far"""

    legal_token_id: list[int] = []

    for token_id, token_string in id_to_str.items():
        candidate = generated_so_far + token_string
        if target.startswith(candidate):
            legal_token_id.append(token_id)

    return legal_token_id


def force_literal(
    target: str, model, id_to_str: dict[int, str], input_ids_so_far: list[int]
) -> str:

    generated_so_far = ""
    while (generated_so_far != target):
        max_token_id = -1
        max_token_logits = float("-inf")
        legal_ids = legal_next_tokens(target, generated_so_far, id_to_str)
        logits = model.get_logits_from_input_ids(input_ids_so_far)
        for token_id in legal_ids:
            if logits[id] >= max_token_logits:
                max_token_id = token_id
                max_token_logits = logits[token_id]
        generated_so_far += id_to_str[max_token_id]
        input_ids_so_far.append(max_token_id)
    return generated_so_far
