import cv2
import numpy as np
import time
from Controllers.realsense_camera import RealSenseCamera
from Controllers.face_controller import FaceController

class DistancesFilter:
    def __init__(self, depth_interval=0.08):
        self.camera = RealSenseCamera()
        self.face = FaceController()
        self.depth_interval = depth_interval
        self.last_depth_time = 0
        self.last_best = None
        self.last_mask = None

    def find_smallest_distance(self, depth_frame, tolerance=0.01):
        depth = np.asanyarray(depth_frame.get_data())
        if depth.dtype != np.float32:
            depth = depth.astype(np.float32)
        depth = depth / 1000.0

        valid_mask = (depth > 0.15)
        if not np.any(valid_mask):
            return None, np.zeros_like(depth, dtype=np.uint8)

        min_dist = np.min(depth[valid_mask])
        min_mask = (depth == min_dist) & valid_mask
        coords = np.column_stack(np.where(min_mask))
        h, w = depth.shape
        center = np.array([h // 2, w // 2])
        dists_to_center = np.linalg.norm(coords - center, axis=1)
        idx = np.argmin(dists_to_center)
        y0, x0 = coords[idx]
        d0 = float(depth[y0, x0])

        grown_mask = np.zeros_like(depth, dtype=bool)
        to_visit = [(y0, x0)]
        grown_mask[y0, x0] = True

        while to_visit:
            y, x = to_visit.pop()
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and not grown_mask[ny, nx] and valid_mask[ny, nx]:
                        if abs(depth[ny, nx] - d0) <= tolerance:
                            grown_mask[ny, nx] = True
                            to_visit.append((ny, nx))

        region_coords = np.column_stack(np.where(grown_mask))

        if len(region_coords) == 0:
            return (int(x0), int(y0), d0), (grown_mask.astype(np.uint8) * 255)
        
        centroid = np.mean(region_coords, axis=0)
        cy, cx = centroid
        avg_dist = np.mean(depth[grown_mask])
        mask = np.zeros_like(depth, dtype=np.uint8)
        mask[grown_mask] = 255

        return (int(round(cx)), int(round(cy)), float(avg_dist)), mask

    def run(self):
        self.face.turn_part("ON", "EYES")
        
        while True:
            color_frame = self.camera.get_color_frame()
            depth_frame = self.camera.get_depth_frame()

            if color_frame is None or depth_frame is None:
                continue

            color_image = color_frame
            now = time.time()

            if now - self.last_depth_time >= self.depth_interval:
                best, mask = self.find_smallest_distance(depth_frame)
                self.last_best = best
                self.last_mask = mask
                self.last_depth_time = now
            else:
                best = self.last_best
                mask = self.last_mask if self.last_mask is not None else np.zeros_like(color_image[:,:,0], dtype=np.uint8)

            if best is not None:
                x, y, d = best
                d = self.camera.get_distance((x, y))
                eyes_point = self.camera.get_eyes_point([float(x), float(y), float(d), 1])
                cv2.circle(color_image, (x, y), 7, (0, 255, 0), -1)
                text = f"x={eyes_point[0]:.2f}, y={eyes_point[1]:.2f}, d={eyes_point[2]:.2f}"
                cv2.putText(color_image, text, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                self.face.look_at(eyes_point)

            cv2.imshow("Distances Filter", color_image)
            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.face.close_connection()
        self.camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    filter = DistancesFilter()
    filter.run()
