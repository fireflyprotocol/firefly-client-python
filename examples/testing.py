from eth_utils import to_wei, from_wei
print(to_wei(1.2,"ether"))
print(to_wei(1.2,"mwei"))
print(from_wei(to_wei(1.2,"mwei"), "mwei"))