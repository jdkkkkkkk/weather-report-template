# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:49:06 2024

@author: Dell
"""


from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,QGraphicsOpacityEffect, QDialog,
                             QLineEdit, QDialogButtonBox,
                             QMenu, QWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QFont, QColor, QIcon, QBrush
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer
from globl import *

class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        clickable_label_font = QFont("Microsoft YaHei", 18, QFont.Weight.Bold)
        self.parent = parent
        self.setFont(clickable_label_font) 
        self.setStyleSheet("color: black; background: transparent;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("city is 南京") 
            if self.parent.new_page is None:
                self.parent.new_page = NewPage(self.parent)
            self.parent.new_page.show()
            self.parent.hide()
            


class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初始化透明效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)  # 默认完全不透明

        # 初始化动画
        self.hover_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hover_animation.setDuration(300)  # 悬停动画持续时间（毫秒）

        self.click_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.click_animation.setDuration(150)  # 点击动画持续时间（毫秒）

    def enterEvent(self, event):
        """鼠标悬停时，开始变为半透明"""
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self.opacity_effect.opacity())
        self.hover_animation.setEndValue(0.7)  # 半透明
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时，恢复为完全不透明"""
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self.opacity_effect.opacity())
        self.hover_animation.setEndValue(1.0)  # 完全不透明
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """点击按钮时，按钮变亮"""
        self.click_animation.stop()
        self.click_animation.setStartValue(self.opacity_effect.opacity())
        self.click_animation.setEndValue(0.3)  # 更亮
        self.click_animation.finished.connect(self.restore_opacity)  # 动画结束后恢复
        self.click_animation.start()
        super().mousePressEvent(event)

    def restore_opacity(self):
        """恢复按钮为默认透明度"""
        self.click_animation.stop()
        self.click_animation.setStartValue(self.opacity_effect.opacity())
        self.click_animation.setEndValue(1.0)  # 恢复为完全不透明
        self.click_animation.start()


            
