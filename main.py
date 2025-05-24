from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.clock import Clock
import math

class CubeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.cube_points = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        self.cube_edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        Clock.schedule_interval(self.update, 1/30)

    def project(self, point, scale, offset_x, offset_y):
        x, y, z = point
        projected_x = (x * scale / (z + 3)) + offset_x
        projected_y = (y * scale / (z + 3)) + offset_y
        return projected_x, projected_y

    def rotate_x(self, point, angle):
        x, y, z = point
        new_y = y * math.cos(angle) - z * math.sin(angle)
        new_z = y * math.sin(angle) + z * math.cos(angle)
        return x, new_y, new_z

    def rotate_y(self, point, angle):
        x, y, z = point
        new_x = x * math.cos(angle) + z * math.sin(angle)
        new_z = -x * math.sin(angle) + z * math.cos(angle)
        return new_x, y, new_z

    def rotate_z(self, point, angle):
        x, y, z = point
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = x * math.sin(angle) + y * math.cos(angle)
        return new_x, new_y, z

    def update(self, dt):
        self.canvas.clear()
        rotated_points = []
        for point in self.cube_points:
            rotated = self.rotate_x(point, self.angle_x)
            rotated = self.rotate_y(rotated, self.angle_y)
            rotated = self.rotate_z(rotated, self.angle_z)
            rotated_points.append(rotated)

        projected_points = [
            self.project(point, 100, self.width / 2, self.height / 2) for point in rotated_points
        ]

        with self.canvas:
            Color(1, 1, 1)
            for edge in self.cube_edges:
                start_point = projected_points[edge[0]]
                end_point = projected_points[edge[1]]
                Line(points=[start_point[0], start_point[1], end_point[0], end_point[1]])

        self.angle_x += 0.02
        self.angle_y += 0.02
        self.angle_z += 0.02

class CubeApp(App):
    def build(self):
        return CubeWidget()

if __name__ == '__main__':
    CubeApp().run()