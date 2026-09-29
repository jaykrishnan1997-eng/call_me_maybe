#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   vocab.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/22 12:32:46 by jay-k               #+#    #+#            #
#   Updated: 2026/09/29 11:20:43 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


def id_to_str(vocab: dict[str, int]) -> dict[int, str]:
    """Flip a string-to-id vocab dict into a id-to-string dict."""
    id_to_str_dict: dict[int, str] = {}
    for key in vocab.keys():
        id_to_str_dict[vocab[key]] = key
    return id_to_str_dict


def eos_checker(tokenid: int) -> bool:
    """end of sequence checker (using EOS token ids)"""
    return tokenid in (151645, 151643)
