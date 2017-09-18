
class Quadtree:

    """
    x = radius · longitude · cosine (latitude)
    y = radius · latitude

    """
    def __init__(self, bounding_box, bucket_size, max_depth):
        self.nodes = list()
