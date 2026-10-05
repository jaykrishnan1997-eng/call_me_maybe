#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   vocab.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/22 12:32:46 by jay-k               #+#    #+#            #
#   Updated: 2026/10/05 19:38:56 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #


def id_to_str(vocab: dict[str, int]) -> dict[int, str]:
    """Flip a string-to-id vocab dict into a id-to-string dict."""
    id_to_str_dict: dict[int, str] = {}
    for key in vocab.keys():
        id_to_str_dict[vocab[key]] = key
    return id_to_str_dict
