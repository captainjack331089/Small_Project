
# card suits: '♣', '♠', '♦', '♥'

from random import shuffle
from time import sleep


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


##check是不是爆掉了
def is_boosted(hand_card):
    sum = calculate_hand(hand_card)
    if sum > 21:
        return True
    else:
        return False


def blackjack():
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
    dealerwin = 'dwin'
    playerwin = 'playerwin'
    draw = 'draw'
    player21win = 'blackjackwin'

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
        return draw
    elif is_Blackjack(player_hand) and not is_Blackjack(dealer_hand):
        print('Player Win!')
        return player21win
    elif is_Blackjack(dealer_hand) and not is_Blackjack(player_hand):
        print('Dealer Win!')
        print('Dealer 手牌为： %s %s' % (dealer_hand[0], dealer_hand[1]))
        return dealerwin

    choice = input('要不要继续发牌？y/n： ')
    while choice in ('y' or 'Y' or 'y\'' or 'Y\''):
        sleep(1)
        deal_card(deck, player_hand)
        print('给你发了一张: %s' % player_hand[-1])
        myhand += ' ' + player_hand[-1]
        print('你现在的手牌为： ' + myhand)
        sleep(1)
        if is_boosted(player_hand):
            print('你爆了！下一局。。。')
            return dealerwin
        else:
            choice = input('要不要继续发牌？y/n： ')

    if choice == 'n' or 'N':
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
            print('Dealer 现在的手牌为： ' + hisrealhand)
            sleep(1)
            if is_boosted(dealer_hand):
                print('Dealer 爆了！你赢了！')
                return playerwin

        print('Dealer 牌发完了！现在计算谁获胜！')
        sleep(2)
        print('玩家手牌为: ' + myhand)
        sleep(2)
        print('Dealer 手牌为: ' + hisrealhand)
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


# 根绝blackjack return的4种结果算钱
def count_money(money, gamble_money):
    result = blackjack()
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
    return money


# playerwin, dealerwin, draw, player21win
def play_blackjack():
    money = float(input('要换多少筹码?'))
    try_count = 0
    while money > 0:
        print('你现在有 %.1f 筹码.' % money)
        for i in range(5):
            gamble_money = float(input('这局压多少? '))
            if gamble_money > money or gamble_money == 0:
                print('好好压!')
                try_count += 1
            else:
                break
        if try_count >= 5:
            print('你在浪费大家的时间！这局不带你了。。我们自己开了！')
            break

        money = count_money(money, gamble_money)
        go_on = input('还玩么？ y/n ')
        if go_on == 'n' or go_on == 'N' or go_on == 'n\'' or go_on == 'N\'':
            print('你选择了退出！')
            break
    if try_count >= 5 or go_on == 'n' or go_on == 'N' or go_on == 'n\'' or go_on == 'N\'':
        return

    print('你没筹码了！')
    refill = input('要换新的筹码继续玩么？y/n ')
    if refill == 'y' or refill == 'Y' or refill == 'y\'' or refill == 'Y\'':
        play_blackjack()


def main():
    play_blackjack()


if __name__ == '__main__':
    main()
