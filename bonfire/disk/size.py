import os
import sys


class FileSizeDto(object):

    def __init__(self, file_path, file_size, error_msg="", next_nodes=None):
        """
         构造函数
        :param file_path: 文件或文件夹路径
        :type file_path str
        :param file_size: 占用磁盘容量,字节
        :type file_size: long
        :param error_msg: 当前文件或目录计算容量失败时，该值不为空
        :type error_msg: str
        :param next_nodes: 当前为文件夹时，该值为子文件(夹)，否则默认为 None。
        :type next_nodes: array. []
        """
        self.file_path = file_path
        self.file_size = file_size
        self.error_msg = error_msg
        self.next_nodes = next_nodes

    def get_size_with_unit(self):
        """
        按最大容量单位数值。 例如 1024字节 返回 1k
        :return:
        """
        unit = 'K'
        count = self.file_size / 1024
        if count > 1024:
            count = count / 1024
            unit = 'M'
        if count > 1024:
            count = count / 1024
            unit = 'G'
        if count > 1024:
            count = count / 1024
            unit = 'T'
        if count > 1024:
            count = count / 1024
            unit = 'P'
        return str(round(count, 2)) + unit

    def print_file_tree(self, max_dir_hierarchy=sys.maxsize, only_print_dir=True, min_size_with_unit='10m'):
        """
        打印目录树
        :param max_dir_hierarchy: 打印目录层级。若max_dir_hierarchy=2，只打印到子文件夹
        :param only_print_dir: only_print_dir=True, 只打印目录大小
        :param min_size_with_unit: 只打印大于等于min_size_with_unit的文件或文件夹, 单位：k、m、g、t、p
        :return:
        """
        min_size_with_unit = min_size_with_unit.lower()
        unit = 1024
        min_file_size = 0
        if min_size_with_unit.__contains__("k"):
            min_file_size = int(min_size_with_unit[:min_size_with_unit.index("k")]) * unit
        if min_size_with_unit.__contains__("m"):
            min_file_size = int(min_size_with_unit[:min_size_with_unit.index("m")]) * pow(unit, 2)
        if min_size_with_unit.__contains__("g"):
            min_file_size = int(min_size_with_unit[:min_size_with_unit.index("g")]) * pow(unit, 3)
        if min_size_with_unit.__contains__("t"):
            min_file_size = int(min_size_with_unit[:min_size_with_unit.index("t")]) * pow(unit, 4)
        if min_size_with_unit.__contains__("p"):
            min_file_size = int(min_size_with_unit[:min_size_with_unit.index("p")]) * pow(unit, 5)

        self.__print_file_tree(dir_hierarchy=0, max_dir_hierarchy=max_dir_hierarchy, only_print_dir=only_print_dir,
                               min_file_size=min_file_size)

    def __print_file_tree(self, dir_hierarchy, max_dir_hierarchy, only_print_dir, min_file_size):
        """
        打印目录树
        :param dir_hierarchy: 目录层级，从0开始
        :param max_dir_hierarchy 打印最大层级
        :param only_print_dir: 只打印目录
        :param min_file_size: 文件大于min_file_size字节才打印，单位字节
        :return: None
        """
        if dir_hierarchy == 0:
            print(self.get_size_with_unit(), self.file_path, self.error_msg)

        if dir_hierarchy >= max_dir_hierarchy:
            return

        if self.next_nodes is None:
            return

        first = '|'
        underline = '___'
        tmp = ''
        i = 0
        while i <= dir_hierarchy:
            tmp += underline
            i = i + 1

        for node in self.next_nodes:
            if only_print_dir and os.path.isdir(node.file_path) and node.file_size >= min_file_size:
                print(first, tmp, node.get_size_with_unit(), node.file_path, node.error_msg)
            node.__print_file_tree(i + 1, max_dir_hierarchy, only_print_dir, min_file_size)


def traverse_directory_size(file_path):
    """
    计算文件(夹)容量
    :param file_path:  文件夹或文件路径
    :return:  FileSizeDto
    """
    if os.path.isfile(file_path):
        try:
            file_size = os.path.getsize(file_path)
            return FileSizeDto(file_path=file_path, file_size=file_size)
        except IOError:
            print("error: Failed to count file size. file_path=%s", file_path)
            return FileSizeDto(file_path=file_path, file_size=0, error_msg="Failed to count file size")

    if os.path.isdir(file_path):
        try:
            file_list = os.listdir(file_path)
            file_num_count = len(file_list)
            if file_num_count == 0:
                return FileSizeDto(file_path=file_path, file_size=0)

            next_nodes = []
            count = 0
            for item_file_name in file_list:
                item_file_path = os.path.join(file_path, item_file_name)
                item_dto = traverse_directory_size(item_file_path)
                next_nodes.append(item_dto)
                count += item_dto.file_size
            return FileSizeDto(file_path=file_path, file_size=count, next_nodes=next_nodes)
        except IOError:
            print("error: Failed to count file size. file_path='%s'" % file_path)
            return FileSizeDto(file_path=file_path, file_size=0)
    return None


if __name__ == '__main__':
    # path = r'C:\Users\Administrator\AppData\Local'
    path = r'D:\data'
    result = traverse_directory_size(path)
    result.print_file_tree(max_dir_hierarchy=2, min_size_with_unit='100M')
