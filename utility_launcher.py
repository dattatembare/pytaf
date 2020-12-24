from argparse import ArgumentParser, SUPPRESS

from lib.utils import format_env
from utilities import delete_all_company_tasks, nacha_svc
from utilities.kafka import kafka_producer

DELETE_ALL_COMPANY_TASKS = 'delete_all_company_tasks'
NACHA_TOKENIZE = 'nacha_tokenize'
NACHA_DETOKENIZE = 'nacha_detokenize'
CODSG_DOCUSIGN_TEMPLATE_LOADER = 'codgs_docusign_template_loader'
KAFKA_PRODUCER = 'kafka_producer'

mapper = {
    DELETE_ALL_COMPANY_TASKS: delete_all_company_tasks.delete_tasks,
    NACHA_TOKENIZE: nacha_svc.tokenize,
    NACHA_DETOKENIZE: nacha_svc.detokenize,
    KAFKA_PRODUCER: kafka_producer.producer,
}
"""Must declare the utility.function name here. Note: No () after function name"""


def execute():
    """
    Get utility function from mapper and execute it
    :return:
    """
    command_args = commandline_args()
    return mapper.get(command_args['utility'])(command_args)


def commandline_args() -> dict:
    # Common argument required for all utilities
    common = ArgumentParser(add_help=False)
    common.add_argument('-e', '--environment', help='Environment (default=dev)',
                        choices=['local', 'dev', 'qa', 'preprod', 'prod'], default='dev')

    parser = ArgumentParser()

    # Specific to utility
    subparsers = parser.add_subparsers(help='types of utilities')
    # delete_all_company_tasks
    delete_company_parser = subparsers.add_parser(DELETE_ALL_COMPANY_TASKS, parents=[common])
    delete_company_parser.add_argument('-u', '--utility', help=SUPPRESS, default=DELETE_ALL_COMPANY_TASKS)
    delete_company_parser.add_argument('-c', '--companyid', help='companyid')
    # tokenize
    nacha_tokenize_parser = subparsers.add_parser(NACHA_TOKENIZE, parents=[common])
    nacha_tokenize_parser.add_argument('-u', '--utility', help=SUPPRESS, default=NACHA_TOKENIZE)
    nacha_tokenize_parser.add_argument('-ban', '--bank_account_number', help='Bank Account Number')
    nacha_tokenize_parser.add_argument('-rn', '--routing_number', help='Routing Number')
    # detokenize
    nacha_detokenize_parser = subparsers.add_parser(NACHA_DETOKENIZE, parents=[common])
    nacha_detokenize_parser.add_argument('-u', '--utility', help=SUPPRESS, default=NACHA_DETOKENIZE)
    nacha_detokenize_parser.add_argument('-t', '--token', help='Bank Account Number')
    nacha_detokenize_parser.add_argument('-rn', '--routing_number', help='Routing Number')
    # Kafka Producer - send Kafka message in avro format
    kafka_producer_parser = subparsers.add_parser(KAFKA_PRODUCER, parents=[common])
    kafka_producer_parser.add_argument('-u', '--utility', help=SUPPRESS, default=KAFKA_PRODUCER)
    kafka_producer_parser.add_argument('-t', '--topic', required=True, help='Topic name')
    kafka_producer_parser.add_argument('-bs', '--bootstrap-servers', required=True, help='Bootstrap server address')
    kafka_producer_parser.add_argument('-sr', '--schema-registry', required=True, help='Schema Registry url')
    kafka_producer_parser.add_argument('-sk', '--schema-key', required=True,
                                       help='Avro schema-key key from schema registry')
    kafka_producer_parser.add_argument('-sv', '--schema-value', required=True,
                                       help='Avro schema-value key from schema registry')
    kafka_producer_parser.add_argument('-mk', '--message-key', required=True,
                                       help='Message key. If not provided, will be a random UUID')
    kafka_producer_parser.add_argument('-mv', '--message-value', required=True, help='message value')

    return format_env(parser.parse_args().__dict__)


"""
How to run utility_launcher: 
Terminal::
Find required arguments: pytaf>utility_launcher.py nacha_tokenize -h
Run utility: pytaf>utility_launcher.py nacha_tokenize -ban 5854890438 -rn 1123123 -e dev
Pycharm:: Run using Run/debug option
"""
if __name__ == '__main__':
    execute()
