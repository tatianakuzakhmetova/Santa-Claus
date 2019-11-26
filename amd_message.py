import random

nicks = ['masha', 'sasha', 'petya', 'valya', 'test1', 'test2', 'test3', 'test4']
adm_base = {}


#Random choice for ADM
while len(adm_base) != len(nicks):
    from_msg = random.choice(nicks)
    to_msg = random.choice(nicks)
    #Verify if from_user == to_user
    if to_msg == from_msg:
        print("Wrong situation! We can't send the message to ourselves'")
        continue
    #Verify if from_useralready has the to_user
    if adm_base.get(from_msg):
        print("Ookey! This user already is ADM!")
        continue
    adm_base[from_msg] = to_msg
    print(adm_base)
print(adm_base)
    