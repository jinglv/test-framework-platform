import os
import threading
import time
from xml.dom.minidom import parse

from seldom import Seldom
from seldom import TestMainExtend
from seldom.logging import log

from backend.settings import REPORT_DIR
from cases.models import CaseResult, TestCase
from environment.models import Envs


def seldom_running(test_dir: str, case_info: list, report_name: str, case_id: int, env: int):
    """
    seldom运行用例
    :param test_dir: 测试目录
    :param case_info:
    :param report_name:
    :param case_id:
    :param env:
    :return:
    """
    # 配置运行环境，根据环境id获取环境信息
    env = Envs.objects.get(id=env)

    # 设置Seldom的环境配置
    Seldom.env = env.env
    if env.browser != "":
        browser = env.browser
    else:
        browser = None

    if env.base_url != "":
        base_url = env.base_url
    else:
        base_url = None

    # 1. 直接执行
    main_extend = TestMainExtend(path=test_dir, report=report_name, browser=browser, base_url=base_url)
    main_extend.run_cases(case_info)

    # 2. 借助项目中的文件执行
    # from cases_collect import run_cases
    # run_cases(case_info, report_name)
    time.sleep(1)

    # 打开xml文档，对测试报告进行处理
    report_path = os.path.join(REPORT_DIR, report_name)
    dom = parse(report_path)
    # 得到文档元素对象
    root = dom.documentElement
    # 获取(一组)标签
    testsuite = root.getElementsByTagName('testsuite')
    name = testsuite[0].getAttribute("name")
    run_time = testsuite[0].getAttribute("time")
    errors = testsuite[0].getAttribute("errors")
    failures = testsuite[0].getAttribute("failures")
    skipped = testsuite[0].getAttribute("skipped")
    tests = testsuite[0].getAttribute("tests")
    passed = int(tests) - int(errors) - int(failures) - int(skipped)

    testcase = root.getElementsByTagName('testcase')
    system_out = ""
    for case in testcase:
        system_out = system_out + "Case Name: " + case.getAttribute("name") + "\n"
        try:
            system_out = system_out + case.childNodes[1].firstChild.data + "\n"
        except (AttributeError, IndexError) as e:
            pass

        try:
            system_out = system_out + case.childNodes[3].firstChild.data + "\n"
        except (AttributeError, IndexError) as e:
            pass

        try:
            system_out = system_out + case.childNodes[5].firstChild.data
        except (AttributeError, IndexError) as e:
            pass

    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()
        # 保存表
        CaseResult.objects.create(
            case_id=case_id,
            name=name,
            report=report_text.encode('utf-8'),
            passed=passed,
            error=errors,
            failure=failures,
            skipped=skipped,
            tests=tests,
            system_out=system_out.encode('utf-8'),
            run_time=run_time,
        )
        # 修改状态
        test_case = TestCase.objects.get(id=case_id)
        test_case.status = 2
        test_case.save()

        # 删除报告文件
        # os.remove(report_path)

    log.info("running end!!")


def thread_run_case(test_dir, case_info, report_name, case_id, env):
    """
    线程运行用例
    """
    threads = []
    t = threading.Thread(target=seldom_running, args=(test_dir, case_info, report_name, case_id, env,))
    threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
