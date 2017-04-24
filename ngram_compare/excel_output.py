from compare import Similar

with open('on.txt','r',encoding='utf-8') as myFile:
    for line in myFile:
        line = line.split('\t')
        url1 = line[0].strip()
        url2 = line[1].strip()
        print(url1)
        try:
            if url1 != url2:
                s = Similar()
                a = s.action(url1, url2)
                with open('new_output_onmarket.csv', 'a', encoding='utf-8') as outFile:
                    outFile.write('"{}","{}","{}","{}","{}","{}"\n'.format(url1,
                                                                           url2,
                                                                           a[0],
                                                                           a[1],
                                                                           a[2],
                                                                           a[3]))
        except Exception as e:
            print(e)
