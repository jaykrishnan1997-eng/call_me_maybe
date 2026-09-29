#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   cli.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 11:50:00 by jkrishna            #+#    #+#            #
#   Updated: 2026/09/29 12:57:19 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import argparse


def parse_args() -> argparse.Namespace:
    """Parse the CLI arguments for
    function_definition, input, and output paths."""
    parser = argparse.ArgumentParser(
        description="Translate natural language"
        "prompt into structured function calling"
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json"
    )
    parser.add_argument(
        "--input", default="data/input/function_calling_tests.json")
    parser.add_argument(
        "--output", default="data/output/function_calling_results.json")
    return parser.parse_args()
