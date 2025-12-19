class LoyaltyAccount:
    def __init__(self):
        self.points = 0

    def add_points(self, amount_spent):
        earned_points = int(amount_spent // 50)
        self.points += earned_points

    def redeem(self, total_amount):
        if self.points <= 0:
            return 0

        redeemed = min(self.points, total_amount)
        self.points -= redeemed
        return redeemed
