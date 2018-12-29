# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx
            #temp_word = lower_word[:index] + vowel + lower_word[(index+1):]

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    """ If length of string is one then return it otherwise remove first element 
        of the sequence and call this function again with sequence(without first element of it)
        and put first element of the sequence into every possible places in return value.
    """
    
    if len(sequence) == 1 :
        return [sequence]
    else:
        all_permutations = []
        for comb in get_permutations(sequence[1:]):
            for index in range(len(comb)+1):
                all_permutations.append(comb[:index] + sequence[0] + comb[index:])
    return all_permutations



if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    print(get_permutations("hjk"))
