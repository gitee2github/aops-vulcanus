#!/usr/bin/python3
# ******************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2021-2021. All rights reserved.
# licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN 'AS IS' BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# ******************************************************************************/
"""
Time:
Author:
Description:
"""
import json

from prettytable import PrettyTable
from pygments import highlight, lexers, formatters

from vulcanus.restful.response import BaseResponse


def add_page(sub_parse):
    """
    Add access_token of the sub parse.
    Args:
        sub_parse(sub_parse): sub_parse of the command
    """
    sub_parse.add_argument("--page", help="page of the query", nargs="?", type=int, default=1)

    sub_parse.add_argument("--per_page", help="items per page.", nargs="?", type=int, default=20)


def cli_request(action, manager_url, pyload, header, access_token=None):
    """
    cli request to manager
    Args:
        action(str): actions of requests
        manager_url(str): route
        pyload(dict): request body
        header(dict): request header
        access_token(str): access token of users

    Returns:
        json: response of manager
    """
    if access_token is not None:
        header["access_token"] = access_token
    result = BaseResponse.get_response(action, manager_url, pyload, header)
    print(result)
    return result


def request_without_print(action, manager_url, pyload, header, access_token=None):
    """
    cli request without print
    Args:
        action(str): actions of requests
        manager_url(str): route
        pyload(dict): request body
        header(dict): request header
        access_token(str): access token of users

    Returns:
        json: response of manager
    """
    if access_token is not None:
        header["access_token"] = access_token
    result = BaseResponse.get_response(action, manager_url, pyload, header)
    return result


def add_query_args(sub_parse, item_list):
    """
    Add query args of the sub parse.
    Args:
        item_list(list): list for sort items
        sub_parse(sub_parse): sub_parse of the command
    Returns:

    """
    sub_parse.add_argument(
        "--sort",
        help="sort for the query result, null is no sort",
        nargs="?",
        type=str,
        default="",
        choices=item_list,
    )

    sub_parse.add_argument(
        "--direction",
        help="asc or desc of the sort",
        nargs="?",
        type=str,
        default="asc",
        choices=["asc", "desc"],
    )


def add_access_token(sub_parse):
    """
    Add access_token of the sub parse.
    Args:
        sub_parse(sub_parse): sub_parse of the command

    """
    sub_parse.add_argument(
        "--access_token",
        help="The access token for operations",
        nargs="?",
        type=str,
        required=True,
    )


def add_start_and_end(sub_parse):
    """
    Add start time and end time of the sub parse.
    Args:
        sub_parse(sub_parse): sub_parse of the command
    """
    group_start_end = sub_parse.add_argument_group("group_start_end", "The group for start and end")

    group_start_end.add_argument(
        "--start",
        nargs="?",
        type=str,
        default="",
        help="original date of raw data, default is 1 hour ago.",
    )

    group_start_end.add_argument(
        "--end",
        nargs="?",
        type=str,
        default="",
        help="end date of raw data, default is now",
    )


def create_table(fields):
    """
    create pretty table for print
    Args:
        fields(list): list of fields
    Returns:
        PrettyTalbe: pretty table for print
    """
    table = PrettyTable()
    if not isinstance(fields, list):
        print("Invalid field of the table, ckeck the data structure of the fields.")
    else:
        table.field_names = fields
    return table


def print_row_from_result(results):
    """
    add row of the table
    Args:
        results(list): results of the report
    """
    if len(results) == 0:
        return
    table = create_table(list(results[0].keys()))
    for result in results:
        table.add_row(list(result.values()))
    print(table)


def pretty_json(input_dict):
    """
    Generate pretty json from dict
    Args:
        input_dict(dict): dict will be transformed.
    Returns:
        json: json with highlight
    """
    format_json = json.dumps(input_dict, indent=2, ensure_ascii=False, sort_keys=True)
    highlight_json = highlight(format_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    return highlight_json
