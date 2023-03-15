from django.db import models


class BaseModel(models.Model):
    # auto_now
    # 这个参数的默认值为false，设置为true时，能够在保存该字段时，将其值设置为当前时间，并且每次修改model，都会自动更新。
    # 因此这个参数在需要存储“最后修改时间”的场景下，十分方便
    # 需要注意的是，设置该参数为true时，并不简单地意味着字段的默认值为当前时间，而是指字段会被“强制”更新到当前时间，你无法从程序中手动为字段赋值
    # 如果使用django再带的admin管理器，那么该字段在admin中是只读的

    # auto_now_add
    # 这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新
    # 该属性通常被用在存储“创建时间”的场景下。与auto_now类似，auto_now_add也具有强制性，一旦被设置为True，就无法在程序中手动为字段赋值，
    # 在admin中字段也会成为只读的

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        # 这个属性说明是抽象类模型 用于继承使用 迁移时不会创建该表
        abstract = True
