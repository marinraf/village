# this is a class with a lot of fake properties

class Fake:
    def __init__(self):
        self.name = 'fake'
        self.cam = None

    def start_camera(self):
        pass
    def stop_preview(self):
        pass
    def start_record(self):
        pass
    def stop_record(self):
        pass
    def stop(self):
        pass  
    def change_focus(self, lensposition):
        pass
    def change_framerate(self, framerate):
        pass
    def print_info_about_config(self):
        pass
    def apply_timestamp(self, request):
        pass
    
    