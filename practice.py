import math

def remove_punctuations(str_engsentences):
  for p in ".,:;!?":
      str_engsentences = str_engsentences.replace(p, "")
  return str_engsentences

print(remove_punctuations(
  'Quiet, uh, donations, you want me to make a donation to the coast guard youth auxiliary?'
) == 'Quiet uh donations you want me to make a donation to the coast guard youth auxiliary')

def atgc_bppair(str_atgc):
    pair = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result = ""
    for ch in str_atgc:
        result += pair[ch]
    return result

print(atgc_bppair('AAGCCCCATGGTAA') == 'TTCGGGGTACCATT')

def swap_colon(str1):
    pos = str1.find(":")
    left = str1[:pos]
    right = str1[pos+1:]
    return right + ":" + left

print(swap_colon("hello:world") == "world:hello")

def atgc_count(str_atgc, str_bpname):
    result = str_atgc.count(str_bpname)
    return result

print(atgc_count('AAGCCCCATGGTAA', 'A') == 5)

def check_lower(str_engsentences):
    return str_engsentences.islower()

print(check_lower('down down down') == True)
print(check_lower('There were doors all round the hall, but they were all locked') == False)

def remove_clause(str_engsentences):
    pos = str_engsentences.find(",")
    right = str_engsentences[pos+2:]
    
    return  right.capitalize()

print(remove_clause("It's being seen, but you aren't observing.") == "But you aren't observing.")