import math
from fractions import Fraction


def main():
    arrival_rate = int(input("Arrival Rate: "))
    service_rate = int(input("Service Rate: "))
    len = input("Infinite? (y/n): ")

    if len == 'y':
        len = math.inf
    else:
        len = int(input("Length? (y/n): "))

    queue = initialize_queue(arrival_rate, service_rate, len)

    print("Queue details: \n", queue['kendalls_notation'])

    gui(queue)


def gui(q):
    menu()

    while True:
        choice = int(input("Enter choice: "))
        answr = None

        match choice:
            case 0:
                quit()

            case 1:
                n = int(input("Length?: "))
                answr = prob_exactly_n(n, q['ρ'])

            case 2:
                n = int(input("Length?: "))
                answr = prob_at_least_n(n, q['ρ'])

            case 3:
                answr = prob_balk(q['n'])

            case 4:
                answr = prob_server_busy()

            case 5:
                answr = prob_no_queue()

            case 6:
                answr = q['ls']

            case 7:
                answr = q['lq']

            case 8:
                answr = q['ws']

            case 9:
                answr = q['wq']

            case _:
                return -1

        print(f"{answr}")
        if not answr.is_integer():
            print(f"approx. {float(answr)}")
        print()


def menu():
    print("MENU")
    print("--------")
    print("1. Probability of exactly n people")
    print("2. Probability of at least n people")
    print("3. Balking probability")
    print("4. Probability server is busy")
    print("5. Probability of no queue")
    print("6. Expected number of people in the system")
    print("7. Expected number of people in the queue")
    print("8. Expected waiting time for the system")
    print("9. Expected waiting time for in the queue")
    print("--------")
    print("0. Exit")


def initialize_queue(a, s, len):
    λ = a
    μ = s
    c = 1
    n = len

    eff_λ: Fraction | None

    ρ: Fraction
    ls: Fraction
    ws: Fraction
    qs: Fraction

    ρ = Fraction(λ, μ)

    if len == math.inf:
        ls = ρ / (1 - ρ)
        lq = ls - ρ
        ws = ls / λ
        wq = lq / λ
        eff_λ = None
    else:
        ls = (ρ * (1 + (n * pow(ρ, n + 1)) - (n + 1) * pow(ρ, n))) / \
            ((1 - ρ) * (1 - pow(ρ, n + 1)))
        eff_λ = λ * (1 - prob_exactly_n(int(n)))
        lq = ls - (eff_λ / μ)
        ws = ls / eff_λ
        wq = lq / eff_λ

    kendalls_notation = f"M/M/{c}/{"∞" if n == math.inf else n}/∞/FCFS\n"
    kendalls_notation += f"λ = {λ}\nμ = {μ}\nρ = {ρ}\nls = {float(ls)}\n"
    kendalls_notation += f"lq = {float(lq)}\nws = {float(ws)}\n"
    kendalls_notation += f"wq = {float(wq)}"

    q = {
        "λ": λ,
        "μ": μ,
        "c": c,
        "n": n,
        "ρ": ρ,
        "ls": ls,
        "lq": lq,
        "ws": ws,
        "wq": wq,
        "kendalls_notation": kendalls_notation
    }

    return q


def prob_exactly_n(n, ρ):
    prob: Fraction
    if (n != math.inf):
        prob = pow(ρ, n) * ((1 - ρ)) / (1-pow(ρ, n + 1))
    else:
        prob = pow(ρ, n) * (1 - ρ)
    return prob


def prob_at_least_n(n):
    prob_sum = 0
    for x in range(0, n):
        prob_sum += Fraction(prob_exactly_n(int(n)))
    return 1 - prob_sum


def prob_balk(n):
    prob: Fraction
    if (n == math.inf):
        Fraction(0)
    else:
        prob_exactly_n(int(n))
    return prob


def prob_server_busy():
    return prob_at_least_n(1)


def prob_no_queue():
    return prob_exactly_n(0) + prob_exactly_n(1)
