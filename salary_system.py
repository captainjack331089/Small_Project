"""
某公司有三种类型的员工 分别是部门经理、程序员和销售员
需要设计一个工资结算系统 根据提供的员工信息来计算月薪
部门经理的月薪是每月固定15000元
程序员的月薪按本月工作时间计算 每小时150元
销售员的月薪是1200元的底薪加上销售额5%的提成
"""

from abc import ABCMeta, abstractmethod
class Employee(object):
    """
    员工
    """
    def __init__(self, name):
        """
        初始化方法
        """
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_salary(self):
        """抽象函数"""
        pass


class Manager(Employee):

    def get_salary(self):
        return 15000.00


class Programmer(Employee):
    """
    程序员的月薪按本月工作时间计算 每小时150元
    """
    def __init__(self, name, working_hour=0):
        super().__init__(name)
        self._working_hour = working_hour

    @property
    def working_hour(self):
        return self._working_hour

    @working_hour.setter
    def working_hour(self,working_hour):
        self._working_hour = working_hour if working_hour > 0 else 0

    def get_salary(self):
        return 150.0 * self._working_hour

class Salesman(Employee):
    """
    销售员的月薪是1200元的底薪加上销售额5%的提成
    """

    def __init__(self, name, sales=0):
        super().__init__(name)
        self._sales = sales

    @property
    def sales(self):
        return self._sales

    @sales.setter
    def sales(self, sales):
        self._sales = sales if sales > 0 else 0

    def get_salary(self):
        return 1200.0 + self._sales * 5 / 100


def main():
    employee_list = [Manager('Jack'), Programmer('Robin'), Programmer('Jobs'), Salesman('Mark'), Salesman('Jason'), Salesman('Sharon')]
    for em in employee_list:
        if isinstance(em,Manager):
            print('The salary of the Manager %s is %s. \n' %(em.name, em.get_salary()))
        elif isinstance(em, Programmer):
            em.working_hour = float(input('Please input this month\'s working hour of Programmer %s: ' %em.name))
            print('The salary of the Programmer %s is %s. \n' %(em.name, em.get_salary()))
        elif isinstance(em, Salesman):
            em.sales = float(input('Please input this month\'s sales of Salesman %s: ' %em.name))
            print('The salary of the Programmer %s is %s. \n' %(em.name, em.get_salary()))



if __name__ == '__main__':
    main()

