import math


def main():
    arrival_rate = int(input("Enter the arrival rate for the queue: "))
    service_rate = int(input("Enter the service rate for the queue: "))
    print("Calculation Type:")
    print("1. Probability that there are people in the system")
    print("2. Probability that there are people in the system")
    opt = int(input("Calculation type, 1 for probility and 2 for at most"))
    n = int(input("Enter number of people for the queue: "))

    rho = Rho(arrival_rate, service_rate)
    prob = Prob(rho, n, opt)

    print(
        f"The probablility that there are {n} people in the queue with an arrival rate of {
            arrival_rate} and service rate of {service_rate} is {format(prob, ".2f")}"
    )


def Rho(a, s):
    return a/s


def Prob(rho, n, opt):
    prob = 0
    if (opt == 3):  # At least
        prob = 0
    elif (opt == 2):  # At most
        for i in range(1, n):
            prob += pow(rho, i)*(1-rho)
    else:
        prob = math.pow(rho, n)*(1-rho)
    return prob


main()
