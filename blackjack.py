# card suits: '♣', '♠', '♦', '♥'
import inquirer, re, string
from random import shuffle
from time import sleep

confirm = {inquirer.Confirm('confirmed', message="要不要继续发牌？"),}
rechip = {inquirer.Confirm('confirmed', message="要换新的筹码继续玩么？")}
#pick_with_split = [inquirer.List('picks', message="请选择你要继续哪个操作？", choices=['yes', 'no', 'split', 'double'],),]
pick_no_split = [inquirer.List('picks', message="请选择你要继续哪个操作？", choices=['yes', 'no', 'double'],),]
pick_no_double = [inquirer.List('picks', message="请选择你要继续哪个操作？", choices=['yes', 'no'],),]


# 初始化一副牌
def shuffle_card():
    """
    初始化一副52张的牌
    :return:
    """
    suits = ['♠', '♣', '♦', '♥']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []

    for suit in suits:
        for card in cards:
            deck.append(suit + ' ' + card)

    shuffle(deck)
    return (deck)


# 依次给玩家，庄家，玩家，庄家各发两张牌
def deal_card(deck, hand_card):
    """
    给参与者（庄家和玩家）发牌
    :return:
    """
    d_card = deck.pop()
    hand_card.append(d_card)
    return d_card


# 要的话继续调用deal_card()，并计算，如果爆掉，打印'玩家输了！'
## 计算手牌
def calculate_hand(hand_card):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
              'A': 11}
    sum = 0
    ace_count = 0
    for i in hand_card:
        if values[i[2:]] == 11:
            ace_count += 1
        sum += values[i[2:]]
        if sum > 21 and ace_count > 0:
            sum -= 10
            ace_count -= 1
    # print('ace count = %d' %ace_count)
    # print('sum = %d' %sum )
    return sum


##check玩家的牌是不是blackjack， 如果是，check dealer的手牌。
def is_Blackjack(hand_card):
    sum = calculate_hand(hand_card)
    if sum == 21:
        return True
    else:
        return False
##是不是满足split
def is_qualified_split(player_hand):
    if player_hand[0][2:] != player_hand[1][2:]:
        print('不可以split')
        return False
    else:
        print('可以split')
        return True

#不同选择的function
# def split_choice(choice, player_hand, deck, myhand, hisrealhand, dealer_hand):
#     while choice == 'split':
#         print('先玩这堆：')
#         player_hand = player_hand[0]
#         myhand = '你手中的牌为： %s' % (player_hand[0])
#         deal_card(deck, player_hand)
#         print('给你发了一张: %s' % player_hand[-1])
#         myhand += ' ' + player_hand[-1]
#         print(myhand)
#         sleep(1)
#         if is_qualified_split(player_hand):
#             choice = inquirer.prompt(pick_with_split)
#             choice = choice.get('picks')
#         else:
#             choice = inquirer.prompt(pick_no_split)
#             choice = choice.get('picks')
#             yes_choice(deck, player_hand, myhand, choice, hisrealhand, dealer_hand)
#             no_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand)

def yes_choice(deck, player_hand, myhand, choice, hisrealhand, dealer_hand):
    while choice == 'yes':
        sleep(1)
        deal_card(deck, player_hand)
        print('给你发了一张: %s' % player_hand[-1])
        myhand += ' ' + player_hand[-1]
        print(myhand)
        sleep(1)
        if is_boosted(player_hand):
            print('你爆了！下一局。。。')
            return dealerwin
        else:
            choice = inquirer.prompt(pick_no_split)
            choice = choice.get('picks')
    return no_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand)


def no_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand):
    while choice == 'no' or choice == 'double':
        sleep(1)
        print('看下庄家牌：')
        print('庄家手牌为：' + hisrealhand)
        sleep(1)
        while calculate_hand(dealer_hand) < 17:
            print('Dealer 没有到17， 给dealer发牌！')
            sleep(1)
            deal_card(deck, dealer_hand)
            print('Dealer发了一张: %s' % dealer_hand[-1])
            sleep(1)
            hisrealhand += ' ' + dealer_hand[-1]
            print(hisrealhand)
            sleep(1)
            if is_boosted(dealer_hand):
                print('Dealer 爆了！你赢了！')
                return playerwin

        print('Dealer 牌发完了！现在计算谁获胜！')
        sleep(2)
        print(myhand)
        sleep(2)
        print(hisrealhand)
        sleep(2)
        if calculate_hand(dealer_hand) > calculate_hand(player_hand):
            print('Dealer 获胜！')
            return dealerwin
        elif calculate_hand(dealer_hand) < calculate_hand(player_hand):
            print('玩家获胜')
            return playerwin
        else:
            print('打平!')
            return draw
def is_valid_double(gamble_money, money):
    # 检查筹码能不能double
    qualify = None
    if gamble_money * 2 > money:
        print('你需要充值，不然不能double')
        print('你现在有 %.1f 筹码.' % money)
        print('你需要充值至少 >= %.1f 筹码.' % (gamble_money * 2 - money))
        try_count = 0
        add_money = 0
        for i in range(5):
            add_money = [inquirer.Text('chips', message="冲多少？", validate=lambda _, x: re.match('^[0-9]*[\.[0-9]*$', x))]
            add_money = inquirer.prompt(add_money)
            add_money = add_money.get('chips')
            if float(add_money) < (gamble_money * 2 - money):
                print('你需要充值至少 >= %.1f 筹码.' % (gamble_money * 2 - money))
                try_count += 1
            else:
                break
        if try_count >= 5:
            print('你不愿充值就算了，正常玩吧！')
            qualify = False
            return qualify
        qualify = True
        money += float(add_money)
        gamble_money = float(gamble_money)*2
        return qualify,money,gamble_money

