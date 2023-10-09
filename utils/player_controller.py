import argparse
import logging
import native_rpc as rpc
import subprocess

ns = rpc.Namespace('player')

'''
    remote class of simple player
'''
@ns.remote_class()
class player_controller:
    def __init__(self, player_path):
        self._player_path = player_path
        self._player = None

    def __del__(self):
        if self._player is not None:
            self._player.kill()
            self._player.wait()
            self._player = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def play(self, video_path):
        print(video_path)
        self._player = subprocess.Popen(f'{self._player_path} {video_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--log', default='INFO')
    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.log))

    server = rpc.Server()
    server.add_namespace(ns)
    server.register_deserializer(rpc.PickleDeserializer())
    server.serializer = rpc.PickleSerializer()
    server.run(host=args.host, port=args.port)
