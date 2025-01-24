from django.http import JsonResponse
from django.shortcuts import render
import random
import math


# Home page view
def index(request):
    return render(request, 'index.html')


# Safe evaluation of mathematical expressions
def safe_eval(expression, i=None, j=None, k=None):
    allowed_names = {"i": i, "j": j, "k": k, "math": math}
    try:
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception:
        return None


# Generate question API
def generate_question(request):
    if request.method == 'GET':
        operator = request.GET.get('operator', 'sum')
        m = int(request.GET.get('m', 1))
        n = int(request.GET.get('n', 5))
        expression = request.GET.get('expression', 'i')
        level = int(request.GET.get('level', 1))
        num_questions = int(request.GET.get('num_questions', 1))

        if operator not in [
            'sum', 'prod', 'sum_sum', 'prod_prod', 'sum_prod', 'prod_sum',
            'sum_sum_sum', 'prod_prod_prod', 'addition', 'subtraction', 'multiplication', 'division'
        ]:
            return JsonResponse({'error': 'Invalid operator provided.'}, status=400)

        if m > n:
            return JsonResponse({'error': 'Initial index (m) must be less than or equal to final index (n).'}, status=400)

        questions = []

        for _ in range(num_questions):
            terms = []
            if operator in ['sum', 'prod']:
                for i in range(m, n + 1):
                    term = safe_eval(expression, i=i)
                    if term is None:
                        return JsonResponse({'error': 'Invalid mathematical expression.'}, status=400)
                    terms.append(adjust_term(term, level))
            elif operator in ['sum_sum', 'prod_prod']:
                for i in range(m, n + 1):
                    inner_terms = []
                    for j in range(m, n + 1):
                        term = safe_eval(expression, i=i, j=j)
                        if term is None:
                            return JsonResponse({'error': 'Invalid mathematical expression for nested operations.'}, status=400)
                        inner_terms.append(adjust_term(term, level))
                    terms.append(sum(inner_terms) if 'sum' in operator else math.prod(inner_terms))
            elif operator in ['sum_prod', 'prod_sum']:
                for i in range(m, n + 1):
                    inner_terms = []
                    for j in range(m, n + 1):
                        term = safe_eval(expression, i=i, j=j)
                        if term is None:
                            return JsonResponse({'error': 'Invalid mathematical expression for mixed operations.'}, status=400)
                        inner_terms.append(adjust_term(term, level))
                    terms.append(sum(inner_terms) if operator == 'sum_prod' else math.prod(inner_terms))
            elif operator in ['sum_sum_sum', 'prod_prod_prod']:
                for i in range(m, n + 1):
                    outer_terms = []
                    for j in range(m, n + 1):
                        inner_terms = []
                        for k in range(m, n + 1):
                            term = safe_eval(expression, i=i, j=j, k=k)
                            if term is None:
                                return JsonResponse({'error': 'Invalid mathematical expression for triple nested operations.'}, status=400)
                            inner_terms.append(adjust_term(term, level))
                        outer_terms.append(sum(inner_terms) if 'sum' in operator else math.prod(inner_terms))
                    terms.append(sum(outer_terms) if 'sum' in operator else math.prod(outer_terms))
            elif operator in ['addition', 'subtraction', 'multiplication', 'division']:
                term1 = safe_eval(expression, i=m)
                term2 = safe_eval(expression, i=n)
                if term1 is None or term2 is None:
                    return JsonResponse({'error': 'Invalid mathematical expression for basic operations.'}, status=400)
                if operator == 'addition':
                    terms = [term1 + term2]
                elif operator == 'subtraction':
                    terms = [term1 - term2]
                elif operator == 'multiplication':
                    terms = [term1 * term2]
                elif operator == 'division' and term2 != 0:
                    terms = [term1 / term2]

            correct_expansion = ' + '.join(map(str, terms)) if 'sum' in operator else ' * '.join(map(str, terms))
            distractors = generate_distractors(terms, correct_expansion, operator)
            question = f"{'∑' if 'sum' in operator else '∏'}_{{i={m}}}^{{{n}}}({expression})"

            questions.append({
                'question': question,
                'correct': correct_expansion,
                'options': [correct_expansion] + distractors
            })

        return JsonResponse({'questions': questions})


# Adjust term complexity based on difficulty level
def adjust_term(term, level):
    if level == 1:
        return term
    elif level == 2:
        return term + random.randint(-3, 3)
    elif level == 3:
        return term * random.randint(1, 3)
    elif level == 4:
        return term ** random.randint(1, 2)
    elif level == 5:
        return (term ** 2) + random.randint(-10, 10)
    return term


# Generate distinct distractor options
def generate_distractors(terms, correct_expansion, operator):
    distractors = set()
    while len(distractors) < 3:
        distractor = terms.copy()
        random.shuffle(distractor)
        distractor_expansion = ' + '.join(map(str, distractor)) if 'sum' in operator else ' * '.join(map(str, distractor))
        if distractor_expansion != correct_expansion:
            distractors.add(distractor_expansion)
    return list(distractors)