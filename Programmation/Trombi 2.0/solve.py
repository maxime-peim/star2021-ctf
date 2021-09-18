from __future__ import annotations

from functools import reduce
from pwn import *
from typing import Optional
from dataclasses import dataclass, field, InitVar
from itertools import combinations
import gc
import sys

@dataclass
class Part:
    name: str = ""
    sub_parts: dict[str, Part] = field(default_factory=dict)

    def add_part(self, part: Part):
        self.sub_parts[part.name] = part

    def attributes_bool_list(self) -> list[bool]:
        return sum((p.attributes_bool_list() for p in self.sub_parts.values()), [])

    def __str__(self) -> str:
        s = f"-> {self.name}\n" + \
            "".join(["\n".join(["  " + s for s in str(sp).rstrip().split("\n")]) + "\n" for sp in self.sub_parts.values()])
        return s

@dataclass
class Attribute(Part):
    value: bool = False

    def attributes_bool_list(self) -> list[bool]:
        return [self.value]

    def __str__(self) -> str:
        s = f"-> {self.name} : {'Oui' if self.value else 'Non'}\n"
        return s

class Person:

    def __init__(self, nom: str, prenom: str, signature: int, parts: list[Part]):
        self._nom = nom
        self._prenom = prenom
        self._signature = signature
        self._parts: dict[str, Part] = {p.name: p for p in parts}

    @property
    def full_name(self) -> str:
        return self._prenom + " " + self._nom

    @property
    def bool_list(self) -> list[bool]:
        return sum((p.attributes_bool_list() for p in self._parts.values()), [])

    @property
    def signature(self) -> int:
        return self._signature
        #return reduce(lambda a,b: (a << 1) + b, self.bool_list)

    def __str__(self) -> str:
        s = f"{self._prenom} {self._nom}\n" + \
            "".join(str(p) for p in self._parts.values())
        return s

def read_next_person(p_s):
    p_lines = p_s.split("\n")
    prenom = p_lines[0].split(' : ')[1]
    nom = p_lines[1].split(' : ')[1]

    parts: list[Part] = []
    parts_stack: list[Part] = []
    parts_list = p_lines[2:]

    signature = 0

    for part in parts_list:
        part_split = part.split("->")
        part_name = part_split[1].strip()
        level = len(part_split[0])

        if " : " in part_name:
            attribute_name, value_name = part_name.split(" : ")
            value = value_name == "Oui"

            signature = (signature << 1) + value

            new_part = Attribute(attribute_name, value=value)
        else:
            new_part = Part(part_name)

        while len(parts_stack) > 0 and parts_stack[-1][1] >= level:
            parts_stack.pop()

        if len(parts_stack) > 0:
            parts_stack[-1][0].add_part(new_part)
        else:
            parts.append(new_part)

        parts_stack.append((new_part, level))

    person = Person(nom, prenom, signature, parts)
    #print(person.full_name, person.bool_list)
    return person
    

def read_people(r) -> list[Person]:
    people_str = r.recvuntil(b"Question").decode("utf8").replace("Question", "").strip()
    people_str_list = people_str.split("###########################################################################")[1:]

    people = [read_next_person(p_s.strip()) for p_s in people_str_list]
    return people

def read_signature(r, questions: list[int], N: int) -> list[bool]:
    s = 0
    for q in questions:
        r.recvuntil(b"Choix: ")
        r.sendline(str(q).encode())
        answer = r.recvline().decode("utf8").rstrip().split(" ")[-1] == "Oui"
        s |= answer << (N - q)
    return s

def asking_questions(r, people_full_signatures: list[int], N: int, Q: int) -> int:

    mask_oui = 0
    mask_non = 0
    questions = []
    
    remaining = people_full_signatures
    total_people = len(remaining)
    total_questions = min(N, Q-1)
    for i in range(total_questions):
        n_people_per_attribute = [sum((p_fs & (1 << (N - a))) > 0 for p_fs in remaining if p_fs & mask_oui == mask_oui and p_fs & mask_non == 0) for a in range(1, N+1)]
        #print(bin(mask_oui), bin(mask_non), n_people_per_attribute)
        #print(n_people_per_attribute)

        q = [_ for _ in range(1, N+1) if _ not in questions][0]
        for qs in range(1, N+1):
            if qs not in questions and abs(total_people - 2*n_people_per_attribute[qs-1]) < abs(total_people - 2*n_people_per_attribute[q-1]):
                q = qs

        #print(q)
        questions.append(q)
        r.recvuntil(b"Choix: ")
        r.sendline(str(q).encode())
        answer = r.recvline().decode("utf8").rstrip().split(" ")[-1] == "Oui"

        if answer:
            mask_oui |= 1 << (N - q)
        else:
            mask_non |= 1 << (N - q)

        remaining = [p_fs for p_fs in remaining if p_fs & mask_oui == mask_oui and p_fs & mask_non == 0]
        total_people = len(remaining)
        sys.stdout.write("\033[F\033[K")
        print(f"[+] Question {i+1}/{total_questions}, remaining {total_people} people")
        
        if total_people == 1:
            break
    
    person_index = people_full_signatures.index(remaining[0])
    return person_index

if __name__ == "__main__":
    r = remote("challs2.hackademint.org", 13407)

    r.recvuntil(b"Choix: ")
    r.sendline(b"2")
    r.recvuntil(b"tous les profils")
    r.sendline(b"")

    for _ in range(100):
        print(f"[+] Run {_+1}/100")
        people = read_people(r)
        print(f"[+] There is {len(people)} people")

        Q = int(r.recvline().decode().split("/")[1])
        print(f"[+] Having a maximum of {Q} questions")

        r.recvuntil(b"Veuillez poser une question parmis les suivantes :\n")

        N = int(r.recvuntil(b"Proposer une personne").decode("utf8").split('\n')[-1].split(".")[0]) - 1
        print(f"[+] There exists {N} attributes")

        try:
            people_full_signatures = [p.signature for p in people]
            print("[+] Asking questions")
            person_index = asking_questions(r, people_full_signatures, N, Q)
            person_full_name = people[person_index].full_name
            fail = False
        except Exception as e:
            print(e)
            fail = True
        finally:
            r.recvuntil(b"Choix: ")
            r.sendline(str(N+1).encode())
            r.recvuntil(b"Quel personne est-ce ? ")
            if fail:
                print(bin(signature)[2:])
                r.sendline(b"a a")
            else:
                r.sendline(person_full_name.encode())

            print(r.recvline().decode("utf8"))

        del people
        del people_full_signatures
        gc.collect()

    r.interactive()

    r.close()
# HackademINT{Te4m_P1po}