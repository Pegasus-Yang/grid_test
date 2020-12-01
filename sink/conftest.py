import os
import re
from typing import List, Dict
from copy import deepcopy
from typing import List

import yaml
from _pytest.config import Config
from _pytest.nodes import Item
from _pytest.python import Function

from mtf.core.suite import Suite
from mtf.core.model import Node

from mtf.core.logger import log
from mtf.core.runner import Runner
from mtf.core.utils import Utils


def pytest_addoption(parser):
    parser.addoption(
        "--index",
        action="store",
        dest="index",
        default="-1",
        help='parallel index',
    )
    parser.addoption(
        "--include",
        action="store",
        dest="include",
        default=None,
        help='case range',
    )
    parser.addoption(
        "--exclude",
        action="store",
        dest="exclude",
        default=None,
        help='case range exclude',
    )

    parser.addoption(
        "--project",
        action="store",
        dest="project",
        default=".",
        help='project dir',
    )


def pytest_itemcollected(item: Item):
    """
    在运行前，对指定 case 设置失败重试次数
    :param item:
    :return:
    """
    print("hello" + item.nodeid)
    item.session.config.option.reruns = 10


def _generate_setup_yaml(matched_case):
    """
    在 suites.yaml 指定用例下产生 setup.yaml 文件
    :param items:
    :return:
    """
    data = []
    tmp_matched_case = deepcopy(matched_case)
    for case in tmp_matched_case:
        if case["type"] != '3':
            continue
        suites = case.pop("suites")
        for suite in suites:
            suite_name = suite['suite_name']
            suite_data = {suite_name: {**case, "setup": suite['setup']}}
            data.append(suite_data)

    with open("setup.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(data, f,
                  default_flow_style=False,
                  indent=2, allow_unicode=True, encoding="utf-8")


def pytest_collection_modifyitems(config: Config, items: List[Function]):
    runner = Runner()
    # log.debug("origin pytest nodeid_map=")
    # nodeids_origin = [item.nodeid for item in items]
    # log.debug(Utils.to_json_str(nodeids_origin))

    # 转成mtf的nodeid
    nodeid_map = {runner.nodeid_format(item.nodeid): item for item in items}
    log.debug("mtf nodeid_map=")
    log.debug(Utils.to_json_str(list(nodeid_map.keys())))

    # 保存所有的mtf nodeid方便别人导入
    with open("testcases.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(
            Utils.to_json_object(Utils.to_json_str(list(nodeid_map.keys()))),
            f,
            default_flow_style=False,
            indent=2, allow_unicode=True, encoding="utf-8"
        )

    # 分成若干组进行多进程并行
    index = int(config.getoption('index', -1))
    log.debug(f'index={index}')

    # 保存当时的目录
    project_dir = config.getoption('project', '.')
    project_dir = Utils.get_current_dir(project_dir)
    Runner.project_dir = project_dir
    suites_conf = os.sep.join([project_dir, "suites.yaml"])
    log.debug(f"project_dir={project_dir}")
    log.debug(f"suites_conf={suites_conf}")

    # 返回多叉树
    tree: Node[Suite] = runner.get_suites(suites_conf=suites_conf)

    # 只运行匹配节点
    include = config.getoption("include", None)
    if include:
        for node, depth in tree.travel():
            suite: Suite = node.data
            if suite.name == include:
                tree = node
                break

    # 不跑特定的测试套
    exclude = config.getoption("exclude", None)
    if exclude:
        tree.delete(f"cur.data['name']=='{exclude}'")

    # todo: 测试用例更新到树中
    for node, depth in tree.travel():
        suite: Suite = node.data
        if suite is not None:
            suite.children = get_nodeids_from_pattern(nodeid_map, suite.pattern)
    log.info(f'testcase tree=')
    log.info(Utils.to_json_str(tree))

    # 把多叉树分拆为多个并行列表  res=[ [suite1, case1, case2,case3], [suite2,case4,case5], [], []]
    # todo：只把type=1的生成并行list
    res = tree.to_list()
    log.debug("parallel list=")
    log.debug(Utils.to_json_str(res))

    suites: List[Suite] = []
    # 如果设置了index，那么直跑特定的某个并行子集
    if index >= 0:
        # [suite1, case1, case2,case3]
        suites = res[index]
    else:
        # [suite1, case1, case2, case3， suite2, case4, case5]
        for item_list in res:
            suites += item_list
    log.debug("suites=")
    log.debug(Utils.to_json_str(suites))

    # 挑选真正的mtf的测试用例
    items_new = []
    # 记录已经匹配上的 testcase
    matched_testcase = []

    suite_order = []
    for suite in suites:
        if suite is not None:
            suite_order.append(suite)
            if suite.children:
                for nodeid in suite.children:
                    Runner.nodeid_suites_map.append({nodeid: suite_order})
                    items_new.append(nodeid_map[nodeid])
        else:
            suite_order = []
    log.info(f"suite order={Utils.to_json_str(Runner.nodeid_suites_map)}")
    items[:] = items_new
    # _generate_setup_yaml(matched_testcase)
    log.debug("items=")
    log.debug(items)


def get_nodeids_from_pattern(nodeid_map: dict, testcase_id):
    items_new: List[dict] = []
    for nodeid, item in nodeid_map.items():
        # log.debug(f"search testcase_id={testcase_id} nodeid={nodeid}")
        if testcase_id not in ["", None] and re.search(testcase_id, nodeid):
            log.debug(f"hit {nodeid}")
            items_new.append(nodeid)
    return items_new
