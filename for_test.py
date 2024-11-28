'''import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QColor, QPainter, QBrush, QPixmap


class Prompt(QWidget):
    """自定义提示框，带图片和可自定义位置的文字"""
    def __init__(self, parent=None, message="", image_path="", text_pos=(10, 30)):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(200, 50)

        # 设置提示框文本
        self.label = QLabel(message, self)
        self.label.setStyleSheet("color: white; font-size: 13px;")
        self.label.adjustSize()  # 根据内容调整大小
        self.label.move(*text_pos)  # 文字相对于提示框左上角的位置

        # 设置图片
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap(image_path))
        self.image_label.setFixedSize(20, 20)
        self.image_label.move(15, 15)  # 图片固定在提示框的左上角偏移10像素

        # 不透明度效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        # 定时器触发淡出
        QTimer.singleShot(1000, self.start_fade_out)

    def paintEvent(self, event):
        """绘制圆角矩形背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0, 200)))  # 半透明黑色背景
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)

    def start_fade_out(self):
        """启动淡出动画"""
        animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        animation.setDuration(1000)  # 1秒淡出
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.finished.connect(self.close)  # 动画结束后关闭窗口
        animation.start()

        # 保存动画对象，避免被垃圾回收
        self.animation = animation


class MainWindow(QWidget):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("提示信息示例")
        self.setGeometry(100, 100, 350, 600)

        # 显示提示信息
        self.show_prompt("这是一个提示信息", "attention.png", (60, 15))

    def show_prompt(self, message, image_path, text_pos):
        """显示提示框"""
        prompt = Prompt(self, message, image_path, text_pos)  # 自定义文字位置
        prompt.move(self.width() // 2 - prompt.width() // 2, 20)  # 提示框居中显示在顶部
        prompt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口
    main_window = MainWindow()
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec())'''
    
    
    
def string_in_file(file_path, search_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件的全部内容
            return search_string in content  # 检查目标字符串是否在内容中
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return False

# 使用示例
file_path = "city_name.txt"
search_string = "南京"
if string_in_file(file_path, search_string):
    print(f"'{search_string}' 存在于文件中")
else:
    print(f"'{search_string}' 不存在于文件中")
