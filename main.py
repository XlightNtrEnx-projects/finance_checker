from statementsummary import StatementSummary
import os
import logging
import datetime


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(
    f'logs\{datetime.date.today()}.log')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main() -> None:
    folder = 'csv'
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        summary = StatementSummary(filepath)
        if file != summary.expected_file:
            expected_filepath = os.path.join(folder, summary.expected_file)
            os.rename(filepath, expected_filepath)
        summary.save()  # object saved to StatementSummary.objects in ascending date
    old_balance: float = 0.00
    net: float = 0.00
    new_balance: float = 0.00
    first_summary = True
    for summary in StatementSummary.objects:
        if first_summary:
            old_balance = summary.ledger_balance
            first_summary = False
        else:
            net = summary.net_change
            new_balance = summary.ledger_balance
            if old_balance + net != new_balance:
                raise ValueError(
                    f'The transactions for {summary} do not add up')
            else:
                logger.debug(f'Validated {summary}:\n \
                        Old balance: {old_balance}\n \
                        Net change: {net}\n \
                        New balance: {new_balance}')
                old_balance = new_balance
        logger.debug(f'Validated {summary}:\n \
                        Old balance: {old_balance}\n \
                        Net change: {net}\n \
                        New balance: {new_balance}')
    logger.info('All summaries add up')


if __name__ == "__main__":
    main()
