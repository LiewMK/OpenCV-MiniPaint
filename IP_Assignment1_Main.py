import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QLabel, QPushButton, \
    QFileDialog, QMessageBox, QMenu, QDesktopWidget, QGroupBox, QFormLayout, QLineEdit, QComboBox, \
    QDialogButtonBox, QVBoxLayout, QDialog
from PyQt5.QtGui import QImage, QBrush, QIcon, QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import QSize, Qt


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.title = 'Mini Paint'
        self.win_x = 350
        self.win_y = 80
        self.width = 1200
        self.height = 820
        self.zoom = 1
        self.x_pos = 0
        self.y_pos = 0
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.pixel = 1
        self.font_scale = 1
        self.select_color_x = 675
        self.select_color_y = 32
        self.color = (0, 0, 0)
        self.font_style = cv2.FONT_HERSHEY_COMPLEX
        self.converted = False
        self.draw_rect = False
        self.draw_elli = False
        self.draw_tri = False
        self.draw_l = False
        self.put_t = False
        self.flag = False
        self.crop = False

        self.label = QLabel(self)
        self.about_window = AboutWindow()

        self.ui_components()

    def ui_components(self):
        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))
        self.menu_bar()
        self.tools_bar()
        self.disable_action()
        self.backup_image()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def menu_bar(self):
        self.menu_file = self.menuBar().addMenu('File')
        self.menu_image = self.menuBar().addMenu('Image')
        self.menu_help = self.menuBar().addMenu('Help')

        self.action_open = QAction('Open', self)
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.triggered.connect(self.browse_image)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()

        self.action_save = QAction('Save', self)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.triggered.connect(self.save_image)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addSeparator()

        self.action_exit = QAction('Exit', self)
        self.action_exit.triggered.connect(app.quit)
        self.menu_file.addAction(self.action_exit)

        self.action_zoom_in = QAction('Zoom In', self)
        self.action_zoom_in.setShortcut('Ctrl++')
        self.action_zoom_in.triggered.connect(self.zoom_in)
        self.menu_image.addAction(self.action_zoom_in)
        self.menu_image.addSeparator()

        self.action_zoom_out = QAction('Zoom Out', self)
        self.action_zoom_out.setShortcut('Ctrl+-')
        self.action_zoom_out.triggered.connect(self.zoom_out)
        self.menu_image.addAction(self.action_zoom_out)
        self.menu_image.addSeparator()

        self.action_convert_to = self.menu_image.addMenu('Convert To')
        self.menu_image.addSeparator()

        self.action_original = QAction('Original', self)
        self.action_convert_to.addAction(self.action_original)
        self.action_original.triggered.connect(self.convert_to_original)
        self.action_gray = QAction('Gray', self)
        self.action_convert_to.addAction(self.action_gray)
        self.action_gray.triggered.connect(self.convert_to_gray)
        self.action_HSV = QAction('HSV', self)
        self.action_convert_to.addAction(self.action_HSV)
        self.action_HSV.triggered.connect(self.convert_to_hsv)
        self.action_HLS = QAction('HLS', self)
        self.action_convert_to.addAction(self.action_HLS)
        self.action_HLS.triggered.connect(self.convert_to_hls)
        self.action_LAB = QAction('LAB', self)
        self.action_convert_to.addAction(self.action_LAB)
        self.action_LAB.triggered.connect(self.convert_to_lab)
        self.action_LUV = QAction('LUV', self)
        self.action_convert_to.addAction(self.action_LUV)
        self.action_LUV.triggered.connect(self.convert_to_luv)
        self.action_YUV = QAction('YUV', self)
        self.action_convert_to.addAction(self.action_YUV)
        self.action_YUV.triggered.connect(self.convert_to_yuv)

        self.action_about = QAction('About', self)
        self.action_about.triggered.connect(self.open_about_window)
        self.menu_help.addAction(self.action_about)

    def tools_bar(self):
        self.button_image_details = QPushButton('', self)
        self.button_image_details.move(10, 33)
        self.button_image_details.resize(55, 55)
        self.button_image_details.setIcon(QIcon(r'pic\icon\icon_image_details.png'))
        self.button_image_details.setIconSize(QSize(30, 30))
        self.button_image_details.setToolTip('Image Details')
        self.button_image_details.clicked.connect(self.show_image_details)

        self.button_rotate = QPushButton('', self)
        self.button_rotate.move(75, 33)
        self.button_rotate.resize(55, 55)
        self.button_rotate.setIcon(QIcon(r'pic\icon\icon_rotate.png'))
        self.button_rotate.setIconSize(QSize(30, 30))
        self.button_rotate.setToolTip('Rotate')
        self.rotate = QMenu(self)
        self.rtt_right = QAction('Rotate Right 90°', self)
        self.rtt_right.triggered.connect(self.rotate_right)
        self.rtt_right.setShortcut('R')
        self.rotate.addAction(self.rtt_right)
        self.rotate.addSeparator()
        self.rtt_left = QAction('Rotate Left 90°', self)
        self.rtt_left.triggered.connect(self.rotate_left)
        self.rtt_left.setShortcut('shift+R')
        self.rotate.addAction(self.rtt_left)
        self.button_rotate.setMenu(self.rotate)

        self.button_flip = QPushButton('', self)
        self.button_flip.move(140, 33)
        self.button_flip.resize(55, 55)
        self.button_flip.setIcon(QIcon(r'pic\icon\icon_flip.png'))
        self.button_flip.setIconSize(QSize(30, 30))
        self.button_flip.setToolTip('Flip')
        self.flip = QMenu(self)
        self.flip_v = QAction('Flip Vertical', self)
        self.flip_v.triggered.connect(self.flip_image_vertical)
        self.flip_v.setShortcut('F')
        self.flip.addAction(self.flip_v)
        self.flip.addSeparator()
        self.flip_h = QAction('Flip Horizontal°', self)
        self.flip_h.triggered.connect(self.flip_image_horizontal)
        self.flip.addAction(self.flip_h)
        self.flip_h.setShortcut('shift+F')
        self.button_flip.setMenu(self.flip)

        self.button_crop = QPushButton('', self)
        self.button_crop.move(205, 33)
        self.button_crop.resize(55, 55)
        self.button_crop.setIcon(QIcon(r'pic\icon\icon_crop.png'))
        self.button_crop.setIconSize(QSize(30, 30))
        self.button_crop.setToolTip('Crop')
        self.button_crop.clicked.connect(self.crop_image_action)
        self.button_crop.setShortcut('C')

        self.button_draw = QPushButton('', self)
        self.button_draw.move(270, 33)
        self.button_draw.resize(55, 55)
        self.button_draw.setIcon(QIcon(r'pic\icon\icon_draw.png'))
        self.button_draw.setIconSize(QSize(30, 30))
        self.button_draw.setToolTip('Draw')
        self.shape = QMenu(self)
        self.rectangle_shape = QAction('Rectangle', self)
        self.rectangle_shape.triggered.connect(self.draw_rectangle)
        self.shape.addAction(self.rectangle_shape)
        self.ellipse_shape = QAction('Ellipse', self)
        self.ellipse_shape.triggered.connect(self.draw_ellipse)
        self.shape.addAction(self.ellipse_shape)
        self.triangle_shape = QAction('Triangle', self)
        self.triangle_shape.triggered.connect(self.draw_triangle)
        self.shape.addAction(self.triangle_shape)
        self.line_shape = QAction('Line', self)
        self.line_shape.triggered.connect(self.draw_line)
        self.shape.addAction(self.line_shape)
        self.button_draw.setMenu(self.shape)

        self.button_text = QPushButton('', self)
        self.button_text.move(335, 33)
        self.button_text.resize(55, 55)
        self.button_text.setIcon(QIcon(r'pic\icon\icon_text.png'))
        self.button_text.setIconSize(QSize(30, 30))
        self.button_text.setToolTip('Text')
        self.button_text.clicked.connect(self.putting_text)

        self.text_pixel = QLabel(self)
        self.text_pixel.setText('Thickness:')
        self.text_pixel.move(402, 30)
        self.combo_box_pixel = QComboBox(self)
        self.combo_box_pixel.move(468, 33)
        self.combo_box_pixel.resize(55, 25)
        self.combo_box_pixel.addItem('1 px')
        self.combo_box_pixel.addItem('2 px')
        self.combo_box_pixel.addItem('3 px')
        self.combo_box_pixel.addItem('4 px')
        self.combo_box_pixel.addItem('5 px')
        self.combo_box_pixel.currentIndexChanged.connect(self.pixel_selection)

        self.text_font_style = QLabel(self)
        self.text_font_style.setText('Font Style:')
        self.text_font_style.move(402, 59)
        self.combo_box_font = QComboBox(self)
        self.combo_box_font.move(468, 62)
        self.combo_box_font.resize(195, 25)
        self.combo_box_font.addItem('HERSHEY COMPLEX')
        self.combo_box_font.addItem('HERSHEY COMPLEX SMALL')
        self.combo_box_font.addItem('HERSHEY DUPLEX')
        self.combo_box_font.addItem('HERSHEY PLAIN')
        self.combo_box_font.addItem('HERSHEY SCRIPT COMPLEX')
        self.combo_box_font.addItem('HERSHEY SCRIPT SIMPLEX')
        self.combo_box_font.addItem('HERSHEY SIMPLEX')
        self.combo_box_font.addItem('HERSHEY TRIPLEX')
        self.combo_box_font.addItem('ITALIC')
        self.combo_box_font.currentIndexChanged.connect(self.font_style_selection)

        self.text_font_scale = QLabel(self)
        self.text_font_scale.setText('Font Scale:')
        self.text_font_scale.move(533, 30)
        self.combo_box_font_size = QComboBox(self)
        self.combo_box_font_size.move(603, 33)
        self.combo_box_font_size.resize(60, 25)
        self.combo_box_font_size.addItem('1')
        self.combo_box_font_size.addItem('2')
        self.combo_box_font_size.addItem('3')
        self.combo_box_font_size.currentIndexChanged.connect(self.font_scale_selection)

        self.button_reset = QPushButton('', self)
        self.button_reset.move(1135, 33)
        self.button_reset.resize(55, 55)
        self.button_reset.setIcon(QIcon(r'pic\icon\icon_reset.png'))
        self.button_reset.setIconSize(QSize(30, 30))
        self.button_reset.setToolTip('Reset')
        self.button_reset.clicked.connect(self.load_original_image)

    # ********************   menu bar operations   ********************************************************************
    def browse_image(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Image Files (*.png *.jpg *.jpeg)')
        if self.filename:
            self.load_original_image()
        self.converted = False

    def save_image(self):
        self.image = self.backup_img
        self.filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if self.filePath:
            cv2.imwrite(self.filePath, self.image)

    def zoom_in(self):
        self.zoom += 0.2
        self.print_image(self.image)

    def zoom_out(self):
        self.zoom -= 0.2
        self.print_image(self.image)

    def convert_to_original(self):
        self.print_image(self.image)
        cv2.imwrite('backup_img.jpg', self.image)
        self.converted = False

    def convert_to_gray(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_hsv(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_hls(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_lab(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_luv(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2LUV)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def convert_to_yuv(self):
        self.backup_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        self.print_image(self.backup_img)
        self.converted = True
        cv2.imwrite('backup_img.jpg', self.backup_img)

    def open_about_window(self):
        self.about_window.show()

    # ********************   tool bar operations   ********************************************************************
    def show_image_details(self):
        QMessageBox.information(self, 'Image Details', "Width : {}".format(self.image.shape[1]) +
                                "\nHeight : {}".format(self.image.shape[0]) +
                                "\nNumber of channels : {}".format(self.image.shape[2]),
                                QMessageBox.Ok, QMessageBox.Ok)

    def rotate_right(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.backup_img = cv2.rotate(self.backup_img, cv2.ROTATE_90_CLOCKWISE)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def rotate_left(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.backup_img = cv2.rotate(self.backup_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def flip_image_vertical(self):
        self.image = cv2.flip(self.image, 0)
        self.backup_img = cv2.flip(self.backup_img, 0)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def flip_image_horizontal(self):
        self.image = cv2.flip(self.image, 1)
        self.backup_img = cv2.flip(self.backup_img, 1)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def crop_image_action(self):
        self.reset_crop_label()
        self.crop = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_rectangle(self):
        self.draw_rect = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_ellipse(self):
        self.draw_elli = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_triangle(self):
        self.draw_tri = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def draw_line(self):
        self.draw_l = True
        QLabel.setCursor(self, Qt.CrossCursor)

    def putting_text(self):
        self.put_t = True
        QLabel.setCursor(self, Qt.IBeamCursor)

    def font_scale_selection(self, index):
        if index == 0:
            self.font_scale = 1
        if index == 1:
            self.font_scale = 2
        if index == 2:
            self.font_scale = 3

    def pixel_selection(self, index):
        if index == 0:
            self.pixel = 1
        if index == 1:
            self.pixel = 2
        if index == 2:
            self.pixel = 3
        if index == 3:
            self.pixel = 4
        if index == 4:
            self.pixel = 5

    def font_style_selection(self, index):
        if index == 0:
            self.font_style = cv2.FONT_HERSHEY_COMPLEX
        if index == 1:
            self.font_style = cv2.FONT_HERSHEY_COMPLEX_SMALL
        if index == 2:
            self.font_style = cv2.FONT_HERSHEY_DUPLEX
        if index == 3:
            self.font_style = cv2.FONT_HERSHEY_PLAIN
        if index == 4:
            self.font_style = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        if index == 5:
            self.font_style = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        if index == 6:
            self.font_style = cv2.FONT_HERSHEY_SIMPLEX
        if index == 7:
            self.font_style = cv2.FONT_HERSHEY_TRIPLEX
        if index == 7:
            self.font_style = cv2.FONT_ITALIC

    def load_original_image(self):
        self.image = cv2.imread(self.filename, 1)
        self.print_image(self.image)
        cv2.imwrite('backup_img.jpg', self.image)
        self.backup_image()

    # ********************   print image   ****************************************************************************
    def print_image(self, image):
        self.enable_action()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        self.qformat = QImage.Format_ARGB32
        self.img = QImage(image.data, int(image.shape[1]), int(image.shape[0]), int(self.qformat))
        self.label.setPixmap((QPixmap.scaled(QPixmap.fromImage(self.img), int(image.shape[1] * self.zoom),
                                             int(image.shape[0] * self.zoom), Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)))
        self.label.setGeometry(11, 110, int(image.shape[1]*self.zoom), int(image.shape[0]*self.zoom))

    # ********************   mouse control   *************************************************************************
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.crop or self.draw_rect or self.draw_elli or self.draw_tri or self.draw_l:
                self.flag = True
                self.x0 = event.x()
                self.y0 = event.y()
            elif self.put_t:
                self.x0 = event.x()
                self.y0 = event.y()
                self.open_text_box()
                QLabel.setCursor(self, Qt.CustomCursor)
            elif 679 < event.x() < 699 and 36 < event.y() < 56:
                self.color = (0, 0, 0)
                self.select_color_x = 675
                self.select_color_y = 32
                self.update()
            elif 708 < event.x() < 728 and 36 < event.y() < 56:
                self.color = (128, 128, 128)
                self.select_color_x = 704
                self.select_color_y = 32
                self.update()
            elif 737 < event.x() < 757 and 36 < event.y() < 56:
                self.color = (0, 0, 128)
                self.select_color_x = 733
                self.select_color_y = 32
                self.update()
            elif 766 < event.x() < 786 and 36 < event.y() < 56:
                self.color = (0, 128, 128)
                self.select_color_x = 762
                self.select_color_y = 32
                self.update()
            elif 795 < event.x() < 815 and 36 < event.y() < 56:
                self.color = (0, 128, 0)
                self.select_color_x = 791
                self.select_color_y = 32
                self.update()
            elif 824 < event.x() < 844 and 36 < event.y() < 56:
                self.color = (128, 128, 0)
                self.select_color_x = 820
                self.select_color_y = 32
                self.update()
            elif 853 < event.x() < 873 and 36 < event.y() < 56:
                self.color = (128, 0, 0)
                self.select_color_x = 849
                self.select_color_y = 32
                self.update()
            elif 882 < event.x() < 902 and 36 < event.y() < 56:
                self.color = (128, 0, 128)
                self.select_color_x = 878
                self.select_color_y = 32
                self.update()

            elif 679 < event.x() < 699 and 64 < event.y() < 84:
                self.color = (255, 255, 255)
                self.select_color_x = 675
                self.select_color_y = 60
                self.update()
            elif 708 < event.x() < 728 and 64 < event.y() < 84:
                self.color = (192, 192, 192)
                self.select_color_x = 704
                self.select_color_y = 60
                self.update()
            elif 737 < event.x() < 757 and 64 < event.y() < 84:
                self.color = (0, 0, 255)
                self.select_color_x = 733
                self.select_color_y = 60
                self.update()
            elif 766 < event.x() < 786 and 64 < event.y() < 84:
                self.color = (0, 255, 255)
                self.select_color_x = 762
                self.select_color_y = 60
                self.update()
            elif 795 < event.x() < 815 and 64 < event.y() < 84:
                self.color = (0, 255, 0)
                self.select_color_x = 791
                self.select_color_y = 60
                self.update()
            elif 824 < event.x() < 844 and 64 < event.y() < 84:
                self.color = (255, 255, 0)
                self.select_color_x = 820
                self.select_color_y = 60
                self.update()
            elif 853 < event.x() < 873 and 64 < event.y() < 84:
                self.color = (255, 0, 0)
                self.select_color_x = 849
                self.select_color_y = 60
                self.update()
            elif 882 < event.x() < 902 and 64 < event.y() < 84:
                self.color = (255, 0, 255)
                self.select_color_x = 878
                self.select_color_y = 60
                self.update()

        elif event.buttons() == Qt.RightButton:
            if self.crop or self.draw_rect or self.draw_elli or self.draw_tri or self.draw_l or self.put_t:
                self.crop = False
                self.draw_rect = False
                self.draw_elli = False
                self.draw_tri = False
                self.draw_l = False
                self.put_t = False
                QLabel.setCursor(self, Qt.CustomCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.flag:
                self.x1 = event.x()
                self.y1 = event.y()
                self.update()
                instant_img = cv2.imread('backup_img.jpg')
                if self.crop:
                    cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110),
                                  (self.x1 - 11, self.y1 - 110), (0, 0, 255), 2)
                elif self.draw_rect:
                    cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110),
                                  (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
                elif self.draw_elli:
                    cv2.ellipse(instant_img, (int(((self.x0-11)+(self.x1-11))/2), int(((self.y0-110)+(self.y1-110)/2))),
                                (int(((self.x1-11) - (self.x0-11))/2), int(((self.y1-110) - (self.y0-110))/2)),
                                1, 0, 360, self.color, self.pixel)
                elif self.draw_tri:
                    cv2.line(instant_img, ((int(((self.x0-11)+(self.x1-11))/2)), self.y0-110),
                             (self.x0-11, self.y1-110), self.color, self.pixel)
                    cv2.line(instant_img, (self.x0-11, self.y1-110), (self.x1-11, self.y1-110), self.color, self.pixel)
                    cv2.line(instant_img, (self.x1-11, self.y1-110),
                             ((int(((self.x0-11)+(self.x1-11))/2)), self.y0-110), self.color, self.pixel)
                elif self.draw_l:
                    cv2.line(instant_img, (self.x0-11, self.y0-110), (self.x1-11, self.y1-110), self.color, self.pixel)
                self.print_image(instant_img)

    def mouseReleaseEvent(self, event):
        if self.crop:
            self.flag = False
            instant_img = cv2.imread('backup_img.jpg')
            cv2.rectangle(instant_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          (0, 0, 255), 2)
            self.print_image(instant_img)
        elif self.draw_rect:
            self.flag = False
            cv2.rectangle(self.backup_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          self.color, self.pixel)
            cv2.rectangle(self.image, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                          self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_rect = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_elli:
            self.flag = False
            cv2.ellipse(self.backup_img,
                        (int(((self.x0 - 11) + (self.x1 - 11)) / 2), int(((self.y0 - 110) + (self.y1 - 110) / 2))),
                        (int(((self.x1 - 11) - (self.x0 - 11)) / 2), int(((self.y1 - 110) - (self.y0 - 110)) / 2)),
                        1, 0, 360, self.color, self.pixel)
            cv2.ellipse(self.image,
                        (int(((self.x0 - 11) + (self.x1 - 11)) / 2), int(((self.y0 - 110) + (self.y1 - 110) / 2))),
                        (int(((self.x1 - 11) - (self.x0 - 11)) / 2), int(((self.y1 - 110) - (self.y0 - 110)) / 2)),
                        1, 0, 360, self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_elli = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_tri:
            self.flag = False
            cv2.line(self.backup_img, ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110),
                     (self.x0 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.backup_img, (self.x0 - 11, self.y1 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.backup_img, (self.x1 - 11, self.y1 - 110),
                     ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110), self.color, self.pixel)
            cv2.line(self.image, ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110),
                     (self.x0 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.image, (self.x0 - 11, self.y1 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            cv2.line(self.image, (self.x1 - 11, self.y1 - 110),
                     ((int(((self.x0 - 11) + (self.x1 - 11)) / 2)), self.y0 - 110), self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_tri = False
            QLabel.setCursor(self, Qt.CustomCursor)
        elif self.draw_l:
            self.flag = False
            cv2.line(self.backup_img, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110),
                     self.color, self.pixel)
            cv2.line(self.image, (self.x0 - 11, self.y0 - 110), (self.x1 - 11, self.y1 - 110), self.color, self.pixel)
            if self.converted:
                self.print_image(self.backup_img)
                cv2.imwrite('backup_img.jpg', self.backup_img)
            else:
                self.print_image(self.image)
                cv2.imwrite('backup_img.jpg', self.image)
            self.draw_l = False
            QLabel.setCursor(self, Qt.CustomCursor)

    # ********************   press enter actions   ********************************************************************
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.crop:
                if self.converted:
                    self.backup_img = self.backup_img[self.y0 - 110:self.y1 - 110,
                                                      self.x0 - 11:self.x1 - 11]
                    self.image = self.image[self.y0 - 110:self.y1 - 110,
                                            self.x0 - 11:self.x1 - 11]
                    self.reset_crop_label()
                    self.print_image(self.backup_img)
                    cv2.imwrite('backup_img.jpg', self.backup_img)
                if not self.converted:
                    self.image = self.image[self.y0 - 110:self.y1 - 110,
                                            self.x0 - 11:self.x1 - 11]
                    self.reset_crop_label()
                    self.print_image(self.image)
                    cv2.imwrite('backup_img.jpg', self.image)
                self.crop = False
                self.cursor_shape()

    # ********************   text box dialog   ************************************************************************
    def open_text_box(self):
        self.dialog = QDialog(self)
        self.form_group_box = QGroupBox('Insert Text')
        self.text_box = QLineEdit(self)

        layout = QFormLayout()
        layout.addRow(QLabel("Text:"), self.text_box)
        self.form_group_box.setLayout(layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.close_text_box1)
        button_box.rejected.connect(self.close_text_box2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)

        self.dialog.setLayout(main_layout)
        self.dialog.setWindowTitle('Text Box')
        self.dialog.show()

    def close_text_box1(self):
        self.put_t = False
        self.dialog.close()
        cv2.putText(self.image, self.text_box.text(), (self.x0 - 11, self.y0 - 100), self.font_style,
                    self.font_scale, self.color, self.pixel)
        cv2.putText(self.backup_img, self.text_box.text(), (self.x0 - 11, self.y0 - 100), self.font_style,
                    self.font_scale, self.color, self.pixel)
        if self.converted:
            self.print_image(self.backup_img)
            cv2.imwrite('backup_img.jpg', self.backup_img)
        else:
            self.print_image(self.image)
            cv2.imwrite('backup_img.jpg', self.image)

    def close_text_box2(self):
        self.put_t = False
        self.dialog.close()

    # ********************   set cursor   *****************************************************************************
    def cursor_shape(self):
        if self.crop:
            QLabel.setCursor(self, Qt.CrossCursor)
        else:
            QLabel.setCursor(self, Qt.CustomCursor)

    # *****************************************************************************************************************
    def backup_image(self):
        self.backup_img = cv2.imread('backup_img.jpg', 1)

    def paintEvent(self, event):
        tool_bar_rect = QPainter(self)
        tool_bar_rect.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        tool_bar_rect.drawRect(-1, 0, 1201, 97)

        black_rect = QPainter(self)
        black_rect.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        black_rect.drawRect(679, 36, 20, 20)
        dark_gray_rect = QPainter(self)
        dark_gray_rect.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        dark_gray_rect.drawRect(708, 36, 20, 20)
        dark_red_rect = QPainter(self)
        dark_red_rect.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))
        dark_red_rect.drawRect(737, 35, 21, 21)
        dark_yellow_rect = QPainter(self)
        dark_yellow_rect.setBrush(QBrush(Qt.darkYellow, Qt.SolidPattern))
        dark_yellow_rect.drawRect(766, 35, 21, 21)
        dark_green_rect = QPainter(self)
        dark_green_rect.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
        dark_green_rect.drawRect(795, 35, 21, 21)
        dark_cyan_rect = QPainter(self)
        dark_cyan_rect.setBrush(QBrush(Qt.darkCyan, Qt.SolidPattern))
        dark_cyan_rect.drawRect(824, 35, 21, 21)
        dark_blue_rect = QPainter(self)
        dark_blue_rect.setBrush(QBrush(Qt.darkBlue, Qt.SolidPattern))
        dark_blue_rect.drawRect(853, 35, 21, 21)
        dark_magenta_rect = QPainter(self)
        dark_magenta_rect.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
        dark_magenta_rect.drawRect(882, 35, 21, 21)

        white_rect = QPainter(self)
        white_rect.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        white_rect.drawRect(679, 64, 20, 20)
        light_gray_rect = QPainter(self)
        light_gray_rect.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))
        light_gray_rect.drawRect(708, 64, 20, 20)
        red_rect = QPainter(self)
        red_rect.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        red_rect.drawRect(737, 64, 21, 21)
        yellow_rect = QPainter(self)
        yellow_rect.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        yellow_rect.drawRect(766, 64, 21, 21)
        green_rect = QPainter(self)
        green_rect.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        green_rect.drawRect(795, 64, 21, 21)
        cyan_rect = QPainter(self)
        cyan_rect.setBrush(QBrush(Qt.cyan, Qt.SolidPattern))
        cyan_rect.drawRect(824, 64, 21, 21)
        blue_rect = QPainter(self)
        blue_rect.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        blue_rect.drawRect(853, 64, 21, 21)
        magenta_rect = QPainter(self)
        magenta_rect.setBrush(QBrush(Qt.magenta, Qt.SolidPattern))
        magenta_rect.drawRect(882, 64, 21, 21)

        select_rect = QPainter(self)
        select_rect.drawRect(self.select_color_x, self.select_color_y, 28, 28)

    def reset_crop_label(self):
        self.x0 = 0
        self.x1 = 0
        self.y0 = 0
        self.y1 = 0

    def disable_action(self):
        self.disabled_list = [self.action_save, self.action_zoom_in, self.action_zoom_out,
                              self.action_convert_to, self.action_original, self.button_image_details,
                              self.button_rotate, self.button_flip, self.button_crop, self.button_draw,
                              self.button_text, self.button_reset]
        for i in range(len(self.disabled_list)):
            self.disabled_list[i].setDisabled(True)

    def enable_action(self):
        for i in range(len(self.disabled_list)):
            self.disabled_list[i].setDisabled(False)


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.title = 'About Mini Paint'
        self.x_pos = 650
        self.y_pos = 250
        self.width = 600
        self.height = 450
        self.ui_components()

    def ui_components(self):
        self.setGeometry(self.x_pos, self.y_pos, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.label_ums = QLabel(self)
        pixmap = QPixmap(r'pic\logo\UMS_logo.png')
        self.label_ums.setPixmap(pixmap)
        self.label_ums.move(42, 61)

        self.label_mcg = QLabel(self)
        pixmap = QPixmap(r'pic\logo\MCG_logo.png')
        self.label_mcg.setPixmap(pixmap)
        self.label_mcg.move(350, 54)

        self.label_message01 = QLabel("This product is the assignment for the course \nImage Processing 2020.", self)
        self.label_message01.move(42, 220)
        self.label_message01.setFont(QFont('Arial', 14))
        self.label_message02 = QLabel("©2020 Liew Ming Kai BS18110392. All right reserved.", self)
        self.label_message02.move(42, 350)
        self.label_message02.setFont(QFont('Arial', 10))

        self.button = QPushButton('OK', self)
        self.button.move(485, 405)
        self.button.clicked.connect(self.close_win)

    def close_win(self):
        self.close()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    @staticmethod
    def draw_line(qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(42, 180, 558, 180)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
