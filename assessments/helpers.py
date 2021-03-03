def calculate_sample(qaa):
    sample = 0
    gfa = qaa.pi.gfa
    gfa_per = 70
    min = 30
    max = 700
    building_type = qaa.building_type
    if building_type == 'A':
        gfa_per = 70
        min = 30
        max = 700
    if building_type == 'B':
        gfa_per =  70
        min = 30
        max = 600
    if building_type == 'C':
        gfa_per = 500
        min = 30
        max = 150
    if building_type == 'D':
        gfa_per = 500
        min = 30
        max = 100

    sample = gfa / gfa_per
    if sample < min:
        sample = min
    elif sample > max:
        sample = max

    return sample