from collections import defaultdict

def group_interests_by_letter(interests):
    objects = defaultdict(list)
    for interest in interests:
        if objects.get(interest.name[0]):
            objects[interest.name[0]].append(interest)
        else:
            objects[interest.name[0]] = [interest]
    return sorted(objects.items(), key=lambda (letter, interests): letter)