import csv
import logging
import datetime


class StatementSummary:
    pass


class StatementSummary:
    '''
    Extracts information from csv file by initializing object with filepath as parameter and making information available in object attributes
    '''
    objects: list[StatementSummary] = []
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(
        f'logs\{datetime.date.today()}.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(StatementSummary.__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    def __init__(self, filepath: str) -> None:
        self.account_details: str
        self.statement_date: str
        self.available_balance: str
        self.ledger_balance: str
        self.earliest_date: datetime.date
        self.latest_date: datetime.date
        self.credit: float = 0.00
        self.debit: float = 0.00
        self.net_change: float = 0.00
        self.parse_csv(filepath)

    def __str__(self) -> str:
        return self.earliest_date.strftime('%Y-%m-%d') + ' - ' + self.latest_date.strftime('%Y-%m-%d')

    def __repr__(self) -> str:
        return self.earliest_date.strftime('%Y-%m-%d') + ' - ' + self.latest_date.strftime('%Y-%m-%d')

    def parse_csv(self, filepath: str) -> None:
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            all_possible_first_value_of_row = [
                'Account Details For:', 'Statement as at:', 'Available Balance:', 'Ledger Balance:']
            attribute_names = [
                'account_details', 'statement_date', 'available_balance', 'ledger_balance']
            for row in reader:
                self.logger.debug(f'Parsing {row}')
                if len(row) > 0:
                    if len(all_possible_first_value_of_row) > 0:
                        first_value = row[0]
                        expected_value = all_possible_first_value_of_row[0]
                        if expected_value == first_value:
                            setattr(self, attribute_names[0], row[1].strip())
                            del all_possible_first_value_of_row[0]
                            del attribute_names[0]
                        else:
                            raise ValueError(
                                f'Expected {expected_value} but got {first_value}')
                    else:
                        if not 'Transaction Date' in row[0]:
                            date = datetime.datetime.strptime(
                                row[0], '%d %b %Y').date()
                            if hasattr(self, 'earliest_date'):
                                if date < self.earliest_date:
                                    self.earliest_date = date
                            else:
                                self.earliest_date = date
                            if hasattr(self, 'latest_date'):
                                if self.latest_date < date:
                                    self.latest_date = date
                            else:
                                self.latest_date = date
                            try:
                                self.debit += float(row[2].strip())
                            except ValueError:
                                pass
                            try:
                                self.credit += float(row[3].strip())
                            except ValueError:
                                pass
            self.net_change = self.credit - self.debit
            self.logger.info(f'Dumping statement summary:\n \
                        Account details: {self.account_details}\n \
                        Statement date: {self.statement_date}\n \
                        Available balance: {self.available_balance}\n \
                        Ledger balance: {self.ledger_balance}\n \
                        Earliest date: {self.earliest_date}\n \
                        Latest date: {self.latest_date}\n \
                        Credit: {self.credit}\n \
                        Debit: {self.debit}\n \
                        Net: {self.net_change}')

    def save(self) -> None:
        if len(self.objects) > 0:
            for index, summary in enumerate(self.objects):
                if self.latest_date < summary.latest_date:
                    self.objects.insert(index, self)
        else:
            self.objects.append(self)
