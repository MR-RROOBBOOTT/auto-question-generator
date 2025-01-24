import random
import math

def aqg_sums_and_products(prob_number, level_number):
    if prob_number == 1:
        return generate_sum(level_number)
    elif prob_number == 2:
        return generate_product(level_number)
    elif prob_number in [3, 4]:
        return generate_nested(prob_number, level_number)
    elif prob_number in range(5, 15):
        return generate_mixed(prob_number, level_number)
    else:
        raise ValueError("Invalid problem number")


def generate_sum(level):
    if level == 1:
        n = random.randint(1, 10)
        question = f"\\sum_{{i=1}}^{{{n}}}i"
        correct = " + ".join(str(i) for i in range(1, n + 1))
        distractors = generate_distractors(correct, level)
    elif level >= 2:
        m = random.randint(-10, 10)
        n = random.randint(-10, 10)
        expression = random.choice(["i", "i^2", "sqrt(i)", "ln(i)"])
        question = f"\\sum_{{i={m}}}^{{{n}}}{expression}"
        correct = generate_correct_expansion(m, n, expression)
        distractors = generate_distractors(correct, level)
    return {"question": question, "correct": correct, "distractors": distractors}


def generate_product(level):
    if level == 1:
        n = random.randint(1, 10)
        question = f"\\prod_{{i=1}}^{{{n}}}i"
        correct = " * ".join(str(i) for i in range(1, n + 1))
        distractors = generate_distractors(correct, level)
    elif level >= 2:
        m = random.randint(-10, 10)
        n = random.randint(-10, 10)
        expression = random.choice(["i", "i^2", "sqrt(i)", "ln(i)"])
        question = f"\\prod_{{i={m}}}^{{{n}}}{expression}"
        correct = generate_correct_expansion(m, n, expression, is_product=True)
        distractors = generate_distractors(correct, level)
    return {"question": question, "correct": correct, "distractors": distractors}


def generate_nested(prob_number, level):
    outer_range = random.randint(1, 5)
    inner_range = random.randint(1, 5)
    expression = random.choice(["(i+j)", "i^j", "2^(i+j)", "3i^2-j"])
    if prob_number == 3:
        question = f"\\sum_{{i=1}}^{{{outer_range}}} \\sum_{{j=1}}^{{{inner_range}}} {expression}"
    else:
        question = f"\\prod_{{i=1}}^{{{outer_range}}} \\prod_{{j=1}}^{{{inner_range}}} {expression}"
    correct = nested_expansion(outer_range, inner_range, expression, prob_number)
    distractors = generate_distractors(correct, level)
    return {"question": question, "correct": correct, "distractors": distractors}


def generate_mixed(prob_number, level):
    levels = {5: "\\sum \\prod", 6: "\\prod \\sum"}
    ranges = [random.randint(1, 5), random.randint(1, 5)]
    expression = random.choice(["(i+j)", "i^j", "2^(i+j)", "3i^2-j"])
    question = f"{levels[prob_number]}_{{i=1}}^{{{ranges[0]}}} {{j=1}}^{{{ranges[1]}}} {expression}"
    correct = nested_expansion(ranges[0], ranges[1], expression, prob_number)
    distractors = generate_distractors(correct, level)
    return {"question": question, "correct": correct, "distractors": distractors}


def generate_correct_expansion(m, n, expression, is_product=False):
    result = []
    for i in range(m, n + 1):
        if "sqrt" in expression:
            result.append(f"sqrt({i})")
        elif "ln" in expression:
            result.append(f"ln({i})")
        elif "^" in expression:
            base, exp = expression.split("^")
            result.append(f"{i}^{exp}")
        else:
            result.append(f"{i}")
    operator = " * " if is_product else " + "
    return operator.join(result)


def nested_expansion(outer, inner, expression, prob_number):
    expansion = []
    for i in range(1, outer + 1):
        for j in range(1, inner + 1):
            if prob_number in [3, 5]:
                expansion.append(expression.replace("i", str(i)).replace("j", str(j)))
            else:
                expansion.append(expression.replace("i", str(i)).replace("j", str(j)))
    return " + ".join(expansion) if prob_number in [3, 5] else " * ".join(expansion)


def generate_distractors(correct, level):
    distractors = [correct[::-1], correct.upper(), correct.lower()]
    return random.sample(distractors, 2)