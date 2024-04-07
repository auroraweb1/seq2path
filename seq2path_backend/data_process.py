senttag2word = {'POS': 'positive', 'NEG': 'negative', 'NEU': 'neutral'}

# 提取目标
def get_extraction_targets(sents, labels):
    targets = []
    for i, label in enumerate(labels):
        all_tri = []
        for tri in label:
            if len(tri[0]) == 1:
                a = sents[i][tri[0][0]]
            else:
                start_idx, end_idx = tri[0][0], tri[0][-1]
                a = ' '.join(sents[i][start_idx:end_idx + 1])
            if len(tri[1]) == 1:
                b = sents[i][tri[1][0]]
            else:
                start_idx, end_idx = tri[1][0], tri[1][-1]
                b = ' '.join(sents[i][start_idx:end_idx + 1])
            c = senttag2word[tri[2]]
            all_tri.append((a, b, c))
        label_strs = ['[' + ' | '.join(l) + ' | true]' for l in all_tri]
        targets.append('; '.join(label_strs))
    return targets

# 从数据集中读取并按行处理数据
def read_line_examples(data_path):
    """
    Read data from file, each line is: sent####labels
    Return List[List[word]], List[Tuple]
    """
    sents, labels = [], []
    results = []
    with open(data_path, 'r', encoding='UTF-8') as fp:
        words = []
        for line in fp:
            line = line.strip()
            if line != '':
                words, tuples = line.split('####')
                tuples = tuples.split('||||')
                for tuple in tuples:
                    sents.append(words.split())  # 将sent填入inputs
                    labels.append(eval(tuple))  # 将tuple填入targets
            targets = get_extraction_targets(sents, labels)
            result_string = '||||'.join([elem.strip('[]') for elem in targets])
            result_string = words + '####' + result_string
            results.append(result_string)
            sents, labels = [], []
    with open('dev.txt', 'w') as file:
        for line in results:
            file.write(line + '\n')
    return sents, labels

sents, labels = read_line_examples('data/uabsa/laptop14/dev.txt')
