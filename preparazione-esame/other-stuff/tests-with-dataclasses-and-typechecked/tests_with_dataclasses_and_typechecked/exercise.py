from dataclasses import *
from dataclass_type_validator import dataclass_type_validator
from typeguard import *
from valid8 import validate

###############################################
'''
@typechecked
@dataclass
class Foo:
    bar: str
    buzz: int = field(default=0)


a = Foo('a string here', 100)   # ok
b = Foo(100)                    # ok
c = Foo('a string here')        # ok
d = Foo(100, 'a string here')   # ok
'''
###############################################
'''
@typechecked
@dataclass
class Foo:
    bar: str
    buzz: int = field(default=0)

    def __post_init__(self):
        dataclass_type_validator(self)


a = Foo('a string here', 100)   # ok
b = Foo(100)                    # ERROR ('bar': "must be an instance of <class 'str'>, but received <class 'int'>"}
c = Foo('a string here')        # ok
d = Foo(100, 'a string here')   # ERROR ('bar': "must be an instance of <class 'str'>, but received <class 'int'>", 'buzz': "must be an instance of <class 'int'>, but received <class 'str'>"
'''
###############################################
'''
@typechecked
@dataclass
class Foo:
    bar: str
    buzz: int = field(default=0, init=False)


a = Foo('a string here', 100)   # ERROR (Too many arguments for __init__())
b = Foo(100)                    # ok
c = Foo('a string here')        # ok
d = Foo(100, 'a string here')   # ERROR (Too many arguments for __init__())
'''
###############################################
'''
@typechecked
@dataclass
class Foo:
    bar: str
    buzz: int = field(default=0, repr=False)


print(Foo('a string here', 100))   # Foo(bar='a string here')
print(Foo(100))                    # Foo(bar=100)
print(Foo('a string here'))        # Foo(bar='a string here')
print(Foo(100, 'a string here'))   # Foo(bar=100)
# i.e., buzz is not included in the repr() of the object
'''
###############################################
'''
@typechecked
@dataclass
class Foo:
    bar: str
    buzz: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        # watch out because here we do not have dataclass_type_validator(self)

    @staticmethod
    def create(bar: str, buzz: int) -> 'Foo':
        return Foo(bar, buzz, Foo.__create_key)


print(Foo.create('a string here', 100))   # ok
Foo('a string here', 100)   # ERROR (Missing positional argument 'create_key')
Foo(100)                    # ERROR (Missing positional argument 'buzz' and 'create_key')
Foo('a string here')        # ERROR (Missing positional argument 'buzz' and 'create_key')
Foo(100, 'a string here')   # ERROR (Missing positional argument 'create_key')
'''
###############################################
'''
@typechecked
@dataclass(frozen=True, order=True)
class Foo:
    bar: str
    buzz: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, equals=self.__create_key)
        # watch out because here we do not have dataclass_type_validator(self)

    @staticmethod
    def create(bar: str, buzz: int) -> 'Foo':
        return Foo(bar, buzz, Foo.__create_key)

    def append_to_bar(self, suffix: str) -> 'Foo':
        self.bar += suffix


obj = Foo.create('a string here', 100)
obj.append_to_bar(' and more')  # ERROR (cannot assign to field 'bar')
obj.bar = 'another string'      # ERROR (cannot assign to field 'bar')
obj.buzz = 200                  # ERROR (cannot assign to field 'buzz')
'''
###############################################
'''
@typechecked
@dataclass(order=True)
class Foo:
    __bar: float

    def __post_init__(self):
        dataclass_type_validator(self)


obj = Foo(1.0)
print(obj)  # Foo(__bar=1.0)
obj._Foo__bar = 2.0
print(obj)  # Foo(__bar=2.0)
'''
###############################################
'''
@typechecked
def do_something(value: int) -> int:
    return value


print(do_something(2))  # ok
print(type(do_something(True)))  # ok and returns True, hence type is <class 'bool'> lol
'''
