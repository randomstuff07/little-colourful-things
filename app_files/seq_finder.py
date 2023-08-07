def process_centers(centers, img_dims):
    hflag = False
    if img_dims[1]>img_dims[0]:
        hflag = True
    scores = []
    if hflag == True:
        for center in centers:
            score = center[0]*img_dims[0]
            scores.append(score)
    else:
        for center in centers:
            score = center[1]*img_dims[1]
            scores.append(score)
    
    return scores

def init_seq(img_dims, red_centers, pink_centers, blue_centers):
    scores = []
    sequence = []
    seq_string = ''
    if pink_centers != []:
        ps = process_centers(pink_centers, img_dims)
        for i in range(len(ps)):
            sequence.append('P')
            seq_string+= 'P'
        for val in ps:
            scores.append(val)

    if red_centers != []:
        rs = process_centers(red_centers, img_dims)
        for i in range(len(rs)):
            sequence.append('R')
            seq_string += 'R'
        for val in rs:
            scores.append(val)

    if blue_centers != []:
        bs = process_centers(blue_centers, img_dims)
        for i in range(len(bs)):
            sequence.append('B')
            seq_string += 'B'
        for val in bs:
            scores.append(val)

    print('init sequence', sequence)
    return seq_string, sequence, scores
    #   bubble sort implementation (couldn't use the inbuilt sort() function 
    #   because of the operation required to be done to the sequence string)

def sort_seq(seq_string, scores, sequence):
    n = len(scores)

    for i in range(n):
        swapped = False

        for j in range(0, n-i-1):

            if scores[j] > scores[j+1]:
                scores[j], scores[j+1] = scores[j+1], scores[j]
                sequence[j], sequence[j+1] = sequence[j+1], sequence[j]
                seq_string[j], seq_string[j+1] = seq_string[j+1], seq_string[j]
                swapped = True
        if (swapped == False):
            break
        
    print('sorted sequence: ', sequence)
    print('sorted sequence string: ', seq_string)
    print('sorted scores: ', scores)
    return sequence, seq_string

def find_type(sequence, seq_string):
    classifier_key = {
        'normal'    : [['B','B','R','R'], ['R','R','B','B']],
        'cco'       : [['R','B','R','B'], ['B','R','B','R'], ['B','R','R','B'], ['R','B','B','R']],
        'mi_ndj'    : [['B','R'], ['R', 'B'],['P', 'P'], ['P']],
        'mi_rs'     : [['R','B','P'], ['B','R','P'], ['P','R','B'], ['P','B','R']],
        'mi_pssc'   : [['R','B','B'], ['B','R','B'], ['R','B','R'], ['B','B','R'], ['B','R','R'], ['R','R','B'],['R','P','B'],['B','P','R']],
        'mii_pssc'  : [['R','B'], ['B','R']]
    }
    string_class_key = {
        'normal'    : ['BBRR', 'RRBB'],
        'cco'       : ['RBRB', 'BRBR', 'BRRB', 'RBBR'],
        'mi_ndj'    : ['RB', 'BR','PP', 'P'],
        'mi_rs'     : ['RBP', 'BRP', 'PRB', 'PBR'],
        'mi_pssc'   : ['RBB', 'BRB', 'RBR', 'BBR', 'BRR', 'RRB','RPB','BPR'],
        'mii_pssc'  : ['RB', 'BR']
    }

    cell_type = ''

    for key, val in classifier_key.items():
        for seq in val:
            if seq == sequence:
                cell_type = key

    subset_key = ''

    for key, val in string_class_key.items():
        for seq in val:
            if (seq.find(seq_string) != -1) & (cell_type == ''):
                subset_key = key

    if cell_type == '':
        print('other')
        print('subset_key: ', subset_key)
        return 'other', subset_key
    else:  
        print(cell_type)
        return cell_type
    

