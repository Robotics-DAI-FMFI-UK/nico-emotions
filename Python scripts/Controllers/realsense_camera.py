import pyrealsense2 as rs
import numpy as np
from Controllers.config import CAMERA_DIMENSIONS, MAXIMUM_STORED_DEPTH_DISTANCES, RGB_CAMERA_FPS, DEPTH_CAMERA_FPS, DEPTH_CAMERA_KERNEL_SIZE

class RealSenseCamera:
    def __init__(self):
        self.dimensions = CAMERA_DIMENSIONS
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, self.dimensions[0], self.dimensions[1], rs.format.bgr8, RGB_CAMERA_FPS)
        self.config.enable_stream(rs.stream.depth, self.dimensions[0], self.dimensions[1], rs.format.z16, DEPTH_CAMERA_FPS)
        self.align = rs.align(rs.stream.color)
                
        self.filters = [
            rs.hole_filling_filter(2),
            # rs.hdr_merge(),
            # rs.threshold_filter(),
            # rs.disparity_transform(True),
            # rs.spatial_filter(),
            # rs.temporal_filter(),
            # rs.disparity_transform(False)
        ]

        self.pipeline.start(self.config)

        self.MAXIMUM_STORED_DISTANCES = MAXIMUM_STORED_DEPTH_DISTANCES
        self.distances = []

    def get_dimensions(self):
        return self.dimensions

    def get_aligned_frames(self):
        frames = self.pipeline.wait_for_frames()
        return self.align.process(frames)

    def get_color_frame(self):
        aligned_frames = self.get_aligned_frames()
        color_frame = aligned_frames.get_color_frame()

        if not color_frame:
            return None
        
        return np.asanyarray(color_frame.get_data())

    def get_depth_frame(self):
        aligned_frames = self.get_aligned_frames()
        depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame:
            return None
        
        for filter in self.filters:
            depth_frame = filter.process(depth_frame)

        return depth_frame
    
    def get_average_depth_point(self, depth_frame, point, kernel_size=DEPTH_CAMERA_KERNEL_SIZE):
        if depth_frame is None:
            return None

        half_k = kernel_size // 2
        x, y = point
        values = []

        for dx in range(-half_k, half_k + 1):
            for dy in range(-half_k, half_k + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.dimensions[0] and 0 <= ny < self.dimensions[1]:
                    d = depth_frame.as_depth_frame().get_distance(nx, ny)
                    if d > 0:
                        values.append(d)

        if not values:
            return 0.15
        return np.mean(values)

    def get_distance(self, point):
        depth_frame = self.get_depth_frame()
        distance = self.get_average_depth_point(depth_frame, point)
        if distance is None:
            return 150

        distance *= 1000
        distance = round(max(150, min(2000, distance)), 2)

        self.distances.append(distance)
        if self.MAXIMUM_STORED_DISTANCES < len(self.distances):
            self.distances.pop(0)

        return int(min(sum(self.distances) / len(self.distances), 2000))
    
    def stop(self):
        self.pipeline.stop()

    def get_eyes_point(self, point):
        x, y, distance, _ = point
        frame_width, frame_height = self.get_dimensions()
        center_x = int(x) - frame_width // 2
        center_y = frame_height // 2 - int(y)

        return [center_x, center_y, int(distance), 1]

