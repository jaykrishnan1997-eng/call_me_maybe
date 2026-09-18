# call_me_maybe

## VOCABULARY:
    1. Basically the collection of tokens from the tokenizer/model.
    2. Total number of the token constitues the vocabulary size.
    3. While predecting next token LLM scores every single token.

## LOGITS:
    The scores mentioned in the vovabulary sessions are called logits. Using probability created from logits we decide which token to be accepted as the next token.

## EXAMPLE:
    Lets consider a question: "The cat is", now we have four seperate steps:
    1.  Tokenization: Tokenizer breaks the sentence into token:
        ["The", " cat", " is"]
        note the space within the tokens.
    2.  Token ID: Instead of processing the word directly, each token get a random ID:
        [154, 3921, 325]
    3.  Scoring: For every possible next token a logits is given:
        " sleeping" -> 8.2
        " hungry"   -> 6.9
        " running"  -> 4.1
        " blue"     -> 1.2
        ...
    4.  Percentage covertion: Mathematical function called "softmax" converts the logits into probabilities after normalization.
        " sleeping" -> 60%
        " hungry"   -> 25%
        " running"  -> 8%
        " blue"     -> 1%
        ...
    5.  Selection: Now the token with max probabilty is selected. So the text become:
        The cat is sleeping
    6.  And this process repeats.

 
