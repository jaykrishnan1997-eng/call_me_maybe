#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   models.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/26 11:12:35 by jay-k               #+#    #+#            #
#   Updated: 2026/09/30 14:01:58 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel
from typing import Literal


class Parameter(BaseModel):
    """A single function parameter's type constraint."""
    type: Literal["number", "string", "boolean", "integer"]


class FunctionDefinition(BaseModel):
    """A callable functions's name, parameters, and return type."""
    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: Parameter
