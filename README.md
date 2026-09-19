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

### TOKENIZATION:
    Program cannot feed the entire sentense directly into a neural network, so each  words, spaces and special characters are converted to token and given an ID called token ID. This entire process is called Tokenization.
 
## TOKEN:
    * Basic unit of text that a particular tokenizer has decided to use.

    * A sentense is N tokens according to a particular token. Kind of like seeds in random.

    * Token can be:
        1. word tokenization : ["The", " cat", " is", " sleeping", "."]
        2. subword-style tokenization : ["un", "believ", "able"] this is just a case ["un", "believable"]
        3. character tokenization: ["H", "e", "l", "l", "o", " !"]
    
    * making every word a token will result in enormous vocabulary.
    * So best practice : ["play"] + "s"/"ed"/"ing"/"full"/"er" etc. LLM work in subword-style tokenization.
    * Fewer token means less computation for same test so no character by character tokeization.
    * Tokens should be small enough to represent unfamiliar text, but large enough to 
    effeciently represent common pieces of language.
    * Note spaces are important when it comes to tokenization. Space are part of the structure of text.
    * Punctuations can also be token.
    * Common words are efficient tokens.

## BPE - Byte Pair Encoding:
    Algorithm that automatically breaks up input text into tokens. This algorithm uses simple statistics of letter sequences to induce a vocabulary of subword tokens.

    Example say [low, low, lower, lowest] is in test data. Now if we use character tokenization we see l o w always occour together in the four case so the token will be: lower : ["low", "er"] and lowest : ["low", "est"].
    

 