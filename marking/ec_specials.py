# TODO improve algorithm
def generate_ec_permutations(word):
    perms = ['']

    if word is None:
        return perms

    specials_map = {'e': ['e', 'ë'], 'c': ['c', 'ç']}
    for char in word:
        if char not in ['e', 'c']:
            perms = [perm + char for perm in perms]
        else:
            some_perms = [perm + specials_map[char][0] for perm in perms]
            other_perms = [perm + specials_map[char][1] for perm in perms]
            perms = some_perms + other_perms

    perms.remove(word)
    return perms
