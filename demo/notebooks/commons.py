from string import punctuation


def remove_symbols(description: str, remove_map: dict) -> str:
    """
    """
    for old, new in remove_map.items():
        description = description.replace(old, new)
    return description.lower()


def extract_symbols(description: str, available_symbols: list) -> set:
    s = set()
    prev = ''
    for word in description.split():
        if word in available_symbols:
            s.add(word)
        elif f'{prev} {word}' in available_symbols:
            s.add(f'{prev} {word}')
        prev = word
    return s


def translate_skills(skills: set, skills_frame, toId=False) -> set:
    if toId:
        return skill_to_id(skills, skills_frame)
    else:
        return id_to_skill(skills, skills_frame)


def id_to_skill(skills: set[int], skills_frame) -> set[str]:
    out = set()
    for skill in skills:
        out.add(skills_frame.loc[skill, 'SKILL'])

    return out


def skill_to_id(skills: set[str], skills_frame) -> set[int]:
    out = set()
    for skill in skills:
        out.add(
            list(
                skills_frame.loc[
                    skills_frame['SKILL'].apply(lambda val: val.lower()) == skill.lower()
                    ].index
            )[0]
        )

    return out


# Symbols to remove
punct = [p for p in punctuation]
punct.remove('+')
punct.remove('#')
# punct.remove('.')

removal = {p: ' ' for p in punct}
removal['\n'] = ' '
removal['/'] = ' '
removal['('] = ' '
removal[')'] = ' '
removal[','] = ' '
removal['>'] = ' '
removal['.'] = ' .'