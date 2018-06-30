# _*_coding:utf-8 -*_

from config import singleton

@singleton
class ScanResult:
    def __init__(self):
        self.wvs_result_list = []

    def has(self, result):
        identifier = "{}_{}".format(result["VulType"], result["VulUrl"])
        for res in self.wvs_result_list:
            res_identifier = "{}_{}".format(res["VulType"], res["VulUrl"])
            print(res_identifier, identifier)
            if res_identifier == identifier:
                return True

        return False

    def add_scan_result(self, result):
        existed = self.has(result)
        if not existed:
            self.wvs_result_list.append(result)
        else:
            pass

    def get_scan_result(self):
        return self.wvs_result_list

    def clear_result_list(self):
        self.wvs_result_list.clear()