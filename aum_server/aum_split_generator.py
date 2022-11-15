from abc import abstractmethod
import random
from aum_split_type import AUMSplit

class AUMSplitGenerator:
    @abstractmethod
    def generate_aum_split(account_name, max_percentage: int = 100) -> AUMSplit:
        if not account_name:
            raise Exception("Cannot generate stock with an empty name")
        percentage = random.randint(0, max_percentage)
        return AUMSplit(account_name=account_name, percentage=percentage)
