import native_rpc_client as rpc_client
import time

class _player_controller_template:
    def __init__(self):
        pass
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @rpc_client.remote_method()
    def play(self, video_path):
        pass

def remote_player_controller(base_url):
    c = rpc_client.Client(base_url)

    c.register_deserializer(rpc_client.PickleDeserializer())
    c.serializer = rpc_client.PickleSerializer()

    ns = c.namespace('player')

    return ns.remote_class(_player_controller_template, 'player_controller')


if __name__ == "__main__":
    player_controller = remote_player_controller('http://localhost:5000')
    myplayer = player_controller('')
    myplayer.play(video_path='E:/projector/Code/utils/data/patterns_video.mp4')
    time.sleep(3)