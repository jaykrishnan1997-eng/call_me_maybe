#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   vocab.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/22 12:32:46 by jay-k               #+#    #+#            #
#   Updated: 2026/09/22 15:00:22 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #


def id_to_str(vocab: dict[str, int]) -> dict[int, str]:
    id_to_str_dict: dict[int, str] = {}
    for key in vocab.keys():
        id_to_str_dict[vocab[key]] = key
    return id_to_str_dict


# end of sequence checker
def eos_checker(tokenid: int) -> bool:
    return tokenid in (151645, 151643)
