# -*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, type_, size, character):
        self.name = name
        self.type = type_
        self.size = size
        self.character = character

    @property
    def is_ferocious(self):
        return self.size != '小' and self.type == '食肉' and self.character == '凶猛'

    def __str__(self):
        return (f"<{self.__class__.__name__}, {self.name}, {self.size}, {self.character}"
                f"{'(凶猛动物)' if self.is_ferocious else ''}>")

    __repr__ = __str__


class Cat(Animal):
    sounds = "~~"

    def __init__(self, name, type_, size, character):
        super().__init__(name, type_, size, character)
        self.as_pet = True


class Zoo:
    def __init__(self, name):
        self.name = name
        self.__animals = set()

    def add_animal(self, animal):
        if animal not in self.__animals:
            self.__animals.add(animal)
            return True
        return False

    def __getattr__(self, item):
        return any(i.__class__.__name__ == item for i in self.__animals)


if __name__ == '__main__':
    try:
        Animal('未知物种', '杂食', '大', '凶猛')
    except TypeError as e:
        print(f"实例化 Animal 类出错: {e}")

    z = Zoo('时间动物园')
    cats = (
        Cat('短毛猫', '食肉', '小', '温顺'),
        Cat('短毛猫', '食肉', '小', '凶猛'),
        Cat('加菲猫', '食肉', '中', '温顺'),
        Cat('加菲猫', '食肉', '中', '凶猛'),
        Cat('波斯猫', '食肉', '大', '温顺'),
        Cat('波斯猫', '食肉', '大', '凶猛'),
        Cat('波斯猫', '杂食', '大', '凶猛'),
    )

    print(f"动物园是否有猫这种动物: {getattr(z, 'Cat')}")
    print(f"动物园是否有狗这种动物: {getattr(z, 'Dog')}")
    print("\n现在往动物园里添加动物：")
    for cat in cats:
        has_add = z.add_animal(cat)
        print(f"添加 {cat}: {'成功' if has_add else '失败'}")

    print("\n现在往动物园里重复添加动物：")
    for cat in cats:
        has_add = z.add_animal(cat)
        print(f"添加 {cat}: {'成功' if has_add else '失败'}")

    print(f"\n动物园是否有猫这种动物: {getattr(z, 'Cat')}")
    print(f"动物园是否有狗这种动物: {getattr(z, 'Dog')}")