import os
import re

class TemplateBlocks():
    def __init__(self, html):
        self.html = html
        pattern         = r'{% *block *(?P<name>\w+) *%}'
        self.block_re   = re.compile(pattern)
        pattern         = r'{% *endblock *%}'
        self.blockend_re = re.compile(pattern)
        self.block      = self.find_block_begin(self.html)
        self.blockend   = self.find_block_end(self.html)
        self.check_blocks_parity()
        self.blockend_matching()

    def check_blocks_parity(self):
        pos = 0
        endpos = len(self.html)
        block_list = []
        while pos < endpos:
            block = self.find_block_begin(self.html, pos)
            print(block)
            if block:
                block_list.append(block)
                pos = block.get('start_pos')
            else:
                pos = endpos
        print('Знайдено %s початків блоків:' % len(block_list))
        for b in block_list: print('%5d %s' % (b.get('start_pos'), b.get('name')))
        print('-'*80)

        pos = 0
        endpos = len(self.html)
        end_list = []
        while pos < endpos:
            block_end = self.find_block_end(self.html, pos)
            print(block_end)
            if block_end:
                end_list.append(block_end)
                pos = block_end.get('new_pos')
            else:
                pos = endpos
        print('Знайдено %s кінців блоків:' % len(end_list))
        for e in end_list: print('%5d %5d' % (e.get('stop_pos'), e.get('new_pos')))
        print('-'*80)
        if len(block_list) == len(end_list):
            print('Теги знайдених блоків "парні"')
        else:
            print('ПОМИЛКА ПАРНОСТІ тегів знайдених блоків')
        self.block_list = block_list
        self.end_list = end_list

    def blockend_matching(self, indent=0):
        for i in range(len(self.block_list)):
            # перевіряємо, чи блок має номер, бо вкладеним блокам
            # номер присвоїся при рекурсивному виклику
            print('blockend_matching:  i =', i, self.block_list[i])
            print('='*80)
            if not 'n' in self.block_list[i]:
                self.match_end_for_block(i, indent)
        print('='*80)
        print('Розпаровано теги початку і кінця блоків:')
        for b in self.block_list:
            print(b)
        for e in self.end_list:
            print(e)

    def match_end_for_block(self, i, indent=0):
        def get_free_end_number(pos):  # повертає № першого
                                        # ще не зідентифікованого кінця
            j = None
            for k in range(len(self.end_list)):
                e = self.end_list[k]
                print(pos, k, e, not 'n' in e, e['stop_pos'] > pos)
                if (not 'n' in e) and e['stop_pos'] > pos:
                    j = k
                    break
            return j

        block = self.block_list[i]  # блок до якого шукаємо кінець
        block['indent'] = indent    # рівень вкладеності блоку
        pos = block['start_pos']    # починаючи звідси шукаємо
        j = get_free_end_number(pos)# беремо перший ще не зідентифікований кінець
        print('j=',j,'*'*10)
        blockend = self.end_list[j]
        print('indent =', indent, 'self.end_list =', self.end_list)
        try:
            next_block = self.block_list[i+1]   # початок наступного блоку (якщо є)
        except:
            next_block = None
        print('match_end_for_block: i =', i, 'indent =', indent)
        print('indent =', indent, 'block     =', block)
        print('indent =', indent, 'nextblock =', next_block)
        print('indent =', indent, 'j =', j, 'blockend =', blockend)

        if next_block and next_block['start_pos'] < blockend['stop_pos']:
            # перед тегом кінця вклинився тег початку наступного блоку
            # тому рекурсивно шукаємо на глибшому рівні
            print('indent =', indent, 'рекурсія--------------------')
            self.match_end_for_block(i+1, indent+1)
            print('indent =', indent, 'кінець рекурсії-------------')

        print('-'*30)
        j = get_free_end_number(pos)   # беремо перший ще не зідентифікований кінець
        blockend = self.end_list[j] # після рекурсії перший ще
                                    # не зідентифікований кінець
                                    # є нашим шуканим кінцем
        blockend['n'] = i       # № блока і одночасно мітка, що цей кінець блока зідентифіковано
        print('indent =', indent, 'self.end_list =', self.end_list)
        print('indent =', indent, 'pos =', pos)
        print('indent =', indent, 'j =', j, 'blockend =', blockend)
        # self.end_list[j] = blockend
        block.update(blockend)  # доповнюємо словник даними кінця блока
        print('indent =', indent, 'block     =', block)
        print('='*50)



    def find_block_begin(self, html, pos=0, endpos=None):
        endpos = endpos or len(html)
        m = self.block_re.search(html, pos, endpos)
        if m:
            start, stop = m.span()  # положення шаблону {% block name %}
            block = m.groupdict()
            block['start_pos'] = stop   # початок вмісту блока
        else:
            block = None
        return block

    def find_block_end(self, html, pos=0, endpos=None):
        endpos = endpos or len(html)
        m = self.blockend_re.search(html, pos, endpos)
        if m:
            start, stop = m.span()  # положення шаблону {% endblock %}
            endblock = {'stop_pos' : start, 'new_pos': stop}
        else:
            endblock = None
        return endblock # кінець вмісту блока і перша позиція поза блоком

tb = TemplateBlocks(html)
# print('-'*80)
# print(tb.block)
# print(tb.blockend)

