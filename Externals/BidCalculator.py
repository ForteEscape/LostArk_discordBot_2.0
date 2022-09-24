import math


class BidCalculator:
    def __init__(self):
        self.__bid_data_four = None
        self.__bid_data_four_before = None
        self.__bid_data_eight = None
        self.__bid_data_eight_before = None

    def calculate(self, gold_data):
        bid_gold_four = gold_data * 0.95 * 0.75
        bid_before_gold_four = gold_data * 0.95 * 0.68
        bid_gold_four = math.floor(bid_gold_four)
        bid_before_gold_four = math.floor(bid_before_gold_four)

        bid_gold_eight = gold_data * 0.95 * 0.875
        bid_before_gold_eight = gold_data * 0.95 * 0.795
        bid_gold_eight = math.floor(bid_gold_eight)
        bid_before_gold_eight = math.floor(bid_before_gold_eight)

        self.__bid_data_eight = bid_gold_eight
        self.__bid_data_eight_before = bid_before_gold_eight
        self.__bid_data_four = bid_gold_four
        self.__bid_data_four_before = bid_before_gold_four

    def get_bid_data(self):
        datalist = [self.__bid_data_eight, self.__bid_data_eight_before,
                    self.__bid_data_four, self.__bid_data_four_before]

        return datalist
