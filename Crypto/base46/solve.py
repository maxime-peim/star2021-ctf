def base46(x):
    in_base = []
    while x > 0:
        in_base.append(x%46)
        x //= 46
    return in_base

ciphered = "03PzIXdw91Nz81M3EDNmJHNw91M3UHNzgzX08VM1F3XyVXbfVHNfNTdxFzZ002XyEDMyFTT7RlTJ1WZkF2ajFGS"