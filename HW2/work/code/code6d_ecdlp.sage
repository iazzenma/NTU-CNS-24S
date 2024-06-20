from data import p_list, a_list, b_list, P_list, Q_list

values = []
mods = []

for i in range(len(p_list)):
    p = p_list[i]
    # elliptic curve y^2 = x^3 + ax + b
    a = a_list[i]
    b = b_list[i]
    P = P_list[i]
    Q = Q_list[i]

    R.<x> = PolynomialRing(GF(p))
    f = x^3 + a*x + b
    roots = f.roots()
    if(len(roots) == 1):
        continue
    for root in roots:
        if root[1] == 2:
            xs = root[0]
    f_ = f.subs(x=x + xs)

    print(f_)
    c = f_.coefficients()[0]
    t = c.square_root()

    u = ((P[1] + t*(P[0] - xs)) / (P[1] - t*(P[0] - xs)))
    v = ((Q[1] + t*(Q[0] - xs)) / (Q[1] - t*(Q[0] - xs)))

    dlog_result = discrete_log(v, u)
    order_result = u.multiplicative_order()

    print(dlog_result)
    print(order_result)

    # Append results to lists
    values.append(dlog_result)
    mods.append(order_result)

solution = crt(values, mods)

# Print the solution
print("Solution:", solution)