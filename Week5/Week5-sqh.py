import jieba

class Tokenizerpro:
    '''
    将文本编码成整数序列
    '''

    def __init__(self, chars, coding='c', PAD=0):
        '''默认情况下是按照字符构建字典'''
        self.chars = chars
        if coding == 'c':
            self.coding = coding
            self.dic = {}
            self.dic['[PAD]'] = 0
            flag = 1

            for i in chars:
                for j in i:
                    if j not in self.dic.keys():
                        self.dic[j] = flag
                        flag += 1
                    else:
                        continue

        elif coding == 'w':
            self.coding = coding
            self.dic = {}
            self.dic['[PAD]'] = 0
            flag = 1
            for i in chars:
                lis = jieba.lcut(i)
                for j in lis:
                    if j not in self.dic.keys():
                        self.dic[j] = flag
                        flag += 1
                else:
                    continue

        else:
            pass

    def tokenize(self, sentence):
        '''
        根据字典的创建规则，对文本进行处理

        如果coding为c，那么就不进行处理
        如果coding为w，那么利用jieba库进行分词处理'''
        list_of_chars = []
        if self.coding == 'c':
            pass
        elif self.coding == 'w':
            sentence = jieba.lcut(sentence)
        for i in sentence:
            list_of_chars.append(i)

        return list_of_chars

    def encode(self, list_of_chars):
        '''
        利用生成的字典，对文本进行编码处理
        '''
        tokens = []
        for i in list_of_chars:
            tokens.append(self.dic[i])

        return tokens

    def trim(self, tokens, seq_len):
        '''
        整理数字列表的长度，不足的用0补齐，超过的部分则进行切片处理
        '''
        if len(tokens) > seq_len:
            return tokens[:seq_len]
        else:
            tokens.extend([0] * (seq_len - len(tokens)))
            return tokens

    def decode(self, tokens):
        '''
        将处理后的数字列表翻译成文本，其中0对应的字符为[PAD]
        '''
        dic = dict(zip(self.dic.values(), self.dic.keys()))
        sentence = ''
        for i in tokens:
            if i != 0:
                sentence += dic[i]
            else:
                sentence += '[PAD]'
        return sentence

    def encode_len(self, seq_len):
        '''
        返回整个文档中所有文本的长度为seq_len的数字序列
        '''
        seq_len_list = []
        for i in self.chars:
            seq_len_list.append(
                self.trim(self.encode(self.tokenize(i)), seq_len))
        return seq_len_list


def main():
    file = 'BUAA_21/Week5/jd_comments.txt'

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open("BUAA_21/Week5/output.txt", "w", encoding='utf-8') as output:

        lines = [i.strip('\n') for i in lines]

        new = Tokenizerpro(lines)

        # 以京东文档中第二个评论为例
        list_of_chars = new.tokenize(lines[1])
        print("List of chars (The second comment):\n",
              list_of_chars, "\n\n", file=output)

        tokens = new.encode(list_of_chars)
        print("Token of the second comment):\n", tokens, "\n\n", file=output)

        new_tokens = new.trim(tokens, 150)
        print("After trim function:\n", new_tokens, "\n\n", file=output)

        sentence = new.decode(new_tokens)
        print("Sentence:\n", sentence, "\n\n", file=output)

        seq_len_list = new.encode_len(100)
        print("Seq_len_list:", *seq_len_list, "\n\n", sep='\n', file=output)


if __name__ == '__main__':
    main()
