from math import isclose

def checker(contestant_output, jury_answer, flag="string", trailing_zero=False, eps=1e-6):

    def integer():
        try:
            jury = int(jury_answer)
            contestant = int(contestant_output)
        except ValueError:
            return False
        return contestant == jury

    def real():
        try:
            jury = float(jury_answer)
            contestant = float(contestant_output)
        except ValueError:
            return False
        return isclose(contestant, jury, rel_tol=eps)

    def string():
        if trailing_zero:
            return contestant_output.strip() == jury_answer
        else:
            return contestant_output == jury_answer

    if flag == "integer":
        return integer()
    elif flag == "real":
        return real()
    elif flag == "string":
        return string()
    else:
        return False