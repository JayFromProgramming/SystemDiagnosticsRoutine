

class TopicTracker:

    def __init__(self, node, topic_name, topic_type, is_listener=False, is_publisher=False):
        self.node = node
        self.topic_name = topic_name
        self.topic_type = topic_type

        self._value = None

        self.is_listener = is_listener
        self.is_publisher = is_publisher

        self.subscriber = None
        self.publisher = None

        if self.is_listener:
            self.subscriber = self.node.create_subscription(
                self.topic_type,
                self.topic_name,
                self.listener_callback,
                10)
            self.node.get_logger().info('Subscribed to topic: ' + self.topic_name)

        if self.is_publisher:
            self.publisher = self.node.create_publisher(
                self.topic_type,
                self.topic_name,
                10)
            self.node.get_logger().info('Publishing to topic: ' + self.topic_name)

    def listener_callback(self, msg):
        # self.node.get_logger().info('Received: ' + str(msg.data))
        self._value = msg.data

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, msg):
        if self.is_publisher:
            self.publisher.publish(msg)
            self.node.get_logger().info('Publishing: ' + str(msg.data))
        else:
            self.node.get_logger().info('Not a publisher, cannot publish: ' + str(msg.data))
            raise Exception('Not a publisher, cannot publish: ' + str(msg.data))