class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("test")
        self.setGeometry(100, 100, 350, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)   #CANNOT maximize the window
        self.setFixedSize(350, 600)    #CANNOT resize the window
        self.new_page = None
        
        self.base_label = QLabel(self)    #base picture
        self.base_label.setGeometry(0, 0, 350, 600)   #base size
        
        self.source_pixmap = QPixmap(BG_IMG_PATH)
        self.base_pixmap = self.source_pixmap.copy(450, 100, 350, 600)
        self.base_pixmap = self.base_pixmap.scaled(350, 600, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.result_pixmap = QPixmap(self.base_pixmap.size())
        self.result_pixmap.fill(Qt.GlobalColor.transparent)
        self.painter = QPainter(self.result_pixmap)
        self.painter.drawPixmap(0, 0, self.base_pixmap)
        self.painter.setOpacity(1)
        
        self.cur_city_name = GET_CURRENT_CITY_NAME()
        self.city_name = ClickableLabel(self.cur_city_name, self)
        self.city_name.setGeometry(70, 50, 200, 50)  # 设置标签位置和大小
        
        gps_pixmap = QPixmap(GPS_IMG_PATH)
        gps_pixmap = gps_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(202, 62, gps_pixmap) 
         
        menu_btn = self.create_btn(300, 20, 25, 25, "menu.png")
        menu_btn.clicked.connect(self.open_new_page)
        
        
        #----------draw blocks----------
        self.color = QColor(50, 50, 50, 80)
        self.rects = [
            self.rect().adjusted(20, 290, -25, -210).toRectF(),
            self.rect().adjusted(20, 400, -25, -155).toRectF(),
            self.rect().adjusted(20, 570, -25, -145).toRectF(),
            ]
        for rect in self.rects:
            self.painter.setBrush(self.color)
            self.painter.setPen(Qt.PenStyle.NoPen)
            path = QPainterPath()
            path.addRoundedRect(rect, 15, 15)
            self.painter.drawPath(path)
        #-------------------------------
    
        
        #----------temperature now----------
        cur_temperature = GET_CURRENT_TEMPERATURE(self.cur_city_name)
        
        now_temperature_label = QLabel(cur_temperature, self)
        now_temperature_label.setGeometry(120, 10, 300, 300) 
        now_temperature_font = QFont("Microsoft YaHei", 100, QFont.Weight.Thin)
        now_temperature_label.setStyleSheet("background: transparent; color: black; font-size: 100px;")
        now_temperature_label.setFont(now_temperature_font)
        now_temperature_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-----------------------------------
        
        
        #----------celsius symbol----------
        celsius = QLabel("°C", self)
        celsius.setGeometry(235, -20, 300, 300)
        celsius_font = QFont("Microsoft YaHei", QFont.Weight.Normal)
        celsius.setStyleSheet("background: transparent; color: black; font-size: 20px;")
        celsius.setFont(celsius_font)
        celsius.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #----------------------------------
        
        
        #----------weather now----------
        cur_weather = GET_CURRENT_WEATHER(self.cur_city_name)
        
        now_weather = QLabel(cur_weather, self)
        now_weather.setGeometry(170, 80, 300, 300)
        new_weather_font = QFont("Microsoft YaHei", QFont.Weight.Normal)
        now_weather.setStyleSheet("background: transparent; color: black; font-size: 16px;")
        now_weather.setFont(new_weather_font)
        now_weather.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-------------------------------
        
        
        #----------temperature range today----------
        cur_temperature_range = GET_CURRENT_TEMPERATURE_RANGE(self.cur_city_name)
        
        temperature_range = QLabel(cur_temperature_range, self)
        temperature_range.setGeometry(135, 110, 300, 300)
        temperature_range_font = QFont("Microsoft YaHei", QFont.Weight.Light)
        temperature_range.setStyleSheet("background: transparent; color: black; font-size: 20px;")
        temperature_range.setFont(temperature_range_font)
        temperature_range.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-------------------------------------------
        
        
        #----------predict module begins----------
        predict_time = GET_PREDICT_TIME(self.cur_city_name)
        predict_weather = []
        predict_temperature = []
        for i in range(0, 3):
            tmp_weather = GET_PREDICT_WEATHER(self.cur_city_name, predict_time[i])
            tmp_temperature = GET_PREDICT_TEMPERATURE(self.cur_city_name, predict_time[i])
            predict_weather.append(tmp_weather)
            predict_temperature.append(tmp_temperature)
            
        #----------predict information 1----------
        predict_time_1 = QLabel(predict_time[0], self)
        predict_time_1.setGeometry(35, 160, 300, 300)
        predict_time_1_font = QFont("Microsoft YaHei", QFont.Weight.Light)
        predict_time_1.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_time_1.setFont(predict_time_1_font)
        predict_time_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        predict_weather_1_pixmap = QPixmap(predict_weather[0] + ".png")
        predict_weather_1_pixmap = predict_weather_1_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(50, 330, predict_weather_1_pixmap) 
        
        predict_temperature_1 = QLabel(str(predict_temperature[0]) + "°C", self)
        predict_temperature_1.setGeometry(45, 220, 300, 300)
        predict_temperature_1_font = QFont("Microsoft YaHei", 100, QFont.Weight.Black)
        predict_temperature_1.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_temperature_1.setFont(predict_temperature_1_font)
        predict_temperature_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-----------------------------------------
        
        
        
        #----------predict information 2----------
        predict_time_2 = QLabel(predict_time[1], self)
        predict_time_2.setGeometry(150, 160, 300, 300)
        predict_time_2_font = QFont("Microsoft YaHei", QFont.Weight.Light)
        predict_time_2.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_time_2.setFont(predict_time_2_font)
        predict_time_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        predict_weather_2_pixmap = QPixmap(predict_weather[1] + ".png")
        predict_weather_2_pixmap = predict_weather_2_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(165, 330, predict_weather_2_pixmap) 
        
        predict_temperature_2 = QLabel(str(predict_temperature[0]) + "°C", self)
        predict_temperature_2.setGeometry(160, 220, 300, 300)
        predict_temperature_2_font = QFont("Microsoft YaHei", 100, QFont.Weight.Black)
        predict_temperature_2.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_temperature_2.setFont(predict_temperature_2_font)
        predict_temperature_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-----------------------------------------
        
        
        #----------predict information 3----------
        predict_time_3 = QLabel(predict_time[2], self)
        predict_time_3.setGeometry(255, 160, 300, 300)
        predict_time_3_font = QFont("Microsoft YaHei", QFont.Weight.Light)
        predict_time_3.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_time_3.setFont(predict_time_3_font)
        predict_time_3.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        predict_weather_3_pixmap = QPixmap(predict_weather[2] + ".png")
        predict_weather_3_pixmap = predict_weather_3_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(275, 330, predict_weather_3_pixmap) 
        
        predict_temperature_3 = QLabel(str(predict_temperature[0]) + "°C", self)
        predict_temperature_3.setGeometry(270, 220, 300, 300)
        predict_temperature_3_font = QFont("Microsoft YaHei", 100, QFont.Weight.Black)
        predict_temperature_3.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        predict_temperature_3.setFont(predict_temperature_3_font)
        predict_temperature_3.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #-----------------------------------------
        #----------predict module ends----------
        
        
        #----------humidity module begins----------
        _, self.humidity_text = GET_HUMIDITY(self.cur_city_name)
        
        humidity_name = QLabel("湿度", self)
        humidity_name.setGeometry(35, 270, 300, 300)
        humidity_name_font = QFont("Microsoft YaHei", 100, QFont.Weight.Medium)
        humidity_name.setStyleSheet("background: transparent; color: white; font-size: 14px;")
        humidity_name.setFont(humidity_name_font)
        humidity_name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.humidity = QLabel(self.humidity_text, self)
        self.humidity.setGeometry(160, 270, 300, 300)
        self.humidity_font = QFont("幼圆", 100, QFont.Weight.Bold)
        self.humidity.setStyleSheet("background: transparent; color: white; font-size: 14px;")
        self.humidity.setFont(self.humidity_font)
        self.humidity.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        humidity_change_display_mode_btn = self.create_btn(280, 410, 15, 20, "down_arrow.png")
        
        humidity_change_menu = QMenu(self)
        humidity_change_menu.addAction("简略", lambda: self.on_option_selected("简略"))
        humidity_change_menu.addAction("显示详细信息", lambda: self.on_option_selected("显示详细信息"))
        humidity_change_display_mode_btn.setMenu(humidity_change_menu)
        #----------humidity module ends----------
        
        
        #----------dressing guide module begins----------
        dressing_guide = QLabel("生活指数", self)
        dressing_guide.setGeometry(145, 320, 300, 300)
        dressing_guide_font = QFont("幼圆", 100, QFont.Weight.Bold)
        dressing_guide.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        dressing_guide.setFont(dressing_guide_font)
        dressing_guide.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        dressing_guide_content = GET_DRESSING_GUIDE(self.cur_city_name)
        
        #----------part 1----------
        dressing_guide_1_pixmap = QPixmap(dressing_guide_content[0][0] + ".png")
        dressing_guide_1_pixmap = dressing_guide_1_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(45, 495, dressing_guide_1_pixmap)
        
        dressing_guide_1 = QLabel(dressing_guide_content[0][1], self)
        dressing_guide_1.setGeometry(48, 390, 300, 300)
        dressing_guide_1_font = QFont("幼圆", 100, QFont.Weight.Bold)
        dressing_guide_1.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        dressing_guide_1.setFont(dressing_guide_1_font)
        dressing_guide_1.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #----------part 1 ends----------
        
        
        #----------part 2----------
        dressing_guide_2_pixmap = QPixmap(dressing_guide_content[1][0] + ".png")
        dressing_guide_2_pixmap = dressing_guide_2_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(155, 495, dressing_guide_2_pixmap)
        
        dressing_guide_2 = QLabel(dressing_guide_content[1][1], self)
        dressing_guide_2.setGeometry(145, 390, 300, 300)
        dressing_guide_2_font = QFont("幼圆", 100, QFont.Weight.Bold)
        dressing_guide_2.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        dressing_guide_2.setFont(dressing_guide_2_font)
        dressing_guide_2.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #----------part 2 ends----------
        
        
        #----------part 3----------
        dressing_guide_3_pixmap = QPixmap(dressing_guide_content[2][0] + ".png")
        dressing_guide_3_pixmap = dressing_guide_3_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.painter.drawPixmap(260, 495, dressing_guide_3_pixmap)
        
        dressing_guide_3 = QLabel(dressing_guide_content[2][1], self)
        dressing_guide_3.setGeometry(255, 390, 300, 300)
        dressing_guide_3_font = QFont("幼圆", 100, QFont.Weight.Bold)
        dressing_guide_3.setStyleSheet("background: transparent; color: white; font-size: 13px;")
        dressing_guide_3.setFont(dressing_guide_3_font)
        dressing_guide_3.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #----------part 3 ends----------
        #----------dressing guide module ends----------
      
        self.painter.end()
        self.base_label.setPixmap(self.result_pixmap)
        
    
    def create_btn(self, x, y, w, h, path):
        btn = AnimatedButton(self)
        btn.setGeometry(x, y, w, h)
        btn_icon = QIcon(QPixmap(path))
        btn.setIcon(btn_icon)
        btn.setIconSize(QSize(w, h))
        btn.setStyleSheet(BTN_STYLE_SHEET)
        return btn
        
        
    def on_option_selected(self, option):
        if option == "简略":   
            _, tmp_humidity_text = GET_HUMIDITY(self.cur_city_name)
        elif option == "显示详细信息":
            tmp_humidity_text, _ = GET_HUMIDITY(self.cur_city_name)
            tmp_humidity_text = str(tmp_humidity_text*100) + "%"
        self.humidity.setText(tmp_humidity_text)
        
        
    def open_new_page(self):
        if self.new_page is None:
            self.new_page = NewPage(self)
        self.new_page.show()
        self.hide()



class NewPage(QWidget):
    def __init__(self, main_page):
        super().__init__()
        self.main_page = main_page  # 保存主页面的引用
        self.setWindowTitle("test2")
        self.setGeometry(100, 100, 350, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)   #CANNOT maximize the window
        self.setFixedSize(350, 600)    #CANNOT resize the window
        
        return_btn = self.create_btn(20, 20, 25, 25, "return.png")
        return_btn.clicked.connect(self.closeEvent)
        
        add_btn = self.create_btn(300, 20, 25, 25, "add.png")
        add_btn.clicked.connect(self.show_dialog)
        self.buttons = []
        self.button_positions = []
        self.dropdowns = []
        self.city = GET_CITY_NAME()
        self.show_dropdown()


    def show_dropdown(self):
        for i in range(0, len(self.city)):
            self.button_positions.append((0, 60 + 45*i))

        # 创建按钮和对应的下拉框
        for i, pos in enumerate(self.button_positions):
            # 创建按钮
            city_name = f"{self.city[i]}"
            if i == 0:
                city_name += "（您的位置）"
            button = QPushButton(city_name, self)
            button.setGeometry(pos[0], pos[1], 350, 40)
            button.clicked.connect(lambda checked, b=button, idx=i: self.toggle_dropdown(b, idx))
            self.buttons.append(button)
            button.show()
            
            # 创建对应的下拉框
            dropdown = self.create_dropdown(i)
            dropdown.setVisible(False)  # 默认隐藏
            self.dropdowns.append(dropdown)
        
        
    def clear_dropdown(self):
        for _button in self.buttons:
            _button.deleteLater()
        for _dropdown in self.dropdowns:
            _dropdown.deleteLater()
        self.buttons.clear()
        self.button_positions.clear()
        self.dropdowns.clear()


    def renew_dropdown(self):
        self.clear_dropdown()
        self.city = GET_CITY_NAME()
        self.show_dropdown()


    def show_dialog(self):
        """
        显示输入对话框
        """
        dialog = MyDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.city_add(dialog.get_text())

    def show_prompt(self, message, text_pos):
        """显示提示框"""
        prompt = Prompt(self, message, text_pos)  # 自定义文字位置
        prompt.move(self.width() // 2 - prompt.width() // 2, 20)  # 提示框居中显示在顶部
        prompt.show()

    def city_add(self, new_name):
        if IS_REPUSH_CITY(new_name):
            self.show_prompt("当前城市已经存在", (60, 15))
            return
        ADD_CITY(new_name)
        CHECK_CITY()
        self.renew_dropdown()

    
    def city_delete(self, idx):
        print(f"number {idx} into NewPage.city_delete()", flush=True)
        if idx == 0:
            self.show_prompt("当前城市不可删除", (60, 15))
            return
        DEL_CITY(self.city[idx])
        CHECK_CITY()
        self.renew_dropdown()
        print(f"number {idx} out NewPage.city_delete()", flush=True)
        

    def city_to_top(self, idx):
        if idx == 0:
            return
        TOP_CITY(idx)
        CHECK_CITY()
        self.renew_dropdown()


    def city_to_bottom(self, idx):
        if idx == 0:
            self.show_prompt("当前城市不可置底", (60, 15))
            return
        BOTTOM_CITY(idx)
        CHECK_CITY()
        self.renew_dropdown()


    def create_dropdown(self, idx):
        # 创建自定义按钮
        top_btn = self.dropdown_btn(35, 35, "to_top.png")
        dustbin_btn = self.dropdown_btn(35, 35, "dustbin.png")
        bottom_btn = self.dropdown_btn(35, 35, "to_bottom.png")
        
        top_btn.clicked.connect(lambda: self.city_to_top(idx))
        dustbin_btn.clicked.connect(lambda: self.city_delete(idx))
        bottom_btn.clicked.connect(lambda: self.city_to_bottom(idx))
        
        # 创建一个水平布局，将按钮添加到布局中
        layout = QHBoxLayout()
        layout.addWidget(top_btn)
        layout.addWidget(dustbin_btn)
        layout.addWidget(bottom_btn)
        layout.setSpacing(25)  # 按钮间距
        layout.setContentsMargins(3, 3, 3, 3)  # 布局边距

        # 创建一个 QWidget 并设置布局
        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setMinimumSize(350, 45)
        return widget


    def toggle_dropdown(self, button, idx):
        """展开或收起下拉框并动态调整下方组件位置"""
        dropdown = self.dropdowns[idx]

        # 获取下拉框的高度，用于调整下方组件位置
        dropdown_height = dropdown.sizeHint().height()
        if dropdown_height == 0:  # 防止为0时不可见
            dropdown_height = 50

        if dropdown.isVisible():
            # 如果下拉框可见，则隐藏并将下方组件向上移动
            dropdown.setVisible(False)
            self.move_components(idx + 1, -dropdown_height)
        else:
            # 如果下拉框隐藏，则显示并将下方组件向下移动
            dropdown.setVisible(True)
            # 将下拉框移动到按钮下方
            button_pos = button.mapToGlobal(QPoint(0, 0))
            dropdown_pos = self.mapFromGlobal(QPoint(button_pos.x(), button_pos.y() + button.height()))
            dropdown.move(dropdown_pos)
            self.move_components(idx + 1, dropdown_height)


    def move_components(self, start_idx, offset):
        """移动下方组件"""
        for i in range(start_idx, len(self.buttons)):
            # 获取当前按钮的位置
            button = self.buttons[i]
            dropdown = self.dropdowns[i]

            # 移动按钮和对应的下拉框
            button.move(button.x(), button.y() + offset)
            dropdown.move(dropdown.x(), dropdown.y() + offset)


    def create_btn(self, x, y, w, h, path):
        btn = AnimatedButton(self)
        btn.setGeometry(x, y, w, h)
        btn_icon = QIcon(QPixmap(path))
        btn.setIcon(btn_icon)
        btn.setIconSize(QSize(w, h))
        btn.setStyleSheet(BTN_STYLE_SHEET)
        return btn

    
    def dropdown_btn(self, w, h, path):
        btn = AnimatedButton(self)
        btn_icon = QIcon(QPixmap(path))
        btn.setIcon(btn_icon)
        btn.setIconSize(QSize(w, h))
        btn.setStyleSheet(BTN_STYLE_SHEET)
        return btn
    
    
    def closeEvent(self, event):
        self.close()
        self.main_page.show()



class Prompt(QWidget):
    """自定义提示框，带图片和可自定义位置的文字"""
    def __init__(self, parent=None, message="", text_pos=(10, 30)):
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
        self.image_label.setPixmap(QPixmap("attention.png"))
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



class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输入文本")
        layout = QVBoxLayout()

        self.label = QLabel("请输入文本：")
        layout.addWidget(self.label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_text(self):
        return self.text_input.text()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())