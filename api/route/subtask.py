from flask import Blueprint

from api.constants.reply import Reply, ListReply
from core.valid_task import VALID_TASK

subtask_api = Blueprint('subtask', __name__)


@subtask_api.route('/subtask/schema', methods=['GET'])
def list_subtask_schema():
    subtask_type: dict = VALID_TASK.T

    res = [parse_validate_task(k, v) for k, v in subtask_type.items()]
    return ListReply(res, len(res))


@subtask_api.route('/subtask/schema/<abbr>', methods=['GET'])
def retrieve_subtask_schma(abbr):
    subtask_type: dict = VALID_TASK.T

    return Reply(parse_validate_task(abbr, subtask_type.get(abbr)))


def parse_validate_task(abbr, rule):
    subtask = {
        'abbr': abbr,
        'title': rule.get('title', ''),
        'desc': rule.get('desc', ''),
        'params': []
    }

    for param in rule.get('params'):
        typ_enum = {
            str: 'str',
            int: 'int',
            float: 'float',
            bool: 'bool',
            list: 'list',
        }
        subtask['params'].append({
            'key': param.key,
            'title': param.title,
            'desc': param.desc,
            'key_type': typ_enum[param.typ],
            'default': param.default,
        })

    return subtask
