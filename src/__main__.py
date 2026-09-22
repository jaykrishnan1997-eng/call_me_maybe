#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/21 10:51:39 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/22 14:03:01 by jay-k              ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from llm_sdk import Small_LLM_Model
from .vocab import id_to_str
import json

model = Small_LLM_Model()
ids = model.encode("Hello")[0].tolist()
print(ids)

logits = model.get_logits_from_input_ids(ids)
print(len(logits), max(logits))

vocab_path = model.get_path_to_vocab_file()
with open(vocab_path) as f:
    vocab = json.load(f)
print(len(vocab), list(vocab.items())[:5])

result = id_to_str(vocab)
print(list(result.items())[:10])


# model = Small_LLM_Model()
# # ids = model.encode("Hello")[0].tolist()
# # print(ids)

# # logits = model.get_logits_from_input_ids(ids)
# # print(len(logits), max(logits))

# vocab_path = model.get_path_to_vocab_file()
# with open(vocab_path) as f:
#     vocab = json.load(f)

# # print(len(vocab), list(vocab.items())[:10])
# # print(type(vocab))
