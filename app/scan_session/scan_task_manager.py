#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import json
import logging
import time
import shutil

from config import basedir, singleton
from .scan_setting import ScanSetting
from .scan_result import ScanResult
from .task_info import TaskInfo

log = logging.getLogger("Server")


@singleton
class ScanTaskManager(object):
    """扫描任务管理类

    Args:
        object ([type]): [description]
    """
    def __init__(self):
        self.task_list_file = os.path.join(basedir, "scan_task",
                                           "task_list.json")
        self.scan_task_list = self.__get_task_list()
        self.__last_task = self.get_last_task()

    def __get_task_list(self):
        """获取任务列表

        Returns:
            [list]: 任务信息列表
        """
        with open(self.task_list_file, 'r') as rf:
            task_dict = json.load(rf)
            return sorted(task_dict.items(), key=lambda d: d[1])

    def load_task_info(self, task_name):
        """依据任务名称获取任务信息

        Args:
            task_name (str): 任务名称

        Returns:
            [type]: 任务信息
        """
        task_path = os.path.join(basedir, "scan_task", task_name)

        with open(os.path.join(task_path, "task_info.json"),
                  'r',
                  encoding='utf-8') as rf:
            # 载入任务信息
            task_info_json = json.load(rf)
            task_info = TaskInfo(task_info_json)
            # 初始化扫描参数和结果信息
            ScanSetting().set_scan_setting(task_name, task_info.start_url,
                                           task_info.scan_policy)
            self.load_task_result(os.path.join(task_path, "scan_result.json"))
            return task_info, ScanSetting().get_scan_setting(), ScanResult(
            ).wvs_result_list

    def load_task_result(self, scan_result_file):
        """从扫描结果文件中载入任务结果信息

        Args:
            scan_result_file ([str]): 任务扫描结果文件
        """
        with open(scan_result_file, 'r', encoding='utf-8') as rf:
            ScanResult().wvs_result_list = json.load(rf)

    def new_task(self, task_name, url, policy):
        task_path = os.path.join(basedir, "scan_task", task_name)
        if not os.path.exists(task_path):
            os.mkdir(task_path)
            self.scan_task_list.append((task_name, time.time()))
            # 新建任务后初始化扫描参数和结果
            ScanSetting().set_scan_setting(task_name, url, policy)
            ScanResult().clear_result_list()
            # 新建任务后保存
            self.save_task(task_name)
            return True
        else:
            log.info("任务已存在，请更改任务名称!")
            return False

    def save_task(self, task_name):
        """保存扫描任务

        Args:
            task_name (str): 任务名称
        """
        task_path = os.path.join(basedir, "scan_task", task_name)
        # 保存任务列表
        self.__save_task_list()

        task_info = TaskInfo()
        # 保存任务信息
        with open(os.path.join(task_path, "task_info.json"),
                  'w',
                  encoding='utf-8') as wf:
            log.info("save task info ::  {}".format(
                ScanSetting().get_scan_setting()))
            _, task_info.start_url, task_info.scan_policy = ScanSetting(
            ).get_scan_setting()
            task_info_json = task_info.get_task_info_dict()
            json.dump(task_info_json, wf)

        # 保存扫描结果
        with open(os.path.join(task_path, task_info.scan_result_file),
                  'w',
                  encoding='utf-8') as wf:
            json.dump(ScanResult().get_scan_result(), wf)

    def __save_task_list(self):
        """保存任务列表
        """
        task_dict = {}
        for task in self.scan_task_list:
            task_dict[task[0]] = task[1]

        with open(self.task_list_file, 'w', encoding='utf-8') as wf:
            json.dump(task_dict, wf)

    def del_task(self, task_name):
        """删除任务

        Args:
            task_name (str): 被删除任务的名称
        """
        task, is_exist = self.__find_task(task_name)
        if is_exist:
            log.info("删除任务_{}".format(task_name))
            task_path = os.path.join(basedir, "scan_task", task_name)

            if os.path.exists(task_path):
                shutil.rmtree(task_path)
            else:
                log.info("任务信息目录不存在，删除任务名称!")

            self.scan_task_list.remove(task)

            self.__save_task_list()
            ScanSetting().set_scan_setting("", "", "Normal")
            ScanResult().clear_result_list()
        else:
            log.info("任务<{}>不存在".format(task_name))

    def get_last_task(self):
        # 返回最近一次任务（名称，time）
        if len(self.scan_task_list) > 0:
            return self.scan_task_list[::-1][0]
        else:
            return None

    def __find_task(self, task_name):
        for task in self.scan_task_list:
            if task[0] == task_name:
                return task, True
        return None, False

    def load_all_task_info(self):
        task_info_list = list()
        if len(self.scan_task_list):
            for task in self.scan_task_list:
                task_info, _, _ = self.load_task_info(task[0])
                task_info_dict = task_info.get_task_info_dict()
                task_info_dict["TaskName"] = task[0]
                task_info_dict["Timestamp"] = time.strftime(
                    "%Y/%m/%d %H:%M:%S",
                    time.localtime(float(task_info_dict["Timestamp"])))
                task_info_list.append(task_info_dict)

            return task_info_list, len(task_info_list)
        else:
            return None, 0
