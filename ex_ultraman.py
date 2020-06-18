from abc import ABCMeta, abstractmethod
from random import randrange, randint

class Fighter(object,metaclass=ABCMeta):
    """打仗的人"""
    """通过__slots__魔法限定对象可以绑定的成员变量"""
    __slots__ = ('_name', '_hp')

    def __init__(self,name,hp):
        """初始化方法
        :param name: 名字
        :param hp: 血量
        """
        self._name = name
        self._hp = hp

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self,hp):
        self._hp = hp if hp >= 0 else 0
    @property
    def alive(self):
        return self._hp > 0

    @abstractmethod
    def attack(self,other):
        """
        :param other: 被攻击的对象
        """
        pass

class Ultraman(Fighter):
    """奥特曼"""
    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self,name,hp,mp):
        """
        初始化方法
        :param name: 名字
        :param hp: 血量
        :param mp: 魔法值
        """
        super().__init__(name,hp)
        self._mp = mp

    def attack(self, other):
        """普通攻击

        :param other: 被攻击的对象
        :return:
        """
        other.hp -= randint(15, 25)

    def huge_attack(self,other):
        """必杀，伤害对手至少50或者3/4的血量

        :param other: 被攻击的对象
        :return: 使用成功返回true， 失败普通攻击返回false
        """
        if self._mp >= 50:
            self._mp -= 50
            dps = other.hp * 3 //4
            dps = dps if dps >= 50 else 50
            other.hp -= dps
            return True
        else:
            self.attack(other)
            return False

    def aoe_attack(self,others):
        """范围攻击

        :param others: 被攻击的群体
        :return: 使用魔法成功返回true，失败就普通攻击返回false
        """
        if self._mp >= 20:
            self._mp -= 20
            for enemy in others:
                if enemy.alive:
                    enemy.hp -= randint(10,20)
            return True
        else:
            return False

    def resume(self):
        """恢复魔法值
        :return:
        """
        incr_mp = randint(4,20)
        self._mp += incr_mp
        return incr_mp

    def __str__(self):
        return '~~~%s奥特曼~~~\n' %self._name + '生命值： %d\n' %self._hp + '魔法值： %d\n' %self._mp

class Monster(Fighter):
    """小怪兽"""
    __slots__ = ('_name', '_hp')

    def attack(self,other):
        other.hp -= randint(5,15)

    def __str__(self):
        return '~~~%s小怪兽~~~\n' %self._name + '生命值： %d\n' %self._hp

def is_any_alive(monsters):
    """判断有没有小怪兽是活着的
    :param monsters:
    :return:
    """
    for monster in monsters:
        if monster.alive > 0:
            return True
    return False

def select_alive_one(monsters):
    """选中活着的一只怪兽"""
    monsters_len = len(monsters)
    while True:
        index = randrange(monsters_len)
        monster = monsters[index]
        if monster.alive > 0:
            return monster

def display_info(ultraman, monsters):
    """显示奥特曼和怪兽的信息"""
    print(ultraman)
    for monster in monsters:
        print(monster, end='')

def main():
    man = Ultraman('Jack', 1000, 400)
    mons1 = Monster('巴尔坦星人', 520)
    mons2 = Monster('金正恩', 660)
    mons3 = Monster('白骨精', 300)
    mons4 = Monster('影魔', 333)
    ml = [mons1, mons2, mons3, mons4]
    round = 1
    while man.alive and is_any_alive(ml):
        print('======第%d回合======\n' %round)
        m = select_alive_one(ml) #选中一个怪兽
        chose = randint(1,10) #通过随机数1-10 来选择一个技能
        if chose <= 6: #普通攻击60%
            print('%s使用普通攻击攻击了%s.' %(man.name,m.name))
            man.attack(m)
            print('%s的魔法值恢复了%d点.' %(man.name, man.resume()))
        elif chose <= 9: #30%的概率施放aoe(可能因为魔法不足失败)
            if man.aoe_attack(ml):
                print('%s使用了aoe.' %man.name)
            else:
                print('施放aoe失败，魔法不足')
                print('%s的魔法值恢复了%d点.' % (man.name, man.resume()))
        else: #施放必杀技(如果魔法不足则使用普通攻击)
            if man.huge_attack(m):
                print('%s使用究极必杀技虐了%s.' % (man.name, m.name))
            else:
                print('%s使用普通攻击攻击了%s.' % man.name, m.name)
                print('%s的魔法值恢复了%d点.' % (man.name, man.resume()))
        if m.alive > 0: #如果选中的怪兽没死，则回击奥特曼
            print('%s回击了%s.' % (m.name, man.name))
            m.attack(man)
        display_info(man,ml)
        round += 1
    print('\n=====战斗结束=====\n')
    if man.alive > 0:
        print('%s奥特曼胜利！！' %man.name)
    else:
        print('怪兽胜利，%s死了 ： （' %man.name)


if __name__ == '__main__':
    main()