def double_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand):
    while choice == 'double':
        sleep(1)
        print('你选择了%s, 只给你发一张~~good luck!' %choice)
        deal_card(deck, player_hand)
        print('给你发了一张: %s' % player_hand[-1])
        myhand += ' ' + player_hand[-1]
        print(myhand)
        sleep(1)
        if is_boosted(player_hand):
            print('你爆了！下一局。。。')
            return dealerwin
        else:
            return no_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand)


##check是不是爆掉了
def is_boosted(hand_card):
    sum = calculate_hand(hand_card)
    if sum > 21:
        return True
    else:
        return False

def blackjack(gamble_money, money):
    print('Game is Started!')
    deck = shuffle_card()
    dealer_hand = []
    player_hand = []
    count = -1
    # return 赢/输/平/21点赢（1.5倍chip）
    global dealerwin
    global playerwin
    global draw
    global player21win
    dealerwin = 'dealerwin'
    playerwin = 'playerwin'
    draw = 'draw'
    player21win = 'blackjackwin'
    choice = None
    print('现在开始发牌！')
    sleep(1)

    for i in range(2):
        deal_card(deck, player_hand)
        deal_card(deck, dealer_hand)
    myhand = '你手中的牌为： %s %s' % (player_hand[0], player_hand[1])
    hisrealhand = 'dealer的手牌为： %s %s' % (dealer_hand[0], dealer_hand[1])
    hishand = 'dealer的手牌为： 未知 %s' % dealer_hand[1]
    print(myhand)
    print(hishand)
    sleep(1)
    if is_Blackjack(player_hand) and is_Blackjack(dealer_hand):
        print('Draw! Next Round!')
        return draw,choice
    elif is_Blackjack(player_hand) and not is_Blackjack(dealer_hand):
        print('Player Win!')
        return player21win,choice
    elif is_Blackjack(dealer_hand) and not is_Blackjack(player_hand):
        print('Dealer Win!')
        print('Dealer 手牌为： %s %s' % (dealer_hand[0], dealer_hand[1]))
        return dealerwin,choice

    result = ''
    # if is_qualified_split(player_hand):
    #     choice = inquirer.prompt(pick_no_split)
    #     choice = choice.get('picks')
    # else:
    choice = inquirer.prompt(pick_no_split)
    choice = choice.get('picks')

    # if choice == 'split':
    #     split_choice(choice,player_hand)
    #else:
    if choice == 'yes':
        result = yes_choice(deck, player_hand, myhand, choice, hisrealhand, dealer_hand)

    elif choice == 'no':
        result = no_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand)

    elif choice == 'double':
        qualify, money, gamble_money = is_valid_double(gamble_money,money)
        if qualify:
            result = double_choice(choice, hisrealhand, dealer_hand, deck, myhand, player_hand)
        else:
            result = yes_choice(deck, player_hand, myhand, choice, hisrealhand, dealer_hand)
        # else:
        #     result = print('不好意思请根据提示项选择: \nPlease type y/n/split/double')
    return result,choice, money, gamble_money

# 根绝blackjack return的4种结果算钱
def count_money(money, gamble_money):
    money = float(money)
    gamble_money = float(gamble_money)

    result, choice, money, gamble_money = blackjack(gamble_money, money)
    if result == draw:
        money = money
        print('你现在还有%.1f的筹码。' % money)
    elif result == playerwin:
        money += gamble_money
        print('你现在还有%.1f的筹码。' % money)
    elif result == dealerwin:
        money -= gamble_money
        print('你现在还有%.1f的筹码。' % money)
    elif result == player21win:
        money += gamble_money * 1.5
        print('你现在还有%.1f的筹码。' % money)
    elif result == playerwin and choice == 'double':
        money += (2 * gamble_money)
        print('你现在还有%.1f的筹码。' % money)
    elif result == dealerwin and choice == 'double':
        money -= (2 * gamble_money)
        print('你现在还有%.1f的筹码。' % money)
    return money


# playerwin, dealerwin, draw, player21win
def play_blackjack():
    money = [inquirer.Text('cash', message="换多少筹码？", validate=lambda _, x: re.match('^[0-9,-_.]*[\.[0-9]*$', x))]
    money = inquirer.prompt(money)
    money = float(money.get('cash'))
    print(money)
    try_count = 0
    while float(money) > 0:
        print('你现在有 %.1f 筹码.' % money)
        for i in range(5):
            gamble_money = [inquirer.Text('chips', message="这局压多少？", validate=lambda _, x: re.match('^[0-9,-_.]*[\.[0-9]*$', x))]
            gamble_money = inquirer.prompt(gamble_money)
            gamble_money = gamble_money.get('chips')
            if float(gamble_money) > money or float(gamble_money) == 0.0:
                print('好好压!')
                try_count += 1
            else:
                break
        if try_count >= 5:
            print('你在浪费大家的时间！这局不带你了。。我们自己开了！')
            break

        money = count_money(money, gamble_money)
        go_on = inquirer.prompt(confirm)
        go_on = go_on.get('confirmed')
        if not go_on:
            print('你选择了退出！')
            break
    if try_count >= 5 or go_on == 'no':
        return False
    if float(money) <= 0:
        print('你没筹码了！')
        refill = inquirer.prompt(rechip)
        refill = refill.get('confirmed')
        return refill


def main():
    refill = play_blackjack()
    while refill:
        play_blackjack()


if __name__ == '__main__':
    main()