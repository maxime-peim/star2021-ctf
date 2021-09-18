from base64 import b64decode

# il manque un = de padding
print(b64decode(b"=03PzIXdw91Nz81M3EDNmJHNw91M3UHNzgzX08VM1F3XyVXbfVHNfNTdxFzZ002XyEDMyFTT7RlTJ1WZkF2ajFGS"[::-1]))