import pika

# 链接到RabbitMQ服务器器
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672, '/',credentials))

# 创建频道
channel = connection.channel()

# 声明消息队列列
channel.queue_declare(queue='desk')

# routing_key是队列列名 body是要插⼊入的内容
channel.basic_publish(exchange='', routing_key='desk', body=b'Hello RabbitMQ!')
print("开始向 'desk' 队列列中发布消息 '汉堡做好啦!'")

# 关闭链接
connection.close()
