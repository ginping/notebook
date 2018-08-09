def xie_zheng(infile, outfile):
    infopen = open(infile, 'r', encoding='utf-8')
    outopen = open(outfile, 'a', encoding='utf-8')
    lines = infopen.readlines()
    list_1 = []
    for line in lines:
        if line not in list_1:
            list_1.append(line)
            outopen.write(line)
    infopen.close()
    outopen.close()


if __name__ == '__main__':
    xie_zheng('xie_zheng.txt', 'xbyz.txt')
