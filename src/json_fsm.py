#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   json_fsm.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/22 15:35:14 by jay-k               #+#    #+#            #
#   Updated: 2026/09/22 21:42:45 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def legal_next_tokens(target: str, generated_so_far: str, id_to_str: dict[int, str]) -> list[int]:
    """ Give me the legal next tokens for this target, generated what i've generated so far"""

    legal_token_id: list[int] = []

    for token_id, token_string in id_to_str.items():
        candidate = generated_so_far + token_string
        if target.startswith(candidate):
            legal_token_id.append(token_id)

    return legal_token_id

